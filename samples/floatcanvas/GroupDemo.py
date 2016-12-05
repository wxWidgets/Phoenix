#!/usr/bin/env python

"""
A small demo of how to use Groups of Objects

"""

import wx

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
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
                                     BackgroundColor = "DARK SLATE BLUE",
                                     )
        Canvas = NC.Canvas
        self.Canvas = Canvas

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )

        Point = (45,40)

        ## create a few Objects:
        C = FloatCanvas.Circle((0, 0), 10, FillColor="Red")
        R = FloatCanvas.Rectangle((5, 5),(15, 8), FillColor="Blue")
        E = FloatCanvas.Ellipse((1.5, 1.5), (12, 8), FillColor="Purple")
        C2 = FloatCanvas.Circle((0, 5), 10, FillColor="cyan")
        T = FloatCanvas.Text("Group A", (5.5, 5.5), Position="cc", Size = 16, Weight=wx.BOLD, Family=wx.SWISS)

        self.GroupA = FloatCanvas.Group((R,C,E))
        self.GroupA.AddObjects((C2,T))
        Canvas.AddObject(self.GroupA)


        ## create another Groups of objects

        R = FloatCanvas.Rectangle((15, 15),(10, 18), FillColor="orange")
        E = FloatCanvas.Ellipse((22, 28), (12, 8), FillColor="yellow")
        C = FloatCanvas.Circle((25, 20), 15, FillColor="Green")
        C2 = FloatCanvas.Circle((12, 22), 10, FillColor="cyan")
        T = FloatCanvas.Text("Group B", (19, 24), Position="cc", Size = 16, Weight=wx.BOLD, Family=wx.SWISS)

        self.GroupB = FloatCanvas.Group((R,E,C,C2,T))
        Canvas.AddObject(self.GroupB)

        self.Groups = {"A":self.GroupA, "B":self.GroupB}

        # Add a couple of tools to the Canvas Toolbar

        tb = NC.ToolBar
#        tb.AddSeparator()

        for Group in self.Groups.keys():
            Button = wx.Button(tb, wx.ID_ANY, "Hide/Show%s"%Group)
            tb.AddControl(Button)
            print(Group)
            Button.Bind(wx.EVT_BUTTON, lambda evt, group=Group: self.HideGroup(evt, group))
        tb.Realize()

        self.Show()
        Canvas.ZoomToBB()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates of the mouse position

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

    def HideGroup(self, evt, group=""):
        G = self.Groups[group]
        G.Visible = not G.Visible
        self.Canvas.Draw(Force=True)

app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













