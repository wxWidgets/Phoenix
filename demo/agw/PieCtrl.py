#!/usr/bin/env python

import wx
from math import pi

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    import agw.piectrl
    from agw.piectrl import PieCtrl, ProgressPie, PiePart
    docs = agw.piectrl.__doc__
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.piectrl
    from wx.lib.agw.piectrl import PieCtrl, ProgressPie, PiePart
    docs = wx.lib.agw.piectrl.__doc__

#----------------------------------------------------------------------
# Auxiliary Timer Class For The Demo (For The ProgressPie)
#----------------------------------------------------------------------

class MyTimer(wx.Timer):


    def __init__(self, parent):

        wx.Timer.__init__(self)
        self._parent = parent


    def Notify(self):

        if self._parent._progresspie.GetValue() <= 0:
            self._parent._incr = 1

        if self._parent._progresspie.GetValue() >= self._parent._progresspie.GetMaxValue():
            self._parent._incr = -1

        try:
            self._parent._progresspie.SetValue(self._parent._progresspie.GetValue() +
                                                                       self._parent._incr)
            self._parent._progresspie.Refresh()
        except RuntimeError:
            pass    # catch error on exit if the ProgressPie control
                    # is deleted and the timer is still active

#----------------------------------------------------------------------
# Beginning Of PIECTRL Demo wxPython Code
#----------------------------------------------------------------------

class PieCtrlDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)

        self.log = log
        # Create Some Maquillage For The Demo: Icon, StatusBar, MenuBar...

        panel = wx.Panel(self, -1)
        self._incr = 1
        self._hiddenlegend = False

        panel.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        # Create A Simple PieCtrl With 3 Sectors
        self._pie = PieCtrl(panel, -1, wx.DefaultPosition, wx.Size(180,270))

        self._pie.GetLegend().SetTransparent(True)
        self._pie.GetLegend().SetHorizontalBorder(10)
        self._pie.GetLegend().SetWindowStyle(wx.STATIC_BORDER)
        self._pie.GetLegend().SetLabelFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                                   wx.FONTSTYLE_NORMAL,
                                                   wx.FONTWEIGHT_NORMAL,
                                                   False, "Courier New"))
        self._pie.GetLegend().SetLabelColour(wx.Colour(0, 0, 127))

        self._pie.SetHeight(30)

        part = PiePart()

        part.SetLabel("SeriesLabel_1")
        part.SetValue(300)
        part.SetColour(wx.Colour(200, 50, 50))
        self._pie._series.append(part)

        part = PiePart()
        part.SetLabel("Series Label 2")
        part.SetValue(200)
        part.SetColour(wx.Colour(50, 200, 50))
        self._pie._series.append(part)

        part = PiePart()
        part.SetLabel("HelloWorld Label 3")
        part.SetValue(50)
        part.SetColour(wx.Colour(50, 50, 200))
        self._pie._series.append(part)

        # Create A ProgressPie
        self._progresspie = ProgressPie(panel, 100, 50, -1, wx.DefaultPosition,
                                        wx.Size(180, 200), wx.SIMPLE_BORDER)

        self._progresspie.SetBackColour(wx.Colour(150, 200, 255))
        self._progresspie.SetFilledColour(wx.RED)
        self._progresspie.SetUnfilledColour(wx.WHITE)
        self._progresspie.SetHeight(20)

        self._slider = wx.Slider(panel, -1, 25, 0, 90, wx.DefaultPosition, wx.DefaultSize, wx.SL_VERTICAL | wx.SL_LABELS)
        self._angleslider = wx.Slider(panel, -1, 200, 0, 360, wx.DefaultPosition, wx.DefaultSize, wx.SL_LABELS | wx.SL_TOP)
        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(sizer)

        hsizer.Add(self._progresspie, 1, wx.EXPAND | wx.ALL, 5)
        hsizer.Add(self._pie, 1, wx.EXPAND | wx.ALL, 5)
        hsizer.Add(self._slider, 0, wx.GROW | wx.ALL, 5)

        btn1 = wx.Button(panel, -1, "Toggle Legend Transparency")
        btn2 = wx.Button(panel, -1, "Toggle Edges")
        btn3 = wx.Button(panel, -1, "Hide Legend")
        btnsizer.Add(btn1, 0, wx.ALL, 5)
        btnsizer.Add(btn2, 0, wx.ALL, 5)
        btnsizer.Add(btn3, 0, wx.ALL, 5)

        sizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self._angleslider, 0, wx.GROW | wx.ALL, 5)
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.LEFT | wx.RIGHT, 5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        mainSizer.Layout()

        self._timer = MyTimer(self)
        self._timer.Start(50)

        self._slider.Bind(wx.EVT_SLIDER, self.OnSlider)
        self._angleslider.Bind(wx.EVT_SLIDER, self.OnAngleSlider)
        btn1.Bind(wx.EVT_BUTTON, self.OnToggleTransparency)
        btn2.Bind(wx.EVT_BUTTON, self.OnToggleEdges)
        btn3.Bind(wx.EVT_BUTTON, self.OnToggleLegend)

        self.OnAngleSlider(None)
        self.OnSlider(None)


    def OnToggleTransparency(self, event):

        self._pie.GetLegend().SetTransparent(not self._pie.GetLegend().IsTransparent())
        self._pie.Refresh()


    def OnToggleEdges(self, event):

        self._pie.SetShowEdges(not self._pie.GetShowEdges())
        self._progresspie.SetShowEdges(not self._progresspie.GetShowEdges())


    def OnToggleLegend(self, event):

        self._hiddenlegend = not self._hiddenlegend

        if self._hiddenlegend:
            self._pie.GetLegend().Hide()
        else:
            self._pie.GetLegend().Show()

        self._pie.Refresh()


    def OnSlider(self, event):

        self._pie.SetAngle(float(self._slider.GetValue())/180.0*pi)
        self._progresspie.SetAngle(float(self._slider.GetValue())/180.0*pi)


    def OnAngleSlider(self, event):

        self._pie.SetRotationAngle(float(self._angleslider.GetValue())/180.0*pi)
        self._progresspie.SetRotationAngle(float(self._angleslider.GetValue())/180.0*pi)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = PieCtrlDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = docs

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


