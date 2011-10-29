import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class scrolwin_Tests(wtc.WidgetTestCase):

    def commonBits(self, w):
        vsize = 750
        rate = 20
        
        w.SetSize(self.frame.GetClientSize())
        w.EnableScrolling(True, True)
        w.ShowScrollbars(wx.SHOW_SB_ALWAYS, wx.SHOW_SB_ALWAYS)
        w.SetVirtualSize((vsize, vsize))
        w.SetScrollRate(rate, rate)
        w.Scroll(3,3) # in scroll units
        self.myYield()
        self.assertEqual(w.GetVirtualSize(),           (vsize,vsize))
        self.assertEqual(w.GetScrollPixelsPerUnit(),   (rate,rate))
        self.assertEqual(w.GetViewStart(),             (3,3))  # scroll units
        self.assertEqual(w.CalcScrolledPosition(0,0),  (-3*rate,-3*rate)) # pixels
        self.assertEqual(w.CalcUnscrolledPosition(0,0),(3*rate,3*rate))   # pixels
        

    def test_scrolwinCtor(self):
        w = wx.ScrolledWindow(self.frame)
        self.commonBits(w)
        
    def test_scrolwinDefaultCtor(self):
        w = wx.ScrolledWindow()
        w.Create(self.frame)
        self.commonBits(w)
        
    def test_scrolcvsCtor(self):
        w = wx.ScrolledCanvas(self.frame)
        self.commonBits(w)

    def test_scrolcvsDefaultCtor(self):
        w = wx.ScrolledCanvas()
        w.Create(self.frame)
        self.commonBits(w)
        
    def test_scrolwinOnDraw(self):
        
        class MyScrolledWin(wx.ScrolledWindow):
            def __init__(self, *args, **kw):
                wx.ScrolledWindow.__init__(self, *args, **kw)
                self.flag = False
            def OnDraw(self, dc):
                self.flag = True
                sz = dc.GetSize()
                dc.SetPen(wx.Pen('blue', 3))
                dc.DrawLine(0, 0, sz.width, sz.height)
                
        w = MyScrolledWin(self.frame)
        self.commonBits(w)
        w.Refresh()
        self.myYield()
        self.assertTrue(w.flag) # True if OnDraw was called
                
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
