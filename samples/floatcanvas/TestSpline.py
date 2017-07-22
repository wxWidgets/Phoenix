#!/usr/bin/env python


"""
This is a very small app using the FloatCanvas

It tests the Spline object, including how you can put points together to
create an object with curves and square corners.


"""
import wx

#### import local version:
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas
#from floatcanvas import FloatCanvas as FC

from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.floatcanvas import NavCanvas

class Spline(FC.Line):
    def __init__(self, *args, **kwargs):
            FC.Line.__init__(self, *args, **kwargs)

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Points = WorldToPixel(self.Points)
        dc.SetPen(self.Pen)
        dc.DrawSpline(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.DrawSpline(Points)

class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas

    """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        ## Set up the MenuBar
        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        item = file_menu.Append(-1, "&Close","Close this frame")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        MenuBar.Append(file_menu, "&File")

        help_menu = wx.Menu()
        item = help_menu.Append(-1, "&About",
                                "More information About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        MenuBar.Append(help_menu, "&Help")

        self.SetMenuBar(MenuBar)
        self.CreateStatusBar()

        # Add the Canvas
        self.Canvas = NavCanvas.NavCanvas(self,
                                          BackgroundColor = "White",
                                          ).Canvas

        self.Canvas.Bind(FC.EVT_MOTION, self.OnMove)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.DrawTest()
        self.Show()
        self.Canvas.ZoomToBB()

    def OnAbout(self, event):
        print("OnAbout called")

        dlg = wx.MessageDialog(self, "This is a small program to demonstrate\n"
                                                  "the use of the FloatCanvas\n",
                                                  "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

    def OnQuit(self,event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

    def DrawTest(self,event=None):
        wx.GetApp().Yield()

        Canvas = self.Canvas

        Points = [(0, 0),
                  (200,0),
                  (200,0),
                  (200,0),
                  (200,15),
                  (185,15),
                  (119,15),
                  (104,15),
                  (104,30),
                  (104,265),
                  (104,280),
                  (119,280),
                  (185,280),
                  (200,280),
                  (200,295),
                  (200,295),
                  (200,295),
                  (0, 295),
                  (0, 295),
                  (0, 295),
                  (0, 280),
                  (15, 280),
                  (81, 280),
                  (96, 280),
                  (96, 265),
                  (96, 30),
                  (96, 15),
                  (81, 15),
                  (15, 15),
                  (0, 15),
                  (0, 0),
                  ]

        Canvas.ClearAll()

        MyLine = FC.Spline(Points,
                      LineWidth = 3,
                      LineColor = "Blue")

        Canvas.AddObject(MyLine)
        Canvas.AddPointSet(Points,
                           Color = "Red",
                           Diameter = 4,
                           )

        ## A regular old spline:
        Points = [(-30, 260),
                  (-10, 130),
                  (70, 185),
                  (160,60),
                  ]

        Canvas.AddSpline(Points,
                             LineWidth = 5,
                             LineColor = "Purple")

class DemoApp(wx.App):

    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)

    def OnInit(self):
        frame = DrawFrame(None, title="FloatCanvas Spline Demo", size = (700,700))

        self.SetTopWindow(frame)
        return True

app = DemoApp(False)# put in True if you want output to go to it's own window.
app.MainLoop()

















