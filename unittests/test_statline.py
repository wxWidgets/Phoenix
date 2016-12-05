import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class statline_Tests(wtc.WidgetTestCase):

    def test_statlineCtor(self):
        sl = wx.StaticLine(self.frame)
        sl = wx.StaticLine(self.frame, style=wx.LI_VERTICAL)


    def test_statlineDefaultCtor(self):
        sl = wx.StaticLine()
        sl.Create(self.frame, style=wx.LI_VERTICAL)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
