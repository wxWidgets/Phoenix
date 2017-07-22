#!/usr/bin/env python
"""

This is a small demo, showing how to make an object that can be moved around.

It also contains a simple prototype for a "Connector" object
  -- a line connecting two other objects

"""

import wx

#ver = 'local'
ver = 'installed'

if ver == 'installed': ## import the installed version
    from wx.lib.floatcanvas import NavCanvas, Resources
    from wx.lib.floatcanvas import FloatCanvas as FC
    from wx.lib.floatcanvas.Utilities import BBox
    print("using installed version: %s" % wx.lib.floatcanvas.__version__)
elif ver == 'local':
    ## import a local version
    import sys
    sys.path.append("..")
    from floatcanvas import NavCanvas,  Resources
    from floatcanvas import FloatCanvas as FC
    from floatcanvas.Utilities import BBox

import numpy as N

## here we create some new mixins:

class MovingObjectMixin:
    """
    Methods required for a Moving object

    """

    def GetOutlinePoints(self):
        BB = self.BoundingBox
        OutlinePoints = N.array( ( (BB[0,0], BB[0,1]),
                                    (BB[0,0], BB[1,1]),
                                    (BB[1,0], BB[1,1]),
                                    (BB[1,0], BB[0,1]),
                                 )
                               )

        return OutlinePoints


class ConnectorObjectMixin:
    """
    Mixin class for DrawObjects that can be connected with lines

    NOte that this versionony works for Objects that have an "XY" attribute:
      that is, one that is derived from XHObjectMixin.

    """

    def GetConnectPoint(self):
        return self.XY

class MovingBitmap(FC.ScaledBitmap, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    ## All we need to do is is inherit from:
    ##  ScaledBitmap, MovingObjectMixin and ConnectorObjectMixin
    pass

class MovingCircle(FC.Circle, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    ## All we need to do is is inherit from:
    ##  ScaledBitmap, MovingObjectMixin and ConnectorObjectMixin
    pass

class MovingArc(FC.Arc, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    ## All we need to do is is inherit from:
    ##  ScaledBitmap, MovingObjectMixin and ConnectorObjectMixin
    pass

class ConnectorLine(FC.LineOnlyMixin, FC.DrawObject,):
    """

    A Line that connects two objects -- it uses the objects to get its coordinates

    """
    ##fixme: this should be added to the Main FloatCanvas Objects some day.
    def __init__(self,
                 Object1,
                 Object2,
                 LineColor = "Black",
                 LineStyle = "Solid",
                 LineWidth    = 1,
                 InForeground = False):
        FC.DrawObject.__init__(self, InForeground)

        self.Object1 =  Object1
        self.Object2 =  Object2
        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth

        self.CalcBoundingBox()
        self.SetPen(LineColor,LineStyle,LineWidth)

        self.HitLineWidth = max(LineWidth,self.MinHitLineWidth)

    def CalcBoundingBox(self):
        self.BoundingBox = BBox.fromPoints((self.Object1.GetConnectPoint(),
                                            self.Object2.GetConnectPoint()) )
        if self._Canvas:
            self._Canvas.BoundingBoxDirty = True


    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Points = N.array( (self.Object1.GetConnectPoint(),
                           self.Object2.GetConnectPoint()) )
        Points = WorldToPixel(Points)
        dc.SetPen(self.Pen)
        dc.DrawLines(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.DrawLines(Points)


class TriangleShape1(FC.Polygon, MovingObjectMixin):

    def __init__(self, XY, L):

        """
        An equilateral triangle object
        XY is the middle of the triangle
        L is the length of one side of the Triangle
        """

        XY = N.asarray(XY)
        XY.shape = (2,)

        Points = self.CompPoints(XY, L)

        FC.Polygon.__init__(self, Points,
                                  LineColor = "Black",
                                  LineStyle = "Solid",
                                  LineWidth    = 2,
                                  FillColor    = "Red",
                                  FillStyle    = "Solid")
    ## Override the default OutlinePoints
    def GetOutlinePoints(self):
        return self.Points

    def CompPoints(self, XY, L):
        c = L/ N.sqrt(3)

        Points = N.array(((0, c),
                          ( L/2.0, -c/2.0),
                          (-L/2.0, -c/2.0)),
                          N.float_)

        Points += XY
        return Points


class DrawFrame(wx.Frame):

    """
    A simple frame used for the Demo

    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.CreateStatusBar()
        # Add the Canvas
        Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                          ProjectionFun = None,
                                          Debug = 0,
                                          BackgroundColor = "DARK SLATE BLUE",
                                          ).Canvas

        self.Canvas = Canvas

        Canvas.Bind(FC.EVT_MOTION, self.OnMove )
        Canvas.Bind(FC.EVT_LEFT_UP, self.OnLeftUp )

        Points = N.array(((0,0),
                          (1,0),
                          (0.5, 1)),
                         N.float)

        data  = (( (0,0),  1),
                 ( (3,3),  2),
                 ( (-2,3), 2.5 ),
                  )

        for p, L in data:
            Tri = TriangleShape1(p, 1)
            Canvas.AddObject(Tri)
            Tri.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)

        Circle = MovingCircle( (1, 3), 2, FillColor="Blue")
        Canvas.AddObject(Circle)
        Circle.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)

        Bitmaps = []
        ## create the bitmaps first
        for Point in ((1,1), (-4,3)):
            Bitmaps.append(MovingBitmap(Resources.getMondrianImage(),
                                  Point,
                                  Height=1,
                                  Position='cc')
                           )
        Line = ConnectorLine(Bitmaps[0], Bitmaps[1], LineWidth=3, LineColor="Red")
        Canvas.AddObject(Line)



        ## then add them to the Canvas, so they are on top of the line
        for bmp in Bitmaps:
            Canvas.AddObject(bmp)
            bmp.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)

        A = MovingArc((-5, 0),(-2, 2),(-5, 2), LineColor="Red", LineWidth=2)
        self.Canvas.AddObject(A)
        A.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)

        self.Show(True)
        self.Canvas.ZoomToBB()

        self.MoveObject = None
        self.Moving = False

        return None

    def ObjectHit(self, object):
        if not self.Moving:
            self.Moving = True
            self.StartPoint = object.HitCoordsPixel
            self.StartObject = self.Canvas.WorldToPixel(object.GetOutlinePoints())
            self.MoveObject = None
            self.MovingObject = object

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        and moves the object it is clicked on

        """
        self.SetStatusText("%.4f, %.4f"%tuple(event.Coords))

        if self.Moving:
            dxy = event.GetPosition() - self.StartPoint
            # Draw the Moving Object:
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.MoveObject is not None:
                dc.DrawPolygon(self.MoveObject)
            self.MoveObject = self.StartObject + dxy
            dc.DrawPolygon(self.MoveObject)

    def OnLeftUp(self, event):
        if self.Moving:
            self.Moving = False
            if self.MoveObject is not None:
                dxy = event.GetPosition() - self.StartPoint
                dxy = self.Canvas.ScalePixelToWorld(dxy)
                self.MovingObject.Move(dxy)
                self.MoveTri = None
            self.Canvas.Draw(True)

if __name__ == "__main__":
    app = wx.App(0)
    DrawFrame(None, -1, "FloatCanvas Moving Object App", wx.DefaultPosition, (700,700) )
    app.MainLoop()
