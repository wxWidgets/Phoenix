#!/usr/bin/env python

"""
A simple demo to show how to drw a bitmap on top of the Canvas at given pixel coords.

"""

import wx
import numpy as np

try:
    # See if there is a local copy
    import sys
    sys.path.append("../")
    from floatcanvas import NavCanvas, FloatCanvas
except ImportError:
    from wx.lib.floatcanvas import NavCanvas, FloatCanvas
FC = FloatCanvas

class PixelBitmap:
    """
    An unscaled bitmap that can be put on top of the canvas using:

    Canvas.GridOver = MyPixelBitmap

    It will always be drawn on top of everything else, and be positioned
    according to pixel coordinates on teh screen, regardless of zoom and
    pan position.

    """
    def __init__(self, Bitmap, XY, Position = 'tl'):
        """
        PixelBitmap (Bitmap, XY, Position='tl')

        Bitmap is a wx.Bitmap or wx.Image

        XY is the (x,y) location to place the bitmap, in pixel coordinates

        Position indicates from where in the window the position is relative to:
           'tl' indicated the position from the top left the the window (the detault)
           'br' the bottom right
           'cr the center right, etc.

        """
        if type(Bitmap) == wx.Bitmap:
            self.Bitmap = Bitmap
        elif type(Bitmap) == wx.Image:
            self.Bitmap = wx.BitmapFromImage(Bitmap)
        else:
            raise FC.FloatCanvasError("PixelBitmap takes only a wx.Bitmap or a wx.Image as input")

        self.XY = np.asarray(XY, dtype=np.int).reshape((2,))
        self.Position = Position

        (self.Width, self.Height) = self.Bitmap.GetWidth(), self.Bitmap.GetHeight()
        self.ShiftFun = FC.TextObjectMixin.ShiftFunDict[Position]

    def _Draw(self, dc, Canvas):
        w, h = Canvas.Size
        XY = self.XY
        if self.Position[0] == 'b':
            XY = (XY[0], h - XY[1] - self.Height)
        elif self.Position[0] == 'c':
            XY = (XY[0], XY[1] + (h - self.Height)/2)

        if self.Position[1] == 'r':
            XY = (w - XY[0] - self.Width, XY[1])
        elif self.Position[1] == 'c':
            XY = (XY[0] + (w - self.Width)/2, XY[1])

        dc.DrawBitmap(self.Bitmap, XY, True)

class GridGroup:
    def __init__(self, grids=[]):
        self.Grids = grids

    def _Draw(self, *args):
        for grid in self.Grids:
            grid._Draw(*args)

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
        bmp = wx.Bitmap('NOAA.png')
        grids = GridGroup([PixelBitmap(bmp, (10, 10), Position='tl'),
                           PixelBitmap(bmp, (10, 10), Position='br'),
                           PixelBitmap(bmp, (10, 10), Position='tr'),
                           PixelBitmap(bmp, (10, 10), Position='bl'),
                           PixelBitmap(bmp, (10, 10), Position='cl'),
                           PixelBitmap(bmp, (10, 10), Position='cr'),
                           PixelBitmap(bmp, (10, 10), Position='cc'),
                           PixelBitmap(bmp, (10, 10), Position='tc'),
                           PixelBitmap(bmp, (10, 10), Position='bc'),
                           ])
        Canvas.GridOver = grids

        FloatCanvas.EVT_MOTION(Canvas, self.OnMove )

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













