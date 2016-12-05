import unittest
from unittests import wtc
import wx
import wx.lib.statbmp

#---------------------------------------------------------------------------

class lib_statbmp_Tests(wtc.WidgetTestCase):

    def test_lib_statbmp1(self):
        pnl = wx.Panel(self.frame)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (32, 32))
        w = wx.lib.statbmp.GenStaticBitmap(pnl, -1, bitmap=bmp, pos=(10,10))
        bs1 = w.GetEffectiveMinSize()

        bmp2 = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (64, 64))
        w.SetBitmap(bmp2)
        bs2 = w.GetEffectiveMinSize()

        self.assertEqual(w.GetBitmap(), bmp2)
        self.assertTrue(bs2.height > bs1.height)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
