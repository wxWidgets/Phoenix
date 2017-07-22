#!/usr/bin/env python

"""
DrawBot.py

This a a demo of how one can use the FloatCanvas to do a drawing similar to one of the "DrawBot" demos:


http://just.letterror.com/ltrwiki/DrawBot

I think it's easier with FloatCavnas, and you get zoomign and scrolling to boot!


"""

import wx
from math import *

try: # see if there is a local FloatCanvas to use
    import sys
    sys.path.append("../")
    from floatcanvas import NavCanvas, FloatCanvas
    print("Using local FloatCanvas")
except ImportError: # Use the wxPython lib one
    from wx.lib.floatcanvas import NavCanvas, FloatCanvas
    print("Using installed FloatCanvas")


class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        # Add the Canvas
        self.Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                          ProjectionFun = None,
                                          Debug = 0,
                                          BackgroundColor = "White",
                                          ).Canvas


        self.Show(True)
        self.MakePic()

        return None

    def MakePic(self):
        Canvas = self.Canvas
        phi = (sqrt(5) + 1)/2 - 1
        oradius = 10.0
        for i in xrange(720):
            radius = 1.5 * oradius * sin(i * pi/720)
            Color = (255*(i / 720.), 255*( i / 720.), 255 * 0.25)
            x = oradius + 0.25*i*cos(phi*i*2*pi)
            y = oradius + 0.25*i*sin(phi*i*2*pi)
            Canvas.AddCircle((x,y),
                             radius,
                             LineColor = "Black",
                             LineWidth = 2,
                             FillColor = Color,
                             )
        self.Canvas.ZoomToBB()

app = wx.App()
DrawFrame(None, -1, "FloatCanvas Demo App", wx.DefaultPosition, (700,700) )
app.MainLoop()

