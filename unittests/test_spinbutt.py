import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class spinbutt_Tests(wtc.WidgetTestCase):

    def test_spinbuttCtor(self):
        sb = wx.SpinButton(self.frame)

    def test_spinbuttDefaultCtor(self):
        sb = wx.SpinButton()
        sb.Create(self.frame)

    def test_spinctrlProperties(self):
        sb = wx.SpinButton(self.frame)
        sb.Max
        sb.Min
        sb.Value
        sb.Range

    def test_spinctrlPropertiesInAction(self):
        sb = wx.SpinButton(self.frame)
        sb.Max = 75
        sb.Min = 25
        sb.Value = 50
        self.assertTrue((sb.GetMin(), sb.GetMax()) == (25, 75))
        self.assertTrue(sb.GetRange() == (25, 75))
        self.assertTrue(sb.Range == (25, 75))
        self.assertTrue(sb.GetValue() == 50)


    def test_spinbuttOther(self):
        wx.SpinEvent

        wx.EVT_SPIN_UP
        wx.EVT_SPIN_DOWN
        wx.EVT_SPIN
        wx.wxEVT_SPIN_UP
        wx.wxEVT_SPIN_DOWN
        wx.wxEVT_SPIN

        wx.SP_HORIZONTAL
        wx.SP_VERTICAL
        wx.SP_ARROW_KEYS
        wx.SP_WRAP


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
