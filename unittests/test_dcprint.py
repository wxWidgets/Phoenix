import imp_unittest, unittest
import wtc
import wx
import sys

#---------------------------------------------------------------------------

class dcprint_tests(wtc.WidgetTestCase):
            
    def test_PrinterDC1(self):
        dc = wx.PrinterDC(wx.PrintData())
                
        

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
