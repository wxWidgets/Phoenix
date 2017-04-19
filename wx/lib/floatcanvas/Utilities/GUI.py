#----------------------------------------------------------------------------
# Name:         GUI.py
# Purpose:      Contains GUI related utilities for FloatCanvas
#
# Author:
#
# Created:
# Version:
# Date:
# Licence:
# Tags:         phoenix-port, unittest, documented, py3-port
#----------------------------------------------------------------------------
"""

Part of the floatcanvas.Utilities package.

This module contains assorted GUI-related utilities that can be used
with FloatCanvas

So far, they are:

RubberBandBox: used to draw a RubberBand Box on the screen

"""

import numpy as np

import wx
from wx.lib.floatcanvas import FloatCanvas, GUIMode

class RubberBandBox(GUIMode.GUIBase):
    """
    Class to provide a GUI Mode that makes a rubber band box that can be drawn on a Window

    """

    def __init__(self, CallBack, Tol=5):

        """
        Default class constructor.

        :param `CallBack`: is the method you want called when the mouse is
                  released. That method will be called, passing in a rect
                  parameter, where rect is: (Point, WH) of the rect in
                  world coords.
        :param `Tol`: The tolerance for the smallest rectangle allowed. defaults
                  to 5. In pixels
        """

        self.Canvas = None # this will be set when the mode is set on a Canvas
        self.CallBack = CallBack
        self.Tol = Tol

        self.Drawing = False
        self.RBRect = None
        self.StartPointWorld = None

        return None

    def OnMove(self, event):
        if self.Drawing:
            x, y = self.StartPoint
            Cornerx, Cornery = event.GetPosition()
            w, h = ( Cornerx - x, Cornery - y)
            if abs(w) > self.Tol and abs(h) > self.Tol:
                # draw the RB box
                dc = wx.ClientDC(self.Canvas)
                dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetLogicalFunction(wx.XOR)
                if self.RBRect:
                    dc.DrawRectangle(*self.RBRect)
                self.RBRect = ((x, y), (w, h) )
                dc.DrawRectangle(*self.RBRect)
        self.Canvas._RaiseMouseEvent(event,FloatCanvas.EVT_FC_MOTION)

    def OnLeftDown(self, event):
        # Start drawing
        self.Drawing = True
        self.StartPoint = event.GetPosition()

    def OnLeftUp(self, event):
        # Stop Drawing
        if self.Drawing:
            self.Drawing = False
            if self.RBRect:
                world_rect = (self.Canvas.PixelToWorld(self.RBRect[0]),
                              self.Canvas.ScalePixelToWorld(self.RBRect[1])
                              )
                wx.CallAfter(self.CallBack, world_rect)
        self.RBRect = None
