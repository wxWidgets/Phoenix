import unittest
from unittests import wtc
import wx
import sys

#---------------------------------------------------------------------------

class ClientDCTests(wtc.WidgetTestCase):

    def test_ClientDC(self):
        dc = wx.ClientDC(self.frame)
        dc.DrawLine(0,0, 50,50)

    def test_WindowDC(self):
        dc = wx.WindowDC(self.frame)
        dc.DrawLine(0,0, 50,50)


    def test_PaintDC(self):
        class TestPanel(wx.Panel):
            def __init__(self, *args, **kw):
                wx.Panel.__init__(self, *args, **kw)
                #self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
                self.Bind(wx.EVT_PAINT, self.onPaint)
                self.onPaintCalled = False

            def onPaint(self, evt):
                dc = wx.PaintDC(self)
                dc.DrawLine(0,0, 50,50)
                self.onPaintCalled = True

        panel = TestPanel(self.frame)
        self.frame.SendSizeEvent()
        panel.Refresh()
        self.myUpdate(panel)
        self.waitFor(200)
        self.assertTrue(panel.onPaintCalled == True)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
