#----------------------------------------------------------------------
# Name:        wx.svg.__init__.py
# Purpose:     Python code to augment or extend the nanosvg wrappers,
#              and provide wxPython-specific integrations.
#
# Author:      Robin Dunn
#
# Created:     23-July-2019
# Copyright:   (c) 2019 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------
"""
"""
import wx
from six.moves import zip_longest

from ._version import __version__
from ._nanosvg import *


class SVGimage(SVGimageBase):
    """
    """

    def RasterizeToBitmap(self, tx=0.0, ty=0.0, scale=1.0,
                          width=-1, height=-1, stride=-1):
        """
        """
        buff = self.RasterizeToBytes(tx, ty, scale, width, height, stride)
        bmp = wx.Bitmap.FromBufferRGBA(width, height, buff)
        return bmp


    def RenderToGC(self, ctx, scale=None, size=None, translate=(0.0, 0.0)):
        """
        """
        ctx.PushState()
        # set scale either from the parameter or as ratio of sizes
        if scale is not None:
            ctx.Scale(scale, scale)
        elif size is not None:
            # scale the context to the given size
            size = wx.Size(*size)
            sx = size.width / self.width
            sy = size.height / self.height
            ctx.Scale(sx, sy)
        ctx.Translate(*translate)

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

        ctx.Flush()
        ctx.PopState()


    def _makeSubPath(self, ctx, svg_path):
        points = svg_path.points
        path = ctx.CreatePath()
        x, y = points[0]
        path.MoveToPoint(x,y)
        for (cx1, cy1), (cx2, cy2), (x,y) in _grouper(points[1:], 3, (0,0)):
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
            # linear gradiants to go from (0, 0) to (0,1) in the transformed
            # space. So once we have the transform set we can use those points
            # too.
            gradient = shape.fill.gradient
            stops = self._makeGradientStops(gradient)
            matrix = ctx.CreateMatrix(*gradient.xform)
            brush = ctx.CreateLinearGradientBrush(0,0, 0,1, stops, matrix)

        # brush with a radial gradient
        elif shape.fill.type == SVG_PAINT_RADIAL_GRADIENT:
            # Likewise, NanoSVG normalizes radial gradients with a a transform
            # that puts the center (cx, cy) at (0,0) and the radius has a length
            # of 1.
            gradient = shape.fill.gradient
            stops = self._makeGradientStops(gradient)
            matrix = ctx.CreateMatrix(*gradient.xform)
            brush = ctx.CreateRadialGradientBrush(0,0, 0,0, 1, stops, matrix)

        else:
            raise ValueError("Unknown fill type")
        return brush


    def _makePen(self, ctx, shape):
        # set up a pen from the shape.stroke (SVGpaint) object
        width = shape.strokeWidth
        join = { SVG_JOIN_MITER : wx.JOIN_MITER,
                    SVG_JOIN_ROUND : wx.JOIN_ROUND,
                    SVG_JOIN_BEVEL : wx.JOIN_BEVEL}.get(shape.strokeLineJoin, 0)
        cap = { SVG_CAP_BUTT : wx.CAP_BUTT,
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
            gradient = shape.stroke.gradient
            stops = self._makeGradientStops(gradient)
            matrix = ctx.CreateMatrix(*gradient.xform)
            info.LinearGradient(0,0, 0,1, stops, matrix)
            pen = ctx.CreatePen(info)

        elif shape.stroke.type == SVG_PAINT_RADIAL_GRADIENT:
            gradient = shape.stroke.gradient
            stops = self._makeGradientStops(gradient)
            matrix = ctx.CreateMatrix(*gradient.xform)
            info.RadialGradient(0,0, 0,0, 1, stops, matrix)
            pen = ctx.CreatePen(info)

        else:
            raise ValueError("Unknown stroke type")
        return pen


def _grouper(iterable, n, fillvalue=None):
    "Collect items from an interable into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

