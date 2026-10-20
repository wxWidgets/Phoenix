import unittest
from unittests import wtc
import wx
import wx.siplib

#---------------------------------------------------------------------------

class tipwin_Tests(wtc.WidgetTestCase):

    def test_tipwinCtor(self):
        w = wx.TipWindow(self.frame, "This is a tip message")
        w.SetBoundingRect(self.frame.GetRect())
        self.waitFor(100)
        # w may have already self-destructed (e.g. lost focus)
        if w:
            w.Close()

    def test_tipwinCtorRectBounds(self):
        w = wx.TipWindow(self.frame, "This is a tip message", 200,
                         self.frame.GetScreenRect())
        self.waitFor(100)
        if w:
            w.Close()

    def test_tipwinClose(self):
        w = wx.TipWindow(self.frame, "This is a tip message")
        assert w
        assert w.Close() is True
        # closed, but not destroyed until idle time
        assert not w
        assert not wx.siplib.isdeleted(w)
        # closing again must not try to destroy it twice
        w.Close()
        self.myYield()
        # wxTipWindow::Close() doesn't destroy the window on wxMac, it relies
        # on a kill focus event that may not happen here.
        if 'wxMac' not in wx.PlatformInfo:
            assert wx.siplib.isdeleted(w)
        assert not w

    def test_tipwinTwoStep(self):
        w = wx.TipWindow()
        assert w.Create(self.frame, "This is a tip message",
                        rectBounds=self.frame.GetScreenRect()) is True
        self.waitFor(100)
        if w:
            w.Close()



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
