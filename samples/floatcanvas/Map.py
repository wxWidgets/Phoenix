#!/usr/bin/env python


TestFileName = "data/TestMap.png"


import wx

from wx.lib.floatcanvas import NavCanvas, FloatCanvas

#import sys
#sys.path.append("..")
#from floatcanvas import NavCanvas, FloatCanvas


class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.CreateStatusBar()

        # Add the Canvas
        NC = NavCanvas.NavCanvas(self,-1,
                                 size = (500,500),
                                 ProjectionFun = None,
                                 Debug = 0,
                                 BackgroundColor = "White",
                                 )
        self.Canvas = NC.Canvas

        self.LoadMap(TestFileName)

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )

        self.Show()
        self.Canvas.ZoomToBB()

    def LoadMap(self, filename):
        Image = wx.Image(filename)
        self.Canvas.AddScaledBitmap(Image, (0,0), Height = Image.GetSize()[1], Position = "tl")

        self.Canvas.AddPoint((0,0), Diameter=3)
        self.Canvas.AddText("(0,0)", (0,0), Position="cl")
        p = (Image.GetSize()[0],-Image.GetSize()[1])
        self.Canvas.AddPoint(p, Diameter=3)
        self.Canvas.AddText("(%i,%i)"%p, p, Position="cl")

        self.Canvas.MinScale = 0.15
        self.Canvas.MaxScale = 1.0

    def Binding(self, event):
        print("Writing a png file:")
        self.Canvas.SaveAsImage("junk.png")
        print("Writing a jpeg file:")
        self.Canvas.SaveAsImage("junk.jpg",wx.BITMAP_TYPE_JPEG)

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        And moves a point if there is one selected

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))


app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()


