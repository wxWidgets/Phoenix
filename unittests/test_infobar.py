import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class infobar_Tests(wtc.WidgetTestCase):

    def test_infobarCtor(self):
        ib = wx.InfoBar(self.frame)

    def test_infobarDefaultCtor(self):
        ib = wx.InfoBar()
        ib.Create(self.frame)

    def test_infobar1(self):
        ib = wx.InfoBar(self.frame)
        ib.ShowMessage("hello world")
        self.myYield()
        ib.Dismiss()

    def test_infobar2(self):
        ib = wx.InfoBar(self.frame)
        ib.AddButton(1234, "New Button")
        ib.AddButton(wx.ID_SAVE)
        ib.ShowMessage("hello world")
        self.myYield()
        ib.RemoveButton(wx.ID_SAVE)
        ib.Dismiss()

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
