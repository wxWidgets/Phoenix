import imp_unittest, unittest
import wtc
import wx
import sys

#---------------------------------------------------------------------------


class ScreenDCTests(wtc.WidgetTestCase):
            
    def test_ScreenDC1(self):
        dc = wx.ScreenDC()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
