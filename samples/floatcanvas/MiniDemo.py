#!/usr/bin/env python

import wx

## import local version:
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas

## import installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

import wx.lib.colourdb

class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        ## Set up the MenuBar

        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        item = file_menu.Append(wx.ID_EXIT, "", "Close this frame")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()

        item = draw_menu.Append(wx.ID_ANY, "&Draw Test","Run a test of drawing random components")
        self.Bind(wx.EVT_MENU,self.DrawTest, item)

        item = draw_menu.Append(wx.ID_ANY, "&Move Test","Run a test of moving stuff in the background")
        self.Bind(wx.EVT_MENU, self.MoveTest, item)

        item = draw_menu.Append(wx.ID_ANY, "&Clear","Clear the Canvas")
        self.Bind(wx.EVT_MENU,self.Clear, item)

        MenuBar.Append(draw_menu, "&Draw")

        view_menu = wx.Menu()
        item = view_menu.Append(wx.ID_ANY, "Zoom to &Fit","Zoom to fit the window")
        self.Bind(wx.EVT_MENU,self.ZoomToFit, item)
        MenuBar.Append(view_menu, "&View")

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
        self.Canvas = NavCanvas.NavCanvas(self,
                                          ProjectionFun = None,
                                          Debug = 0,
                                          BackgroundColor = "DARK SLATE BLUE",
                                          ).Canvas


        self.Show(True)


        # get a list of colors for random colors
        wx.lib.colourdb.updateColourDB()
        self.colors = wx.lib.colourdb.getColourList()

        self.LineStyles = FloatCanvas.DrawObject.LineStyleList.keys()

        return None

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to demonstrate\n"
                                                  "the use of the FloatCanvas\n",
                                                  "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def ZoomToFit(self,event):
        self.Canvas.ZoomToBB()

    def Clear(self,event = None):
        self.Canvas.ClearAll()
        self.Canvas.Draw()

    def OnQuit(self,event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

    def DrawTest(self,event):
        wx.GetApp().Yield()
        import random
        import numpy.random as RandomArray
        Range = (-10,10)

        Canvas = self.Canvas
        Canvas.ClearAll()

        # Set some zoom limits:
        self.Canvas.MinScale = 15.0
        self.Canvas.MaxScale = 500.0

        #### Draw a few Random Objects ####

        # Rectangles
        for i in range(5):
            xy = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            lw = random.randint(1,5)
            cf = random.randint(0,len(self.colors)-1)
            h = random.randint(1,5)
            w = random.randint(1,5)
            Canvas.AddRectangle(xy, (h,w),
                                LineWidth = lw,
                                FillColor = self.colors[cf])

            # Ellipses
        for i in range(5):
            xy = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            lw = random.randint(1,5)
            cf = random.randint(0,len(self.colors)-1)
            h = random.randint(1,5)
            w = random.randint(1,5)
            Canvas.AddEllipse(xy, (h,w),
                              LineWidth = lw,
                              FillColor = self.colors[cf])

        # Circles
        for i in range(5):
            point = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            D = random.randint(1,5)
            lw = random.randint(1,5)
            cf = random.randint(0,len(self.colors)-1)
            cl = random.randint(0,len(self.colors)-1)
            Canvas.AddCircle(point, D,
                             LineWidth = lw,
                             LineColor = self.colors[cl],
                             FillColor = self.colors[cf])
            Canvas.AddText("Circle # %i"%(i),
                           point,
                           Size = 12,
                           Position = "cc")

            # Lines
        for i in range(5):
            points = []
            for j in range(random.randint(2,10)):
                point = (random.randint(Range[0],Range[1]),random.randint(Range[0],Range[1]))
                points.append(point)
            lw = random.randint(1,10)
            cf = random.randint(0,len(self.colors)-1)
            cl = random.randint(0,len(self.colors)-1)
            Canvas.AddLine(points, LineWidth = lw, LineColor = self.colors[cl])

            # Polygons
        for i in range(3):
            points = []
            for j in range(random.randint(2,6)):
                point = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
                points.append(point)
            lw = random.randint(1,6)
            cf = random.randint(0,len(self.colors)-1)
            cl = random.randint(0,len(self.colors)-1)
            Canvas.AddPolygon(points,
                              LineWidth = lw,
                              LineColor = self.colors[cl],
                              FillColor = self.colors[cf],
                              FillStyle = 'Solid')

        self.Canvas.ZoomToBB()

    def MoveTest(self,event=None):
        print("Running: TestHitTestForeground")
        wx.GetApp().Yield()

        self.UnBindAllMouseEvents()
        Canvas = self.Canvas

        Canvas.ClearAll()
        # Clear the  zoom limits:
        self.Canvas.MinScale = None
        self.Canvas.MaxScale = None

        Canvas.SetProjectionFun(None)

        #Add a Hitable rectangle
        w,h = 60, 20

        dx = 80
        dy = 40
        x,y = 20, 20

        color = "Red"
        R = Canvas.AddRectangle((x,y), (w,h),
                                LineWidth = 2,
                                FillColor = color
                                )

        R.Name = color + "Rectangle"
        Canvas.AddText(R.Name, (x, y+h), Position = "tl")

        ## A set of Rectangles that move together

        ## NOTE: In a real app, it might be better to create a new
        ## custom FloatCanvas DrawObject

        self.MovingRects = []
        x += dx
        color = "LightBlue"
        R = Canvas.AddRectangle((x,y), (w/2, h/2),
                                LineWidth = 2,
                                FillColor = color)

        R.HitFill = True
        R.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.RectMoveLeft)
        L = Canvas.AddText("Left", (x + w/4, y + h/4),
                           Position = "cc")
        self.MovingRects.extend( (R,L) )

        x += w/2
        R = Canvas.AddRectangle((x, y), (w/2, h/2),
                                LineWidth = 2,
                                FillColor = color)

        R.HitFill = True
        R.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.RectMoveRight)
        L = Canvas.AddText("Right", (x + w/4, y + h/4),
                           Position = "cc")
        self.MovingRects.extend( (R,L) )

        x -= w/2
        y += h/2
        R = Canvas.AddRectangle((x, y), (w/2, h/2),
                                LineWidth = 2,
                                FillColor = color)
        R.HitFill = True
        R.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.RectMoveUp)
        L = Canvas.AddText("Up", (x + w/4, y + h/4),
                           Position = "cc")
        self.MovingRects.extend( (R,L) )


        x += w/2
        R = Canvas.AddRectangle((x, y), (w/2, h/2),
                                LineWidth = 2,
                                FillColor = color)
        R.HitFill = True
        R.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.RectMoveDown)
        L = Canvas.AddText("Down", (x + w/4, y + h/4),
                           Position = "cc")
        self.MovingRects.extend( (R,L) )

        self.Canvas.ZoomToBB()

    def RectMoveLeft(self,Object):
        self.MoveRects("left")

    def RectMoveRight(self,Object):
        self.MoveRects("right")

    def RectMoveUp(self,Object):
        self.MoveRects("up")

    def RectMoveDown(self,Object):
        self.MoveRects("down")

    def MoveRects(self, Dir):
        for Object in self.MovingRects:
            X,Y = Object.XY
            if Dir == "left": X -= 10
            elif Dir == "right": X += 10
            elif Dir == "up": Y += 10
            elif Dir == "down": Y -= 10
            Object.SetPoint((X,Y))
        self.Canvas.Draw(True)

    def UnBindAllMouseEvents(self):
        ## Here is how you catch FloatCanvas mouse events
        self.Canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.dummyHandler)
        self.Canvas.Bind(FloatCanvas.EVT_LEFT_UP, self.dummyHandler)
        self.Canvas.Bind(FloatCanvas.EVT_LEFT_DCLICK, self.dummyHandler)

        self.Canvas.Bind(FloatCanvas.EVT_MIDDLE_DOWN, self.dummyHandler)
        self.Canvas.Bind(FloatCanvas.EVT_MIDDLE_UP, self.dummyHandler)
        self.Canvas.Bind(FloatCanvas.EVT_MIDDLE_DCLICK, self.dummyHandler)

        self.Canvas.Bind(FloatCanvas.EVT_RIGHT_DOWN, self.dummyHandler)
        self.Canvas.Bind(FloatCanvas.EVT_RIGHT_UP, self.dummyHandler)
        self.Canvas.Bind(FloatCanvas.EVT_RIGHT_DCLICK, self.dummyHandler)

        self.Canvas.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.dummyHandler)

        self.EventsAreBound = False

    def dummyHandler(self, evt):
        evt.Skip()

