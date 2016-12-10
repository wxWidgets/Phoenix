#!/usr/bin/env python


import wx

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas
from wx.lib.floatcanvas.FCObjects import PieChart

## import a local version
#import sys
#sys.path.append("..")
#from floatcanvas import NavCanvas, FloatCanvas
#from floatcanvas.SpecialObjects import PieChart


import numpy as N

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
                                     Debug = 0,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ).Canvas

        self.Canvas = Canvas

        Values = (10,10,10)
        Colors = ('Red', 'Blue', 'Green')
        Pie1 = PieChart(N.array((0, 0)), 10, Values, Colors, Scaled=False)
        Canvas.AddObject(Pie1)

        Values = (10, 5, 5)
        Pie2 = PieChart(N.array((40, 0)), 10, Values, Colors)
        Canvas.AddObject(Pie2)

        # test default colors
        Values = (10, 15, 12, 24, 6, 10, 13, 11, 9, 13, 15, 12)
        Pie3 = PieChart(N.array((20, 20)), 10, Values, LineColor="Black")
        Canvas.AddObject(Pie3)

        # missng slice!
        Values = (10, 15, 12, 24)
        Colors = ('Red', 'Blue', 'Green', None)
        Pie4 = PieChart(N.array((0, -15)), 10, Values, Colors, LineColor="Black")
        Canvas.AddObject(Pie4)


        # Test the styles
        Values = (10, 12, 14)
        Styles = ("Solid", "CrossDiagHatch","CrossHatch")
        Colors = ('Red', 'Blue', 'Green')
        Pie4 = PieChart(N.array((20, -20)), 10, Values, Colors, Styles)
        Canvas.AddObject(Pie2)

        Pie1.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.Pie1Hit)
        Pie2.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.Pie2Hit)

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )

        self.Show()
        Canvas.ZoomToBB()

    def Pie1Hit(self, obj):
        print("Pie1 hit!")

    def Pie2Hit(self, obj):
        print("Pie2 hit!")

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%.2g, %.2g"%tuple(event.Coords))


app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()
