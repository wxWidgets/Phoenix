import unittest
from unittests import wtc
import wx

import wx.lib.agw.balloontip as BT

#---------------------------------------------------------------------------

class lib_agw_balloontip_Tests(wtc.WidgetTestCase):

    def test_lib_agw_balloontipCtor(self):
        tip = BT.BalloonTip(toptitle='Balloon', message='Hello wxPython',
                            shape=BT.BT_ROUNDED, tipstyle=BT.BT_BUTTON)

    def test_lib_agw_balloontipMethods(self):
        tip = BT.BalloonTip(toptitle='Balloon', message='Hello wxPython',
                            shape=BT.BT_ROUNDED, tipstyle=BT.BT_BUTTON)

        self.assertTrue(tip.GetBalloonShape() == BT.BT_ROUNDED)
        self.assertTrue(tip.GetBalloonTipStyle() == BT.BT_BUTTON)

        tip.SetBalloonShape(BT.BT_RECTANGLE)
        tip.SetBalloonTipStyle(BT.BT_LEAVE)
        self.assertTrue(tip.GetBalloonShape() == BT.BT_RECTANGLE)
        self.assertTrue(tip.GetBalloonTipStyle() == BT.BT_LEAVE)

    def test_lib_agw_balloontipFrameShape(self):
        tip = BT.BalloonTip(toptitle='Balloon', message='Hello wxPython',
                            shape=BT.BT_ROUNDED, tipstyle=BT.BT_BUTTON)
        frame = BT.BalloonFrame(self.frame, classparent=tip)
        try:
            frame.SetBalloonShape()
            self.assertTrue(frame.hasShape)
        finally:
            frame.Destroy()

    def test_lib_agw_balloontipConstantsExist(self):
        BT.BT_ROUNDED
        BT.BT_RECTANGLE
        BT.BT_LEAVE
        BT.BT_CLICK
        BT.BT_BUTTON


    def test_lib_agw_balloontipCloseButtonWithoutTitle(self):
        # wx 3.3 asserts about alignment flags that a sizer would ignore
        tip = BT.BalloonTip(message='Hello wxPython', tipstyle=BT.BT_BUTTON)
        target = wx.Window(self.frame)
        tip.SetTarget(target)
        frame = BT.BalloonFrame(self.frame, classparent=tip)
        frame.Destroy()

    def waitFor(self, ms):
        for _ in range(ms // 50):
            wx.MilliSleep(50)
            self.myYield()

    def test_lib_agw_balloontipEndDelay(self):
        tip = BT.BalloonTip(message='Hello wxPython', tipstyle=BT.BT_BUTTON)
        tip.SetEndDelay(100)
        tip.SetTarget(wx.Button(self.frame, label='target'))
        tip.NotifyTimer(None)
        self.assertTrue(tip.BalloonFrame)
        self.waitFor(600)
        self.assertFalse(tip.BalloonFrame)

    def test_lib_agw_balloontipTargetDestroyed(self):
        tip = BT.BalloonTip(message='Hello wxPython', tipstyle=BT.BT_BUTTON)
        tip.SetEndDelay(200)
        target = wx.Button(self.frame, label='target')
        tip.SetTarget(target)
        tip.NotifyTimer(None)
        # Don't let a timer that wasn't stopped crash the rest of the tests
        self.addCleanup(lambda: tip.destroytime.Stop())
        target.Destroy()
        # The timer belongs to the destroyed target, so it must not fire
        self.assertFalse(tip.destroytime.IsRunning())

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
