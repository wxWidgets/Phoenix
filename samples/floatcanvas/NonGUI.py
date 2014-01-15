#!/usr/bin/env python

"""
Demo of a FloatCanvas App that will create an image, without
actually showing anything on screen. It seems to work, but you do need
to have an X-server running on *nix for this to work.

Note: you need to specify the size in the FloatCanvas Constructor.

hmm -- I wonder if you'd even need the frame?

"""

import wx

## import the installed version
from wx.lib.floatcanvas import FloatCanvas

## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas

app = wx.App()

f = wx.Frame(None)
Canvas = FloatCanvas.FloatCanvas(f,
                                  BackgroundColor = "Cyan",
                                  size=(500,500)
                                  )


Canvas.AddRectangle((0,0), (16,20))
Canvas.AddRectangle((1,1), (6,8.5))
Canvas.AddRectangle((9,1), (6,8.5))
Canvas.AddRectangle((9,10.5), (6,8.5))
Canvas.AddRectangle((1,10.5), (6,8.5))
Canvas.ZoomToBB()


print("Saving the image: junk.png")
Canvas.SaveAsImage("junk.png")

