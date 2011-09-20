import imp_unittest, unittest
import wtc
import wx
import sys

#---------------------------------------------------------------------------

class MemoryDCTests(wtc.WidgetTestCase):
            
    def test_MemoryDC1(self):
        bmp = wx.Bitmap(25,25)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)

        
    def test_MemoryDC2(self):
        bmp = wx.Bitmap(25,25)
        dc = wx.MemoryDC(bmp)
        
    def test_MemoryDC3(self):
        cdc = wx.ClientDC(self.frame)
        dc = wx.MemoryDC(cdc)
        bmp = wx.Bitmap(25,25)
        dc.SelectObject(bmp)
        

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
