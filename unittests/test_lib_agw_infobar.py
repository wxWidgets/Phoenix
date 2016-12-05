import unittest
from unittests import wtc
import wx

import wx.lib.agw.infobar as IB

#---------------------------------------------------------------------------

class lib_agw_infobar_Tests(wtc.WidgetTestCase):

    def test_lib_agw_infobarCtor(self):
        ib = IB.InfoBar(self.frame)

    def test_lib_agw_infobar1(self):
        ib = IB.InfoBar(self.frame)
        ib.ShowMessage("hello world")
        self.myYield()
        ib.Dismiss()

    def test_lib_agw_infobar2(self):
        ib = IB.InfoBar(self.frame)
        ib.AddButton(1234, "New Button")
        ib.AddButton(wx.ID_SAVE)
        ib.ShowMessage("hello world")
        self.myYield()
        ib.RemoveButton(wx.ID_SAVE)
        ib.Dismiss()

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()