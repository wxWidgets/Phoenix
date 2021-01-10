#----------------------------------------------------------------------
# Name:        wx.svg.__init__.py
# Purpose:     Python code to augment or extend the nanosvg wrappers,
#              and provide wxPython-specific integrations.
#
# Author:      Robin Dunn
#
# Created:     23-July-2019
# Copyright:   (c) 2019-2020 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------
"""
The classes in this package facilitate the parsing, normalizing, drawing and
rasterizing of Scalable Vector Graphics (SVG) images. The primary interface to
this functionality is via the :class:`wx.svg.SVGimage` class, which provides
various integrations with wxPython. It, in turn, uses a set of wrappers around
the NanoSVG library (https://github.com/memononen/nanosvg) to do the low-level
work. There are a few features defined in the SVG spec that are not supported,
but all the commonly used ones seem to be there.

Example 1
---------
Drawing an SVG image to a window, scaled to fit the size of the window and using
a :class:`wx.GraphicsContext` can be done like this::

    def __init__(self, ...):
        ...
        self.img = wx.svg.SVGimage.CreateFromFile(svg_filename)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()

        dcdim = min(self.Size.width, self.Size.height)
        imgdim = min(self.img.width, self.img.height)
        scale = dcdim / imgdim
        width = int(self.img.width * scale)
        height = int(self.img.height * scale)

        ctx = wx.GraphicsContext.Create(dc)
        self.img.RenderToGC(ctx, scale)

Since it is drawing the SVG shapes and paths using the equivalent GC primitives
then any existing transformations that may be active on the context will be
applied automatically to the SVG shapes.

Note that not all GraphicsContext backends are created equal. Specifically, the
GDI+ backend (the default on Windows) simply can not support some features that
are commonly used in SVG images, such as applying transforms to gradients. The
Direct2D backend on Windows does much better, and the Cairo backend on Windows
is also very good. The default backends on OSX and Linux do very good as well.

Example 2
---------
If you're not already using a ``wx.GraphicsContext`` then a :class:`wx.Bitmap`
can easily be created instead. For example, the last 2 lines in the code above
could be replaced by the following, and accomplish basically the same thing::

    bmp = self.img.ConvertToBitmap(scale=scale, width=width, height=height)
    dc.DrawBitmap(bmp, 0, 0)

Example 3
---------
The ``ConvertToBitmap`` shown above gives a lot of control around scaling,
translating and sizing the SVG image into a bitmap, but most of the time you
probably just want to get a bitmap of a certain size to use as an icon or
similar. The ``ConvertToScaledBitmap`` provides an easier API to do just that
for you. It automatically scales the SVG image into the requested size in
pixels.::

    bmp = img.ConvertToScaledBitmap(wx.Size(24,24))

Optionally, it can accept a window parameter that will automatically adjust the
size according to the Content Scale Factor of that window, if supported by the
platform and if the window is located on a HiDPI display the the bitmap's size
will be adjusted accordingly.::

    bmp = img.ConvertToScaledBitmap(wx.Size(24,24), self)

"""

import wx
from six.moves import zip_longest

from ._nanosvg import *

# All the supported renderers now support gradient transforms, more or less, but
# let's leave this in place in case it's needed again in the future.
_RenderersWithoutGradientTransforms = []


