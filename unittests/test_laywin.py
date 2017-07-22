import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class laywin_Tests(wtc.WidgetTestCase):

    def test_laywin1(self):
        wx.adv.LAYOUT_HORIZONTAL
        wx.adv.LAYOUT_VERTICAL
        wx.adv.LAYOUT_NONE
        wx.adv.LAYOUT_TOP
        wx.adv.LAYOUT_LEFT
        wx.adv.LAYOUT_RIGHT
        wx.adv.LAYOUT_BOTTOM

        wx.adv.wxEVT_QUERY_LAYOUT_INFO
        wx.adv.wxEVT_CALCULATE_LAYOUT
        wx.adv.EVT_QUERY_LAYOUT_INFO
        wx.adv.EVT_CALCULATE_LAYOUT


    def test_laywin2(self):
        la = wx.adv.LayoutAlgorithm()
        la.LayoutFrame(self.frame)

    def test_laywin3(self):
        w = wx.adv.SashLayoutWindow(self.frame)

    def test_laywin4(self):
        evt = wx.adv.QueryLayoutInfoEvent()

    def test_laywin5(self):
        evt = wx.adv.CalculateLayoutEvent()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
