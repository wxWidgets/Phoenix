#!/usr/bin/env python

"""
A test of some simple animation

this is very old-style code: don't imitate it!

"""

from time import clock
import wx
print(wx.VERSION_STRING)
from numpy import *

## import local version:
import sys

#ver = 'local'
ver = 'installed'

if ver == 'installed': ## import the installed version
    from wx.lib.floatcanvas import NavCanvas
    from wx.lib.floatcanvas import FloatCanvas
    print("using installed version: %s" % wx.lib.floatcanvas.__version__)
elif ver == 'local':
    ## import a local version
    import sys
    sys.path.append("..")
    from floatcanvas import NavCanvas
    from floatcanvas import FloatCanvas

ID_DRAW_BUTTON = 100
ID_QUIT_BUTTON = 101
ID_CLEAR_BUTTON = 103
ID_ZOOM_IN_BUTTON = 104
ID_ZOOM_OUT_BUTTON = 105
ID_ZOOM_TO_FIT_BUTTON = 110
ID_MOVE_MODE_BUTTON = 111
ID_TEST_BUTTON = 112

ID_TEST = 500


class DrawFrame(wx.Frame):
    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        ## Set up the MenuBar

        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        exit = file_menu.Append(wx.ID_EXIT, "", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnQuit, exit)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()
        draw = draw_menu.Append(wx.ID_ANY,
                                "&Draw Test",
                                "Run a test of drawing random components")
        self.Bind(wx.EVT_MENU, self.DrawTest, draw)
        amap = draw_menu.Append(wx.ID_ANY,
                               "Draw &Movie","Run a test of drawing a map")
        self.Bind(wx.EVT_MENU, self.RunMovie, amap)
        clear = draw_menu.Append(wx.ID_ANY, "&Clear","Clear the Canvas")
        self.Bind(wx.EVT_MENU, self.Clear, clear)
        MenuBar.Append(draw_menu, "&Draw")


        view_menu = wx.Menu()
        zoom = view_menu.Append(wx.ID_ANY, "Zoom to &Fit","Zoom to fit the window")
        self.Bind(wx.EVT_MENU, self.ZoomToFit, zoom)
        MenuBar.Append(view_menu, "&View")

        help_menu = wx.Menu()
        about = help_menu.Append(wx.ID_ABOUT, "",
                                 "More information About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, about)
        MenuBar.Append(help_menu, "&Help")

        self.SetMenuBar(MenuBar)

        self.CreateStatusBar()
        self.SetStatusText("")

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Other event handlers:
        self.Bind(wx.EVT_RIGHT_DOWN, self.RightButtonEvent)

        # Add the Canvas
        self.Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                  Debug = False,
                                  BackgroundColor = "WHITE").Canvas
        self.Canvas.NumBetweenBlits = 1000
        self.Show(True)

        self.DrawTest(None)
        return None

    def RightButtonEvent(self,event):
        print("Right Button has been clicked in DrawFrame")
        print("coords are: %i, %i"%(event.GetX(),event.GetY()))
        event.Skip()

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

    def DrawTest(self,event = None):
        import random
        import numpy.random as RandomArray

        Range = (-10,10)

        colors = ["AQUAMARINE", "BLACK", "BLUE", "BLUE VIOLET", "BROWN",
                  "CADET BLUE", "CORAL", "CORNFLOWER BLUE", "CYAN", "DARK GREY",
                  "DARK GREEN", "DARK OLIVE GREEN", "DARK ORCHID", "DARK SLATE BLUE",
                  "DARK SLATE GREY", "DARK TURQUOISE", "DIM GREY",
                  "FIREBRICK", "FOREST GREEN", "GOLD", "GOLDENROD", "GREY",
                  "GREEN", "GREEN YELLOW", "INDIAN RED", "KHAKI", "LIGHT BLUE",
                  "LIGHT GREY", "LIGHT STEEL BLUE", "LIME GREEN", "MAGENTA",
                  "MAROON", "MEDIUM AQUAMARINE", "MEDIUM BLUE", "MEDIUM FOREST GREEN",
                  "MEDIUM GOLDENROD", "MEDIUM ORCHID", "MEDIUM SEA GREEN",
                  "MEDIUM SLATE BLUE", "MEDIUM SPRING GREEN", "MEDIUM TURQUOISE",
                  "MEDIUM VIOLET RED", "MIDNIGHT BLUE", "NAVY", "ORANGE", "ORANGE RED",
                  "ORCHID", "PALE GREEN", "PINK", "PLUM", "PURPLE", "RED",
                  "SALMON", "SEA GREEN", "SIENNA", "SKY BLUE", "SLATE BLUE",
                  "SPRING GREEN", "STEEL BLUE", "TAN", "THISTLE", "TURQUOISE",
                  "VIOLET", "VIOLET RED", "WHEAT", "WHITE", "YELLOW", "YELLOW GREEN"]
        Canvas = self.Canvas

        # Some Polygons in the background:
