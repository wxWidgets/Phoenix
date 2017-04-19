import unittest
from unittests import wtc
import wx
import wx.lib.intctrl as IC

#---------------------------------------------------------------------------


class IntCtrlTests(wtc.WidgetTestCase):

    def test_intctrlCtor(self):
        t1 = IC.IntCtrl(self.frame)
        t2 = IC.IntCtrl(self.frame, -1, 10)
        t3 = IC.IntCtrl(self.frame, value=32, min=32, max=72)
        t3.ChangeValue(16)
        self.assertTrue(not t3.IsInBounds())


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
