#!/usr/bin/env python

"""
A simple example of sub-classing the Navcanvas

-- an alternative to simply putting a NavCanvas on your yoru oen panle or whatever
"""

import wx

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas

class DrawFrame(wx.Frame):

    """
    A frame used for the Demo
    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.CreateStatusBar()

        panel = NavPanel(self)

        self.Show()

class NavPanel(NavCanvas.NavCanvas):
    """
    a subclass of NavCAnvas -- with some specific drawing code
    """
    def __init__(self, parent):
        NavCanvas.NavCanvas.__init__(self,
                                     parent,
                                     ProjectionFun = None,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     )

        self.parent_frame = parent
        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)

        # create the image:
        self.Canvas.AddPolygon( ( (2,3),
                                   (5,6),
                                   (7,1), ),
                                 FillColor = "red",
                                 )


        wx.CallAfter(self.Canvas.ZoomToBB) # so it will get called after everything is created and sized

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.parent_frame.SetStatusText("%f, %f"%tuple(event.Coords))
        pass

app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()
