#!/usr/bin/env python
"""

A small test app that uses FloatCanvas to draw a vector plot.

"""

import wx
import numpy as N
import random

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas


class DrawFrame(wx.Frame):
    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        ## Set up the MenuBar

        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        item = file_menu.Append(wx.ID_ANY, "E&xit","Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()
        item = draw_menu.Append(wx.ID_ANY, "&Plot","Re-do Plot")
        self.Bind(wx.EVT_MENU, self.Plot, item)
        MenuBar.Append(draw_menu, "&Plot")


        help_menu = wx.Menu()
        item = help_menu.Append(wx.ID_ANY, "&About",
                                "More information About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        MenuBar.Append(help_menu, "&Help")

        self.SetMenuBar(MenuBar)


        self.CreateStatusBar()
        self.SetStatusText("")

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Add the Canvas
        self.Canvas = NavCanvas.NavCanvas(self ,wx.ID_ANY ,(500,300),
                                          ProjectionFun = None,
                                          Debug = 0,
                                          BackgroundColor = "WHITE"
                                          ).Canvas

        self.Canvas.NumBetweenBlits = 1000


        self.Show(True)

        self.Plot()
        return None


    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to demonstrate\n"
                               "the use of the FloatCanvas\n"
                               "for vector plotting",
                               "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def ZoomToFit(self,event):
        self.Canvas.ZoomToBB()

    def OnQuit(self,event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()


    def DrawAxis(self):
        Canvas = self.Canvas

        # Draw the Axis

        # Note: the AddRectangle Parameters all have sensible
        # defaults. I've put them all here explicitly, so you can see
        # what the options are.

        self.Canvas.AddRectangle((0, -1.1),
                                 (2*N.pi, 2.2),
                                 LineColor = "Black",
                                 LineStyle = "Solid",
                                 LineWidth    = 1,
                                 FillColor    = None,
                                 FillStyle    = "Solid",
                                 InForeground = 0)
        for tic in N.arange(7):
            self.Canvas.AddText("%1.1f"%tic,
                                (tic, -1.1),
                                Position = 'tc')

        for tic in N.arange(-1,1.1,0.5):
            self.Canvas.AddText("%1.1f"%tic,
                                (0,tic),
                                Position = 'cr')

        # Add a phantom rectangle to get the bounding box right
        #  (the bounding box doesn't get unscaled text right)
        self.Canvas.AddRectangle((-0.7, -1.5),
                                 (7, 3),
                                 LineColor = None)

        #Canvas.ZoomToBB()
        #Canvas.Draw()

    def Plot(self, event = None):
        x = N.arange(0, 2*N.pi, 0.1)
        x.shape = (-1,1)
        y = N.sin(x)
        data = N.concatenate((x, y),1)

        Canvas = self.Canvas
        self.Canvas.ClearAll()
        self.DrawAxis()
        for p in data:
            Canvas.AddPoint(p,
                            Diameter = 4,
                            Color = "Red",
                            InForeground = 1)
            theta = random.uniform(0, 360)
            Canvas.AddArrow(p,
                            Length = 20,
                            Direction = p[1]*360,
                            LineColor = "Red",
                            )
        self.Canvas.ZoomToBB()
        self.Canvas.Draw()
        self.Canvas.SaveAsImage("junk.png")


class DemoApp(wx.App):
    """
    How the demo works:

    Either under the Draw menu, or on the toolbar, you can push Run and Stop

    "Run" start an oscilloscope like display of a moving sine curve
    "Stop" stops it.

    While the plot os running (or not) you can zoom in and out and move
    about the picture. There is a tool bar with three tools that can be
    selected.

    The magnifying glass with the plus is the zoom in tool. Once selected,
    if you click the image, it will zoom in, centered on where you
    clicked. If you click and drag the mouse, you will get a rubber band
    box, and the image will zoom to fit that box when you release it.

    The magnifying glass with the minus is the zoom out tool. Once selected,
    if you click the image, it will zoom out, centered on where you
    clicked.

    The hand is the move tool. Once selected, if you click and drag on
    the image, it will move so that the part you clicked on ends up
    where you release the mouse. Nothing is changed while you are
    dragging, but you can see the outline of the former picture.

    I'd like the cursor to change as you change tools, but the stock
    wx.Cursors didn't include anything I liked, so I stuck with the
    pointer. Please let me know if you have any nice cursor images for me to
    use.


    Any bugs, comments, feedback, questions, and especially code are welcome:

    -Chris Barker

    Chris.Barker@noaa.gov

    """

    def OnInit(self):
        frame = DrawFrame(None, wx.ID_ANY, "Plotting Test",wx.DefaultPosition,wx.Size(700,400))

        self.SetTopWindow(frame)

        return True


if __name__ == "__main__":

    app = DemoApp(0)
    app.MainLoop()


