import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class collheaderctrl_Tests(wtc.WidgetTestCase):

    def test_collheaderctrl1(self):
        chc = wx.CollapsibleHeaderCtrl(self.frame, label='Hello')
        chc.SetCollapsed(True)
        assert chc.IsCollapsed()
        chc.SetCollapsed(False)
        assert not chc.IsCollapsed()


    def test_collheaderctrl2(self):
        chc = wx.CollapsibleHeaderCtrl()
        chc.Create(self.frame, label='Hello')
        chc.SetCollapsed(True)
        assert chc.IsCollapsed()
        chc.SetCollapsed(False)
        assert not chc.IsCollapsed()


    def test_collheaderctrl3(self):
        wx.wxEVT_COLLAPSIBLEHEADER_CHANGED
        wx.EVT_COLLAPSIBLEHEADER_CHANGED
        assert wx.EVT_COLLAPSIBLEHEADER_CHANGED.typeId == wx.wxEVT_COLLAPSIBLEHEADER_CHANGED

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
