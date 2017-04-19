#!/usr/bin/env python

"""
This is a little demo of how to make clickable (and changeable) objects with
FloatCanvas

Also an example of constant size, rather than the usual zooming and panning

Developed as an answer to a question on the wxPYhton mailing lilst:
   "get panel id while dragging across several panels'
    April 5, 2012

"""

import random
import wx

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import FloatCanvas as FC


colors = [ (255, 0  , 0  ),
           (0  , 255, 0  ),
           (0  , 0,   255),
           (255, 255, 0  ),
           (255,   0, 255),
           (0  , 255, 255),
           ]


class DrawFrame(wx.Frame):

    """
    A frame used for the  Demo

    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        # Add the Canvas
        Canvas = FloatCanvas.FloatCanvas(self,
                                         size = (500,500),
                                         ProjectionFun = None,
                                         Debug = 0,
                                         BackgroundColor = "Black",
                                         )

        self.Canvas = Canvas

        self.Canvas.Bind(wx.EVT_SIZE, self.OnSize)

        # build the squares:
        w = 10
        dx = 14
        for i in range(9):
            for j in range(9):
                Rect = Canvas.AddRectangle((i*dx, j*dx), (w, w), FillColor="White", LineStyle = None)
                Outline = Canvas.AddRectangle((i*dx, j*dx), (w, w),
                                              FillColor=None,
                                              LineWidth=4,
                                              LineColor='Red',
                                              LineStyle=None)
                Rect.indexes = (i,j)
                Rect.outline = Outline
                Rect.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.SquareHitLeft)
                Rect.Bind(FloatCanvas.EVT_FC_ENTER_OBJECT, self.SquareEnter)
                Rect.Bind(FloatCanvas.EVT_FC_LEAVE_OBJECT, self.SquareLeave)

        self.Show()
        Canvas.ZoomToBB()

    def SquareHitLeft(self, square):
        print("square hit:", square.indexes)
        # set a random color
        c = random.sample(colors, 1)[0]
        square.SetFillColor( c )
        self.Canvas.Draw(True)

    def SquareEnter(self, square):
        print("entering square:", square.indexes)
        square.outline.SetLineStyle("Solid")
        self.Canvas.Draw(True)

    def SquareLeave(self, square):
        print("leaving square:", square.indexes)
        square.outline.SetLineStyle(None)
        self.Canvas.Draw(True)


    def OnSize(self, event):
        """
        re-zooms the canvas to fit the window

        """
        print("in OnSize")
        self.Canvas.ZoomToBB()
        event.Skip()

app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













