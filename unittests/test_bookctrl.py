import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class panel_Tests(wtc.WidgetTestCase):

    def test_bookctrl1(self):
        wx.BK_DEFAULT
        wx.BK_TOP
        wx.BK_BOTTOM
        wx.BK_LEFT
        wx.BK_RIGHT
        wx.BK_HITTEST_NOWHERE
        wx.BK_HITTEST_ONICON
        wx.BK_HITTEST_ONLABEL
        wx.BK_HITTEST_ONITEM
        wx.BK_HITTEST_ONPAGE


    def test_bookctrl2(self):
        # These are actually aliases for wx.Notebook
        wx.BookCtrl
        wx.wxEVT_COMMAND_BOOKCTRL_PAGE_CHANGED
        wx.wxEVT_COMMAND_BOOKCTRL_PAGE_CHANGING
        wx.EVT_BOOKCTRL_PAGE_CHANGED
        wx.EVT_BOOKCTRL_PAGE_CHANGING


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
