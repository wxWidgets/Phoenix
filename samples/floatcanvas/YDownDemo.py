#!/usr/bin/env python

"""
This demonstrates how to use FloatCanvas with a coordinate system where
Y is increased down, instead of up. This is a standard system for
images, for instance.

Note that there are some problems with doing this for bitmaps and text: things that require positioning.

I'm sure it can be fixed, but I don't have a need for it, so I haven't taken the time yet.
-chb

"""

import wx

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
#import sys
#sys.path.append("..")
#from floatcanvas import NavCanvas, FloatCanvas


import numpy as N

def YDownProjection(CenterPoint):
    return N.array((1,-1))

class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.CreateStatusBar()

        # Add the Canvas
        Canvas = NavCanvas.NavCanvas(self,-1,
                                     size = (500,500),
                                     ProjectionFun = YDownProjection,
                                     Debug = 0,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ).Canvas

        self.Canvas = Canvas

        Point = (0,0)
        Box = Canvas.AddRectangle(Point,
                                  (80,100),
                                  FillColor = "blue"
                                  )

        Canvas.AddText("%s"%(Point,), Point, Position="cr")
        Canvas.AddPoint(Point, Diameter=3, Color = "red")


        Point = (0,100)
        Canvas.AddText("%s"%(Point,), Point, Position="cr")
        Canvas.AddPoint(Point, Diameter=3, Color = "red")

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )


        self.Show()
        Canvas.ZoomToBB()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))


app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













