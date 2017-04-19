import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class timer_Tests(wtc.WidgetTestCase):

    def onTimerEvt(self, *evt):
        self.flag = True


    def test_timerOwner1(self):
        t = wx.Timer(self.frame)
        self.flag = False
        self.frame.Bind(wx.EVT_TIMER, self.onTimerEvt, t)
        t.Start(250, wx.TIMER_ONE_SHOT)
        self.waitFor(500)
        self.assertTrue(self.flag)


    def test_timerOwner2(self):
        t = wx.Timer(self.frame)
        self.flag = False
        self.frame.Bind(wx.EVT_TIMER, self.onTimerEvt, t)
        t.Start(1000, wx.TIMER_ONE_SHOT)
        # timer will not have expired yet by this time, so flag shouldn't be set
        self.waitFor(500)
        self.assertFalse(self.flag)


    def test_timerPyTimer(self):
        t = wx.PyTimer(self.onTimerEvt)
        self.flag = False
        t.Start(250, wx.TIMER_ONE_SHOT)
        self.waitFor(500)
        self.assertTrue(self.flag)


    def test_timerDerivedClass(self):
        class MyTimer(wx.Timer):
            def __init__(self):
                wx.Timer.__init__(self)
                self.flag = False
            def Notify(self):
                self.flag = True

        t = MyTimer()
        t.Start(250, wx.TIMER_ONE_SHOT)
        self.waitFor(500)
        self.assertTrue(t.flag)


    def onCallLater(self):
        self.flag = True
        return 1234

    def test_timerCallLater1(self):
        # simple CallLater usage
        wx.CallLater(150, self.onCallLater)
        self.waitFor(500)
        self.assertTrue(self.flag)


    def test_timerCallLater2(self):
        # test getting the result and restarting the CallLater
        cl = wx.CallLater(250, self.onCallLater)
        self.assertTrue(cl.IsRunning())
        self.waitFor(500)
        self.assertTrue(self.flag)
        self.assertTrue(cl.GetResult() == 1234)
        self.flag = False
        cl.Restart()
        self.waitFor(500)
        self.assertTrue(self.flag)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