class DemoApp(wx.App):
    """
    How the demo works:

    Under the Draw menu, there are three options:

    *Draw Test: will put up a picture of a bunch of randomly generated
    objects, of each kind supported.

    *Draw Map: will draw a map of the world. Be patient, it is a big map,
    with a lot of data, and will take a while to load and draw (about 10 sec
    on my 450Mhz PIII). Redraws take about 2 sec. This demonstrates how the
    performance is not very good for large drawings.

    *Clear: Clears the Canvas.

    Once you have a picture drawn, you can zoom in and out and move about
    the picture. There is a tool bar with three tools that can be
    selected.

    The magnifying glass with the plus is the zoom in tool. Once selected,
    if you click the image, it will zoom in, centered on where you
    clicked. If you click and drag the mouse, you will get a rubber band
    box, and the image will zoom to fit that box when you release it.

    The magnifying glass with the minus is the zoom out tool. Once selected,
    if you click the image, it will zoom out, centered on where you
    clicked. (note that this takes a while when you are looking at the map,
    as it has a LOT of lines to be drawn. The image is double buffered, so
    you don't see the drawing in progress)

    The hand is the move tool. Once selected, if you click and drag on the
    image, it will move so that the part you clicked on ends up where you
    release the mouse. Nothing is changed while you are dragging. The
    drawing is too slow for that.

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
                          title = "FloatCanvas Demo App",
                          size = (700,700) )

        self.SetTopWindow(frame)

        return True

app =  DemoApp(False)
app.MainLoop()













