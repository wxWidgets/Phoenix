#!/usr/bin/env python
"""

A test and demo of  the features of the ScaledTextBox

"""

import wx

## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import the local version
#import sys
#sys.path.append("..")
#from floatcanvas import NavCanvas, FloatCanvas

import numpy as N

class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        # Add the Canvas
        self.CreateStatusBar()
        Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                          ProjectionFun = None,
                                          Debug = 0,
                                          BackgroundColor = "DARK SLATE BLUE",
                                          ).Canvas

        self.Canvas = Canvas
        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove )

        Point = (45,40)
        Box = Canvas.AddScaledTextBox("A Two Line\nString",
                                      Point,
                                      2,
                                      Color = "Black",
                                      BackgroundColor = None,
                                      LineColor = "Red",
                                      LineStyle = "Solid",
                                      LineWidth = 1,
                                      Width = None,
                                      PadSize = 5,
                                      Family = wx.ROMAN,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'br',
                                      Alignment = "left",
                                      InForeground = False)

        # All defaults
        Box = Canvas.AddScaledTextBox("A Two Line\nString",
                                      Point,
                                      2)

        Box = Canvas.AddScaledTextBox("A Two Line\nString",
                                      Point,
                                      2,
                                      BackgroundColor = "Yellow",
                                      LineColor = "Red",
                                      LineStyle = "Solid",
                                      PadSize = 5,
                                      Family = wx.TELETYPE,
                                      Position = 'bl')

        Box = Canvas.AddScaledTextBox("A Two Line\nString",
                                      Point,
                                      2,
                                      BackgroundColor = "Yellow",
                                      LineColor = "Red",
                                      LineStyle = "Solid",
                                      PadSize = 5,
                                      Family = wx.TELETYPE,
                                      Position = 'tr')




        Box.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.binding2)

        Canvas.AddPoint(Point, Diameter = 4)

        Point = (45,15)
        Box = Canvas.AddScaledTextBox("A Two Line\nString",
                                      Point,
                                      2,
                                      Color = "Black",
                                      BackgroundColor = 'Red',
                                      LineColor = "Blue",
                                      LineStyle = "LongDash",
                                      LineWidth = 2,
                                      Width = None,
                                      PadSize = 5,
                                      Family = wx.TELETYPE,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'cr',
                                      Alignment = "left",
                                      InForeground = False)

        Box = Canvas.AddScaledTextBox("A Two Line\nString",
                                      Point,
                                      1.5,
                                      Color = "Black",
                                      BackgroundColor = 'Red',
                                      LineColor = "Blue",
                                      LineStyle = "LongDash",
                                      LineWidth = 2,
                                      Width = None,
                                      PadSize = 5,
                                      Family = wx.TELETYPE,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'cl',
                                      Alignment = "left",
                                      InForeground = False)

        Canvas.AddPoint(Point, Diameter = 4)

        Point = (45,-10)
        Box = Canvas.AddScaledTextBox("A Two Line\nString",
                                      Point,
                                      2,
                                      Color = "Black",
                                      BackgroundColor = 'Red',
                                      LineColor = "Blue",
                                      LineStyle = "LongDash",
                                      LineWidth = 2,
                                      Width = None,
                                      PadSize = 3,
                                      Family = wx.TELETYPE,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'tc',
                                      Alignment = "left",
                                      InForeground = False)

        Box = Canvas.AddScaledTextBox("A three\nLine\nString",
                                      Point,
                                      1.5,
                                      Color = "Black",
                                      BackgroundColor = 'Red',
                                      LineColor = "Blue",
                                      LineStyle = "LongDash",
                                      LineWidth = 2,
                                      Width = None,
                                      PadSize = 0.5,
                                      Family = wx.TELETYPE,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'bc',
                                      Alignment = "left",
                                      InForeground = False)


        Canvas.AddPoint(Point, Diameter = 4)

        Box = Canvas.AddScaledTextBox("Some Auto Wrapped Text. There is enough to do.",
                                      (80,40),
                                      2,
                                      BackgroundColor = 'White',
                                      LineWidth = 2,
                                      Width = 20,
                                      PadSize = 0.5,
                                      Family = wx.TELETYPE,
                                      )

        Box = Canvas.AddScaledTextBox("Some more auto wrapped text. Wrapped to a different width and right aligned.\n\nThis is another paragraph.",
                                      (80,20),
                                      2,
                                      BackgroundColor = 'White',
                                      LineWidth = 2,
                                      Width = 40,
                                      PadSize = 0.5,
                                      Family = wx.ROMAN,
                                      Alignment = "right"
                                      )
        Point = N.array((100, -20), N.float_)
        Box = Canvas.AddScaledTextBox("Here is even more auto wrapped text. This time the line spacing is set to 0.8. \n\nThe Padding is set to 0.",
                                      Point,
                                      Size = 3,
                                      BackgroundColor = 'White',
                                      LineWidth = 1,
                                      Width = 40,
                                      PadSize = 0.0,
                                      Family = wx.ROMAN,
                                      Position = "cc",
                                      LineSpacing = 0.8
                                      )
        Canvas.AddPoint(Point, "Red", 2)

        Point = N.array((0, -40), N.float_)
