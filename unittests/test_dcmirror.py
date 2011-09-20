import imp_unittest, unittest
import wtc
import wx
import sys

#---------------------------------------------------------------------------

class MirrorDCTests(wtc.WidgetTestCase):
            
    def test_MirrorDC1(self):
        cdc = wx.ClientDC(self.frame)
        dc = wx.MirrorDC(cdc, True)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
