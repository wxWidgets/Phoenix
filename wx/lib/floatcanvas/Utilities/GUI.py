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


import wx
from wx.lib.floatcanvas import FloatCanvas, GUIMode


class RubberBandBox(GUIMode.GUIBase):
    """
    Class to provide a GUI Mode that makes a rubber band box
    that can be drawn on a Window
    """

    def __init__(self, CallBack, Tol=5, style='dashed'):

        """

        Create a Rubber Band Box

        :param `CallBack`: is the method you want called when the mouse is
                  released. That method will be called, passing in a rect
                  parameter, where rect is: (Point, WH) of the rect in
                  world coords.
        :param `Tol`: The tolerance for the smallest rectangle allowed. defaults
                  to 5. In pixels
        :param style: style of RB box: 'dashed': a dashed outline
                      'grey' a black outline with grey fill
        """

        self.Canvas = None # this will be set when the mode is set on a Canvas
        self.CallBack = CallBack
        self.Tol = Tol
        if style not in {'dashed', 'grey'}:
            raise ValueError("style must be one of: 'dashed', 'grey'")
        self.style = style

        self.Drawing = False
        self.RBRect = None
        self.StartPointWorld = None
        self.overlay = wx.Overlay()

        return None

    def OnMove(self, event):
        if self.Drawing:
            x, y = self.StartPoint
            Cornerx, Cornery = event.GetPosition()
            w, h = (Cornerx - x, Cornery - y)
            if abs(w) > self.Tol and abs(h) > self.Tol:
                # Draw the rubber-band rectangle using an overlay so it
                # will manage keeping the rectangle and the former window
                # contents separate.
                dc = wx.ClientDC(self.Canvas)
                odc = wx.DCOverlay(self.overlay, dc)
                odc.Clear()
                self.RBRect = ((x, y), (w, h))
                if self.style == 'dashed':
                    dc.SetBrush(wx.TRANSPARENT_BRUSH)
                    dc.SetPen(wx.Pen(wx.Colour(200, 200, 200), 3))
                    dc.DrawRectangle(*self.RBRect)
                    dc.SetPen(wx.Pen("black", 3, style=wx.PENSTYLE_SHORT_DASH))
                    dc.DrawRectangle(*self.RBRect)
                else:
                    dc.SetBrush(wx.Brush(wx.Colour(192, 192, 192, 128)))
                    dc.SetPen(wx.Pen("black", 1))
                    dc.DrawRectangle(*self.RBRect)
                del odc  # work around a bug in the Python wrappers to make
                         # sure the odc is destroyed before the ClientDC is.

        self.Canvas._RaiseMouseEvent(event,FloatCanvas.EVT_FC_MOTION)

    def OnLeftDown(self, event):
        # Start drawing
        self.Drawing = True
        self.StartPoint = event.GetPosition()

    def OnLeftUp(self, event):
        # Stop Drawing and clear the overlay
        if self.Drawing:
            self.Drawing = False
        dc = wx.ClientDC(self.Canvas)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        if self.RBRect:
            world_rect = (self.Canvas.PixelToWorld(self.RBRect[0]),
                          self.Canvas.ScalePixelToWorld(self.RBRect[1])
                          )
            wx.CallAfter(self.CallBack, world_rect)
        self.RBRect = None
