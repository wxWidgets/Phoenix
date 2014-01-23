#!/usr/bin/env python

import wx
import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import pygauge as PG
except ImportError: # if it's not there locally, try the wxPython lib.
    try:
        import wx.lib.agw.pygauge as PG
    except:
        raise Exception("This demo requires wxPython version greater than 2.9.0.0")


class PyGaugeDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)
        self.log = log

        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour(wx.WHITE)

        self.gauge1 = PG.PyGauge(self.mainPanel, -1, size=(100,25),style=wx.GA_HORIZONTAL)
        self.gauge1.SetValue(80)
        self.gauge1.SetBackgroundColour(wx.WHITE)
        self.gauge1.SetBorderColor(wx.BLACK)

        self.gauge2 = PG.PyGauge(self.mainPanel, -1, size=(100,25),style=wx.GA_HORIZONTAL)
        self.gauge2.SetValue([20,80])
        self.gauge2.SetBarColor([wx.Colour(162,255,178),wx.Colour(159,176,255)])
        self.gauge2.SetBackgroundColour(wx.WHITE)
        self.gauge2.SetBorderColor(wx.BLACK)
        self.gauge2.SetBorderPadding(2)
        self.gauge2.Update([30,0],2000)

        self.gauge3 = PG.PyGauge(self.mainPanel, -1, size=(100,25),style=wx.GA_HORIZONTAL)
        self.gauge3.SetValue(50)
        self.gauge3.SetBarColor(wx.GREEN)
        self.gauge3.SetBackgroundColour(wx.WHITE)
        self.gauge3.SetBorderColor(wx.BLACK)

        self.backColour   = wx.ColourPickerCtrl(self.mainPanel, colour=self.gauge3.GetBackgroundColour())
        self.borderColour = wx.ColourPickerCtrl(self.mainPanel, colour=self.gauge3.GetBorderColour())
        self.barColour    = wx.ColourPickerCtrl(self.mainPanel, colour=self.gauge3.GetBarColour())
        self.gaugeValue   = wx.TextCtrl(self.mainPanel, -1, str(self.gauge3.GetValue()), style=wx.TE_PROCESS_ENTER)
        self.gaugeRange   = wx.TextCtrl(self.mainPanel, -1, str(self.gauge3.GetRange()),  style=wx.TE_PROCESS_ENTER)
        self.gaugePadding = wx.TextCtrl(self.mainPanel, -1, str(self.gauge3.GetBorderPadding()),  style=wx.TE_PROCESS_ENTER)

        self.DoLayout()
        self.BindEvents()


    def DoLayout(self):

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        colourSizer = wx.FlexGridSizer(2, 6, 1, 10)

        label1 = wx.StaticText(self.mainPanel, -1, "Welcome to the PyGauge demo for wxPython!")
        mainSizer.Add(label1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)

        mainSizer.Add(self.gauge1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 20)
        mainSizer.Add(self.gauge2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 20)
        mainSizer.Add(self.gauge3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 20)

        labelBack    = wx.StaticText(self.mainPanel, -1, "Background Colour")
        labelHover   = wx.StaticText(self.mainPanel, -1, "Border Colour")
        labelText    = wx.StaticText(self.mainPanel, -1, "Bar Colour")
        labelValue   = wx.StaticText(self.mainPanel, -1, "Gauge Value ")
        labelRange   = wx.StaticText(self.mainPanel, -1, "Gauge Range")
        labelPadding = wx.StaticText(self.mainPanel, -1, "Border Padding")

        colourSizer.Add(labelBack)
        colourSizer.Add(labelHover)
        colourSizer.Add(labelText)
        colourSizer.Add(labelValue)
        colourSizer.Add(labelRange)
        colourSizer.Add(labelPadding)

        colourSizer.Add(self.backColour, 0, wx.EXPAND)
        colourSizer.Add(self.borderColour, 0, wx.EXPAND)
        colourSizer.Add(self.barColour, 0, wx.EXPAND)
        colourSizer.Add(self.gaugeValue, 0, wx.EXPAND)
        colourSizer.Add(self.gaugeRange, 0, wx.EXPAND)
        colourSizer.Add(self.gaugePadding, 0, wx.EXPAND)

        mainSizer.Add(colourSizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 10)


        boldFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldFont.SetWeight(wx.FONTWEIGHT_BOLD)

        for child in self.mainPanel.GetChildren():
            if isinstance(child, wx.StaticText):
                child.SetFont(boldFont)

        self.mainPanel.SetSizer(mainSizer)
        mainSizer.Layout()
        frameSizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        frameSizer.Layout()


    def BindEvents(self):

        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnPickColour)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter, self.gaugeValue)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter, self.gaugeRange)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter, self.gaugePadding)

    def OnEnter(self,event):
        obj = event.GetEventObject()
        if obj == self.gaugeValue:
            self.gauge3.SetValue(int(self.gaugeValue.GetValue()))
        if obj == self.gaugeRange:
            self.gauge3.SetRange(int(self.gaugeRange.GetValue()))
        if obj == self.gaugePadding:
            self.gauge3.SetBorderPadding(int(self.gaugePadding.GetValue()))
        self.gauge3.Refresh()


    def OnPickColour(self, event):

        obj = event.GetEventObject()
        colour = event.GetColour()
        if obj == self.backColour:
            self.gauge3.SetBackgroundColour(colour)
        elif obj == self.borderColour:
            self.gauge3.SetBorderColour(colour)
        else:
            self.gauge3.SetBarColour(colour)

        self.gauge3.Refresh()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = PyGaugeDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = PG.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


