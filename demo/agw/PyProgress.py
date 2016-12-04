#!/usr/bin/env python

import wx
import wx.lib.colourselect as csel

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import pyprogress as PP
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pyprogress as PP


class PyProgressDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)

        self.panel = wx.Panel(self, -1)
        self.log = log

        self.LayoutItems()


    def LayoutItems(self):

        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        rightsizer = wx.FlexGridSizer(7, 2, 5, 5)

        startbutton = wx.Button(self.panel, -1, "Start PyProgress!")

        self.elapsedchoice = wx.CheckBox(self.panel, -1, "Show Elapsed Time")
        self.elapsedchoice.SetValue(1)

        self.cancelchoice = wx.CheckBox(self.panel, -1, "Enable Cancel Button")
        self.cancelchoice.SetValue(1)

        static1 = wx.StaticText(self.panel, -1, "Gauge Proportion (%): ")
        self.slider1 = wx.Slider(self.panel, -1, 20, 1, 99, style=wx.SL_HORIZONTAL|
                                 wx.SL_AUTOTICKS|wx.SL_LABELS)
        self.slider1.SetTickFreq(10)
        self.slider1.SetValue(20)

        static2 = wx.StaticText(self.panel, -1, "Gauge Steps: ")
        self.slider2 = wx.Slider(self.panel, -1, 50, 2, 100, style=wx.SL_HORIZONTAL|
                                 wx.SL_AUTOTICKS|wx.SL_LABELS)
        self.slider2.SetTickFreq(10)
        self.slider2.SetValue(50)

        static3 = wx.StaticText(self.panel, -1, "Gauge Background Colour: ")
        self.csel3 = csel.ColourSelect(self.panel, -1, "Choose...", wx.WHITE)

        static4 = wx.StaticText(self.panel, -1, "Gauge First Gradient Colour: ")
        self.csel4 = csel.ColourSelect(self.panel, -1, "Choose...", wx.WHITE)

        static5 = wx.StaticText(self.panel, -1, "Gauge Second Gradient Colour: ")
        self.csel5 = csel.ColourSelect(self.panel, -1, "Choose...", wx.BLUE)

        rightsizer.Add(self.elapsedchoice, 0, wx.EXPAND|wx.TOP, 10)
        rightsizer.Add((10, 0))
        rightsizer.Add(self.cancelchoice, 0, wx.EXPAND|wx.TOP, 3)
        rightsizer.Add((10, 0))
        rightsizer.Add(static1, 0, wx.ALIGN_CENTER_VERTICAL, 10)
        rightsizer.Add(self.slider1, 0, wx.EXPAND|wx.TOP, 10)
        rightsizer.Add(static2, 0, wx.ALIGN_CENTER_VERTICAL, 10)
        rightsizer.Add(self.slider2, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)
        rightsizer.Add(static3, 0, wx.ALIGN_CENTER_VERTICAL)
        rightsizer.Add(self.csel3, 0)
        rightsizer.Add(static4, 0, wx.ALIGN_CENTER_VERTICAL)
        rightsizer.Add(self.csel4, 0)
        rightsizer.Add(static5, 0, wx.ALIGN_CENTER_VERTICAL)
        rightsizer.Add(self.csel5, 0)

        mainsizer.Add(startbutton, 0, wx.ALL, 20)
        mainsizer.Add(rightsizer, 1, wx.EXPAND|wx.ALL, 10)

        self.panel.SetSizer(mainsizer)
        mainsizer.Layout()

        framesizer = wx.BoxSizer(wx.VERTICAL)
        framesizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(framesizer)
        framesizer.Layout()

        startbutton.Bind(wx.EVT_BUTTON, self.OnStartProgress)


    def OnStartProgress(self, event):

        event.Skip()

        style = wx.PD_APP_MODAL
        if self.elapsedchoice.GetValue():
            style |= wx.PD_ELAPSED_TIME
        if self.cancelchoice.GetValue():
            style |= wx.PD_CAN_ABORT

        dlg = PP.PyProgress(None, -1, "PyProgress Example",
                            "An Informative Message",
                            agwStyle=style)

        proportion = self.slider1.GetValue()
        steps = self.slider2.GetValue()

        backcol = self.csel3.GetColour()
        firstcol = self.csel4.GetColour()
        secondcol = self.csel5.GetColour()

        dlg.SetGaugeProportion(proportion/100.0)
        dlg.SetGaugeSteps(steps)
        dlg.SetGaugeBackground(backcol)
        dlg.SetFirstGradientColour(firstcol)
        dlg.SetSecondGradientColour(secondcol)

        max = 400
        keepGoing = True
        count = 0

        while keepGoing and count < max:
            count += 1
            wx.MilliSleep(30)

            if count >= max / 2:
                keepGoing = dlg.UpdatePulse("Half-time!")
            else:
                keepGoing = dlg.UpdatePulse()

        dlg.Destroy()
        wx.SafeYield()
        wx.GetApp().GetTopWindow().Raise()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = PyProgressDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = PP.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
