import unittest
from unittests import wtc
import wx
import wx.adv
import os

icoFile = os.path.join(os.path.dirname(__file__), 'mondrian.ico')

#---------------------------------------------------------------------------

class taskbar_Tests(wtc.WidgetTestCase):

    def test_taskbar1(self):
        icon = wx.adv.TaskBarIcon(wx.adv.TBI_DOCK)
        icon.SetIcon(wx.Icon(icoFile), "The tip string")
        self.assertTrue(icon.IsOk())
        icon.Destroy()
        self.myYield()


    def test_taskbar2(self):
        wx.adv.TBI_DOCK
        wx.adv.TBI_CUSTOM_STATUSITEM
        wx.adv.TBI_DEFAULT_TYPE

        wx.adv.TaskBarIconEvent

        wx.adv.wxEVT_TASKBAR_MOVE
        wx.adv.wxEVT_TASKBAR_LEFT_DOWN
        wx.adv.wxEVT_TASKBAR_LEFT_UP
        wx.adv.wxEVT_TASKBAR_RIGHT_DOWN
        wx.adv.wxEVT_TASKBAR_RIGHT_UP
        wx.adv.wxEVT_TASKBAR_LEFT_DCLICK
        wx.adv.wxEVT_TASKBAR_RIGHT_DCLICK
        wx.adv.wxEVT_TASKBAR_CLICK
        wx.adv.wxEVT_TASKBAR_BALLOON_TIMEOUT
        wx.adv.wxEVT_TASKBAR_BALLOON_CLICK

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
