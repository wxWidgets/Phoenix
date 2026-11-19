import sys
import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.lib.platebtn as PB

#---------------------------------------------------------------------------

class lib_platebtn_Tests(wtc.WidgetTestCase):

    def test_lib_platebtnCtor(self):
        btn = PB.PlateButton(self.frame, label='Button', style=PB.PB_STYLE_GRADIENT)
        self.assertEqual(btn.GetLabel(), 'Button')

    def test_lib_platebtnNoBg(self):
        btn = PB.PlateButton(self.frame, label='Button', style=PB.PB_STYLE_NOBG)
        if 'wxMSW' in wx.PlatformInfo:
            self.assertEqual(btn.GetBackgroundStyle(), wx.BG_STYLE_TRANSPARENT)

    def test_lib_platebtnDestroyedAfterLeave(self):
        # Leaving the button, and pressing space on it, update it with timers
        with mock.patch.object(sys, 'excepthook') as excepthook:
            btn = PB.PlateButton(self.frame, label='Button')
            btn.ProcessEvent(wx.MouseEvent(wx.wxEVT_LEAVE_WINDOW))
            evt = wx.KeyEvent(wx.wxEVT_KEY_UP)
            evt.SetKeyCode(wx.WXK_SPACE)
            btn.ProcessEvent(evt)
            btn.Destroy()
            sw = wx.StopWatch()
            while sw.Time() < 300:
                wx.MilliSleep(10)
                self.myYield()
        self.assertFalse(excepthook.called)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
