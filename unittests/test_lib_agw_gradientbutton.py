import unittest
from unittests import wtc
import wx
import os

import wx.lib.agw.gradientbutton as GB

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class lib_agw_gradientbutton_Tests(wtc.WidgetTestCase):

    def test_lib_agw_gradientbuttonCtor(self):

        # Initialize GradientButton 1 (with image)
        bitmap = wx.Bitmap(pngFile, wx.BITMAP_TYPE_PNG)
        btn1 = GB.GradientButton(self.frame, -1, bitmap, "GradientButton")
        # Initialize GradientButton 2 (no image)
        btn2 = GB.GradientButton(self.frame, -1, None, "Hello World!")


    def test_lib_agw_gradientbuttonMethods(self):
        # Initialize AquaButton 2 (no image)
        btn2 = GB.GradientButton(self.frame, -1, None, "Hello World!")

        bitmap = wx.Bitmap(pngFile, wx.BITMAP_TYPE_PNG)
        btn2.SetBitmapLabel(bitmap)

        btn2.SetTopStartColour(wx.Colour('grey'))
        btn2.SetBottomStartColour(wx.WHITE)
        btn2.SetPressedBottomColour(wx.BLACK)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
