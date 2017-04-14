#!/usr/bin/env python

"""
A simple example of how to use FloatCanvas by itself, without the NavCanvas toolbar

"""

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
        Canvas = FloatCanvas.FloatCanvas(self,
                                         size = (500,500),
                                         BackgroundColor = "DARK SLATE BLUE",
                                         )

        self.Canvas = Canvas

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)

        Point = (45,40)
        Box = Canvas.AddScaledTextBox("A Two Line\nString",
                                      Point,
                                      2,
                                      Color = "Black",
                                      BackgroundColor = None,
                                      LineColor = "Red",
                                      LineStyle = "Solid",
                                      LineWidth = 1,
                                      Width = None,
                                      PadSize = 5,
                                      Family = wx.ROMAN,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'br',
                                      Alignment = "left",
                                      InForeground = False)

        Box.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.Binding)
        self.Show()
        Canvas.ZoomToBB()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

    def Binding(self, event):
        print("Writing a png file:")
        self.Canvas.SaveAsImage("junk.png")
        print("Writing a jpeg file:")
        self.Canvas.SaveAsImage("junk.jpg",wx.BITMAP_TYPE_JPEG)


app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













