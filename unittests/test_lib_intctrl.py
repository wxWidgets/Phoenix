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

    def test_disallowLongKeepsIntValue(self):
        t = IC.IntCtrl(self.frame, value=-5, min=-10, max=10, limited=True,
                       allow_long=True)
        t.SetLongAllowed(False)
        self.assertEqual(t.GetValue(), -5)
        t.SetValue(7)
        self.assertEqual(t.GetValue(), 7)

    def test_allowLongCtorArg(self):
        self.assertFalse(IC.IntCtrl(self.frame).IsLongAllowed())
        self.assertTrue(IC.IntCtrl(self.frame, allow_long=True).IsLongAllowed())

    def test_longValues(self):
        big = IC.MAXSIZE + 1
        t = IC.IntCtrl(self.frame, allow_long=True)
        t.SetValue(big)
        self.assertEqual(t.GetValue(), big)
        t.SetLongAllowed(False)
        self.assertEqual(t.GetValue(), IC.MAXSIZE)
        with self.assertRaises(ValueError):
            t.SetValue(big)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
