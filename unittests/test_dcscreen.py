import unittest
from unittests import wtc
import wx
import sys

#---------------------------------------------------------------------------


class ScreenDCTests(wtc.WidgetTestCase):

    def test_ScreenDC1(self):
        dc = wx.ScreenDC()
        dc.DrawLine(0,0, 50,50)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
