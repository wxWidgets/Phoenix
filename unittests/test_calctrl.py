import unittest
from unittests import wtc
import wx
import wx.adv
import datetime

#---------------------------------------------------------------------------

class calctrl_Tests(wtc.WidgetTestCase):

    def test_calctrl1(self):
        evt = wx.adv.CalendarEvent()
        attr = wx.adv.CalendarDateAttr()

        wx.adv.CAL_SUNDAY_FIRST
        wx.adv.CAL_MONDAY_FIRST
        wx.adv.CAL_SHOW_HOLIDAYS
        wx.adv.CAL_NO_YEAR_CHANGE
        wx.adv.CAL_NO_MONTH_CHANGE
        wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION
        wx.adv.CAL_SHOW_SURROUNDING_WEEKS
        wx.adv.CAL_SHOW_WEEK_NUMBERS

        wx.adv.CAL_HITTEST_NOWHERE
        wx.adv.CAL_HITTEST_HEADER
        wx.adv.CAL_HITTEST_DAY
        wx.adv.CAL_HITTEST_INCMONTH
        wx.adv.CAL_HITTEST_DECMONTH
        wx.adv.CAL_HITTEST_SURROUNDING_WEEK
        wx.adv.CAL_HITTEST_WEEK

        wx.adv.CAL_BORDER_NONE
        wx.adv.CAL_BORDER_SQUARE
        wx.adv.CAL_BORDER_ROUND


    def test_calctrl2(self):
        cal = wx.adv.CalendarCtrl(self.frame, date=wx.DateTime.Today())


    def test_calctrl3(self):
        cal = wx.adv.CalendarCtrl()
        cal.Create(self.frame, date=wx.DateTime.Today())


    def test_calctrl4(self):
        cal = wx.adv.CalendarCtrl(self.frame, date=wx.DateTime.Today())
        d = cal.PyGetDate()
        assert isinstance(d, datetime.datetime)



    def test_genericcalctrl2(self):
        cal = wx.adv.GenericCalendarCtrl(self.frame, date=wx.DateTime.Today())


    def test_genericcalctrl3(self):
        cal = wx.adv.GenericCalendarCtrl()
        cal.Create(self.frame, date=wx.DateTime.Today())


    def test_genericcalctrl4(self):
        cal = wx.adv.GenericCalendarCtrl(self.frame, date=wx.DateTime.Today())
        d = cal.PyGetDate()
        assert isinstance(d, datetime.datetime)



    def test_calevt1(self):
        evt = wx.adv.CalendarEvent()
        evt.SetDate(wx.DateTime.Today())
        d = evt.PyGetDate()
        assert isinstance(d, datetime.datetime)


    def test_calevt2(self):
        wx.adv.EVT_CALENDAR
        wx.adv.EVT_CALENDAR_SEL_CHANGED
        wx.adv.EVT_CALENDAR_WEEKDAY_CLICKED
        wx.adv.EVT_CALENDAR_PAGE_CHANGED
        wx.adv.EVT_CALENDAR_WEEK_CLICKED

        wx.adv.wxEVT_CALENDAR_SEL_CHANGED
        wx.adv.wxEVT_CALENDAR_PAGE_CHANGED
        wx.adv.wxEVT_CALENDAR_DOUBLECLICKED
        wx.adv.wxEVT_CALENDAR_WEEKDAY_CLICKED
        wx.adv.wxEVT_CALENDAR_WEEK_CLICKED


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
