import unittest
from unittests import wtc
import wx

import wx.lib.agw.knobctrl as KC

#---------------------------------------------------------------------------

class lib_agw_knobctrl_Tests(wtc.WidgetTestCase):

    def test_lib_agw_knobctrlCtor(self):
        knobctrl = KC.KnobCtrl(self.frame, size=(100, 100))


    def test_lib_agw_knobctrlMethods(self):
        knobctrl = KC.KnobCtrl(self.frame, size=(100, 100))

        knobctrl.SetTags(range(0, 151, 10))
        knobctrl.SetAngularRange(-45, 225)
        knobctrl.SetValue(45)

        # Some methods tests...
        self.assertEqual(knobctrl.GetAngularRange(), (-45, 225))
        self.assertEqual(knobctrl.GetTags(), range(0, 151, 10))

        # Should not be possible...
        knobctrl.SetValue(-10)
        self.assertEqual(knobctrl.GetValue(), 45)

        self.assertEqual(knobctrl.GetMinValue(), 0)
        self.assertEqual(knobctrl.GetMaxValue(), 150)

    def test_lib_agw_knobctrlConstantsExist(self):
        KC.KC_BUFFERED_DC

    def test_lib_agw_knobctrlEvents(self):
        KC.EVT_KC_ANGLE_CHANGED
        KC.EVT_KC_ANGLE_CHANGING
        KC.wxEVT_KC_ANGLE_CHANGED
        KC.wxEVT_KC_ANGLE_CHANGING


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
