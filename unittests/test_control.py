import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class ControlTests(wtc.WidgetTestCase):

    def test_ControlCtors(self):
        c = wx.Control(self.frame)
        c = wx.Control(self.frame, -1, wx.Point(10,10), wx.Size(80,-1))


    def test_ControlDefaultCtor(self):
        c = wx.Control()
        c.Create(self.frame)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
