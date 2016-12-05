import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class helpext_Tests(wtc.WidgetTestCase):

    def test_helpext1(self):
        hc = wx.adv.ExtHelpController()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
