import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class popupwin_Tests(wtc.WidgetTestCase):

    def test_popupwinCtor(self):
        p = wx.PopupWindow(self.frame, wx.BORDER_SIMPLE)
        p.Position(self.frame.GetPosition() + (50,50), (100,100))
        p.Show()
        wx.CallAfter(p.Destroy)
        self.myYield()

    def test_popupwinDefaultCtor(self):
        p = wx.PopupWindow()
        p.Create(self.frame)

    def test_popuptranswinCtor(self):
        p = wx.PopupTransientWindow(self.frame, wx.BORDER_SIMPLE)
        p.Popup()
        p.Dismiss()

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
