#!/usr/bin/env python

import wx
import random

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import peakmeter as PM
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.peakmeter as PM


class PeakMeterCtrlDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)
        self.log = log

        self.mainPanel = wx.Panel(self)

        # Initialize Peak Meter control 1
        self.vertPeak = PM.PeakMeterCtrl(self.mainPanel, -1, style=wx.SIMPLE_BORDER, agwStyle=PM.PM_VERTICAL)
        # Initialize Peak Meter control 2
        self.horzPeak = PM.PeakMeterCtrl(self.mainPanel, -1, style=wx.SUNKEN_BORDER, agwStyle=PM.PM_HORIZONTAL)

        self.startButton = wx.Button(self.mainPanel, -1, "Start")
        self.stopButton = wx.Button(self.mainPanel, -1, "Stop")
        self.staticLine = wx.StaticLine(self.mainPanel)

        self.gridCheck = wx.CheckBox(self.mainPanel, -1, "Show Grid")
        self.falloffCheck = wx.CheckBox(self.mainPanel, -1, "Show Falloff Effect")

        colour = self.mainPanel.GetBackgroundColour()
        self.backColour = wx.ColourPickerCtrl(self.mainPanel, colour=colour)
        self.lowColour = wx.ColourPickerCtrl(self.mainPanel, colour=wx.GREEN)
        self.mediumColour = wx.ColourPickerCtrl(self.mainPanel, colour=wx.YELLOW)
        self.highColour = wx.ColourPickerCtrl(self.mainPanel, colour=wx.RED)

        self.timer = wx.Timer(self)

        self.SetProperties()
        self.DoLayout()
        self.BindEvents()


    def SetProperties(self):

        self.vertPeak.SetMeterBands(10, 15)
        self.horzPeak.SetMeterBands(10, 15)
        self.falloffCheck.SetValue(1)


    def DoLayout(self):

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        horzSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        checkSizer = wx.BoxSizer(wx.VERTICAL)
        colourSizer = wx.FlexGridSizer(2, 4, 1, 10)

        horzSizer.Add(self.vertPeak, 0, wx.EXPAND|wx.ALL, 15)
        horzSizer.Add(self.horzPeak, 0, wx.EXPAND|wx.ALL, 15)

        rightSizer.Add(self.startButton, 0, wx.ALL, 5)
        rightSizer.Add(self.stopButton, 0, wx.LEFT|wx.RIGHT, 5)
        horzSizer.Add(rightSizer, 0, wx.ALIGN_TOP|wx.ALL, 5)
        horzSizer.Add((15, 0))

        mainSizer.Add(horzSizer, 0, wx.EXPAND)
        mainSizer.Add(self.staticLine, 0, wx.EXPAND|wx.ALL, 5)

        checkSizer.Add(self.gridCheck, 0, wx.EXPAND|wx.ALL, 5)
        checkSizer.Add(self.falloffCheck, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)

        labelBack = wx.StaticText(self.mainPanel, -1, "Background")
        labelLow = wx.StaticText(self.mainPanel, -1, "Low Freq")
        labelMed = wx.StaticText(self.mainPanel, -1, "Med Freq")
        labelHigh = wx.StaticText(self.mainPanel, -1, "High Freq")

        colourSizer.Add(labelBack)
        colourSizer.Add(labelLow)
        colourSizer.Add(labelMed)
        colourSizer.Add(labelHigh)

        colourSizer.Add(self.backColour, 0, wx.EXPAND)
        colourSizer.Add(self.lowColour, 0, wx.EXPAND)
        colourSizer.Add(self.mediumColour, 0, wx.EXPAND)
        colourSizer.Add(self.highColour, 0, wx.EXPAND)

        bottomSizer.Add(checkSizer, 0, wx.EXPAND|wx.ALL, 5)
        bottomSizer.Add((0, 0), 1, wx.EXPAND)
        bottomSizer.Add(colourSizer, 0, wx.EXPAND|wx.ALL, 5)
        bottomSizer.Add((0, 5))
        mainSizer.Add(bottomSizer, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT, 5)

        self.mainPanel.SetSizer(mainSizer)
        mainSizer.Layout()
        frameSizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        frameSizer.Layout()


    def BindEvents(self):

        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_CHECKBOX, self.OnGrid, self.gridCheck)
        self.Bind(wx.EVT_CHECKBOX, self.OnFalloff, self.falloffCheck)
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.startButton)
        self.Bind(wx.EVT_BUTTON, self.OnStop, self.stopButton)

        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnPickColour)


    def OnTimer(self, event):

        # generate 15 random number and set them as data for the meter
        nElements = 15
        arrayData = []

        for i in range(nElements):
            nRandom = random.randint(0, 100)
            arrayData.append(nRandom)

        self.vertPeak.SetData(arrayData, 0, nElements)
        self.horzPeak.SetData(arrayData, 0, nElements)


    def OnGrid(self, event):

        self.vertPeak.ShowGrid(event.IsChecked())


    def OnFalloff(self, event):

        self.vertPeak.SetFalloffEffect(event.IsChecked())


    def OnStart(self, event):

        self.timer.Start(1000/2)        # 2 fps

        self.vertPeak.Start(1000/18)        # 18 fps
        self.horzPeak.Start(1000/20)        # 20 fps


    def OnStop(self, event):

        self.timer.Stop()
        self.vertPeak.Stop()
        self.horzPeak.Stop()


    def OnPickColour(self, event):

        obj = event.GetEventObject()
        colour = event.GetColour()
        if obj == self.backColour:
            self.horzPeak.SetBackgroundColour(colour)
        else:
            low = self.lowColour.GetColour()
            med = self.mediumColour.GetColour()
            high = self.highColour.GetColour()
            self.horzPeak.SetBandsColour(low, med, high)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = PeakMeterCtrlDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = PM.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


