import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class timectrl_Tests(wtc.WidgetTestCase):

    def test_timectrl1(self):
        pnl = wx.Panel(self.frame)
        tc = wx.adv.TimePickerCtrl(pnl, pos=(10,10))
        tc.SetValue(wx.DateTime.Now())
        tc.GetValue()
        tc.SetTime(12, 34, 59)
        h, m, s = tc.GetTime()
        self.assertEqual( (h, m, s),  (12, 34, 59) )


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
