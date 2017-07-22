import unittest
from unittests import wtc
import wx

import wx.lib.agw.pygauge as PG

#---------------------------------------------------------------------------

class lib_agw_pygauge_Tests(wtc.WidgetTestCase):

    def test_lib_agw_pygaugeCtor(self):
        gauge = PG.PyGauge(self.frame, style=wx.GA_HORIZONTAL)

    def test_lib_agw_pygaugeMethods(self):
        gauge = PG.PyGauge(self.frame, range=120, style=wx.GA_HORIZONTAL)

        gauge.SetValue([20, 80])
        gauge.SetBarColor([wx.RED, wx.BLUE])
        gauge.SetBackgroundColour(wx.WHITE)
        gauge.SetBorderColor(wx.BLACK)
        gauge.SetBorderPadding(2)

        # Some methods tests...
        self.assertEqual(gauge.GetValue(), 20)

        self.assertEqual(gauge.GetBarColour(), wx.Colour('red'))
        self.assertEqual(gauge.GetBackgroundColour(), wx.Colour('white'))
        self.assertEqual(gauge.GetBorderColour(), wx.Colour('black'))

        self.assertEqual(gauge.GetRange(), 120)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
