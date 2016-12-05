import unittest
from unittests import wtc
import wx
import os

import wx.lib.agw.aquabutton as AB

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class lib_agw_aquabutton_Tests(wtc.WidgetTestCase):

    def test_lib_agw_aquabuttonCtor(self):

        # Initialize AquaButton 1 (with image)
        bitmap = wx.Bitmap(pngFile, wx.BITMAP_TYPE_PNG)
        btn1 = AB.AquaButton(self.frame, -1, bitmap, "AquaButton")
        # Initialize AquaButton 2 (no image)
        btn2 = AB.AquaButton(self.frame, -1, None, "Hello World!")

        btn3 = AB.AquaToggleButton(self.frame, -1, None, 'Toggle')


    def test_lib_agw_aquabuttonMethods(self):
        # Initialize AquaButton 2 (no image)
        btn2 = AB.AquaButton(self.frame, -1, None, "Hello World!")

        bitmap = wx.Bitmap(pngFile, wx.BITMAP_TYPE_PNG)
        btn2.SetBitmapLabel(bitmap)

        btn2.SetPulseOnFocus(True)
        self.assertTrue(btn2.GetPulseOnFocus())

        btn2.SetShadowColour(wx.Colour('grey'))
        btn2.SetRectColour(wx.WHITE)
        btn2.SetHoverColour(wx.BLACK)
        btn2.SetFocusColour(wx.GREEN)

        btn3 = AB.AquaToggleButton(self.frame, -1, None, 'Toggle')
        btn3.SetToggle(True)
        self.assertTrue(btn3.GetToggle())


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
