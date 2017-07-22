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
        self.assertTrue(f1 == f2)

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
