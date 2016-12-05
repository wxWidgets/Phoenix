import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class renderer_Tests(wtc.WidgetTestCase):

    # TODO:  Expand these tests, this is really minimal currently

    def test_renderer1(self):
        dc = wx.ClientDC(self.frame)
        r = wx.RendererNative.Get()
        r.DrawCheckBox(self.frame, dc, (10,10, 40,20))

    def test_renderer2(self):
        sp = wx.SplitterRenderParams(5, 5, False)

    def test_renderer3(self):
        hbp = wx.HeaderButtonParams()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
