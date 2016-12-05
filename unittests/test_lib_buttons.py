import unittest
from unittests import wtc
import wx
import os

import wx.lib.buttons as buttons
pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class lib_buttons_Tests(wtc.WidgetTestCase):

    def test_lib_buttons1(self):

        btn = buttons.GenButton(self.frame, label='label')
        btn = buttons.GenButton(self.frame, -1, 'label', (10,10), (100,-1), wx.BU_LEFT)

        bmp = wx.Bitmap(pngFile)
        btn = buttons.GenBitmapButton(self.frame, bitmap=bmp)
        btn = buttons.GenBitmapTextButton(self.frame, label='label', bitmap=bmp)

        btn.SetBitmapFocus(bmp)
        btn.SetBitmapDisabled(bmp)
        btn.SetBitmapSelected(bmp)

        btn = buttons.GenBitmapToggleButton(self.frame, bitmap=bmp)
        btn.SetToggle(True)

        self.assertTrue(btn.GetValue())
        self.assertEqual(btn.GetBitmapLabel(), bmp)


    def test_lib_buttons2(self):

        btn = buttons.ThemedGenButton(self.frame, label='label')
        btn = buttons.ThemedGenButton(self.frame, -1, 'label', (10,10), (100,-1), wx.BU_LEFT)

        bmp = wx.Bitmap(pngFile)
        btn = buttons.ThemedGenBitmapButton(self.frame, bitmap=bmp)
        btn = buttons.ThemedGenBitmapTextButton(self.frame, label='label', bitmap=bmp)

        btn.SetBitmapFocus(bmp)
        btn.SetBitmapDisabled(bmp)
        btn.SetBitmapSelected(bmp)

        btn = buttons.ThemedGenBitmapToggleButton(self.frame, bitmap=bmp)
        btn.SetToggle(True)

        self.assertTrue(btn.GetValue())
        self.assertEqual(btn.GetBitmapLabel(), bmp)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()