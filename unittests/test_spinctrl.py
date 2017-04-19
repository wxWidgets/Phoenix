import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class spinctrl_Tests(wtc.WidgetTestCase):

    def test_spinctrlCtor(self):
        sp = wx.SpinCtrl(self.frame)
        sp = wx.SpinCtrl(self.frame, value='123')

    def test_spinctrlDefaultCtor(self):
        sp = wx.SpinCtrl()
        sp.Create(self.frame)

    def test_spinctrlProperties(self):
        sp = wx.SpinCtrl(self.frame)
        sp.Max
        sp.Min
        sp.Value

    def test_spinctrlDoubleCtor(self):
        sp = wx.SpinCtrlDouble(self.frame)
        sp = wx.SpinCtrlDouble(self.frame, value='123')

    def test_spinctrlDoubleDefaultCtor(self):
        sp = wx.SpinCtrlDouble()
        sp.Create(self.frame)

    def test_spinctrlDoubleProperties(self):
        sp = wx.SpinCtrlDouble(self.frame)
        sp.Max
        sp.Min
        sp.Value
        sp.Digits
        sp.Increment

    def test_spinctrlOther(self):
        wx.SpinDoubleEvent
        wx.EVT_SPINCTRL
        wx.EVT_SPINCTRLDOUBLE
        wx.wxEVT_COMMAND_SPINCTRL_UPDATED
        wx.wxEVT_COMMAND_SPINCTRLDOUBLE_UPDATED


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
