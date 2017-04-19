import unittest
from unittests import wtc
import wx
import sys

#---------------------------------------------------------------------------

class dcgraph_tests(wtc.WidgetTestCase):

    def test_GCDC1(self):
        dc = wx.ClientDC(self.frame)
        gdc = wx.GCDC(dc)


    def test_GCDC2(self):
        bmp = wx.Bitmap(25,25)
        dc = wx.MemoryDC(bmp)
        gdc = wx.GCDC(dc)


    @unittest.skipIf('wxGTK' in wx.PlatformInfo, 'PrinterDC not supported on wxGTK')
    def test_GCDC3(self):
        dc = wx.PrinterDC(wx.PrintData())
        gdc = wx.GCDC(dc)


    def test_GCDC4(self):
        bmp = wx.Bitmap(25,25)
        dc = wx.MemoryDC(bmp)
        ctx = wx.GraphicsContext.Create(dc)
        gdc = wx.GCDC(ctx)
        del gdc

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
