import unittest
from unittests import wtc
import wx

import wx.lib.agw.pybusyinfo as PBI

#---------------------------------------------------------------------------

class lib_agw_pybusyinfo_Tests(wtc.WidgetTestCase):

    def test_lib_agw_pybusyinfoCtor(self):
        message = 'Please wait...'
        busy = PBI.PyBusyInfo(message, parent=self.frame, title='Really Busy')

        wx.Yield()
        self.assertTrue(busy._infoFrame.IsShown())

        for indx in range(5):
            wx.MilliSleep(10)

        del busy


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
