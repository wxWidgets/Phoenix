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
                                     BackgroundColor = "White",
                                     ).Canvas
#        Canvas = FloatCanvas.FloatCanvas(self,-1,
#                                     size = (500,500),
#                                     ProjectionFun = None,
#                                     Debug = 0,
#                                     BackgroundColor = "White",
#                                     )

        self.Canvas = Canvas

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )
        self.Canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnLeft)


        # Some default sizes:
        self.LineHeight = 1
        self.TextWidth = 8
        self.SpaceWidth = 1
        self.Labels = ["SW Tasks", "Set RX Rf"] + ["A Row Label"]*16
        self.NumRows = len(self.Labels)

        self.BuildChartBackground()
        self.AddLabels()
        self.Show()
        Canvas.MinScale=28
        Canvas.MaxScale=28
        Canvas.ZoomToBB()

    def BuildChartBackground(self):
        Canvas = self.Canvas
        top = 0
        bottom = -(self.LineHeight * self.NumRows)
        width = self.SpaceWidth * 16 + self.TextWidth
        # put in the rows:
        for i in range(1, self.NumRows+1, 2):
            Canvas.AddRectangle((0-self.TextWidth, -i*self.LineHeight),
                                (width, self.LineHeight),
                                LineColor = None,
                                FillColor = "LightGrey",
                                FillStyle = "Solid",)

        # put a dashed line in every 1 unit:
        for i in range(16):
            Canvas.AddLine(((i*self.SpaceWidth,bottom),(i*self.SpaceWidth,top)),
                           LineColor = "Black",
                           LineStyle = "Dot",
                           # or "Dot", "ShortDash", "LongDash","ShortDash", "DotDash"
                           LineWidth    = 1,)
    def AddLabels(self):
        Canvas = self.Canvas

        for i, label in enumerate(self.Labels):
            Canvas.AddScaledText(label,
                                 ( -self.TextWidth, -(i+0.2)*self.LineHeight ),
                                 Size = 0.6 * self.LineHeight,
                                 Color = "Black",
                                 BackgroundColor = None,
                                 Family = wx.MODERN,
                                 Style = wx.NORMAL,
                                 Weight = wx.NORMAL,
                                 Underlined = False,
                                 Position = 'tl',
                                 )

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

    def OnLeft(self, event):
        """
        Prints various info about the state of the canvas to stdout

        """
        print("Scale is:", self.Canvas.Scale)


app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













