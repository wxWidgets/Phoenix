#!/usr/bin/env python

import wx
import wx.lib.buttons
from math import pi, sqrt

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

try:
    from agw import speedmeter as SM
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.speedmeter as SM


#----------------------------------------------------------------------
# Beginning Of SPEEDMETER Demo wxPython Code
#----------------------------------------------------------------------

def _getAndScaleIcon(filename, width, height):
    img = wx.Image(filename, wx.BITMAP_TYPE_ICO)
    img.Rescale(width, height)
    icon = wx.Icon(img.ConvertToBitmap())
    return icon


class SpeedMeterDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL|wx.NO_FULL_REPAINT_ON_RESIZE)

        panel = wx.Panel(self, -1)
        sizer = wx.FlexGridSizer(rows=2, cols=3, vgap=2, hgap=5)

        # 6 Panels To Hold The SpeedMeters ;-)

        panel1 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel2 = wx.Panel(panel, -1, style=wx.RAISED_BORDER)
        panel3 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel4 = wx.Panel(panel, -1, style=wx.RAISED_BORDER)
        panel5 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel6 = wx.Panel(panel, -1, style=wx.RAISED_BORDER)

        # First SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_SECTORS: Full Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_MIDDLE_TEXT: We Draw Some Text In The Center Of SpeedMeter
        # SM_DRAW_SECONDARY_TICKS: We Draw Secondary (Intermediate) Ticks Between
        #                          The Main Ticks (Intervals)

        self.SpeedWindow1 = SM.SpeedMeter(panel1,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_MIDDLE_TEXT |
                                          SM.SM_DRAW_SECONDARY_TICKS
                                          )

        # Set The Region Of Existence Of SpeedMeter (Always In Radians!!!!)
        self.SpeedWindow1.SetAngleRange(-pi/6, 7*pi/6)

        # Create The Intervals That Will Divide Our SpeedMeter In Sectors
        intervals = range(0, 201, 20)
        self.SpeedWindow1.SetIntervals(intervals)

        # Assign The Same Colours To All Sectors (We Simulate A Car Control For Speed)
        # Usually This Is Black
        colours = [wx.BLACK]*10
        self.SpeedWindow1.SetIntervalColours(colours)

        # Assign The Ticks: Here They Are Simply The String Equivalent Of The Intervals
        ticks = [str(interval) for interval in intervals]
        self.SpeedWindow1.SetTicks(ticks)
        # Set The Ticks/Tick Markers Colour
        self.SpeedWindow1.SetTicksColour(wx.WHITE)
        # We Want To Draw 5 Secondary Ticks Between The Principal Ticks
        self.SpeedWindow1.SetNumberOfSecondaryTicks(5)

        # Set The Font For The Ticks Markers
        self.SpeedWindow1.SetTicksFont(wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # Set The Text In The Center Of SpeedMeter
        self.SpeedWindow1.SetMiddleText("Km/h")
        # Assign The Colour To The Center Text
        self.SpeedWindow1.SetMiddleTextColour(wx.WHITE)
        # Assign A Font To The Center Text
        self.SpeedWindow1.SetMiddleTextFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        # Set The Colour For The Hand Indicator
        self.SpeedWindow1.SetHandColour(wx.Colour(255, 50, 0))

        # Do Not Draw The External (Container) Arc. Drawing The External Arc May
        # Sometimes Create Uglier Controls. Try To Comment This Line And See It
        # For Yourself!
        self.SpeedWindow1.DrawExternalArc(False)

        # Set The Current Value For The SpeedMeter
        self.SpeedWindow1.SetSpeedValue(44)


        # Second SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_SECTORS: Full Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_MIDDLE_TEXT: We Draw Some Text In The Center Of SpeedMeter
        # SM_DRAW_SECONDARY_TICKS: We Draw Secondary (Intermediate) Ticks Between
        #                          The Main Ticks (Intervals)
        # SM_DRAW_PARTIAL_FILLER: The Region Passed By The Hand Indicator Is Highlighted
        #                         With A Different Filling Colour
        # SM_DRAW_SHADOW: A Shadow For The Hand Indicator Is Drawn

        self.SpeedWindow2 = SM.SpeedMeter(panel2,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_MIDDLE_TEXT |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_DRAW_PARTIAL_FILLER |
                                          SM.SM_DRAW_SHADOW
                                          )

        # We Want To Simulate A Clock. Somewhat Tricky, But Did The Job
        self.SpeedWindow2.SetAngleRange(pi/2, 5*pi/2)

        intervals = range(0, 13)
        self.SpeedWindow2.SetIntervals(intervals)

        colours = [wx.SystemSettings.GetColour(0)]*12
        self.SpeedWindow2.SetIntervalColours(colours)

        ticks = [str(interval) for interval in intervals]
        ticks[-1] = ""
        ticks[0] = "12"
        self.SpeedWindow2.SetTicks(ticks)
        self.SpeedWindow2.SetTicksColour(wx.BLUE)
        self.SpeedWindow2.SetTicksFont(wx.Font(11, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True))
        self.SpeedWindow2.SetNumberOfSecondaryTicks(4)

        # Set The Colour For The External Arc
        self.SpeedWindow2.SetArcColour(wx.BLUE)

        self.SpeedWindow2.SetHandColour(wx.BLACK)

        self.SpeedWindow2.SetMiddleText("0 s")
        self.SpeedWindow2.SetMiddleTextColour(wx.RED)

        # We Set The Background Colour Of The SpeedMeter OutSide The Control
        self.SpeedWindow2.SetSpeedBackground(wx.WHITE)

        # Set The Colour For The Shadow
        self.SpeedWindow2.SetShadowColour(wx.Colour(128, 128, 128))

        self.SpeedWindow2.SetSpeedValue(0.0)


        # Third SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_PARTIAL_SECTORS: Partial Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_MIDDLE_ICON: We Draw An Icon In The Center Of SpeedMeter

        self.SpeedWindow3 = SM.SpeedMeter(panel3,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_PARTIAL_SECTORS |
                                          SM.SM_DRAW_MIDDLE_ICON
                                          )

        # We Want To Simulate A Car Gas-Control
        self.SpeedWindow3.SetAngleRange(-pi/3, pi/3)

        intervals = range(0, 5)
        self.SpeedWindow3.SetIntervals(intervals)

        colours = [wx.BLACK]*3
        colours.append(wx.RED)
        self.SpeedWindow3.SetIntervalColours(colours)

        ticks = ["F", "", "", "", "E"]
        self.SpeedWindow3.SetTicks(ticks)
        self.SpeedWindow3.SetTicksColour(wx.WHITE)

        self.SpeedWindow3.SetHandColour(wx.YELLOW)

        # Define The Icon We Want
        icon = _getAndScaleIcon(
            os.path.normpath(os.path.join(bitmapDir, "smfuel.ico")), 24, 24)

        # Draw The Icon In The Center Of SpeedMeter
        self.SpeedWindow3.SetMiddleIcon(icon)

        self.SpeedWindow3.SetSpeedBackground(wx.BLACK)

        self.SpeedWindow3.SetArcColour(wx.WHITE)

        self.SpeedWindow3.SetSpeedValue(0.7)


        # Fourth SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_SECTORS: Full Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_SHADOW: A Shadow For The Hand Indicator Is Drawn
        # SM_DRAW_MIDDLE_ICON: We Draw An Icon In The Center Of SpeedMeter
        #
        # NOTE: We Use The Mouse Style mousestyle=SM_MOUSE_TRACK. In This Way, Mouse
        # Events Are Caught (Mainly Left Clicks/Drags) And You Can Change The Speed
        # Value Using The Mouse

        self.SpeedWindow4 = SM.SpeedMeter(panel4,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_SHADOW |
                                          SM.SM_DRAW_MIDDLE_ICON,
                                          mousestyle=SM.SM_MOUSE_TRACK
                                          )

        # We Want To Simulate Some Kind Of Thermometer (In Celsius Degrees!!!)
        self.SpeedWindow4.SetAngleRange(pi, 2*pi)

        intervals = range(35, 44)
        self.SpeedWindow4.SetIntervals(intervals)

        colours = [wx.BLUE]*5
        colours.extend([wx.YELLOW]*2)
        colours.append(wx.RED)
        self.SpeedWindow4.SetIntervalColours(colours)

        ticks = [str(interval) + "C" for interval in intervals]
        self.SpeedWindow4.SetTicks(ticks)
        self.SpeedWindow4.SetTicksColour(wx.BLACK)
        self.SpeedWindow4.SetTicksFont(wx.Font(7, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.SpeedWindow4.SetHandColour(wx.BLUE)

        self.SpeedWindow4.SetSpeedBackground(wx.SystemSettings.GetColour(0))

        self.SpeedWindow4.DrawExternalArc(False)

        self.SpeedWindow4.SetHandColour(wx.GREEN)
        self.SpeedWindow4.SetShadowColour(wx.Colour(50, 50, 50))

        # We Want A Simple Arrow As Indicator, Not The More Scenic Hand ;-)
        self.SpeedWindow4.SetHandStyle("Arrow")

        # Define The Icon We Want
        icon = _getAndScaleIcon(
            os.path.normpath(os.path.join(bitmapDir, "smtemp.ico")), 16, 16)

        # Draw The Icon In The Center Of SpeedMeter
        self.SpeedWindow4.SetMiddleIcon(icon)

        # Quite An High Fever!!!
        self.SpeedWindow4.SetSpeedValue(41.4)


        # Fifth SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_PARTIAL_SECTORS: Partial Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_SECONDARY_TICKS: We Draw Secondary (Intermediate) Ticks Between
        #                          The Main Ticks (Intervals)
        # SM_DRAW_MIDDLE_TEXT: We Draw Some Text In The Center Of SpeedMeter
        # SM_ROTATE_TEXT: The Ticks Texts Are Rotated Accordingly To Their Angle

        self.SpeedWindow5 = SM.SpeedMeter(panel5,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_PARTIAL_SECTORS |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_DRAW_MIDDLE_TEXT |
                                          SM.SM_ROTATE_TEXT
                                          )

        # We Want To Simulate The Round Per Meter Control In A Car
        self.SpeedWindow5.SetAngleRange(-pi/6, 7*pi/6)

        intervals = range(0, 9)
        self.SpeedWindow5.SetIntervals(intervals)

        colours = [wx.BLACK]*6
        colours.append(wx.YELLOW)
        colours.append(wx.RED)
        self.SpeedWindow5.SetIntervalColours(colours)

        ticks = [str(interval) for interval in intervals]
        self.SpeedWindow5.SetTicks(ticks)
        self.SpeedWindow5.SetTicksColour(wx.WHITE)
        self.SpeedWindow5.SetTicksFont(wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        self.SpeedWindow5.SetHandColour(wx.Colour(255, 50, 0))

        self.SpeedWindow5.SetSpeedBackground(wx.SystemSettings.GetColour(0))

        self.SpeedWindow5.DrawExternalArc(False)

        self.SpeedWindow5.SetShadowColour(wx.Colour(50, 50, 50))

        self.SpeedWindow5.SetMiddleText("rpm")
        self.SpeedWindow5.SetMiddleTextColour(wx.WHITE)
        self.SpeedWindow5.SetMiddleTextFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.SpeedWindow5.SetSpeedBackground(wx.Colour(160, 160, 160))

        self.SpeedWindow5.SetSpeedValue(5.6)


        # Sixth SpeedMeter: That Is Complete And Complex Example.
        #                   We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_PARTIAL_FILLER: The Region Passed By The Hand Indicator Is Highlighted
        #                         With A Different Filling Colour
        # SM_DRAW_MIDDLE_ICON: We Draw An Icon In The Center Of SpeedMeter
        # SM_DRAW_GRADIENT: A Circular Colour Gradient Is Drawn Inside The SpeedMeter, To
        #                   Give Some Kind Of Scenic Effect
        # SM_DRAW_FANCY_TICKS: We Use wx.lib.
        # SM_DRAW_SHADOW: A Shadow For The Hand Indicator Is Drawn

        self.SpeedWindow6 = SM.SpeedMeter(panel6,
                                          agwStyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_PARTIAL_FILLER  |
                                          SM.SM_DRAW_MIDDLE_ICON |
                                          SM.SM_DRAW_GRADIENT |
                                          SM.SM_DRAW_FANCY_TICKS |
                                          SM.SM_DRAW_SHADOW
                                          )

        self.SpeedWindow6.SetAngleRange(0, 4*pi/3)

        intervals = [0, pi/6, sqrt(pi), 2./3.*pi, pi**2/4, pi, 7./6.*pi, 4*pi/3]
        self.SpeedWindow6.SetIntervals(intervals)

        # If You Use The Style SM_DRAW_FANCY_TICKS, Refer To wx.lib.fancytext To Create
        # Correct XML Strings To Put Here
        ticks = ["0", "<pi/>/6", "sq(<pi/>)", "2<pi/>/3", "<pi/><sup>2</sup>/4", "<pi/>", "7<pi/>/6", "4<pi/>/3"]
        self.SpeedWindow6.SetTicks(ticks)
        self.SpeedWindow6.SetTicksColour(wx.Colour(0, 90, 0))
        self.SpeedWindow6.SetTicksFont(wx.Font(6, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.SpeedWindow6.SetHandColour(wx.Colour(60, 60, 60))

        self.SpeedWindow6.DrawExternalArc(False)

        self.SpeedWindow6.SetFillerColour(wx.Colour(145, 220, 200))

        self.SpeedWindow6.SetShadowColour(wx.BLACK)

        self.SpeedWindow6.SetDirection("Reverse")

        self.SpeedWindow6.SetSpeedBackground(wx.SystemSettings.GetColour(0))

        # Set The First Gradient Colour, Which Is The Colour Near The External Arc
        self.SpeedWindow6.SetFirstGradientColour(wx.RED)
        # Set The Second Gradient Colour, Which Is The Colour Near The Center Of The SpeedMeter
        self.SpeedWindow6.SetSecondGradientColour(wx.WHITE)

        icon = _getAndScaleIcon(
            os.path.normpath(os.path.join(bitmapDir, "smpi.ico")), 12, 12)
        self.SpeedWindow6.SetMiddleIcon(icon)

        self.SpeedWindow6.SetSpeedValue(pi/3)


        # End Of SpeedMeter Controls Construction. Add Some Functionality

        self.isalive = 0

        # These Are Cosmetics For The First SpeedMeter Control
        bsizer1 = wx.BoxSizer(wx.VERTICAL)

        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        slider = wx.Slider(panel1, -1, 44, 0, 200,
                           style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS )
        slider.SetTickFreq(5)
        slider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
        slider.SetToolTip(wx.ToolTip("Drag The Slider To Change The Speed!"))

        hsizer1.Add(slider, 1, wx.EXPAND)

        bsizer1.Add(self.SpeedWindow1, 1, wx.EXPAND)
        bsizer1.Add(hsizer1, 0, wx.EXPAND)
        panel1.SetSizer(bsizer1)


        # These Are Cosmetics For The Second SpeedMeter Control

        # Create The Timer For The Clock
        self.timer = wx.PyTimer(self.ClockTimer)
        self.currvalue = 0

        bsizer2 = wx.BoxSizer(wx.VERTICAL)

        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        stattext2 = wx.StaticText(panel2, -1, "A Simple Clock", style=wx.ALIGN_CENTER)

        button2 = wx.Button(panel2, -1, "Stop")
        self.stopped = 0
        button2.Bind(wx.EVT_BUTTON, self.OnStopClock)
        button2.SetToolTip(wx.ToolTip("Click To Stop/Resume The Clock"))

        hsizer2.Add(button2, 0, wx.LEFT, 5)
        hsizer2.Add(stattext2, 1, wx.EXPAND)

        bsizer2.Add(self.SpeedWindow2, 1, wx.EXPAND)
        bsizer2.Add(hsizer2, 0, wx.EXPAND)
        panel2.SetSizer(bsizer2)


        # These Are Cosmetics For The Third SpeedMeter Control
        self.timer3 = wx.PyTimer(self.OilTimer)

        bsizer3 = wx.BoxSizer(wx.VERTICAL)

        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sc = wx.SpinCtrl(panel3, -1)
        sc.SetRange(1, 250)
        sc.SetValue(50)

        self.spinctrl = sc

        strs = "Change The Speed And See How Much Fuel You Loose"
        self.spinctrl.SetToolTip(wx.ToolTip(strs))

        button3 = wx.Button(panel3, -1, "Refill!", size=(60,20))
        button3.SetToolTip(wx.ToolTip("Click Here To Refill!"))
        button3.Bind(wx.EVT_BUTTON, self.OnRefill)

        hsizer3.Add(self.spinctrl, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer3.Add(button3, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer3.Add((1,0), 2, wx.EXPAND)

        bsizer3.Add(self.SpeedWindow3, 1, wx.EXPAND)
        bsizer3.Add(hsizer3, 0, wx.EXPAND)
        panel3.SetSizer(bsizer3)


        # These Are Cosmetics For The Fourth SpeedMeter Control
        bsizer4 = wx.BoxSizer(wx.VERTICAL)

        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        stattext4 = wx.StaticText(panel4, -1, "Use The Mouse ;-)")

        hsizer4.Add(stattext4, 1, wx.EXPAND | wx.LEFT, 5)

        bsizer4.Add(self.SpeedWindow4, 1, wx.EXPAND)
        bsizer4.Add(hsizer4, 0, wx.EXPAND)
        panel4.SetSizer(bsizer4)


        # These Are Cosmetics For The Fifth SpeedMeter Control
        bsizer5 = wx.BoxSizer(wx.VERTICAL)

        hsizer5 = wx.BoxSizer(wx.HORIZONTAL)

        button5 = wx.Button(panel5, -1, "Simulate")
        button5.SetToolTip(wx.ToolTip("Start A Car Acceleration Simulation"))
        button5.Bind(wx.EVT_BUTTON, self.OnSimulate)

        hsizer5.Add(button5, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer5.Add((1,0), 1, wx.EXPAND)

        bsizer5.Add(self.SpeedWindow5, 1, wx.EXPAND)
        bsizer5.Add(hsizer5, 0, wx.EXPAND)
        panel5.SetSizer(bsizer5)


        # These Are Cosmetics For The Sixth SpeedMeter Control
        bsizer6 = wx.BoxSizer(wx.VERTICAL)
        hsizer6 = wx.BoxSizer(wx.HORIZONTAL)

        txtctrl6 = wx.TextCtrl(panel6, -1, "60", size=(60, 20))
        txtctrl6.SetToolTip(wx.ToolTip("Insert An Angle In DEGREES"))

        self.txtctrl = txtctrl6

        button6 = wx.Button(panel6, -1, "Go!")
        button6.SetToolTip(wx.ToolTip("Calculate The Equivalent In Radians And Display It"))

        hsizer6.Add(txtctrl6, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer6.Add(button6, 0, wx.EXPAND | wx.LEFT, 5)
        hsizer6.Add((1,0), 1, wx.EXPAND)

        button6.Bind(wx.EVT_BUTTON, self.OnCalculate)
        bsizer6.Add(self.SpeedWindow6, 1, wx.EXPAND)
        bsizer6.Add(hsizer6, 0, wx.EXPAND)
        panel6.SetSizer(bsizer6)

        bsizer1.Layout()
        bsizer2.Layout()
        bsizer3.Layout()
        bsizer4.Layout()
        bsizer5.Layout()
        bsizer6.Layout()

        sizer.Add(panel1, 1, wx.EXPAND)
        sizer.Add(panel2, 1, wx.EXPAND)
        sizer.Add(panel3, 1, wx.EXPAND)

        sizer.Add(panel4, 1, wx.EXPAND)
        sizer.Add(panel5, 1, wx.EXPAND)
        sizer.Add(panel6, 1, wx.EXPAND)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)

        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        mainSizer.Layout()

        self.SendSizeEvent()

        self.timer.Start(1000)
        self.timer3.Start(500)


    def ShutdownDemo(self):
        self.timer.Stop()
        self.timer3.Stop()
        del self.timer
        del self.timer3


    def OnSliderScroll(self, event):

        slider = event.GetEventObject()
        self.SpeedWindow1.SetSpeedValue(slider.GetValue())

        event.Skip()


    def ClockTimer(self):
        if self.currvalue >= 59:
            self.currvalue = 0
        else:
            self.currvalue = self.currvalue + 1

        self.SpeedWindow2.SetMiddleText(str(self.currvalue) + " s")
        self.SpeedWindow2.SetSpeedValue(self.currvalue/5.0)


    def OnStopClock(self, event):

        btn = event.GetEventObject()

        if self.stopped == 0:
            self.stopped = 1
            self.timer.Stop()
            btn.SetLabel("Resume")
        else:
            self.stopped = 0
            self.timer.Start()
            btn.SetLabel("Stop")


    def OilTimer(self):

        val = self.spinctrl.GetValue()

        if val > 250:
            return

        current = self.SpeedWindow3.GetSpeedValue()
        new = current + val*0.0005

        if new > 4.0:
            return

        self.SpeedWindow3.SetSpeedValue(new)


    def OnRefill(self, event):

        self.SpeedWindow3.SetSpeedValue(0)


    def OnSimulate(self, event):

        for ii in range(50):
            self.SpeedWindow5.SetSpeedValue(ii/10.0)
            wx.MilliSleep(10)

        current = self.SpeedWindow5.GetSpeedValue()
        for ii in range(40):
            current = current - 1.0/10.0
            self.SpeedWindow5.SetSpeedValue(current)
            wx.MilliSleep(40)

        wx.MilliSleep(50)
        current = self.SpeedWindow5.GetSpeedValue()

        for ii in range(59):
            current = current + 1.0/10.0
            self.SpeedWindow5.SetSpeedValue(current)
            wx.MilliSleep(10)

        event.Skip()


    def OnCalculate(self, event):

        try:
            myval = self.txtctrl.GetValue()
            val = float(myval)
        except:
            msg = "ERROR: Value Entered In The TextCtrl:\n\n" + myval + "\n\n"
            msg = msg + "Is Not A Valid Integer/Float Number."
            dlg = wx.MessageDialog(self, msg, "SpeedMeter Demo Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Verdana"))
            dlg.ShowModal()
            dlg.Destroy()
            return

        newval = val*pi/180.0
        anglerange = self.SpeedWindow6.GetAngleRange()
        start = anglerange[0]
        end = anglerange[1]

        error = 0

        if newval < start:
            msg = "ERROR: Value Entered In The TextCtrl:\n\n" + myval + "\n\n"
            msg = msg + "Is Smaller Than Minimum Value."
            error = 1
        elif newval > end:
            msg = "ERROR: Value Entered In The TextCtrl:\n\n" + myval + "\n\n"
            msg = msg + "Is Greater Than Maximum Value."
            error = 1

        if error:
            dlg = wx.MessageDialog(self, msg, "SpeedMeter Demo Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Verdana"))
            dlg.ShowModal()
            dlg.Destroy()
            return

        self.SpeedWindow6.SetSpeedValue(newval)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = SpeedMeterDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = SM.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

