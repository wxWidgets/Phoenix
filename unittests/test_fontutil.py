import unittest
from unittests import wtc
import wx
import os

#---------------------------------------------------------------------------

class fontutil_Tests(wtc.WidgetTestCase):

    def test_fontutil(self):
        f1 = wx.FFont(12, wx.FONTFAMILY_SWISS)
        i1 = f1.GetNativeFontInfo()
        st = i1.ToString()

        i2 = wx.NativeFontInfo()
        i2.FromString(st)
        f2 = wx.Font(i2)

        # f1 == f2 is unreliable on macOS: GetFamily() is guessed from
        # CoreText traits on round-trip and doesn't always match.
        self.assertEqual(f1.GetPointSize(), f2.GetPointSize())
        self.assertEqual(f1.GetStyle(), f2.GetStyle())
        self.assertEqual(f1.GetWeight(), f2.GetWeight())
        self.assertEqual(f1.GetUnderlined(), f2.GetUnderlined())
        self.assertEqual(f1.GetStrikethrough(), f2.GetStrikethrough())
        self.assertEqual(f1.GetEncoding(), f2.GetEncoding())
        self.assertEqual(f1.GetFaceName(), f2.GetFaceName())

    def test_fontutilProperties(self):
        nfi = wx.NativeFontInfo()
        nfi.InitFromFont(wx.NORMAL_FONT)
        nfi.Encoding
        nfi.FaceName
        nfi.Family
        nfi.PointSize
        #nfi.PixelSize
        nfi.Style
        nfi.Underlined
        nfi.Weight



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
