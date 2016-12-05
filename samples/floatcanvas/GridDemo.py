#!/usr/bin/env python

"""
A simple demo to show how to do grids

"""

import wx


try:
    # See if there is a local copy
    import sys
    sys.path.append("../")
    from floatcanvas import NavCanvas, FloatCanvas
except ImportError:
    from wx.lib.floatcanvas import NavCanvas, FloatCanvas

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


        Point = (45,40)
        Box = Canvas.AddCircle(Point,
                               Diameter = 10,
                               FillColor = "Black",
                               LineColor = "Red",
                               LineWidth = 6)

        # Crosses:
        Grid = FloatCanvas.DotGrid( Spacing=(1, .5), Size=2, Color="Cyan", Cross=True, CrossThickness=2)
        #Dots:
        #Grid = FloatCanvas.DotGrid( (0.5, 1), Size=3, Color="Red")

        Canvas.GridUnder = Grid
        #Canvas.GridOver = Grid

        Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )

        self.Show()
        Canvas.ZoomToBB()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))



app = wx.App(False) # true to get its own output window.
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













