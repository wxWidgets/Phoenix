import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class debug_Tests(wtc.WidgetTestCase):

    def test_debug1(self):
        wx.Abort
        wx.Trap
        wx.DisableAsserts

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
