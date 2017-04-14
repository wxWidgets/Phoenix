import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class radiobut_Tests(wtc.WidgetTestCase):

    def test_radiobutCtors(self):
        b = wx.RadioButton(self.frame, -1, 'radiobutton', wx.Point(10,10), wx.Size(80,-1))
        b = wx.RadioButton(self.frame, label='radiobutton', style=wx.RB_GROUP)

    def test_radiobutDefaultCtor(self):
        b = wx.RadioButton()
        b.Create(self.frame, label="radiobutton")

    def test_radiobutValue(self):
        b = wx.RadioButton(self.frame, label='radiobutton', style=wx.RB_GROUP)
        b1 = wx.RadioButton(self.frame, label='radiobutton1')
        b1.Value = True
        self.assertTrue(b.GetValue() == False)
        self.assertTrue(b1.GetValue() == True)
        b.Value = True
        self.assertTrue(b.GetValue() == True)
        self.assertTrue(b1.GetValue() == False)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
