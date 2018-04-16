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

    def test_canSetValueToNone(self):
        t1 = IC.IntCtrl(self.frame, allow_none=True, value=None)
        assert t1.GetValue() is None
        t2 = IC.IntCtrl(self.frame, allow_none=True)
        t2.SetValue(None)
        assert t2.GetValue() is None


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
