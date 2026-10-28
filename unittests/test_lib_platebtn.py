import unittest
from unittests import wtc
import wx

import wx.lib.platebtn as PB

#---------------------------------------------------------------------------

class lib_platebtn_Tests(wtc.WidgetTestCase):

    def test_lib_platebtnCtor(self):
        btn = PB.PlateButton(self.frame, label='Button', style=PB.PB_STYLE_GRADIENT)
        self.assertEqual(btn.GetLabel(), 'Button')

    def test_lib_platebtnNoBg(self):
        btn = PB.PlateButton(self.frame, label='Button', style=PB.PB_STYLE_NOBG)
        if 'wxMSW' in wx.PlatformInfo:
            self.assertEqual(btn.GetBackgroundStyle(), wx.BG_STYLE_TRANSPARENT)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
