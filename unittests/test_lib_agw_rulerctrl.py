import unittest
from unittests import wtc
import wx

import wx.lib.agw.rulerctrl as RC

#---------------------------------------------------------------------------

class lib_agw_rulerctrl_Tests(wtc.WidgetTestCase):

    def test_lib_agw_rulerctrlCtor(self):
        ruler = RC.RulerCtrl(self.frame, -1, orient=wx.HORIZONTAL, style=wx.SUNKEN_BORDER)

    def test_lib_agw_rulerctrlMethods(self):
        ruler = RC.RulerCtrl(self.frame, -1, orient=wx.VERTICAL, style=wx.STATIC_BORDER)

        # Some methods tests...
        self.assertEqual(ruler.GetFormat(), RC.RealFormat)

    def test_lib_agw_rulerctrlEvents(self):
        RC.EVT_INDICATOR_CHANGED
        RC.EVT_INDICATOR_CHANGING
        RC.wxEVT_INDICATOR_CHANGED
        RC.wxEVT_INDICATOR_CHANGING


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
