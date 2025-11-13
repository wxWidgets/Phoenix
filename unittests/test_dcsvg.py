import unittest
from unittests import wtc
import wx
import wx.svg
import os

fileName = 'svgtest.svg'

#---------------------------------------------------------------------------

class SvgDCTests(wtc.WidgetTestCase):

    def test_SvgDC1(self):
        dc = wx.SVGFileDC(fileName)
        dc.DrawLine(0,0, 50,50)
        del dc

        self.img = wx.svg.SVGimage.CreateFromFile(fileName)

        dc = wx.ClientDC(self.frame)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()

        dcdim = min(self.frame.Size.width, self.frame.Size.height)
        imgdim = min(self.img.width, self.img.height)
        scale = dcdim / imgdim

        ctx = wx.GraphicsContext.Create(dc)
        self.img.RenderToGC(ctx, scale)

        os.remove(fileName)

    def test_SvgDC2(self):
        assert wx.svg.SVGpaintType.SVG_PAINT_NONE == wx.svg.SVG_PAINT_NONE
        assert wx.svg.SVGpaintType.SVG_PAINT_COLOR == wx.svg.SVG_PAINT_COLOR
        assert wx.svg.SVGpaintType.SVG_PAINT_LINEAR_GRADIENT == wx.svg.SVG_PAINT_LINEAR_GRADIENT
        assert wx.svg.SVGpaintType.SVG_PAINT_RADIAL_GRADIENT == wx.svg.SVG_PAINT_RADIAL_GRADIENT

        assert wx.svg.SVGspreadType.SVG_SPREAD_PAD == wx.svg.SVG_SPREAD_PAD
        assert wx.svg.SVGspreadType.SVG_SPREAD_REFLECT == wx.svg.SVG_SPREAD_REFLECT
        assert wx.svg.SVGspreadType.SVG_SPREAD_REPEAT == wx.svg.SVG_SPREAD_REPEAT

        assert wx.svg.SVGlineJoin.SVG_JOIN_MITER == wx.svg.SVG_JOIN_MITER
        assert wx.svg.SVGlineJoin.SVG_JOIN_ROUND == wx.svg.SVG_JOIN_ROUND
        assert wx.svg.SVGlineJoin.SVG_JOIN_BEVEL == wx.svg.SVG_JOIN_BEVEL

        assert wx.svg.SVGlineCap.SVG_CAP_BUTT == wx.svg.SVG_CAP_BUTT
        assert wx.svg.SVGlineCap.SVG_CAP_ROUND == wx.svg.SVG_CAP_ROUND
        assert wx.svg.SVGlineCap.SVG_CAP_SQUARE == wx.svg.SVG_CAP_SQUARE

        assert wx.svg.SVGfillRule.SVG_FILLRULE_NONZERO == wx.svg.SVG_FILLRULE_NONZERO
        assert wx.svg.SVGfillRule.SVG_FILLRULE_EVENODD == wx.svg.SVG_FILLRULE_EVENODD

        assert wx.svg.SVGflags.SVG_FLAGS_VISIBLE ==  wx.svg.SVG_FLAGS_VISIBLE

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
