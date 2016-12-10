import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class dateevt_Tests(wtc.WidgetTestCase):

    def test_dateevt1(self):
        evt = wx.adv.DateEvent()
        evt.GetDate()
        evt.Date

    def test_dateevt2(self):
        wx.adv.wxEVT_DATE_CHANGED
        wx.adv.wxEVT_TIME_CHANGED
        wx.adv.EVT_DATE_CHANGED
        wx.adv.EVT_TIME_CHANGED


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
