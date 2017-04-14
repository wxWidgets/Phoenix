#!/usr/bin/env python

"""
A simple demo that shows how to use FloatCanvas to draw rectangles on the screen

Note: this is now broken -- the events are not getting to the Rubber Band Box object.
      It should be re-factored to use GUIMode
"""


import wx

## import a local version
#import sys
#sys.path.append("..")
#from floatcanvas import NavCanvas, FloatCanvas, Resources, Utilities, GUIMode
#from floatcanvas.Utilities import GUI

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, GUIMode
from wx.lib.floatcanvas.Utilities import GUI

import numpy as N

class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        self.CreateStatusBar()
        # Add the Canvas
        NC = NavCanvas.NavCanvas(self,
                                 size= (500,500),
                                 ProjectionFun = None,
                                 Debug = 0,
                                 BackgroundColor = "DARK SLATE BLUE",
                                 )

        self.Canvas = NC.Canvas

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)

        # Add some buttons to the Toolbar
        tb = NC.ToolBar
        tb.AddSeparator()

        ClearButton = wx.Button(tb, wx.ID_ANY, "Clear")
        tb.AddControl(ClearButton)
        ClearButton.Bind(wx.EVT_BUTTON, self.Clear)

        DrawButton = wx.Button(tb, wx.ID_ANY, "StopDrawing")
        tb.AddControl(DrawButton)
        DrawButton.Bind(wx.EVT_BUTTON, self.SetDraw)
        self.DrawButton = DrawButton

        tb.Realize()

        # Initialize a few values
        self.Rects = []

        self.RBBoxMode = GUI.RubberBandBox(self.NewRect)
        self.Canvas.SetMode(self.RBBoxMode)

        self.Canvas.ZoomToBB()

        self.Show(True)
        return None

    def Clear(self, event=None):
        self.Rects = []
        self.Canvas.ClearAll()
        self.Canvas.Draw()

    def SetDraw(self, event=None):
        label = self.DrawButton.GetLabel()
        if label == "Draw":
            self.DrawButton.SetLabel("StopDrawing")
            self.Canvas.SetMode(self.RBBoxMode)
        elif label == "StopDrawing":
            self.DrawButton.SetLabel("Draw")
            self.Canvas.SetMode(GUIMode.GUIMouse())
        else: # huh?
            pass

    def NewRect(self, rect):
        self.Rects.append(self.Canvas.AddRectangle(*rect, LineWidth=4))
        self.Canvas.Draw(True)

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%.4f, %.4f"%tuple(event.Coords))
        event.Skip()

app = wx.App()
DrawFrame(None, -1, "FloatCanvas Rectangle Drawer", wx.DefaultPosition, (700,700) )
app.MainLoop()













