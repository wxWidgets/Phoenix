import imp_unittest, unittest
import wtc
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
        
        
    def test_GCDC3(self):
        dc = wx.PrinterDC(wx.PrintData())
        gdc = wx.GCDC(dc)
                
     

    def test_GCDC4(self):
        # TODO: This one is crashing when deallocating the context. Not sure
        # yet if the problem is here or in the GraphicsContext code... To
        # avoid a crash for now I'll just have this test explicitly fail instead.

        self.fail("wxGCDC(context) has known problems...")
        
        #bmp = wx.Bitmap(25,25)
        #dc = wx.MemoryDC(bmp)
        #ctx = wx.GraphicsContext.Create(dc)
        #gdc = wx.GCDC(ctx)
        #del gdc
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
