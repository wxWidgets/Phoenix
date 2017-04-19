import unittest
from unittests import wtc
import wx
import sys

#---------------------------------------------------------------------------

class MemoryDCTests(wtc.WidgetTestCase):

    def test_MemoryDC1(self):
        bmp = wx.Bitmap(250,250)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.DrawLine(0,0, 50,50)


    def test_MemoryDC2(self):
        bmp = wx.Bitmap(250,250)
        dc = wx.MemoryDC(bmp)
        dc.DrawLine(0,0, 50,50)

    def test_MemoryDC3(self):
        cdc = wx.ClientDC(self.frame)
        dc = wx.MemoryDC(cdc)
        bmp = wx.Bitmap(250,250)
        dc.SelectObject(bmp)
        dc.DrawLine(0,0, 50,50)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
