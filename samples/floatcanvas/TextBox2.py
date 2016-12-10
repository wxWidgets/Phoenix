#!/usr/bin/env python


"""
A test and demo of the ScaledTextbox.

It also shows how one can use the Mouse to interact and change objects on a Canvas.

this really needs to be re-done with GUI-Modes.
"""


import wx


## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources

## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas, Resources


import numpy as N

LongString = (
"""This is a long string. It is a bunch of text. I am using it to test how the nifty wrapping text box works when you want to re-size.

This is another paragraph. I am trying to make it long enough to wrap a reasonable amount. Let's see how it works.


    This is a way to start a paragraph with indenting
"""
)

##LongString = (
##""" This is a not so long string
##Another line""")

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

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )
        self.Canvas.Bind(FloatCanvas.EVT_LEFT_UP, self.OnLeftUp )
        self.Canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnLeftDown)

        Point = N.array((0,0), N.float)



        Canvas.AddCircle(Point,

                         Diameter=40,

                         FillColor="Red",

                         LineStyle=None,

                         )


        Width = 300
        self.Box = Canvas.AddScaledTextBox(LongString,
                                      Point,
                                      10,
                                      Color = "Black",
                                      BackgroundColor = 'White',
                                      LineStyle = "Solid",
                                      LineWidth = 2,
                                      Width = Width,
                                      PadSize = 10.0,
                                      Family = wx.ROMAN,
                                      #Family = wx.TELETYPE,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'tl',
                                      LineSpacing = 0.8,
                                      Alignment = "left",
                                      #Alignment = "center",
                                      #Alignment = "right",
                                      InForeground = False)


        self.Handle1 = Canvas.AddBitmap(Resources.getMoveCursorBitmap(), Point, Position='cc')
        self.Handle2a = Canvas.AddBitmap(Resources.getMoveRLCursorBitmap(), Point, Position='cc')
        self.Handle2b = Canvas.AddBitmap(Resources.getMoveRLCursorBitmap(), Point, Position='cc')

        self.SetHandles()

        self.Handle1.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.Handle1Hit)
        self.Handle2a.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.Handle2Hit)
        self.Handle2b.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.Handle2Hit)


        self.Show(True)
        self.Canvas.ZoomToBB()

        self.Resizing = False
        self.ResizeRect = None
        self.Moving = False

        return None

    def Handle1Hit(self, object):
        if not self.Moving:
            self.Moving = True
            self.StartPoint = object.HitCoordsPixel

    def Handle2Hit(self,event=None):
        if not self.Resizing:
            self.Resizing = True

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        And moves a point if there is one

        """
        self.SetStatusText("%.4f, %.4f"%tuple(event.Coords))

        if self.Resizing:
            ((xy),(wh))  = self.Box.GetBoxRect()
            (xp, yp) = self.Canvas.WorldToPixel(xy)
            (wp, hp) = self.Canvas.ScaleWorldToPixel(wh)
            hp = -hp
            Corner = event.GetPosition()
            if self.Box.Position[1] in 'lc':
                wp = max(20, Corner[0]-xp) # don't allow the box to get narrower than 20 pixels
            elif self.Box.Position[1] in 'r':
                DeltaX = Corner[0]-xp
                xp += DeltaX
                wp -= DeltaX
            # draw the RB box
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.ResizeRect:
                dc.DrawRectangle(*self.ResizeRect)
            self.ResizeRect = (xp,yp,wp,hp)
            dc.DrawRectangle(*self.ResizeRect)
        elif self.Moving:
            dxy = event.GetPosition() - self.StartPoint
            ((xy),(wh))  = self.Box.GetBoxRect()
            xp, yp  = self.Canvas.WorldToPixel(xy) + dxy
            (wp, hp) = self.Canvas.ScaleWorldToPixel(wh)
            hp = -hp
            # draw the RB box
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.ResizeRect:
                dc.DrawRectangle(*self.ResizeRect)
            self.ResizeRect = (xp,yp,wp,hp)
            dc.DrawRectangle(*self.ResizeRect)

    def OnLeftDown(self, event):
        pass

    def OnLeftUp(self, event):
        if self.Resizing:
            self.Resizing = False
            if self.ResizeRect:
                Point = self.Canvas.PixelToWorld(self.ResizeRect[:2])
                W, H = self.Canvas.ScalePixelToWorld(self.ResizeRect[2:4])
                self.ResizeRect = None
                self.Box.ReWrap(W)
                self.SetHandles()
        elif self.Moving:
            self.Moving = False
            if self.ResizeRect:
                dxy = event.GetPosition() - self.StartPoint
                dxy = self.Canvas.ScalePixelToWorld(dxy)
                self.Box.Move(dxy)
                self.ResizeRect = None
                # self.Box.SetPoint(Point1)
                self.SetHandles()

        self.Canvas.Draw(True)

    def SetHandles(self):
        ((x,y),(w,h))  = self.Box.GetBoxRect()
        if self.Box.Position[1] in "lc":
            x += w
        y -= h/3
        self.Handle2a.SetPoint((x,y))
        y -= h/3
        self.Handle2b.SetPoint((x,y))
        self.Handle1.SetPoint(self.Box.XY)


app = wx.App()
DrawFrame(None, -1, "FloatCanvas TextBox Test App", wx.DefaultPosition, (700,700) )
app.MainLoop()













