import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class activityindicator_Tests(wtc.WidgetTestCase):

    def test_activityindicator1(self):
        ai = wx.ActivityIndicator(self.frame)
        ai.Start()
        self.myYield()
        assert ai.IsRunning()
        ai.Stop()
        assert not ai.IsRunning()

    def test_activityindicator2(self):
        ai = wx.ActivityIndicator()
        ai.Create(self.frame)
        ai.Start()
        self.myYield()
        assert ai.IsRunning()
        ai.Stop()
        assert not ai.IsRunning()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
