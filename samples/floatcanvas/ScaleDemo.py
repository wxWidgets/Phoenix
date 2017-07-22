#!/usr/bin/env python

"""
This demonstrates how to use FloatCanvas with a coordinate system where
X and Y have different scales. In the example, a user had:

X data in the range: 50e-6 to 2000e-6
Y data in the range: 0 to 50000

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

def YScaleFun(center):
    """
    function that returns a scaling vector to scale y data to same range as x data

    """
    # center gets ignored in this case
    return N.array((5e7, 1), N.float)

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
                                     ProjectionFun = YScaleFun,
                                     Debug = 0,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ).Canvas

        self.Canvas = Canvas

        Point = N.array((50e-6, 0))
        Size = N.array(( (2000e-6 - 5e-6), 50000))
        Box = Canvas.AddRectangle(Point,
                                  Size,
                                  FillColor = "blue"
                                  )

        Canvas.AddText("%s"%(Point,), Point, Position="cr")
        Canvas.AddPoint(Point, Diameter=3, Color = "red")


        Point = Point + Size
        Canvas.AddText("%s"%(Point,), Point, Position="cl")
        Canvas.AddPoint(Point, Diameter=3, Color = "red")

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)


        self.Show()
        Canvas.ZoomToBB()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%.2g, %.2g"%tuple(event.Coords))


app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













