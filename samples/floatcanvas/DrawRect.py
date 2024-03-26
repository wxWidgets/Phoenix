#!/usr/bin/env python

"""
A simple demo that shows how to use FloatCanvas to draw rectangles
on a Canvas.
"""
import wx

from wx.lib.floatcanvas import NavCanvas, FloatCanvas, GUIMode
from wx.lib.floatcanvas.Utilities import GUI


class DrawFrame(wx.Frame):
    """
    A frame used for the  Demo
    """

    def __init__(self, parent, id, title, position, size):
        wx.Frame.__init__(self, parent, id, title, position, size)

        self.CreateStatusBar()
        # Add the Canvas
        NC = NavCanvas.NavCanvas(self,
                                 size=(500, 500),
                                 ProjectionFun=None,
                                 Debug=0,
                                 BackgroundColor="DARK SLATE BLUE",
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
        self.SetStatusText(f"{event.Coords[0]:.2f}, {event.Coords[1]:.2f}")
        event.Skip()


app = wx.App()
DrawFrame(None, wx.ID_ANY, "FloatCanvas Rectangle Drawer",
          wx.DefaultPosition, (700,700) )
app.MainLoop()