#        Point = N.array((0, 0), N.float_)
        for Position in ["tl", "bl", "tr", "br"]:
#        for Position in ["br"]:
            Box = Canvas.AddScaledTextBox("Here is a\nfour liner\nanother line\nPosition=%s"%Position,
                                      Point,
                                      Size = 4,
                                      Color = "Red",
                                      BackgroundColor = None,#'LightBlue',
                                      LineWidth = 1,
                                      LineColor = "White",
                                      Width = None,
                                      PadSize = 2,
                                      Family = wx.ROMAN,
                                      Position = Position,
                                      LineSpacing = 0.8
                                      )
        Canvas.AddPoint(Point, "Red", 4)

        Point = N.array((-20, 60), N.float_)
        Box = Canvas.AddScaledTextBox("Here is some\ncentered\ntext",
                                      Point,
                                      Size = 4,
                                      Color = "Red",
                                      BackgroundColor = 'LightBlue',
                                      LineWidth = 1,
                                      LineColor = "White",
                                      Width = None,
                                      PadSize = 2,
                                      Family = wx.ROMAN,
                                      Position = "tl",
                                      Alignment = "center",
                                      LineSpacing = 0.8
                                      )

        Point = N.array((-20, 20), N.float_)
        Box = Canvas.AddScaledTextBox("Here is some\nright aligned\ntext",
                                      Point,
                                      Size = 4,
                                      Color = "Red",
                                      BackgroundColor = 'LightBlue',
                                      LineColor = None,
                                      Width = None,
                                      PadSize = 2,
                                      Family = wx.ROMAN,
                                      Position = "tl",
                                      Alignment = "right",
                                      LineSpacing = 0.8
                                      )

        Point = N.array((100, -60), N.float_)
        Box = Canvas.AddScaledTextBox("Here is some auto wrapped text. This time it is centered, rather than right aligned.\n\nThe Padding is set to 2.",
                                      Point,
                                      Size = 3,
                                      BackgroundColor = 'White',
                                      LineWidth = 1,
                                      Width = 40,
                                      PadSize = 2.0,
                                      Family = wx.ROMAN,
                                      Position = "cc",
                                      LineSpacing = 0.8,
                                      Alignment = 'center',
                                      )


        self.Show(True)
        self.Canvas.ZoomToBB()

        return None
    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))


    def binding(self, event):
        print("I'm the Rectangle")

    def binding2(self, event):
        print("I'm the TextBox")

app = wx.App()
DrawFrame(None, -1, "FloatCanvas Demo App", wx.DefaultPosition, (700,700) )
app.MainLoop()













