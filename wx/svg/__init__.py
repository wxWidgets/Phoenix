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


    def RenderToGC(self, ctx, scale=None, size=None, translate=(0.0, 0.0)):
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

            # Draw the combined set of paths.
            # If the fill is a radial gradient then first draw the fill with the
            # outer color, to ensure that the total area of the shape is filled.
            # NOTE: if there are transparencies infolved here then this solution
            # is probably wrong.
            if shape.fill.type == SVG_PAINT_RADIAL_GRADIENT:
                color = wx.Colour(*self._getGradientColors(shape.fill.gradient)[-1])
                ctx.SetBrush(wx.Brush(color))
                ctx.FillPath(path, rule)

            # Now fill and stroke the shape with the given pen and brush
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


    def _makeGradientStops(self, gradient, prnt=False):
        gcstops = wx.GraphicsGradientStops()
        for stop in gradient.stops:
            if prnt:
                print('stop:   ', stop.offset, stop.color_rgba)
            color = wx.Colour(*stop.color_rgba)
            gcstop = wx.GraphicsGradientStop(color, stop.offset)
            gcstops.Add(gcstop)
        return gcstops


    def _getGradientColors(self, gradient):
        return [stop.color_rgba for stop in gradient.stops]


    def _makeBrush(self, ctx, shape):
        # set up a brush from the shape.fill (SVGpaint)

        # no brush
        if shape.fill.type == SVG_PAINT_NONE:
            brush = wx.NullGraphicsBrush

        # brush with a solid color
        elif shape.fill.type == SVG_PAINT_COLOR:
            #print(shape.fill.color, shape.fill.color_rgba)
            r,g,b,a = shape.fill.color_rgba
            brush = ctx.CreateBrush(wx.Brush(wx.Colour(r,g,b,a)))

        # brush with a linear gradient
        elif shape.fill.type == SVG_PAINT_LINEAR_GRADIENT:
            gradient = shape.fill.gradient
            (x1, y1), (x2, y2) = gradient.linearPoints
            print('shape:  ', shape.bounds)
            print('lingrad:', (x1, y1), (x2, y2))
            stops = self._makeGradientStops(gradient, True)
            brush = ctx.CreateLinearGradientBrush(x1, y1, x2, y2, stops)

        # brush with a radial gradient
        elif shape.fill.type == SVG_PAINT_RADIAL_GRADIENT:
            gradient = shape.fill.gradient
            # print('(fx,fy):', (gradient.fx, gradient.fy))
            (cx, cy), radius = gradient.radialPointRadius
            #print('1: (cx, cy, radius) (fx, fy):', (cx, cy, radius, gradient.fx, gradient.fy))
            stops = self._makeGradientStops(gradient)

            # FIXME: *2 seems to be close for this test case, but it is surely
            # wrong generally... figure out what needs to be done in
            # gradient.radialPointRadius to get the correct value.
            brush = ctx.CreateRadialGradientBrush(cx, cy, cx, cy, radius*2, stops)

        else:
            raise ValueError("Unknown fill type")
        return brush


    def _makePen(self, ctx, shape):
        width = shape.strokeWidth
        join = { SVG_JOIN_MITER : wx.JOIN_MITER,
                    SVG_JOIN_ROUND : wx.JOIN_ROUND,
                    SVG_JOIN_BEVEL : wx.JOIN_BEVEL}.get(shape.strokeLineJoin, 0)
        cap = { SVG_CAP_BUTT : wx.CAP_BUTT,
                SVG_CAP_ROUND : wx.CAP_ROUND,
                SVG_CAP_SQUARE : wx.CAP_PROJECTING}.get(shape.strokeLineCap, 0)
        # TODO: handle dashes

        # set up a brush from the shape.stroke (SVGpaint)
        if shape.stroke.type == SVG_PAINT_NONE:
            pen = wx.NullGraphicsPen

        elif shape.stroke.type == SVG_PAINT_COLOR:
            r,g,b,a = shape.stroke.color_rgba
            pen = ctx.CreatePen(
                wx.GraphicsPenInfo(wx.Colour(r,g,b,a)).Width(width).Join(join).Cap(cap))

        elif shape.stroke.type == SVG_PAINT_LINEAR_GRADIENT:
            # print("TODO: linear GradientPen")
            # TODO: wxWidgets can't do gradient pens (yet?)
            # Just average the stops to use as an approximation
            colors = self._getGradientColors(shape.stroke.gradient)
            ave = [round(sum(x)/len(x)) for x in zip(*colors)]
            pen = ctx.CreatePen(
                wx.GraphicsPenInfo(wx.Colour(*ave)).Width(width).Join(join).Cap(cap))

        elif shape.stroke.type == SVG_PAINT_RADIAL_GRADIENT:
            # print("TODO: radial GradientPen")
            # TODO: wxWidgets can't do gradient pens (yet?)
            # Just average the stops to use as an approximation
            colors = self._getGradientColors(shape.stroke.gradient)
            ave = [round(sum(x)/len(x)) for x in zip(*colors)]
            pen = ctx.CreatePen(
                wx.GraphicsPenInfo(wx.Colour(*ave)).Width(width).Join(join).Cap(cap))

        else:
            raise ValueError("Unknown stroke type")
        return pen


def _grouper(iterable, n, fillvalue=None):
    "Collect items from an interable into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

