import imp_unittest, unittest
import wx
import wtc
import datetime
import time

##import os; print 'PID:', os.getpid(); raw_input('Ready to start, press enter...')

#---------------------------------------------------------------------------

class datetime_Tests(wtc.WidgetTestCase):

    def test_datetime1(self):
        d1 = wx.DateTime()
        self.assertTrue(not d1.IsValid())
        d2 = wx.DateTime(1, wx.DateTime.Mar, 2012, 8, 15, 45, 123)
        self.assertEqual(d2.year, 2012)
        self.assertEqual(d2.month, wx.DateTime.Mar)
        self.assertEqual(d2.day, 1)
        self.assertEqual(d2.hour, 8)
        self.assertEqual(d2.minute, 15)
        self.assertEqual(d2.second, 45)

    def test_datetime2(self):
        d1 = wx.DateTime.FromHMS(8, 15, 45, 123)
        d2 = wx.DateTime.FromJDN(12345.67)
        d3 = wx.DateTime.FromTimeT(int(time.time()))
        d4 = wx.DateTime.FromDMY(1, wx.DateTime.Mar, 2012, 8, 15, 45, 123)
        
    def test_datetime3(self):
        d1 = wx.DateTime.Today()
        d2 = wx.DateTime.Now()
        self.assertTrue( d1 != d2)
        self.assertTrue( d2 > d1)
        d3 = wx.DateTime(d1)
        self.assertTrue(d1 is not d3)
        self.assertTrue(d1 == d3)

    def test_datetime4(self):
        d1 = wx.DateTime.Today()
        d2 = wx.DateTime.Now()
        span = d2 - d1
        self.assertTrue(isinstance(span, wx.TimeSpan))
        
    def test_datetimeGetAmPm(self):
        am, pm = wx.DateTime.GetAmPmStrings()
        if wtc.isPython3():
            base = str
        else:
            base = unicode
        self.assertTrue(isinstance(am, base) and am != "")
        self.assertTrue(isinstance(pm, base) and pm != "")
        
        
    def test_datetimeProperties(self):
        d1 = wx.DateTime.Today()
        d1.day 
        d1.month 
        d1.year 
        d1.hour 
        d1.minute 
        d1.second 
        d1.millisecond 
        d1.JDN 
        d1.DayOfYear 
        d1.JulianDayNumber 
        d1.LastMonthDay 
        d1.MJD 
        d1.ModifiedJulianDayNumber 
        d1.RataDie 
        d1.Ticks 
        d1.WeekOfMonth 
        d1.WeekOfYear 
        
        
    def test_datetimeConvertFromPyDatetime(self):
        dt = datetime.datetime(2012, 3, 1, 8, 15, 45)
        d = wx.DateTime(dt)
        self.assertEqual(d.year, 2012)
        self.assertEqual(d.month, wx.DateTime.Mar)
        self.assertEqual(d.day, 1)
        self.assertEqual(d.hour, 8)
        self.assertEqual(d.minute, 15)
        self.assertEqual(d.second, 45)

    def test_datetimeConvertFromPyDate(self):
        dt = datetime.date(2012, 3, 1)
        d = wx.DateTime(dt)
        self.assertEqual(d.year, 2012)
        self.assertEqual(d.month, wx.DateTime.Mar)
        self.assertEqual(d.day, 1)
        self.assertEqual(d.hour, 0)
        self.assertEqual(d.minute, 0)
        self.assertEqual(d.second, 0)


    def test_datetimeTm(self):
        d = wx.DateTime.Now()
        tm = d.GetTm()
        self.assertTrue(isinstance(tm, wx.DateTime.Tm))
        self.assertTrue(tm.IsValid())
        tm.msec
        tm.sec 
        tm.min 
        tm.hour
        tm.mday
        tm.yday
        tm.mon 
        tm.year


    def test_datetimeSet(self):
        d1 = wx.DateTime.Now()
        tm = d1.GetTm()
        
        d2 = wx.DateTime()
        d2.SetTm(tm)
        self.assertTrue(d1 == d2)
        
        d3 = wx.DateTime()
        d3.Set(tm.mday, tm.mon, tm.year, tm.hour, tm.min, tm.sec, tm.msec)
        self.assertTrue(d1 == d3)
       

    def test_datetimeFormatParse(self):
        d = wx.DateTime(1, wx.DateTime.Mar, 2012, 8, 15, 45)
        fmt = '%Y-%m-%d %H:%M:%S'
        st = d.Format(fmt)
        self.assertEqual(st, '2012-03-01 08:15:45')

        d2 = wx.DateTime()
        d2.ParseFormat(st, fmt)
        self.assertEqual(d, d2)


    def test_datetimeConvertHelpers(self):
        d1 = wx.DateTime(1, wx.DateTime.Mar, 2012, 8, 15, 45)
        pd = wx.wxdate2pydate(d1)
        d2 = wx.pydate2wxdate(pd)
        self.assertTrue(isinstance(pd, datetime.datetime))
        self.assertEqual(d1, d2)
        
                                   
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
