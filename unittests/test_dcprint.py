import unittest
from unittests import wtc
import wx
import sys

#---------------------------------------------------------------------------

class dcprint_tests(wtc.WidgetTestCase):

    @unittest.skipIf('wxGTK' in wx.PlatformInfo, 'PrinterDC not supported on wxGTK')
    def test_PrinterDC1(self):
        dc = wx.PrinterDC(wx.PrintData())
        dc.DrawLine(0,0, 50,50)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
