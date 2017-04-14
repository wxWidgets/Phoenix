import unittest
from unittests import wtc
import wx
import random

import wx.lib.agw.peakmeter as PM

#---------------------------------------------------------------------------

class lib_agw_peakmeter_Tests(wtc.WidgetTestCase):

    def get_data(self):
        arrayData = []
        for i in range(15):
            nRandom = random.randint(0, 100)
            arrayData.append(nRandom)

        return arrayData

    def test_lib_agw_peakmeterCtor(self):
        peak = PM.PeakMeterCtrl(self.frame, -1, style=wx.SIMPLE_BORDER, agwStyle=PM.PM_VERTICAL)
        peak.SetMeterBands(10, 15)
        peak.SetRangeValue(1, 10, 20)

        peak.SetData(self.get_data(), 0, 15)


    def test_lib_agw_peakmeterMethods(self):
        peak = PM.PeakMeterCtrl(self.frame, -1, style=wx.SIMPLE_BORDER, agwStyle=PM.PM_HORIZONTAL)
        peak.SetMeterBands(10, 15)
        peak.SetRangeValue(1, 10, 20)

        peak.SetData(self.get_data(), 0, 15)

        self.assertTrue(peak.GetFalloffEffect())
        self.assertTrue(not peak.IsGridVisible())
        self.assertTrue(peak.GetAGWWindowStyleFlag() & PM.PM_HORIZONTAL == 0)

        self.assertEqual(peak.GetRangeValue(), (1, 10, 20))

    def test_lib_agw_peakmeterConstantsExist(self):
        PM.BAND_DEFAULT
        PM.BAND_PERCENT
        PM.DEFAULT_SPEED
        PM.FALL_INCREASEBY
        PM.GRID_INCREASEBY
        PM.LEDS_DEFAULT
        PM.PM_HORIZONTAL
        PM.PM_VERTICAL

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
