#!/usr/bin/env python

import wx

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas


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
                                     ProjectionFun = None,
                                     Debug = 0,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ).Canvas

        self.Canvas = Canvas

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)

        Pts = ((45,40), (20, 15), (10, 40), (30,30))

        Points = Canvas.AddPointSet(Pts, Diameter=3, Color="Red")
        Points.HitLineWidth = 10

        Points.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.OnOverPoints)
        Points.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.OnLeavePoints)
        Points.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.OnLeftDown)

        self.Show()
        Canvas.ZoomToBB()

    def OnOverPoints(self, obj):
        print("Mouse over point: %s" % obj.FindClosestPoint(obj.HitCoords))

    def OnLeavePoints(self, obj):
        print("Mouse left point: %s" % obj.FindClosestPoint(obj.HitCoords))

    def OnLeftDown(self, obj):
        print("Mouse left down on point: %s" % obj.FindClosestPoint(obj.HitCoords))

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%.2f, %.2f" % tuple(event.Coords))

app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













