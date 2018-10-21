import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class statbox_Tests(wtc.WidgetTestCase):

    def test_statboxCtor(self):
        s = wx.StaticBox(self.frame, label='StaticBox')

    def test_statboxDefaultCtor(self):
        s = wx.StaticBox()
        s.Create(self.frame, label='StaticBox')

    def test_statboxGetBordersForSizer(self):
        s = wx.StaticBox(self.frame, label='StaticBox')
        topBorder, otherBorder = s.GetBordersForSizer()
        assert isinstance(topBorder, int)
        assert isinstance(otherBorder, int)
        assert topBorder >= 0
        assert otherBorder >= 0

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
