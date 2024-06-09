#!/usr/bin/env python

"""
A simple demo that shows how to use FloatCanvas to draw shapes
on a Canvas with RubberBandShapes.  This also demonstrates the
use of GUIModes to customize drawing behavior.
"""
import wx

from wx.lib.floatcanvas import NavCanvas, FloatCanvas, GUIMode, Resources
from wx.lib.floatcanvas.Utilities import GUI


class DrawFrame(wx.Frame):
    """
    A frame used for the  Demo
    """

    def __init__(self, parent, id, title, position, size):

        try:
            imgFilename = 'data/TestMap.png'
            self.bgImage = wx.Image(imgFilename)
#            imgSize = self.bgImage.GetSize()
#            if self.bgImage.IsOk():
#                size=(imgSize[0] / 2, imgSize[1] / 2)
        except:

            print("Problem loading {0}".format(imgFilename))

            import sys
            err = sys.exc_info()
            print(err[0])
            print(err[1])

        
        wx.Frame.__init__(self, parent, id, title, position, size)

        self.CreateStatusBar()
        # Add the Canvas
        NC = NavCanvas.NavCanvas(self,
                                 size=(500, 500),
                                 ProjectionFun=None,
                                 Debug=0,
                                 BackgroundColor="DARK SLATE BLUE",
                                 )

        # We need to hijack the NavCanvas GUIMouse Mode Button
        NC.Modes 

        self.Canvas = NC.Canvas

        self.Canvas.Bind(FloatCanvas.EVT_MOTION, self.OnMove)

        # Add some buttons to the Toolbar
        tb = NC.ToolBar
        tb.AddSeparator()

        ClearButton = wx.Button(tb, wx.ID_ANY, "Clear")
        tb.AddControl(ClearButton)
        ClearButton.Bind(wx.EVT_BUTTON, self.Clear)

        DrawButton = wx.Button(tb, wx.ID_ANY, "StopDrawing")
        tb.AddControl(DrawButton)
        DrawButton.Bind(wx.EVT_BUTTON, self.SetDraw)
        self.DrawButton = DrawButton

        self.Shape = wx.Choice(tb, wx.ID_ANY, choices=("Rectangle", "Ellipse", "Line"))
        self.Shape.SetStringSelection("Rectangle")
        tb.AddControl(self.Shape)
        self.Shape.Bind(wx.EVT_CHOICE, self.SetShape)

        self.Color = wx.Choice(tb, wx.ID_ANY, choices=('Black', 'Red', 'Green', 'Blue', 'White'))
        self.Color.SetStringSelection('Black')
        tb.AddControl(self.Color)

        self.Width = wx.Choice(tb, wx.ID_ANY, choices=('1', '2', '3', '4', '5', '6'))
        self.Width.SetStringSelection('4')
        tb.AddControl(self.Width)

        tb.Realize()

        # Initialize a few values
        self.Clear()

        self.RBShapeMode = RubberBandShape(self.Shape.GetStringSelection(), self.NewShape)
        self.Canvas.SetMode(self.RBShapeMode)

        # The "Pointer" button from the NavCanvas loads a GUI.GUIMouse GUIMode object.  We need it to load our
        # RBShapeMode GUIMode object instead.  Here, we replace that button's GUIMode.  (See NavCanvas code.)
        keys = list(NC.ModesDict.keys())
        NC.ModesDict[keys[0]] = self.RBShapeMode

        self.Canvas.Draw()

        self.Show(True)
        self.Canvas.ZoomToBB()
        return None

    def Clear(self, event=None):
        self.Shapes = []
        oldScale = self.Canvas.Scale
        oldViewPortCenter = self.Canvas.ViewPortCenter
        self.Canvas.ClearAll()
        self.Canvas.AddScaledBitmap(self.bgImage, (0 - (float(self.bgImage.GetWidth()) / 2.0), (float(self.bgImage.GetHeight()) / 2.0)), Height = self.bgImage.GetSize()[1], Position = "tl")
        self.Canvas.Scale = oldScale
        self.Canvas.SetToNewScale()
        self.Canvas.ViewPortCenter = oldViewPortCenter
        self.Canvas.Draw()
        # This is necessary to get the Scale and ViewPortCenter settings displayed correctly
        self.Canvas.SendSizeEvent()

    def SetDraw(self, event=None):
        label = self.DrawButton.GetLabel()
        if label == "Draw":
            self.DrawButton.SetLabel("StopDrawing")
            self.Canvas.SetMode(self.RBShapeMode)
        elif label == "StopDrawing":
            self.DrawButton.SetLabel("Draw")
            self.Canvas.SetMode(GUIMode.GUIMouse())
        else: # huh?
            pass

    def SetShape(self, event=None):
        # When the Shape changes, we need to let the RubberBandShape know.
        self.RBShapeMode.SetShape(self.Shape.GetStringSelection())

    def NewShape(self, rect):

