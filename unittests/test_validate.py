import unittest
from unittests import wtc
import wx
import os


#---------------------------------------------------------------------------

class MyValidator(wx.Validator):
    def __init__(self, startingValue=""):
        wx.Validator.__init__(self)
        self.value = startingValue

    def Clone(self):
        return MyValidator(self.value)

    def TransferToWindow(self):
        self.GetWindow().SetValue(self.value)
        return True

    def TransferFromWindow(self):
        self.value = self.Window.Value # test using the properties
        return True

    def Validate(self, parent):
        value = self.GetWindow().GetValue()
        return value in ["", "hello", "world"]


class validate_Tests(wtc.WidgetTestCase):

    def setUp(self):
        super(validate_Tests, self).setUp()
        self.pnl = wx.Panel(self.frame)
        self.tc = wx.TextCtrl(self.pnl, pos=(10,10))
        self.frame.SendSizeEvent()
        validator = MyValidator("hello")
        self.tc.SetValidator(validator)


    def test_validateTransfer(self):
        self.assertTrue(self.tc.Value == "")
        self.pnl.TransferDataToWindow()
        self.assertTrue(self.tc.Value == "hello")
        self.tc.Value = "world"
        self.pnl.TransferDataFromWindow()
        v = self.tc.GetValidator()
        self.assertTrue(v.value == "world")



    def test_validateDefault(self):
        wx.DefaultValidator

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
