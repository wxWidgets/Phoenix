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
    from agw import knobctrl as KC
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.knobctrl as KC


#----------------------------------------------------------------------

class KnobCtrlDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)
        self.log = log

        self.panel = wx.Panel(self, -1)
        self.LayoutItems()


    def LayoutItems(self):

        leftbottomsizer_staticbox = wx.StaticBox(self.panel, -1, "Play With Me!")
        lefttopsizer_staticbox = wx.StaticBox(self.panel, -1, "Change My Properties!")

        self.knob1 = KC.KnobCtrl(self.panel, -1, size=(100, 100))
        self.knob2 = KC.KnobCtrl(self.panel, -1, size=(100, 100))

        self.knob1.SetTags(range(0, 151, 10))
        self.knob1.SetAngularRange(-45, 225)
        self.knob1.SetValue(45)

        self.knob2.SetTags(range(0, 151, 10))
        self.knob2.SetAngularRange(0, 270)
        self.knob2.SetValue(100)

        self.knobtracker1 = wx.StaticText(self.panel, -1, "Value = 45")
        self.knobtracker2 = wx.StaticText(self.panel, -1, "Value = 100")

        knobslider = wx.Slider(self.panel, -1, 4, 1, 10, style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)
        tickslider = wx.Slider(self.panel, -1, 16, 3, 20, style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)
        tagscolour = wx.ColourPickerCtrl(self.panel, -1, wx.BLACK, style=wx.CLRP_USE_TEXTCTRL)
        boundingcolour = wx.ColourPickerCtrl(self.panel, -1, wx.WHITE, style=wx.CLRP_USE_TEXTCTRL)
        firstcolour = wx.ColourPickerCtrl(self.panel, -1, wx.WHITE, style=wx.CLRP_USE_TEXTCTRL)
        secondcolour = wx.ColourPickerCtrl(self.panel, -1, wx.Colour(170, 170, 150), style=wx.CLRP_USE_TEXTCTRL)

        knobslider.SetValue(4)
        tickslider.SetValue(16)

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        panelsizer = wx.BoxSizer(wx.HORIZONTAL)
        rightsizer = wx.FlexGridSizer(6, 2, 10, 10)
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        leftbottomsizer = wx.StaticBoxSizer(leftbottomsizer_staticbox, wx.VERTICAL)
        lefttopsizer = wx.StaticBoxSizer(lefttopsizer_staticbox, wx.VERTICAL)

        lefttopsizer.Add(self.knob1, 1, wx.ALL|wx.EXPAND, 5)
        lefttopsizer.Add(self.knobtracker1, 0, wx.ALL, 5)
        leftsizer.Add(lefttopsizer, 1, wx.ALL|wx.EXPAND, 5)
        leftbottomsizer.Add(self.knob2, 1, wx.ALL|wx.EXPAND, 5)
        leftbottomsizer.Add(self.knobtracker2, 0, wx.ALL, 5)
        leftsizer.Add(leftbottomsizer, 1, wx.ALL|wx.EXPAND, 5)
        panelsizer.Add(leftsizer, 1, wx.EXPAND|wx.ALL, 20)

        label_1 = wx.StaticText(self.panel, -1, "Knob Radius: ")
        rightsizer.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        rightsizer.Add(knobslider, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        label_2 = wx.StaticText(self.panel, -1, "Number Of Ticks: ")
        rightsizer.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        rightsizer.Add(tickslider, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        label_3 = wx.StaticText(self.panel, -1, "Tags Colour: ")
        rightsizer.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        rightsizer.Add(tagscolour, 0)
        label_4 = wx.StaticText(self.panel, -1, "Bounding Colour: ")
        rightsizer.Add(label_4, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        rightsizer.Add(boundingcolour, 0)
        label_5 = wx.StaticText(self.panel, -1, "First Gradient Colour: ")
        rightsizer.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        rightsizer.Add(firstcolour, 0)
        label_6 = wx.StaticText(self.panel, -1, "Second Gradient Colour: ")
        rightsizer.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        rightsizer.Add(secondcolour, 0)
        panelsizer.Add(rightsizer, 1, wx.ALL|wx.EXPAND, 20)

        self.panel.SetSizer(panelsizer)
        panelsizer.Layout()

        mainsizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(mainsizer)
        mainsizer.Layout()

        self.Bind(wx.EVT_COMMAND_SCROLL, self.OnKnobRadius, knobslider)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.OnTicks, tickslider)
        self.Bind(KC.EVT_KC_ANGLE_CHANGED, self.OnAngleChanged1, self.knob1)
        self.Bind(KC.EVT_KC_ANGLE_CHANGED, self.OnAngleChanged2, self.knob2)
        tagscolour.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnTagsColour)
        boundingcolour.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnBoundingColour)
        firstcolour.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnFirstColour)
        secondcolour.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnSecondColour)


    def OnAngleChanged1(self, event):

        value = event.GetValue()
        self.knobtracker1.SetLabel("Value = " + str(value))
        self.log.write("KnobCtrl 1 changed value to %s\n"%value)
        self.knobtracker1.Refresh()


    def OnAngleChanged2(self, event):

        value = event.GetValue()
        self.knobtracker2.SetLabel("Value = " + str(value))
        self.log.write("KnobCtrl 2 changed value to %s\n"%value)
        self.knobtracker2.Refresh()


    def OnKnobRadius(self, event):

        value = event.GetPosition()
        self.knob1.SetKnobRadius(value)
        event.Skip()


    def OnTicks(self, event):

        minvalue = self.knob1.GetMinValue()
        maxvalue = self.knob1.GetMaxValue()

        therange = int((maxvalue-minvalue)/(event.GetPosition()-1))
        tickrange = range(minvalue, maxvalue+1, therange)
        self.knob1.SetTags(tickrange)

        event.Skip()


    def OnTagsColour(self, event):

        self.knob1.SetTagsColour(event.GetColour())


    def OnBoundingColour(self, event):

        self.knob1.SetBoundingColour(event.GetColour())


    def OnFirstColour(self, event):

        self.knob1.SetFirstGradientColour(event.GetColour())


    def OnSecondColour(self, event):

        self.knob1.SetSecondGradientColour(event.GetColour())


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = KnobCtrlDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = KC.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