#        print('NewShape():', self.Shape.GetStringSelection(), rect)
#        print()

        color = self.Color.GetStringSelection()
        width = int(self.Width.GetStringSelection())
        if self.Shape.GetStringSelection() == "Rectangle":
            shape = self.Canvas.AddRectangle(*rect, LineColor=color, LineWidth=width)
        elif self.Shape.GetStringSelection() == "Ellipse":
            shape = self.Canvas.AddEllipse(*rect, LineColor=color, LineWidth=width)
        elif self.Shape.GetStringSelection() == "Line":
            # Data passed back for Lines by RubberBandShapes is in the form of
            # ((x1, y1), (w, h)) so it's the same as Rectangles and Ellipses.
            # See the RubberBandShapes object below for more.
            # This code converts ((x1, y1), (w, h)) to (x1, y1), (x2, y2))
            # needed for AddLine().
            ((x1, y1), (w, h)) = rect
            x2 = w + x1
            y2 = h + y1
            points = [(x1, y1), (x2, y2)]
            shape = self.Canvas.AddLine(points, LineColor=color, LineWidth=width)

        self.Shapes.append(shape)
        self.Canvas.Draw(True)

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText(f"{event.Coords[0]:.2f}, {event.Coords[1]:.2f}")
        event.Skip()

