import imp_unittest, unittest
import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'pointy.png')

#---------------------------------------------------------------------------

class headercol_Tests(wtc.WidgetTestCase):

    def test_headercolCtor1(self):
        hc = wx.HeaderColumnSimple('title', 80, wx.ALIGN_RIGHT, wx.COL_RESIZABLE)

        
    def test_headercolCtor2(self):
        bmp = wx.Bitmap(pngFile)
        hc = wx.HeaderColumnSimple(bmp, flags=wx.COL_RESIZABLE)
        hc.Bitmap

        
    def test_headercolProperties(self):
        hc = wx.HeaderColumnSimple('title', 80, wx.ALIGN_RIGHT, wx.COL_RESIZABLE)
        # normal properties
        hc.Title
        hc.Width
        hc.MinWidth
        hc.Alignment
        hc.Flags

        # monkey-patched
        hc.Hidden
        self.assertTrue(hc.Hidden == hc.IsHidden())
        hc.Hidden = True
        self.assertTrue(hc.Hidden == hc.IsHidden())
        self.assertTrue(hc.Shown == hc.IsShown())
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
