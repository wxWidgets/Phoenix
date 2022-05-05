import unittest
from unittests import wtc
import wx
import random

import wx.lib.agw.speedmeter as SM

from math import pi, sqrt


#---------------------------------------------------------------------------

class lib_agw_speedmeter_Tests(wtc.WidgetTestCase):

    def test_lib_agw_speedmeterCtor(self):
        spW = SM.SpeedMeter(self.frame,
                            agwStyle=SM.SM_DRAW_HAND |
                            SM.SM_DRAW_SECTORS |
                            SM.SM_DRAW_MIDDLE_TEXT |
                            SM.SM_DRAW_SECONDARY_TICKS
                            )


    def test_lib_agw_speedmeterMethods(self):
        panel = wx.Panel(self.frame)
        spW = SM.SpeedMeter(panel,
                            agwStyle=SM.SM_DRAW_HAND |
                            SM.SM_DRAW_SECTORS |
                            SM.SM_DRAW_MIDDLE_TEXT |
                            SM.SM_DRAW_SECONDARY_TICKS
                            )

        # Set The Region Of Existence Of SpeedMeter (Always In Radians!!!!)
        spW.SetAngleRange(-pi/6, 7*pi/6)
        self.assertEqual(spW.GetAngleRange(), [-pi/6, 7*pi/6])

        # Create The Intervals That Will Divide Our SpeedMeter In Sectors
        intervals = range(0, 201, 20)
        spW.SetIntervals(intervals)
        self.assertEqual(spW.GetIntervals(), intervals)

        # Assign The Same Colours To All Sectors (We Simulate A Car Control For Speed)
        # Usually This Is Black
        colours = [wx.BLACK]*10
        spW.SetIntervalColours(colours)
        self.assertEqual(spW.GetIntervalColours(), colours)

        # Assign The Ticks: Here They Are Simply The String Equivalent Of The Intervals
        ticks = [str(interval) for interval in intervals]
        spW.SetTicks(ticks)
        self.assertEqual(spW.GetTicks(), ticks)

        # Set The Ticks/Tick Markers Colour
        spW.SetTicksColour(wx.WHITE)
        self.assertEqual(spW.GetTicksColour(), wx.WHITE)

        # We Want To Draw 5 Secondary Tickis Between The Principal Ticks
        spW.SetNumberOfSecondaryTicks(5)
        self.assertEqual(spW.GetNumberOfSecondaryTicks(), 5)

        # Set The Font For The Ticks Markers
        tf = wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        spW.SetTicksFont(tf)
        self.assertEqual(spW.GetTicksFont(), ([tf], 7))

        # Set The Text In The Center Of SpeedMeter
        spW.SetMiddleText("Km/h")
        self.assertEqual(spW.GetMiddleText(), "Km/h")

        # Assign The Colour To The Center Text
        spW.SetMiddleTextColour(wx.WHITE)
        self.assertEqual(spW.GetMiddleTextColour(), wx.WHITE)

        # Assign A Font To The Center Text
        mf = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        spW.SetMiddleTextFont(mf)
        self.assertEqual(spW.GetMiddleTextFont(), (mf, 8))

        # Set The Colour For The Hand Indicator
        hc = wx.Colour(255, 50, 0)
        spW.SetHandColour(hc)
        self.assertEqual(spW.GetHandColour(), hc)

        # Do Not Draw The External (Container) Arc. Drawing The External Arc May
        # Sometimes Create Uglier Controls. Try To Comment This Line And See It
        # For Yourself!
        spW.DrawExternalArc(False)

        # Set The Current Value For The SpeedMeter
        spW.SetSpeedValue(44)
        self.assertEqual(spW.GetSpeedValue(), 44)

    def test_lib_agw_speedmeterSizerLayout(self):
        panel = wx.Panel(self.frame, -1)
        fgSizer = wx.FlexGridSizer(rows=2, cols=3, vgap=2, hgap=5)
        panel.SetSizer(fgSizer)

        panel1 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        fgSizer.Add(panel1, 1, wx.EXPAND)

        boxSizer = wx.BoxSizer()
        panel1.SetSizer(boxSizer)
        spW = SM.SpeedMeter(panel1,
                            agwStyle=SM.SM_DRAW_HAND |
                            SM.SM_DRAW_SECTORS |
                            SM.SM_DRAW_MIDDLE_TEXT |
                            SM.SM_DRAW_SECONDARY_TICKS
                            )
        boxSizer.Add(spW, 1, wx.EXPAND)
        boxSizer.Layout()


    def test_lib_agw_peakmeterConstantsExist(self):
        SM.SM_BUFFERED_DC
        SM.SM_DRAW_FANCY_TICKS
        SM.SM_DRAW_GRADIENT
        SM.SM_DRAW_HAND
        SM.SM_DRAW_MIDDLE_ICON
        SM.SM_DRAW_MIDDLE_TEXT
        SM.SM_DRAW_PARTIAL_FILLER
        SM.SM_DRAW_PARTIAL_SECTORS
        SM.SM_DRAW_SECONDARY_TICKS
        SM.SM_DRAW_SECTORS
        SM.SM_DRAW_SHADOW
        SM.SM_MOUSE_TRACK
        SM.SM_NORMAL_DC
        SM.SM_ROTATE_TEXT


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
