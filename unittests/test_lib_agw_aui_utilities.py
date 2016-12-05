import unittest
from unittests import wtc
import wx
import os

import wx.lib.agw.aui.aui_utilities as auiu

#---------------------------------------------------------------------------

class lib_agw_aui_utilities_Tests(wtc.WidgetTestCase):

    def test_lib_agw_aui_utilititiesCtor(self):
        auiu.StepColour(auiu.GetBaseColour(), 60)

        auiu.LightContrastColour(wx.RED)

        auiu.LightColour(wx.RED, 50)

        dc = wx.GCDC()
        auiu.ChopText(dc, "a little test text", 10)

        button_dropdown_bits = b"\xe0\xf1\xfb"
        bmp = auiu.BitmapFromBits(button_dropdown_bits, 5, 3, wx.BLACK)

        auiu.MakeDisabledBitmap(bmp)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
