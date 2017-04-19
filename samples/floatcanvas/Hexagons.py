#!/usr/bin/env python

"""
A simple demo to display a lot of hexagons

This was an example someone had on the wxPython-users list

"""
import wx
import wx.lib.colourdb

## import local version:
#import sys
#sys.path.append("..")
#from floatcanvas import NavCanvas, FloatCanvas

## import installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

NumHexagons = 1000

import numpy as N
from numpy.random import uniform

import  random
import time

class DrawFrame(wx.Frame):
    """
    A frame used for the FloatCanvas Demo

    """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        # Add the Canvas
        self.Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                          ProjectionFun = None,
                                          Debug = 1,
                                          BackgroundColor = "DARK SLATE BLUE",
                                          ).Canvas
        self.MakeHexagons()

        self.Show(True)
        print("Drawing the Hexagons")
        self.Canvas.ZoomToBB()

        return None

    def MakeHexagons(self):
        print("Building %i Hexagons"%NumHexagons)
        # get a list of colors for random colors

        wx.lib.colourdb.updateColourDB()
        self.colors = wx.lib.colourdb.getColourList()
        print("Max colors:", len(self.colors))
        Canvas = self.Canvas
        D = 1.0
        h = D *N.sqrt(3)/2
        Hex = N.array(((D   , 0),
                     (D/2 , -h),
                     (-D/2, -h),
                     (-D  , 0),
                     (-D/2, h),
                     (D/2 , h),
                     ))
        Centers = uniform(-100, 100, (NumHexagons, 2))
        for center in Centers:
            # scale the hexagon
            Points = Hex * uniform(5,20)
            #print(Points)
            # shift the hexagon
            Points = Points + center
            #print(Points)
            cf = random.randint(0,len(self.colors)-1)
            #cf = 55
            H = Canvas.AddPolygon(Points, LineColor = None, FillColor = self.colors[cf])
            #print("BrushList is: %i long"%len(H.BrushList))
            H.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.HexHit)
            print("BrushList is: %i long"%len(H.BrushList))

    def HexHit(self, Hex):
        print("A %s Hex was hit, obj ID: %i"%(Hex.FillColor, id(Hex)))



app = wx.App(False)
DrawFrame(None, -1, "FloatCanvas Demo App", wx.DefaultPosition, (700,700) )
app.MainLoop()













