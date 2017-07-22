#!/usr/bin/env python
"""
Test of an alternaive hit test methoid that used the bounding boxes of teh objects instead.

Poorly tested!

Edited from code contributed by Benjamin Jessup on the mailing list

"""

import wx

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas
FC = FloatCanvas

def BB_HitTest(self, event, HitEvent):
    """ Hit Test Function for BoundingBox Based HitMap System"""
    if self.HitDict and self.HitDict[HitEvent]:
        # loop though the objects associated with this event
        objects = [] #Create object list for holding multiple objects
        object_index_list = [] #Create list for holding the indexes
        xy_p = event.GetPosition()
        xy = self.PixelToWorld( xy_p ) #Convert to the correct coords
        for key2 in self.HitDict[HitEvent].keys():
            #Get Mouse Event Position
            bb =  self.HitDict[HitEvent][key2].BoundingBox
            if bb.PointInside(xy):
                Object = self.HitDict[HitEvent][key2]
                objects.append(Object)
                try:
                    #First try the foreground index and add the length of the background index
                    #to account for the two 'layers' that already exist in the code
                    index = self._ForeDrawList.index(Object) + len(self._DrawList)
                except ValueError:
                    index = self._DrawList.index(Object) #Now check background if not found in foreground
                object_index_list.append(index) #append the index found
            else:
                Object = self.HitDict[HitEvent][key2]
        if len(objects) > 0: #If no objects then do nothing
            #Get the highest index object
            highest_object = objects[object_index_list.index(max(object_index_list))]
            highest_object.HitCoords = xy
            highest_object.HitCoordsPixel = xy_p
            highest_object.CallBackFuncs[HitEvent](highest_object)
            return True
        else:
            return False
    return False

FC.FloatCanvas.HitTest = BB_HitTest

class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.CreateStatusBar()

        # Add the Canvas
        Canvas = NavCanvas.NavCanvas(self,-1,
                                     size = (500,500),
                                     ProjectionFun = None,
                                     Debug = 0,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ).Canvas

        self.Canvas = Canvas

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)

        Point = (45,40)
        Text = Canvas.AddScaledText("A String",
                                      Point,
                                      20,
                                      Color = "Black",
                                      BackgroundColor = None,
                                      Family = wx.ROMAN,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'bl',
                                      InForeground = False)
        Text.MinFontSize = 4 # the default is 1
        Text.DisappearWhenSmall = False #the default is True

        Rect1 = Canvas.AddRectangle((50, 20), (40,15), FillColor="Red", LineStyle = None)
        Rect1.Bind(FC.EVT_FC_LEFT_DOWN, self.OnLeft)
        Rect1.Name = "red"

        Rect2 = Canvas.AddRectangle((70, 30), (40,15), FillColor="Blue", LineStyle = None)
        Rect2.Bind(FC.EVT_FC_LEFT_DOWN, self.OnLeft)
        Rect2.Name = 'blue'

        self.Show()
        Canvas.ZoomToBB()

    def OnLeft(self, object):
        print("Rect %s got hit"%object.Name)

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()













