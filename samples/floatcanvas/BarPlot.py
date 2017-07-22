#!/usr/bin/env python

import wx
## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas

import numpy as N
from numpy import random as random

NumChannels = 200
MaxValue = 2000
#MaxValue = 2**24


def YScaleFun(center):
    """
    Function that returns a scaling vector to scale y data to same range as x data

    This is used by FloatCanvas as a "projection function", so that you can have
    a different scale for X and Y. With the default projection, X and Y are the same scale.

    """

    # center gets ignored in this case
    return N.array((1, float(NumChannels)/MaxValue), N.float)

def ScaleWorldToPixel(self, Lengths):
    """
        This is a new version of a function that will get passed to the
        drawing functions of the objects, to Change a length from world to
        pixel coordinates.

        This version uses the "ceil" function, so that fractional pixel get
        rounded up, rather than down.

        Lengths should be a NX2 array of (x,y) coordinates, or
        a 2-tuple, or sequence of 2-tuples.
    """
    return  N.ceil(( (N.asarray(Lengths, N.float)*self.TransformVector) )).astype('i')


class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.CreateStatusBar()

        # Add the Canvas
        FloatCanvas.FloatCanvas.ScaleWorldToPixel = ScaleWorldToPixel
        NC = NavCanvas.NavCanvas(self,-1,
                                     size = (500,500),
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ProjectionFun = YScaleFun,
                                     )

        self.Canvas = Canvas = NC.Canvas
        #self.Canvas.ScaleWorldToPixel = ScaleWorldToPixel

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)

        self.Values = random.randint(0, MaxValue, (NumChannels,))

        self.Bars = []
        self.BarWidth = 0.75
        # add an X axis
        Canvas.AddLine(((0,0), (NumChannels, 0 )),)
        for x in N.linspace(1, NumChannels, 11):
            Canvas.AddText("%i"%x, (x-1+self.BarWidth/2,0), Position="tc")

        for i, Value in enumerate(self.Values):
            bar = Canvas.AddRectangle(XY=(i, 0),
                                      WH=(self.BarWidth, Value),
                                      LineColor = None,
                                      LineStyle = "Solid",
                                      LineWidth    = 1,
                                      FillColor    = "Red",
                                      FillStyle    = "Solid",
                                      )
            self.Bars.append(bar)

        # Add a couple a button the Toolbar

        tb = NC.ToolBar
        tb.AddSeparator()

        ResetButton = wx.Button(tb, label="Reset")
        tb.AddControl(ResetButton)
        ResetButton.Bind(wx.EVT_BUTTON, self.ResetData)

#        PlayButton = wx.Button(tb, wx.ID_ANY, "Run")
#        tb.AddControl(PlayButton)
#        PlayButton.Bind(wx.EVT_BUTTON, self.RunTest)
        tb.Realize()

        self.Show()
        Canvas.ZoomToBB()
        Canvas.Draw(True)


    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        channel, value = event.Coords
        if 0 < channel < NumChannels  :
            channel = "%i,"%(channel+1)
        else:
            channel = ""

        if value >=0:
            value = "%3g"%value
        else:
            value = ""
        self.SetStatusText("Channel: %s  Value: %s"%(channel, value))

    def ResetData(self, event):
        self.Values = random.randint(0, MaxValue, (NumChannels,))
        for i, bar in enumerate(self.Bars):
            bar.SetShape(bar.XY, (self.BarWidth, self.Values[i]))
        self.Canvas.Draw(Force=True)

app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













