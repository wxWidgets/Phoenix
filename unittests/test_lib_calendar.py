import unittest
from unittests import wtc
import wx
import wx.lib.calendar as cal

#---------------------------------------------------------------------------

class lib_calendar_Tests(wtc.WidgetTestCase):

    def test_lib_calendar_CalendarCtor(self):
        pnl = wx.Panel(self.frame)

        acal = cal.Calendar(pnl)

    def test_lib_calendar_CalendarSetDate(self):
        pnl = wx.Panel(self.frame)

        acal = cal.Calendar(pnl)

        acal.SetYear(2014)
        acal.SetMonth(1)
        acal.SetDayValue(31)
        self.assertEqual(acal.GetDate(), (31, 1, 2014))
        self.assertEqual(acal.SetDate(29, 2, 2020), (29, 2, 2020))
        self.assertEqual(acal.SetDate(29, 2, 2019), (28, 2, 2019))
        with self.assertRaises(ValueError):
            acal.SetDate(29, 13, 2019)

    def test_lib_calendar_CalendarMoveDate(self):
        pnl = wx.Panel(self.frame)

        acal = cal.Calendar(pnl)
        acal.SetDate(31, 1, 2020)
        self.assertEqual(acal.IncMonth(), (29, 2, 2020))
        self.assertEqual(acal.IncYear(), (28, 2, 2021))
        self.assertEqual(acal.DecMonth(), (28, 1, 2021))
        self.assertEqual(acal.DecYear(), (28, 1, 2020))

    def test_lib_calendar_CalenDlgCtor(self):
        dlg = cal.CalenDlg(self.frame, month=1, day=11, year=2014)
        dlg.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
