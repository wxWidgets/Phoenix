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

    def test_lib_calendar_CalenDlgCtor(self):
        dlg = cal.CalenDlg(self.frame, month=1, day=11, year=2014)
        dlg.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