class SVGimage(SVGimageBase):
    """
    The SVGimage class provides various ways to load and use SVG images
    in wxPython applications.
    """

    def ConvertToBitmap(self, tx=0.0, ty=0.0, scale=1.0,
                        width=-1, height=-1, stride=-1):
        """
        Creates a :class:`wx.Bitmap` containing a rasterized version of the SVG image.

        :param float `tx`: Image horizontal offset (applied after scaling)
        :param float `ty`: Image vertical offset (applied after scaling)
        :param float `scale`: Image scale
        :param int `width`: width of the image to render, defaults to width from the SVG file
        :param int `height`: height of the image to render, defaults to height from the SVG file
        :param int `stride`: number of bytes per scan line in the destination buffer, typically ``width * 4``

        :returns: :class:`wx.Bitmap`
        """
        buf = self.Rasterize(tx, ty, scale, width, height, stride)
        bmp = wx.Bitmap.FromBufferRGBA(width, height, buf)
        return bmp


    def ConvertToScaledBitmap(self, size, window=None):
        """
        Automatically scales the SVG image so it will fit in the given size,
        and creates a :class:`wx.Bitmap` of that size, containing a rasterized
        version of the SVG image. If a window is passed then the size of the
        bitmap will automatically be adjusted to the content scale factor of
        that window. For example, if a (32,32) pixel bitmap is requested for a
        window on a Retina display, then a (64,64) pixel bitmap will be created.

        :param wx.Size `size`: Size of the bitmap to create, in pixels
        :param wx.Window `window`: Adjust the size by this window's content scale factor, if supported on the platform

        :returns: :class:`wx.Bitmap`
        """
        size = wx.Size(*size)
        if window:
            size.width *= window.GetContentScaleFactor()
            size.height *= window.GetContentScaleFactor()

        # We can only have one overall scale factor for both dimensions with
        # this rasterization method, so chose either the minimum of width or
        # height to help ensure it fits both ways within the specified size.
        sx = size.width / self.width
        sy = size.height / self.height
        scale = min(sx, sy)
        return self.ConvertToBitmap(scale=scale, width=size.width, height=size.height)


    def RenderToGC(self, ctx, scale=None, size=None):
        """
        Draw the collection of shapes and paths in the SVG image
        onto the given :class:`wx.GraphicsContext` using the drawing primitives
        provided by the context. The Context's state is saved and restored so
        any transformations done while rendering the SVG will be undone.

        :param wx.GraphicsContext `ctx`: The context to draw upon
        :param float `scale`: If given, apply to the context's scale.
        :param (float, float) `size`: If given, scale the image's width and height
            to that provided in this parameter. Ignored if ``scale`` is also specified.

        .. note::
            Some GraphicsContext backends perform better than others.
            The default GDI+ backend on Windows is the most glitchy, but the
            Direct2D backend works well.
        """
        ctx.PushState()
        try:
            # set scale either from the scale parameter or as ratio of the sizes
            if scale is not None:
                ctx.Scale(scale, scale)
            elif size is not None:
                # scale the context to the given size
                size = wx.Size(*size)
                sx = size.width / self.width
                sy = size.height / self.height
                ctx.Scale(sx, sy)

            for shape in self.shapes:
                if not shape.flags & SVG_FLAGS_VISIBLE:
                    continue
                if shape.opacity != 1.0:
                    ctx.BeginLayer(shape.opacity)
                brush = self._makeBrush(ctx, shape)
                pen = self._makePen(ctx, shape)

                rule = { SVG_FILLRULE_NONZERO : wx.WINDING_RULE,
                        SVG_FILLRULE_EVENODD : wx.ODDEVEN_RULE }.get(shape.fillRule, 0)

                # The shape's path is comprised of one or more subpaths, collect
                # and accumulate them in a new GraphicsPath
                path = ctx.CreatePath()
                for svg_path in shape.paths:
                    subpath = self._makeSubPath(ctx, svg_path)
                    path.AddPath(subpath)

                # Draw the combined set of paths, using the given pen and brush to
                # fill and stroke the shape.
                ctx.SetBrush(brush)
                ctx.SetPen(pen)
                ctx.DrawPath(path, rule)

                if shape.opacity != 1.0:
                    ctx.EndLayer()
        finally:
            ctx.Flush()
            ctx.PopState()


    def _makeSubPath(self, ctx, svg_path):
        points = svg_path.points
        path = ctx.CreatePath()
        x, y = points[0]
        path.MoveToPoint(x,y)
        for (cx1, cy1), (cx2, cy2), (x,y) in _chunker(points[1:], 3, (0,0)):
            path.AddCurveToPoint(cx1, cy1, cx2, cy2, x,y)
        if svg_path.closed:
            path.CloseSubpath()
        return path


    def _makeGradientStops(self, gradient):
        stops = [stop for stop in gradient.stops]
        first = stops[0]
        last = stops[-1]
        gcstops = wx.GraphicsGradientStops(wx.Colour(*first.color_rgba),
                                           wx.Colour(*last.color_rgba))
        for stop in stops:
            color = wx.Colour(*stop.color_rgba)
            gcstop = wx.GraphicsGradientStop(color, stop.offset)
            gcstops.Add(gcstop)
        return gcstops


    def _getGradientColors(self, gradient):
        return [stop.color_rgba for stop in gradient.stops]


    def _makeBrush(self, ctx, shape):
        # set up a brush from the shape.fill (SVGpaint) object

        # no brush
        if shape.fill.type == SVG_PAINT_NONE:
            brush = wx.NullGraphicsBrush

        # brush with a solid color
        elif shape.fill.type == SVG_PAINT_COLOR:
            r,g,b,a = shape.fill.color_rgba
            brush = ctx.CreateBrush(wx.Brush(wx.Colour(r,g,b,a)))

        # brush with a linear gradient
        elif shape.fill.type == SVG_PAINT_LINEAR_GRADIENT:
            # NanoSVG gives gradients their own transform which normalizes the
            # linear gradients to go from (0, 0) to (0,1) in the transformed
            # space. So once we have the transform set we can use those points
            # too.
            x1, y1, = (0.0, 0.0)
            x2, y2, = (0.0, 1.0)
            gradient = shape.fill.gradient
            matrix = ctx.CreateMatrix(*gradient.xform)

            # Except for GDI+, which doesn't support applying a transform to a
            # gradient, so we'll translate the points back to real space
            # ourselves. This is only an approximation of the desired outcome
            # however, as things like scale and shear in the transform will not
            # be applied to the rest of the fill.
            if ctx.Renderer.Type in _RenderersWithoutGradientTransforms:
                matrix.Invert()
                x1, y1 = matrix.TransformPoint(x1, y1)
                x2, y2 = matrix.TransformPoint(x2, y2)
                matrix = wx.NullGraphicsMatrix

            stops = self._makeGradientStops(gradient)
            brush = ctx.CreateLinearGradientBrush(x1,y1, x2,y2, stops, matrix)

        # brush with a radial gradient
        elif shape.fill.type == SVG_PAINT_RADIAL_GRADIENT:
            # Likewise, NanoSVG normalizes radial gradients with a transform
            # that puts the center (cx, cy) at (0,0) and the radius has a length
            # of 1.
            cx, cy = (0.0, 0.0)
            radius = 1
            gradient = shape.fill.gradient
            matrix = ctx.CreateMatrix(*gradient.xform)

            # Except for GDI+...  See note above
            if ctx.Renderer.Type in _RenderersWithoutGradientTransforms:
                matrix.Invert()
                cx, cy = matrix.TransformPoint(cx, cy)
                r1, r2 = matrix.TransformPoint(0, 1)
                radius = r2 - cy
                matrix = wx.NullGraphicsMatrix

            stops = self._makeGradientStops(gradient)
            brush = ctx.CreateRadialGradientBrush(cx,cy, cx,cy, radius, stops, matrix)

        else:
            raise ValueError("Unknown fill type")
        return brush


    def _makePen(self, ctx, shape):
        # set up a pen from the shape.stroke (SVGpaint) object
        width = shape.strokeWidth
        join = { SVG_JOIN_MITER : wx.JOIN_MITER,
                 SVG_JOIN_ROUND : wx.JOIN_ROUND,
                 SVG_JOIN_BEVEL : wx.JOIN_BEVEL}.get(shape.strokeLineJoin, 0)
        cap =  { SVG_CAP_BUTT : wx.CAP_BUTT,
                 SVG_CAP_ROUND : wx.CAP_ROUND,
                 SVG_CAP_SQUARE : wx.CAP_PROJECTING}.get(shape.strokeLineCap, 0)
        # TODO: handle dashes

        info = wx.GraphicsPenInfo(wx.BLACK).Width(width).Join(join).Cap(cap)

        if shape.stroke.type == SVG_PAINT_NONE:
            pen = wx.NullGraphicsPen

        elif shape.stroke.type == SVG_PAINT_COLOR:
            info.Colour(shape.stroke.color_rgba)
            pen = ctx.CreatePen(info)

        elif shape.stroke.type == SVG_PAINT_LINEAR_GRADIENT:
            x1, y1, = (0.0, 0.0)
            x2, y2, = (0.0, 1.0)
            gradient = shape.stroke.gradient
            matrix = ctx.CreateMatrix(*gradient.xform)

            # Except for GDI+...  See note above
            if ctx.Renderer.Type in _RenderersWithoutGradientTransforms:
                matrix.Invert()
                x1, y1 = matrix.TransformPoint(x1, y1)
                x2, y2 = matrix.TransformPoint(x2, y2)
                matrix = wx.NullGraphicsMatrix

            stops = self._makeGradientStops(gradient)
            info.LinearGradient(x1,y1, x2,y2, stops, matrix)
            pen = ctx.CreatePen(info)

        elif shape.stroke.type == SVG_PAINT_RADIAL_GRADIENT:
            cx, cy = (0.0, 0.0)
            radius = 1
            gradient = shape.stroke.gradient
            matrix = ctx.CreateMatrix(*gradient.xform)

            # Except for GDI+...  See note above
            if ctx.Renderer.Type in _RenderersWithoutGradientTransforms:
                matrix.Invert()
                cx, cy = matrix.TransformPoint(cx, cy)
                r1, r2 = matrix.TransformPoint(0, 1)
                radius = r2 - cy
                matrix = wx.NullGraphicsMatrix

            stops = self._makeGradientStops(gradient)
            info.RadialGradient(0,0, 0,0, 1, stops, matrix)
            pen = ctx.CreatePen(info)

        else:
            raise ValueError("Unknown stroke type")
        return pen


def _chunker(iterable, n, fillvalue=None):
    "Collect items from an iterable into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

