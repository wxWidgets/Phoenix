#!/usr/bin/env python
"""

A small test app that uses FloatCanvas to draw a plot, and have an
efficient moving line on it.

"""

import wx
import numpy as N

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas


class DrawFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        ## Set up the MenuBar

        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        item = file_menu.Append(wx.ID_EXIT, "", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()
        item = draw_menu.Append(wx.ID_ANY, "&Run", "Run the test")
        self.Bind(wx.EVT_MENU, self.RunTest, item)
        item = draw_menu.Append(wx.ID_ANY, "&Stop", "Stop the test")
        self.Bind(wx.EVT_MENU, self.Stop, item)
        MenuBar.Append(draw_menu, "&Plot")


        help_menu = wx.Menu()
        item = help_menu.Append(wx.ID_ABOUT, "",
                                "More information About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        MenuBar.Append(help_menu, "&Help")

        self.SetMenuBar(MenuBar)


        self.CreateStatusBar()
        self.SetStatusText("")

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Add the Canvas
        NC = NavCanvas.NavCanvas(self ,wx.ID_ANY ,(500,300),
                                          ProjectionFun = None,
                                          Debug = 0,
                                          BackgroundColor = "WHITE"
                                          )
        self.Canvas = NC.Canvas

        self.Canvas.NumBetweenBlits = 1000

        # Add a couple of tools to the Canvas Toolbar

        tb = NC.ToolBar
        tb.AddSeparator()

        StopButton = wx.Button(tb, wx.ID_ANY, "Stop")
        tb.AddControl(StopButton)
        StopButton.Bind(wx.EVT_BUTTON, self.Stop)

        PlayButton = wx.Button(tb, wx.ID_ANY, "Run")
        tb.AddControl(PlayButton)
        PlayButton.Bind(wx.EVT_BUTTON, self.RunTest)

        tb.Realize()

        self.Show(True)

        self.timer = None

        self.DrawAxis()

        return None


    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to demonstrate\n"
                               "the use of the FloatCanvas\n"
                               "for simple plotting",
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
                                (tic,-1.1),
                                Position = 'tc')

        for tic in N.arange(-1, 1.1, 0.5):
            self.Canvas.AddText("%1.1f"%tic,
                                (0,tic),
                                Position = 'cr')

        # Add a phantom rectangle to get the bounding box right
        #  (the bounding box doesn't get unscaled text right)
        self.Canvas.AddRectangle((-0.7, -1.5), (7, 3), LineColor = None)

        Canvas.ZoomToBB()
        Canvas.Draw()

    def Stop(self,event):
        if self.timer:
            self.timer.Stop()


    def OnTimer(self,event):
        self.count += .1
        self.data1[:,1] = N.sin(self.time+self.count) #fake move

        self.line.SetPoints(self.data1)

        self.Canvas.Draw()

    def RunTest(self,event = None):
        self.n  = 100
        self.dT = 0.05

        self.time = 2.0*N.pi*N.arange(100)/100.0

        self.data1 = 1.0*N.ones((100,2))
        self.data1[:,0] = self.time
        self.data1[:,1] = N.sin(self.time)
        Canvas = self.Canvas
        self.Canvas.ClearAll()
        self.DrawAxis()
        self.line = Canvas.AddLine(self.data1,
                                   LineColor = "Red",
                                   LineStyle = "Solid",
                                   LineWidth    = 2,
                                   InForeground = 1)
        self.Canvas.Draw()

        self.timerID = wx.NewIdRef()
        self.timer   = wx.Timer(self,self.timerID)

        self.Bind(wx.EVT_TIMER, self.OnTimer, id=self.timerID)

        self.count = 0
        self.timer.Start(int(self.dT*1000))

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
        frame = DrawFrame(None, wx.ID_ANY,
                          title = "Plotting Test",
                          size = (700,400) )

        self.SetTopWindow(frame)

        return True


if __name__ == "__main__":

    app = DemoApp(0)
    app.MainLoop()


