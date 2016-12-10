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

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )

        Point = (45,40)
        Text = Canvas.AddScaledText("A String",
                                      Point,
                                      20,
                                      Color = "Black",
                                      BackgroundColor = None,
                                      Family = wx.ROMAN,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'bl',
                                      InForeground = False)
        Text.MinFontSize = 4 # the default is 1
        Text.DisappearWhenSmall = False #the default is True

        Rect = Canvas.AddRectangle((50, 20), (40,10), FillColor="Red", LineStyle = None)
        Rect.MinSize = 4 # default is 1
        Rect.DisappearWhenSmall = False # defualt is True

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













