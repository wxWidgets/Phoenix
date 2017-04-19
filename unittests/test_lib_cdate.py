import unittest
from unittests import wtc
import wx.lib.CDate as cdate
import six


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
        bd = cdate.Date(2014, 1, 10)
        jd = cdate.julianDay(bd.year, bd.month, bd.day)

        self.assertTrue(jd == bd.julian,
                        msg='Expected them to be equal')

    def test_lib_cdate_Dayofweek(self):
        jd = cdate.julianDay(2014, 1, 10)
        dw = cdate.dayOfWeek(jd)
        self.assertTrue(dw == 4, msg='Expected "4" assuming Monday is 1, got %s' % dw)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
