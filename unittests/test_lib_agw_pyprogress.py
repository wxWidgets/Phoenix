import unittest
from unittests import wtc
import wx

import wx.lib.agw.pyprogress as PP

#---------------------------------------------------------------------------

class lib_agw_pyprogress_Tests(wtc.WidgetTestCase):

    def test_lib_agw_pyprogressCtor(self):
        dlg = PP.PyProgress(self.frame, -1, 'PyProgress Example',
                            'An Informative Message',
                            agwStyle=wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME)
        dlg.Destroy()

    def test_lib_agw_pyprogressMethods(self):
        dlg = PP.PyProgress(self.frame, -1, 'PyProgress Example',
                            'An Informative Message',
                            agwStyle=wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME)

        dlg.SetGaugeProportion(0.2)
        dlg.SetGaugeSteps(50)
        dlg.SetFirstGradientColour(wx.WHITE)
        dlg.SetSecondGradientColour(wx.BLUE)

        # Some methods tests...
        self.assertEqual(dlg.GetGaugeProportion(), 0.2)
        self.assertEqual(dlg.GetGaugeSteps(), 50)
        self.assertEqual(dlg.GetFirstGradientColour(), wx.Colour('white'))
        self.assertEqual(dlg.GetSecondGradientColour(), wx.Colour('blue'))
        self.assertTrue(dlg.GetAGWWindowStyleFlag() & wx.PD_REMAINING_TIME == 0)
        dlg.Destroy()

    def test_lib_agw_pyprogressConstantsExists(self):
        PP.LAYOUT_MARGIN
        PP.PD_APP_MODAL
        PP.PD_AUTO_HIDE
        PP.PD_CAN_ABORT
        PP.PD_ELAPSED_TIME

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

