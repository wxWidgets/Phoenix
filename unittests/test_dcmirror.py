import unittest
from unittests import wtc
import wx
import sys

#---------------------------------------------------------------------------

class MirrorDCTests(wtc.WidgetTestCase):

    def test_MirrorDC1(self):
        cdc = wx.ClientDC(self.frame)
        dc = wx.MirrorDC(cdc, True)
        dc.DrawLine(0,0, 50,50)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