#        for i in range(500):
#            points = RandomArray.uniform(-100,100,(10,2))
        for i in range(500):
#        for i in range(1):
            points = RandomArray.uniform(-100,100,(10,2))
            lw = random.randint(1,6)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            self.Canvas.AddPolygon(points,
                                   LineWidth = lw,
                                   LineColor = colors[cl],
                                   FillColor = colors[cf],
                                   FillStyle = 'Solid',
                                   InForeground = False)

        ## Pointset
        print("Adding Points to Foreground" )
        for i in range(1):
            points = RandomArray.uniform(-100,100,(1000,2))
            D = 2
            self.LEs = self.Canvas.AddPointSet(points, Color = "Black", Diameter = D, InForeground = True)

        self.Canvas.AddRectangle((-200,-200), (400,400))
        Canvas.ZoomToBB()

    def RunMovie(self,event = None):
        import numpy.random as RandomArray
        start = clock()
        #shift = RandomArray.randint(0,0,(2,))
        for i in range(100):
            points = self.LEs.Points
            shift = RandomArray.randint(-5,6,(2,))
            points += shift
            self.LEs.SetPoints(points)
            self.Canvas.Draw()
            wx.GetApp().Yield(True)
        print("running the movie took %f seconds"%(clock() - start))

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
    pointer. Pleae let me know if you have any nice cursor images for me to
    use.


    Any bugs, comments, feedback, questions, and especially code are welcome:

    -Chris Barker

    ChrisHBarker@home.net
    http://members.home.net/barkerlohmann

    """

    def OnInit(self):
        frame = DrawFrame(None, -1, "Simple Drawing Window",wx.DefaultPosition, (700,700) )

        self.SetTopWindow(frame)

        return True

def Read_MapGen(filename,stats = False):
    """
    This function reads a MapGen Format file, and
    returns a list of NumPy arrays with the line segments in them.

    Each NumPy array in the list is an NX2 array of Python Floats.

    The demo should have come with a file, "world.dat" that is the
    shorelines of the whole worls, in MapGen format.

    """
    from numpy import array
    file = open(filename,'rt')
    data = file.readlines()
    data = [s.strip() for s in data]

    Shorelines = []
    segment = []
    for line in data:
        if line == "# -b": #New segment begining
            if segment: Shorelines.append(array(segment))
            segment = []
        else:
            segment.append(map(float,string.split(line)))
    if segment: Shorelines.append(array(segment))

    if stats:
        NumSegments = len(Shorelines)
        NumPoints = False
        for segment in Shorelines:
            NumPoints = NumPoints + len(segment)
        AvgPoints = NumPoints / NumSegments
        print("Number of Segments: ", NumSegments)
        print("Average Number of Points per segment: ",AvgPoints)

    return Shorelines

if __name__ == "__main__":

    app = DemoApp(0)
    app.MainLoop()










