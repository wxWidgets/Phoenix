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


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
