#!/usr/bin/env python
"""

This is a small demo, showing how to make an object that can be moved around.

"""

import wx

#ver = 'local'
ver = 'installed'

if ver == 'installed': ## import the installed version
    from wx.lib.floatcanvas import NavCanvas, Resources
    from wx.lib.floatcanvas import FloatCanvas as FC
    print("using installed version: %s" % wx.lib.floatcanvas.__version__)
elif ver == 'local':
    ## import a local version
    import sys
    sys.path.append("..")
    from floatcanvas import NavCanvas,  Resources
    from floatcanvas import FloatCanvas as FC

import numpy as N

## here we create a new DrawObject:
##  code borrowed and adapted from Werner Bruhin

class ShapeMixin:
    """
    just here for added features later
    """
    def __init__(self):
        pass

class TriangleShape1(FC.Polygon, ShapeMixin):

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
        ShapeMixin.__init__(self)

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
    A frame used for the FloatCanvas Demo

    """

    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

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

        Canvas.AddRectangle((-5,-5),
                            (10,10),
                            LineColor = "Red",
                            LineStyle = "Solid",
                            LineWidth = 2,
                            FillColor    = "CYAN",
                            FillStyle    = "Solid")

        Points = N.array(((0,0),
                          (1,0),
                          (0.5, 1)),
                         N.float_)

        data  = (( (0,0),  1),
                 ( (3,3),  2),
                 ( (-2,3), 2.5 ),
                  )

        for p, L in data:
            Tri = TriangleShape1(p, 1)
            Canvas.AddObject(Tri)
            Tri.Bind(FC.EVT_FC_LEFT_DOWN, self.TriHit)


        self.MoveTri = None

        self.Show(True)
        self.Canvas.ZoomToBB()

        self.Moving = False

    def TriHit(self, object):
        print("In TriHit")
        if not self.Moving:
            self.Moving = True
            self.StartPoint = object.HitCoordsPixel
            self.StartTri = self.Canvas.WorldToPixel(object.Points)
            self.MoveTri = None
            self.MovingTri = object

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        And moves the triangle it it is clicked on

        """
        self.SetStatusText("%.4f, %.4f"%tuple(event.Coords))

        if self.Moving:
            dxy = event.GetPosition() - self.StartPoint
            # Draw the Moving Triangle:
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.MoveTri is not None:
                dc.DrawPolygon(self.MoveTri)
            self.MoveTri = self.StartTri + dxy
            dc.DrawPolygon(self.MoveTri)

    def OnLeftUp(self, event):
        if self.Moving:
            self.Moving = False
            if self.MoveTri is not None:
                dxy = event.GetPosition() - self.StartPoint
                dxy = self.Canvas.ScalePixelToWorld(dxy)
                self.MovingTri.Move(dxy) ## The Move function has jsut been added
                                    ## to the FloatCanvas PointsObject
                                    ## It does the next three lines for you.
                #self.Tri.Points += dxy
                #self.Tri.BoundingBox += dxy
                #self.Canvas.BoundingBoxDirty = True
                self.MoveTri = None
            self.Canvas.Draw(True)

if __name__ == "__main__":
    app = wx.App(0)
    x = DrawFrame(None, -1, "FloatCanvas TextBox Test App", wx.DefaultPosition, (700,700) )
    x.Show()
    app.MainLoop()













