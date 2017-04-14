import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class defs_Tests(wtc.WidgetTestCase):


    def test_constants1(self):
        # These constants are not plain int's
        self.assertEqual(wx.UINT32_MAX, 2**32-1)
        self.assertEqual(wx.INT64_MIN, (-9223372036854775807)-1)
        self.assertEqual(wx.INT64_MAX, 9223372036854775807)
        self.assertEqual(wx.UINT64_MAX, 0xFFFFFFFFFFFFFFFF)

    def test_constants2(self):
        # These constants needed some special tweaking.  Make sure it
        # was done right.
        self.assertEqual(wx.VSCROLL, -2147483648)
        self.assertEqual(wx.CANCEL_DEFAULT, -2147483648)
        self.assertEqual(wx.WINDOW_STYLE_MASK, -65536)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
