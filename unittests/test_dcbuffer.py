import unittest
from unittests import wtc
import wx
import sys

#---------------------------------------------------------------------------

class BufferedDCTests(wtc.WidgetTestCase):

    def test_0_CheckKeepReference(self):
        # We're using the KeepReference annotation for the dc and bitmap args
        # to ensure that they will live as long as the DC does. This test will
        # try to verify that it works the way I think it does, that the extra
        # reference is made, and also released when the DC goes away.
        cdc = wx.ClientDC(self.frame)
        bmp = wx.Bitmap(1,1)
        cdc_cnt1 = sys.getrefcount(cdc)
        bmp_cnt1 = sys.getrefcount(bmp)

        dc = wx.BufferedDC(cdc, bmp)

        cdc_cnt2 = sys.getrefcount(cdc)
        bmp_cnt2 = sys.getrefcount(bmp)

        del dc

        cdc_cnt3 = sys.getrefcount(cdc)
        bmp_cnt3 = sys.getrefcount(bmp)

        self.assertTrue(cdc_cnt2 == cdc_cnt1 + 1)
        self.assertTrue(cdc_cnt3 == cdc_cnt1)
        self.assertTrue(bmp_cnt2 == bmp_cnt1 + 1)
        self.assertTrue(bmp_cnt3 == bmp_cnt1)



    def test_BufferedDCDefaultCtor(self):
        dc = wx.BufferedDC()
        dc.Init(None, wx.Bitmap(25,25))
        dc.DrawLine(0,0, 50,50)


    def test_BufferedDCCtors(self):
        dc = wx.BufferedDC(wx.ClientDC(self.frame), wx.Size(100,100))
        dc.DrawLine(0,0, 50,50)
        dc = wx.BufferedDC(wx.ClientDC(self.frame))
        dc.DrawLine(0,0, 50,50)
        dc = wx.BufferedDC(None, wx.Bitmap(100,100))
        dc.DrawLine(0,0, 50,50)


    def test_BufferedPaintDC(self):
        class TestPanel(wx.Panel):
            def __init__(self, *args, **kw):
                wx.Panel.__init__(self, *args, **kw)
                self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
                self.Bind(wx.EVT_PAINT, self.onPaint)
                self.bmp = wx.Bitmap(100,100)
                self.onPaintCalled = False

            def onPaint(self, evt):
                dc = wx.BufferedPaintDC(self, self.bmp)
                dc.DrawLine(0,0, 50,50)
                self.onPaintCalled = True

        panel = TestPanel(self.frame)
        self.frame.SendSizeEvent()
        panel.Refresh()
        self.myUpdate(panel)
        self.waitFor(200)
        self.assertTrue(panel.onPaintCalled == True)


    def test_AutoBufferedPaintDC(self):
        class TestPanel(wx.Panel):
            def __init__(self, *args, **kw):
                wx.Panel.__init__(self, *args, **kw)
                self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
                self.Bind(wx.EVT_PAINT, self.onPaint)
                self.onPaintCalled = False

            def onPaint(self, evt):
                dc = wx.AutoBufferedPaintDC(self)
                dc.DrawLine(0,0, 50,50)
                self.onPaintCalled = True

        panel = TestPanel(self.frame)
        self.frame.SendSizeEvent()
        panel.Refresh()
        self.myUpdate(panel)
        self.waitFor(200)
        self.assertTrue(panel.onPaintCalled == True)


    def test_BufferedDCConstantsExist(self):
        wx.BUFFER_VIRTUAL_AREA
        wx.BUFFER_CLIENT_AREA
        wx.BUFFER_USES_SHARED_BUFFER

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
