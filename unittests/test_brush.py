import imp_unittest, unittest
import wtc
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
        
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
