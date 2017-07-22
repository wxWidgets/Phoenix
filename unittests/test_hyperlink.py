import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class hyperlink_Tests(wtc.WidgetTestCase):

    def test_hyperlink1(self):
        w = wx.adv.HyperlinkCtrl(self.frame, label='label', url='http://wxPython.org')

    def test_hyperlink2(self):
        w = wx.adv.HyperlinkCtrl()
        w.Create(self.frame, label='label', url='http://wxPython.org')

    def test_hyperlink3(self):
        evt = wx.adv.HyperlinkCtrl(self.frame, 123, 'url')

        wx.adv.HL_CONTEXTMENU
        wx.adv.HL_ALIGN_LEFT
        wx.adv.HL_ALIGN_RIGHT
        wx.adv.HL_ALIGN_CENTRE
        wx.adv.HL_DEFAULT_STYLE

        wx.adv.wxEVT_COMMAND_HYPERLINK
        wx.adv.EVT_HYPERLINK

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
