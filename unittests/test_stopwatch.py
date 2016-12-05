import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class stopwatch_Tests(wtc.WidgetTestCase):

    def test_stopwatch1(self):
        sw = wx.StopWatch()
        self.waitFor(1000)
        t = sw.Time()
        self.assertTrue(t > 900)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
