import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class sashwin_Tests(wtc.WidgetTestCase):

    def test_sashwin1(self):
        wx.adv.SW_NOBORDER
        wx.adv.SW_BORDER
        wx.adv.SW_3DSASH
        wx.adv.SW_3DBORDER
        wx.adv.SW_3D
        wx.adv.SASH_TOP
        wx.adv.SASH_RIGHT
        wx.adv.SASH_BOTTOM
        wx.adv.SASH_LEFT
        wx.adv.SASH_NONE
        wx.adv.SASH_STATUS_OK
        wx.adv.SASH_STATUS_OUT_OF_RANGE

        wx.adv.wxEVT_SASH_DRAGGED
        wx.adv.EVT_SASH_DRAGGED

    def test_sashwin2(self):
        sw = wx.adv.SashWindow(self.frame)

    def test_sashwin3(self):
        evt = wx.adv.SashEvent()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
