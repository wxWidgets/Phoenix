import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class checkbox_Tests(wtc.WidgetTestCase):

    def test_checkboxCtors(self):
        c = wx.CheckBox(self.frame, label="checkbox")
        c = wx.CheckBox(self.frame, -1, "checkbox", wx.Point(10,10), wx.Size(80,-1))


    def test_checkboxDefaultCtor(self):
        c = wx.CheckBox()
        c.Create(self.frame, label="checkbox")



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
