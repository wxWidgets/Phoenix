import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class caret_Tests(wtc.WidgetTestCase):

    def test_caret1(self):
        pnl = wx.Window(self.frame)
        c = wx.Caret(pnl, (2, 15))
        self.assertTrue(c.IsOk())
        wx.Caret.SetBlinkTime(100)
        c.Move((50,50))
        c.Show()
        self.waitFor(300)

    def test_caret2(self):
        pnl = wx.Window(self.frame)
        c = wx.Caret()
        c.Create(pnl, 2, 15)
        self.assertTrue(c.IsOk())
        wx.Caret.SetBlinkTime(100)
        c.Move(50,50)
        c.Show()
        self.waitFor(300)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
