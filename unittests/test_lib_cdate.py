import unittest
from unittests import wtc
import wx.lib.CDate as cdate
import six
import datetime

class lib_cdate_Tests(wtc.WidgetTestCase):

    def test_lib_cdate_DateCtor(self):
        cdate.Date(2014, 1, 31)

    def test_lib_cdate_NowCtor(self):
        cdate.now()

    def test_lib_cdate_IsleapTrue(self):
        l1 = cdate.isleap(2012)
        self.assertTrue(l1, msg='Expected a leap year')

    def test_lib_cdate_IsleapFalse(self):
        l2 = cdate.isleap(2013)
        self.assertFalse(l2, msg='Expected a non leap year')

    def test_lib_cdate_Julianday(self):
        for m in range(3, 6):
            for d in range(10, 20):
                j = cdate.julianDay(2020, m, d)
                jy, jm, jd = cdate.FromJulian(j)
                self.assertEqual((2020, m, d), (jy, jm, jd), 
                    msg='Julian/Gregorian round-trip failed for 2020-%i-%i' % (m, d))

    def test_lib_cdate_Dayofweek(self):
        # this also validates cdate.julianDay, since Date.day_of_week depends on it
        for m in range(3, 6):
            for d in range(10, 20):
                realwd = datetime.date(2020, m, d).weekday()
                testwd = cdate.Date(2020, m, d).day_of_week
                self.assertEqual(realwd, testwd, 
                    msg="Expected weekday to be %i for date 2020-%i-%i, got %i" % (realwd, m, d, testwd))

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