class RubberBandShape(GUI.RubberBandBox):
    """
    Class to provide a GUI Mode that makes a rubber band shape
    that can be drawn on a Window
    """

    def __init__(self, Shape, CallBack, Tol=5, style='dashed'):
        """
        Create a Rubber Band Box
        :param `Shape`: The Shape to be drawn in RubberBand style
        :param `CallBack`: is the method you want called when the mouse is
                  released. That method will be called, passing in a rect
                  parameter, where rect is: (Point, WH) of the rect in
                  world coords.
        :param `Tol`: The tolerance for the smallest rectangle allowed. defaults
                  to 5. In pixels
        :param style: style of RB box: 'dashed': a dashed outline
                      'grey' a black outline with grey fill
        """
        if not Shape in ('Rectangle', 'Ellipse', 'Line'):
            raise Exception('Illegal Shape for RubberBandShape')
        GUI.RubberBandBox.__init__(self, CallBack, Tol, style)
        self.Shape = Shape
        self.EndPoint = None

    def SetShape(self, Shape):
        if not Shape in ('Rectangle', 'Ellipse', 'Line'):
            raise Exception('Illegal Shape for RubberBandShape')
        self.Shape = Shape

    def OnMove(self, event):
        """ Over-rides RubberBandBox's OnMove() to allow different shapes """
        mac = 'wxMac' in wx.PlatformInfo
        if self.Drawing:
            x, y = self.StartPoint
            Cornerx, Cornery = event.GetPosition()
            # Rectangles and Ellipses need to compensate for StartPoint
            if self.Shape in ('Rectangle', 'Ellipse'):
                w, h = (Cornerx - x, Cornery - y)
            # Lines do not compensate for StartPoint.  If you do, the
            # RubberBandShape Line position is wrong.
            else:
                w, h = ( Cornerx, Cornery )
            if abs(w) > self.Tol and abs(h) > self.Tol:
                # Draw the rubber-band rectangle using an overlay so it
                # will manage keeping the rectangle and the former window
                # contents separate.
                dc = wx.ClientDC(self.Canvas)
                if mac:
                    odc = wx.DCOverlay(self.overlay, dc)
                    odc.Clear()
                if self.style == 'dashed':
                    dc.SetBrush(wx.TRANSPARENT_BRUSH)
                    dc.SetPen(wx.Pen(wx.Colour(200, 200, 200), 3))
                else:
                    dc.SetBrush(wx.Brush(wx.Colour(192, 192, 192, 128)))
                    dc.SetPen(wx.Pen("black", 1))
                if not mac:
                    dc.SetLogicalFunction(wx.XOR)
                if self.RBRect:
                    if self.Shape == "Rectangle":
                        dc.DrawRectangle(*self.RBRect)
                    elif self.Shape == "Ellipse":
                        dc.DrawEllipse(*self.RBRect)
                    elif self.Shape == "Line":
                        dc.DrawLine(*self.RBRect)
                self.RBRect = ((x, y), (w, h) )
                if self.Shape == "Rectangle":
                    dc.DrawRectangle(*self.RBRect)
                elif self.Shape == "Ellipse":
                    dc.DrawEllipse(*self.RBRect)
                elif self.Shape == "Line":
                    dc.DrawLine(*self.RBRect)
                if mac:
                    if self.style == 'dashed':
                        dc.SetPen(wx.Pen("black", 3, style=wx.PENSTYLE_SHORT_DASH))
                        if self.Shape == "Rectangle":
                            dc.DrawRectangle(*self.RBRect)
                        elif self.Shape == "Ellipse":
                            dc.DrawEllipse(*self.RBRect)
                        elif self.Shape == "Line":
                            dc.DrawLine(*self.RBRect)
                    del odc  # work around a bug in the Python wrappers to make
                             # sure the odc is destroyed before the ClientDC is.
        self.Canvas._RaiseMouseEvent(event,FloatCanvas.EVT_FC_MOTION)

    def OnLeftUp(self, event):
        """ Over-rides RubberBandBox's OnLeftUp() so that data for Lines is
            correctly provided. """
        self.EndPoint = event.GetPosition()
        # Stop Drawing
        if self.Drawing:
            self.Drawing = False
        dc = wx.ClientDC(self.Canvas)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        if self.RBRect:
            # Rectangles and Ellipses have already compensated for StartPoint
            if self.Shape in ('Rectangle', 'Ellipse'):
                world_rect = (self.Canvas.PixelToWorld(self.RBRect[0]),
                              self.Canvas.ScalePixelToWorld(self.RBRect[1])
                              )
            # Lines compensate for StartPoint here for (w, h).  If you do not, the
            # finalized Line position is wrong.
            elif self.Shape in ('Line',):
                world_rect = (self.Canvas.PixelToWorld(self.RBRect[0]),
                              self.Canvas.ScalePixelToWorld(self.EndPoint - self.StartPoint)
                              )
            wx.CallAfter(self.CallBack, world_rect)
        self.RBRect = None
        wx.CallAfter(self._delete_overlay)

    def _delete_overlay(self):
        """
        This is a total Kludge, but I was getting crashes (on a Mac) if it was kept around

        Putting it in __del__ didn't work :-(

        Clearing it directly in OnLeftUp crashed also - I guess rending wasn't completely done?

        I *think* this is due to a bug in wxPython -- it should delete an Overlay on it's own,
        but what can you do?
        """
        self.overlay = None



app = wx.App()
DrawFrame(None, wx.ID_ANY, "FloatCanvas Shape Drawer",
          wx.DefaultPosition, (700,700) )
app.MainLoop()













