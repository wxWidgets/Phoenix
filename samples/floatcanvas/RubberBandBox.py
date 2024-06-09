#!/usr/bin/env python

import wx

from wx.lib.floatcanvas import NavCanvas, FloatCanvas
from wx.lib.floatcanvas.Utilities.GUI import RubberBandBox


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

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )

        # Just to have something to display
        Rect = Canvas.AddRectangle((50, 20), (40,10), FillColor="Red", LineStyle = None)

        self.RBBoxMode = RubberBandBox(self.RBBoxDone, style='grey')
        self.Canvas.SetMode(self.RBBoxMode)

        self.Show()
        Canvas.ZoomToBB()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%.2f, %.2f" % tuple(event.Coords))

    def RBBoxDone(self, rect):
        print(f"Rubber Band Box Released at: {rect}")

app = wx.App(False)
F = DrawFrame(None, title="Rubber Band Box Demo", size=(700, 700))
app.MainLoop()













