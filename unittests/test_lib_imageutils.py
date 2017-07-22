import unittest
from unittests import wtc
import wx
import wx.lib.imageutils

#---------------------------------------------------------------------------

class lib_imageutils_Tests(wtc.WidgetTestCase):

    def test_lib_imageutils1(self):

        base = wx.Colour(100, 120, 140)
        white = wx.lib.imageutils.stepColour(base, 200)
        black = wx.lib.imageutils.stepColour(base, 0)

        self.assertEqual(white, wx.WHITE)
        self.assertEqual(black, wx.BLACK)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
