import unittest
from unittests import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class BrushTests(wtc.WidgetTestCase):

    def test_BrushCtors(self):
        b = wx.Brush()
        b = wx.Brush(wx.Colour(1,2,3), wx.BRUSHSTYLE_SOLID)
        bmp = wx.Bitmap(pngFile)
        b = wx.Brush(bmp)
        copy = wx.Brush(b)


    def test_BrushOperators(self):
        b1 = wx.Brush(wx.Colour(1,2,3), wx.BRUSHSTYLE_SOLID)
        b2 = wx.Brush(wx.Colour(1,2,3), wx.BRUSHSTYLE_SOLID)
        b3 = wx.Brush(wx.Colour(4,5,6), wx.BRUSHSTYLE_SOLID)

        self.assertTrue(b1 == b2)
        self.assertTrue(b2 != b3)
        self.assertFalse(b1 != b2)
        self.assertFalse(b2 == b3)


    def test_nonzero(self):
        b = wx.Brush(wx.Colour(1,2,3), wx.BRUSHSTYLE_SOLID)
        if not b:
            self.fail("__nonzero__ should have avoided this branch")
        if wx.NullBrush:
            self.fail("__nonzero__ should have avoided this branch")


    def test_StockBrushesExist(self):
        wx.BLUE_BRUSH
        wx.GREEN_BRUSH
        wx.YELLOW_BRUSH
        wx.WHITE_BRUSH
        wx.BLACK_BRUSH
        wx.GREY_BRUSH
        wx.MEDIUM_GREY_BRUSH
        wx.LIGHT_GREY_BRUSH
        wx.TRANSPARENT_BRUSH
        wx.CYAN_BRUSH
        wx.RED_BRUSH
        wx.NullBrush


    def test_StockBrushesInitialized(self):
        self.assertTrue(wx.BLUE_BRUSH.IsOk())
        self.assertTrue(wx.GREEN_BRUSH.IsOk())
        self.assertTrue(wx.YELLOW_BRUSH.IsOk())
        self.assertTrue(wx.WHITE_BRUSH.IsOk())
        self.assertTrue(wx.BLACK_BRUSH.IsOk())
        self.assertTrue(wx.GREY_BRUSH.IsOk())
        self.assertTrue(wx.MEDIUM_GREY_BRUSH.IsOk())
        self.assertTrue(wx.LIGHT_GREY_BRUSH.IsOk())
        self.assertTrue(wx.TRANSPARENT_BRUSH.IsOk())
        self.assertTrue(wx.CYAN_BRUSH.IsOk())
        self.assertTrue(wx.RED_BRUSH.IsOk())


    def test_brushOldStyleNames(self):
        b = wx.Brush(wx.RED, wx.SOLID)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
