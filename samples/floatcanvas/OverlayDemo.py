#!/usr/bin/env python

"""
A simple demo to show how to "Overlays": i.e. drawing something
on top of eveything else on the Canvas, relative to window coords,
rather than screen coords.

This method uses the "GridOver" object in the FloatCanvas
  - it was orginally dsigend for girds, graticule,s etc. that
    are always drawn regardless of zoom, pan, etc, but it works
    for overlays too.

"""

import wx


try:
    # See if there is a local copy
    import sys
    sys.path.append("../")
    from floatcanvas import NavCanvas, FloatCanvas
except ImportError:
    from wx.lib.floatcanvas import NavCanvas, FloatCanvas

class TextOverlay(FloatCanvas.Text):
    """
    An example of an Overlay object:

    all it needs is a new _Draw method.

    NOTE: you may want to get fancier with this,
          deriving from ScaledTextBox

    """
    def __init__(self,
                 String,
                 xy,
                 Size = 24,
                 Color = "Black",
                 BackgroundColor = None,
                 Family = wx.MODERN,
                 Style = wx.NORMAL,
                 Weight = wx.NORMAL,
                 Underlined = False,
                 Font = None):
        FloatCanvas.Text.__init__(self,
                                  String,
                                  xy,
                                  Size = Size,
                                  Color = Color,
                                  BackgroundColor = BackgroundColor,
                                  Family = Family,
                                  Style = Style,
                                  Weight = Weight,
                                  Underlined = Underlined,
                                  Font = Font)

    def _Draw(self, dc, Canvas):
        """
        _Draw method for Overlay
         note: this is a differeent signarture than the DrawObject Draw
        """
        dc.SetFont(self.Font)
        dc.SetTextForeground(self.Color)
        if self.BackgroundColor:
            dc.SetBackgroundMode(wx.SOLID)
            dc.SetTextBackground(self.BackgroundColor)
        else:
            dc.SetBackgroundMode(wx.TRANSPARENT)
        ## maybe inpliment this...
        #if self.TextWidth is None or self.TextHeight is None:
        #    (self.TextWidth, self.TextHeight) = dc.GetTextExtent(self.String)
        #XY = self.ShiftFun(XY[0], XY[1], self.TextWidth, self.TextHeight)
        dc.DrawText(self.String, self.XY)


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
                               FillColor = "Cyan",
                               LineColor = "Red",
                               LineWidth = 6)

        Canvas.GridOver = TextOverlay("Some Text",
                                      (20,20),
                                      Size = 48,
                                      Color = "Black",
                                      BackgroundColor = 'Pink',
                                      )

        Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)

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













