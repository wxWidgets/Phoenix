#----------------------------------------------------------------------------
# Name:         FloatCanvas.py
# Purpose:
#
# Author:
#
# Created:
# Version:
# Date:
# Licence:
# Tags:         phoenix-port, unittest, documented, py3-port
#----------------------------------------------------------------------------
"""
This is the main module of the floatcanvas package, it contains the :class:`~lib.floatcanvas.FloatCanvas.FloatCanvas`
and all the all the different objects which are sub-classed from :class:`~lib.floatcanvas.FloatCanvas.DrawObject`.

In the following very simple sample ``self`` is a frame, but it could be another
container type control::

    from wx.lib.floatcanvas import FloatCanvas

    self.Canvas = FloatCanvas.FloatCanvas(self, -1,
                                 size=(500, 500),
                                 ProjectionFun=None,
                                 Debug=0,
                                 BackgroundColor="White",
                                 )


    # add a circle
    cir = FloatCanvas.Circle((10, 10), 100)
    self.Canvas.AddObject(cir)

    # add a rectangle
    rect = FloatCanvas.Rectangle((110, 10), (100, 100), FillColor='Red')
    self.Canvas.AddObject(rect)

    self.Canvas.Draw()


Many samples are available in the `wxPhoenix/samples/floatcanvas` folder.

"""

from __future__ import division

import sys
mac = sys.platform.startswith("darwin")

import numpy as N
try:
    from time import process_time as clock
except ImportError:
    from time import clock
import wx
import six

from .FCObjects import *

from .Utilities import BBox
from . import GUIMode


## Custom Exceptions:

class FloatCanvasError(Exception):
    """Custom FloatCanvas exception."""
    pass

## Import all EVT_* event types and event binders
from .FCEvents import *


class _MouseEvent(wx.PyCommandEvent):

    """
    This event class takes a regular wxWindows mouse event as a parameter,
    and wraps it so that there is access to all the original methods. This
    is similar to subclassing, but you can't subclass a wxWindows event

    The goal is to be able to it just like a regular mouse event.

    It adds the method:

    GetCoords() , which returns an (x,y) tuple in world coordinates.

    Another difference is that it is a CommandEvent, which propagates up
    the window hierarchy until it is handled.

    """

    def __init__(self, EventType, NativeEvent, WinID, Coords = None):
        super(_MouseEvent, self).__init__()

        self.SetEventType( EventType )
        self._NativeEvent = NativeEvent
        self.Coords = Coords

    def GetCoords(self):
        return self.Coords

    def __getattr__(self, name):
        d = self._getAttrDict()
        if name in d:
            return d[name]
        return getattr(self._NativeEvent, name)


#---------------------------------------------------------------------------
class FloatCanvas(wx.Panel):
    """
    The main class of the floatcanvas package :class:`~lib.floatcanvas.FloatCanvas`.

    """

    def __init__(self, parent, id = -1,
                 size = wx.DefaultSize,
                 ProjectionFun = None,
                 BackgroundColor = "WHITE",
                 Debug = False,
                 **kwargs):

        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param `size`: a tuple or :class:`wx.Size`
        :param `ProjectionFun`: This allows you to change the transform from
         world to pixel coordinates. We can point to :meth:`~lib.floatcanvas.FloatCanvas.FloatCanvas.FlatEarthProjection`
         for an example -- though that should really be a class method, or even
         better, simply a function in the module. There is a tiny bit on info
         in the error message in FloatCanvas.SetProjectionFun()

         (Note: this really should get re-factored to allow more generic
         projections...)
        :param string `BackgroundColor`: any value accepted by :class:`wx.Brush`
        :param `Debug`: activate debug, currently it prints some debugging
         information, could be improved.

        """

        wx.Panel.__init__( self, parent, id, wx.DefaultPosition, size, **kwargs)

        ComputeFontScale()
        self.InitAll()

        self.BackgroundBrush = wx.Brush(BackgroundColor, wx.SOLID)

        self.Debug = Debug

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_LEFT_DOWN, self.LeftDownEvent)
        self.Bind(wx.EVT_LEFT_UP, self.LeftUpEvent)
        self.Bind(wx.EVT_LEFT_DCLICK, self.LeftDoubleClickEvent)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.MiddleDownEvent)
        self.Bind(wx.EVT_MIDDLE_UP, self.MiddleUpEvent)
        self.Bind(wx.EVT_MIDDLE_DCLICK, self.MiddleDoubleClickEvent)
        self.Bind(wx.EVT_RIGHT_DOWN, self.RightDownEvent)
        self.Bind(wx.EVT_RIGHT_UP, self.RightUpEvent)
        self.Bind(wx.EVT_RIGHT_DCLICK, self.RightDoubleCLickEvent)
        self.Bind(wx.EVT_MOTION, self.MotionEvent)
        self.Bind(wx.EVT_MOUSEWHEEL, self.WheelEvent)
        self.Bind(wx.EVT_KEY_DOWN, self.KeyDownEvent)
        self.Bind(wx.EVT_KEY_UP, self.KeyUpEvent)


        ## CHB: I'm leaving these out for now.
        #self.Bind(wx.EVT_ENTER_WINDOW, self. )
        #self.Bind(wx.EVT_LEAVE_WINDOW, self. )

        self.SetProjectionFun(ProjectionFun)

        self.GUIMode = None # making sure the arrribute exists
        self.SetMode(GUIMode.GUIMouse()) # make the default Mouse Mode.

        # timer to give a delay when re-sizing so that buffers aren't re-built too many times.
        self.SizeTimer = wx.PyTimer(self.OnSizeTimer)

#        self.InitializePanel()
#        self.MakeNewBuffers()

#        self.CreateCursors()


    def InitAll(self):
        """
        Sets everything in the Canvas to default state.

        It can be used to reset the Canvas

        """

        self.HitColorGenerator = None
        self.UseHitTest = False

        self.NumBetweenBlits = 500

        ## create the Hit Test Dicts:
        self.HitDict = None
        self._HTdc = None

        self._DrawList = []
        self._ForeDrawList = []
        self.InitializePanel()
        self.MakeNewBuffers()
        self.BoundingBox = BBox.NullBBox()
        self.BoundingBoxDirty = False
        self.MinScale = None
        self.MaxScale = None
        self.ViewPortCenter= N.array( (0,0), N.float)

        self.SetProjectionFun(None)

        self.MapProjectionVector = N.array( (1,1), N.float) # No Projection to start!
        self.TransformVector = N.array( (1,-1), N.float) # default Transformation

        self.Scale = 1
        self.ObjectUnderMouse = None

        self.GridUnder = None
        self.GridOver = None

        self._BackgroundDirty = True

    def SetProjectionFun(self, ProjectionFun):
        """
        Set a custom projection function

        :param `ProjectionFun`: valid entries are ``FlatEarth``, ``None``
          or a callable object that takes the ``ViewPortCenter`` and returns
          ``MapProjectionVector``

        """
        if ProjectionFun == 'FlatEarth':
            self.ProjectionFun = self.FlatEarthProjection
        elif callable(ProjectionFun):
            self.ProjectionFun = ProjectionFun
        elif ProjectionFun is None:
            self.ProjectionFun = lambda x=None: N.array( (1,1), N.float)
        else:
            raise FloatCanvasError('Projectionfun must be either:'
                                   ' "FlatEarth", None, or a callable object '
                                   '(function, for instance) that takes the '
                                   'ViewPortCenter and returns a MapProjectionVector')

    def FlatEarthProjection(self, CenterPoint):
        """
        Compute the scaling array for the flat-earth projection

        :param `CenterPoint`: center point of viewport (lon, lat) -- the
         longitude is scaled to the latitude of this point. a 2-tuple, or a
         (2,) `NumPy <http://www.numpy.org/>`_ array of point coordinates

         :returns : a (2,) numpy array that scales world coordinates. This
          scaling is applied when converting to-from world to pixel coordinates.

        """
        MaxLatitude = 75 # these were determined essentially arbitrarily
        MinLatitude = -75
        Lat = min(CenterPoint[1],MaxLatitude)
        Lat = max(Lat,MinLatitude)
        return N.array((N.cos(N.pi*Lat/180),1),N.float)

    def SetMode(self, Mode):
        """
        Set the GUImode to any of the available mode.

        :param `Mode`: a valid GUI Mode, out of the box valid modes
         are subclassed from :class:`~lib.floatcanvas.GUIMode.GUIBase` or a mode
         can also be user defined.
        """
        # Set mode
        if self.GUIMode is not None:
            self.GUIMode.UnSet() # this lets the old mode clean up.
        Mode.Canvas = self # make sure the mode is linked to this canvas
        self.GUIMode = Mode
        self.SetCursor(self.GUIMode.Cursor)

    def MakeHitDict(self):
        """Initialize the Hit dictonary."""
        ##fixme: Should this just be None if nothing has been bound?
        self.HitDict = {EVT_FC_LEFT_DOWN: {},
                        EVT_FC_LEFT_UP: {},
                        EVT_FC_LEFT_DCLICK: {},
                        EVT_FC_MIDDLE_DOWN: {},
                        EVT_FC_MIDDLE_UP: {},
                        EVT_FC_MIDDLE_DCLICK: {},
                        EVT_FC_RIGHT_DOWN: {},
                        EVT_FC_RIGHT_UP: {},
                        EVT_FC_RIGHT_DCLICK: {},
                        EVT_FC_ENTER_OBJECT: {},
                        EVT_FC_LEAVE_OBJECT: {},
                        }

    def _RaiseMouseEvent(self, Event, EventType):
        """
        This is called in various other places to raise a Mouse Event.
        """
        pt = self.PixelToWorld( Event.GetPosition() )
        evt = _MouseEvent(EventType, Event, self.GetId(), pt)
        self.GetEventHandler().ProcessEvent(evt)

    if wx.__version__ >= "2.8":
        HitTestBitmapDepth = 32
        #print("Using hit test code for 2.8")
        def GetHitTestColor(self, xy):
            """
            Get the hit test colour

            :param `xy`: the position to get the hit test colour for
            """
            if self._ForegroundHTBitmap:
                pdata = wx.AlphaPixelData(self._ForegroundHTBitmap)
            else:
                pdata = wx.AlphaPixelData(self._HTBitmap)
            if not pdata:
                raise RuntimeError("Trouble Accessing Hit Test bitmap")
            pacc = pdata.GetPixels()
            pacc.MoveTo(pdata, xy[0], xy[1])
            return pacc.Get()[:3]
    else:
        HitTestBitmapDepth = 24
        #print("using pre-2.8 hit test code")
        def GetHitTestColor(self,  xy ):
            """
            Get the hit test colour

            :param `xy`: the position to get the hit test colour for
            """
            dc = wx.MemoryDC()
            if self._ForegroundHTBitmap:
                dc.SelectObject(self._ForegroundHTBitmap)
            else:
                dc.SelectObject(self._HTBitmap)
            hitcolor = dc.GetPixel( xy )
            return hitcolor.Get()

    def UnBindAll(self):
        """Removes all bindings to Objects."""
        self.HitDict = None

    def _CallHitCallback(self, Object, xy, HitEvent):
        """
        A little book keeping to be done when a callback is called.
        """
        Object.HitCoords = self.PixelToWorld( xy )
        Object.HitCoordsPixel = xy
        Object.CallBackFuncs[HitEvent](Object)

    def HitTest(self, event, HitEvent):
        """Check if any objects in the dict for this event."""
        if self.HitDict:
            if HitEvent in self.HitDict:
                xy = event.GetPosition()
                color = self.GetHitTestColor( xy )
                if color in self.HitDict[ HitEvent ]:
                    Object = self.HitDict[ HitEvent ][color]
                    self._CallHitCallback(Object, xy, HitEvent)
                    return True
            return False


    def MouseOverTest(self, event):
        """Check if mouse is over an object."""
        ##fixme: Can this be cleaned up?
        if (self.HitDict and
            (self.HitDict[EVT_FC_ENTER_OBJECT ] or
             self.HitDict[EVT_FC_LEAVE_OBJECT ]    )
            ):
            xy = event.GetPosition()
            color = self.GetHitTestColor( xy )
            OldObject = self.ObjectUnderMouse
            ObjectCallbackCalled = False
            if color in self.HitDict[ EVT_FC_ENTER_OBJECT ]:
                Object = self.HitDict[ EVT_FC_ENTER_OBJECT][color]
                if (OldObject is None):
                    try:
                        self._CallHitCallback(Object, xy, EVT_FC_ENTER_OBJECT)
                        ObjectCallbackCalled =  True
                    except KeyError:
                        pass # this means the enter event isn't bound for that object
                elif OldObject == Object: # the mouse is still on the same object
                    pass
                    ## Is the mouse on a different object as it was...
                elif not (Object == OldObject):
                    # call the leave object callback
                    try:
                        self._CallHitCallback(OldObject, xy, EVT_FC_LEAVE_OBJECT)
                        ObjectCallbackCalled =  True
                    except KeyError:
                        pass # this means the leave event isn't bound for that object
                    try:
                        self._CallHitCallback(Object, xy, EVT_FC_ENTER_OBJECT)
                        ObjectCallbackCalled =  True
                    except KeyError:
                        pass # this means the enter event isn't bound for that object
                    ## set the new object under mouse
                self.ObjectUnderMouse = Object
            elif color in self.HitDict[ EVT_FC_LEAVE_OBJECT ]:
                Object = self.HitDict[ EVT_FC_LEAVE_OBJECT][color]
                self.ObjectUnderMouse = Object
            else:
                # no objects under mouse bound to mouse-over events
                self.ObjectUnderMouse = None
                if OldObject:
                    try:
                        ## Add the hit coords to the Object
                        self._CallHitCallback(OldObject, xy, EVT_FC_LEAVE_OBJECT)
                        ObjectCallbackCalled =  True
                    except KeyError:
                        pass # this means the leave event isn't bound for that object
            return ObjectCallbackCalled
        return False

    ## fixme: There is a lot of repeated code here
    ##        Is there a better way?
    ##    probably -- shouldn't there always be a GUIMode?
    ##    there could be a null GUI Mode, and use that instead of None
    def LeftDoubleClickEvent(self, event):
        """Left double click event."""
        if self.GUIMode:
            self.GUIMode.OnLeftDouble(event)
        event.Skip()

    def MiddleDownEvent(self, event):
        """Middle down event."""
        if self.GUIMode:
            self.GUIMode.OnMiddleDown(event)
        event.Skip()

    def MiddleUpEvent(self, event):
        """Middle up event."""
        if self.GUIMode:
            self.GUIMode.OnMiddleUp(event)
        event.Skip()

    def MiddleDoubleClickEvent(self, event):
        """Middle double click event."""
        if self.GUIMode:
            self.GUIMode.OnMiddleDouble(event)
        event.Skip()

    def RightDoubleCLickEvent(self, event):
        """Right double click event."""
        if self.GUIMode:
            self.GUIMode.OnRightDouble(event)
        event.Skip()

    def WheelEvent(self, event):
        """Wheel event."""
        if self.GUIMode:
            self.GUIMode.OnWheel(event)
        event.Skip()

    def LeftDownEvent(self, event):
        """Left down event."""
        if self.GUIMode:
            self.GUIMode.OnLeftDown(event)
        event.Skip()

    def LeftUpEvent(self, event):
        """Left up event."""
        if self.HasCapture():
            self.ReleaseMouse()
        if self.GUIMode:
            self.GUIMode.OnLeftUp(event)
        event.Skip()

    def MotionEvent(self, event):
        """Motion event."""
        if self.GUIMode:
            self.GUIMode.OnMove(event)
        event.Skip()

    def RightDownEvent(self, event):
        """Right down event."""
        if self.GUIMode:
            self.GUIMode.OnRightDown(event)
        event.Skip()

    def RightUpEvent(self, event):
        """Right up event."""
        if self.GUIMode:
            self.GUIMode.OnRightUp(event)
        event.Skip()

    def KeyDownEvent(self, event):
        """Key down event."""
        if self.GUIMode:
            self.GUIMode.OnKeyDown(event)
        event.Skip()

    def KeyUpEvent(self, event):
        """Key up event."""
        if self.GUIMode:
            self.GUIMode.OnKeyUp(event)
        event.Skip()

    def MakeNewBuffers(self):
        """Make a new buffer."""
        ##fixme: this looks like tortured logic!
        self._BackgroundDirty = True
        # Make new offscreen bitmap:
        self._Buffer = wx.Bitmap(*self.PanelSize)
        if self._ForeDrawList:
            self._ForegroundBuffer = wx.Bitmap(*self.PanelSize)
            if self.UseHitTest:
                self.MakeNewForegroundHTBitmap()
            else:
                self._ForegroundHTBitmap = None
        else:
            self._ForegroundBuffer = None
            self._ForegroundHTBitmap = None

        if self.UseHitTest:
            self.MakeNewHTBitmap()
        else:
            self._HTBitmap = None
            self._ForegroundHTBitmap = None

    def MakeNewHTBitmap(self):
        """
        Off screen Bitmap used for Hit tests on background objects

        """
        self._HTBitmap = wx.Bitmap(self.PanelSize[0],
                                        self.PanelSize[1],
                                        depth=self.HitTestBitmapDepth)

    def MakeNewForegroundHTBitmap(self):
        ## Note: the foreground and backround HT bitmaps are in separate functions
        ##       so that they can be created separate --i.e. when a foreground is
        ##       added after the backgound is drawn
        """
        Off screen Bitmap used for Hit tests on foreground objects

        """
        self._ForegroundHTBitmap = wx.Bitmap(self.PanelSize[0],
                                                  self.PanelSize[1],
                                                  depth=self.HitTestBitmapDepth)

    def OnSize(self, event=None):
        """On size handler."""
        self.InitializePanel()
        self.SizeTimer.Start(50, oneShot=True)

    def OnSizeTimer(self, event=None):
        """On size timer handler."""
        self.MakeNewBuffers()
        self.Draw()

    def InitializePanel(self):
        """Intialize the panel."""
        PanelSize  = N.array(self.GetClientSize(),  N.int32)
        self.PanelSize  = N.maximum(PanelSize, (2,2)) ## OS-X sometimes gives a Size event when the panel is size (0,0)
        self.HalfPanelSize = self.PanelSize / 2 # lrk: added for speed in WorldToPixel
        self.AspectRatio = float(self.PanelSize[0]) / self.PanelSize[1]

    def OnPaint(self, event):
        """On paint handler."""
        dc = wx.PaintDC(self)
        if self._ForegroundBuffer:
            dc.DrawBitmap(self._ForegroundBuffer,0,0)
        else:
            dc.DrawBitmap(self._Buffer,0,0)
        ## this was so that rubber band boxes and the like could get drawn here
        ##  but it looks like a wx.ClientDC is a better bet still.
        #try:
        #    self.GUIMode.DrawOnTop(dc)
        #except AttributeError:
        #    pass

    def Draw(self, Force=False):
        """

        Canvas.Draw(Force=False)

        Re-draws the canvas.

        Note that the buffer will not be re-drawn unless something has
        changed. If you change a DrawObject directly, then the canvas
        will not know anything has changed. In this case, you can force
        a re-draw by passing int True for the Force flag:

        Canvas.Draw(Force=True)

        There is a main buffer set up to double buffer the screen, so
        you can get quick re-draws when the window gets uncovered.

        If there are any objects in self._ForeDrawList, then the
        background gets drawn to a new buffer, and the foreground
        objects get drawn on top of it. The final result if blitted to
        the screen, and stored for future Paint events.  This is done so
        that you can have a complicated background, but have something
        changing on the foreground, without having to wait for the
        background to get re-drawn. This can be used to support simple
        animation, for instance.

        """

        if N.sometrue(self.PanelSize <= 2 ):
            # it's possible for this to get called before being properly initialized.
            return
        if self.Debug: start = clock()
        ScreenDC =  wx.ClientDC(self)
        ViewPortWorld = N.array(( self.PixelToWorld((0,0)),
                                  self.PixelToWorld(self.PanelSize) )
                                     )
        self.ViewPortBB = N.array( ( N.minimum.reduce(ViewPortWorld),
                              N.maximum.reduce(ViewPortWorld) ) )

        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        if self._BackgroundDirty or Force:
            dc.SetBackground(self.BackgroundBrush)
            dc.Clear()
            if self._HTBitmap is not None:
                HTdc = wx.MemoryDC()
                HTdc.SelectObject(self._HTBitmap)
                HTdc.Clear()
            else:
                HTdc = None
            if self.GridUnder is not None:
                self.GridUnder._Draw(dc, self)
            self._DrawObjects(dc, self._DrawList, ScreenDC, self.ViewPortBB, HTdc)
            self._BackgroundDirty = False
            del HTdc

        if self._ForeDrawList:
            ## If an object was just added to the Foreground, there might not yet be a buffer
            if self._ForegroundBuffer is None:
                self._ForegroundBuffer = wx.Bitmap(self.PanelSize[0],
                                                        self.PanelSize[1])

            dc = wx.MemoryDC() ## I got some strange errors (linewidths wrong) if I didn't make a new DC here
            dc.SelectObject(self._ForegroundBuffer)
            dc.DrawBitmap(self._Buffer,0,0)
            if self._ForegroundHTBitmap is not None:
                ForegroundHTdc = wx.MemoryDC()
                ForegroundHTdc.SelectObject( self._ForegroundHTBitmap)
                ForegroundHTdc.Clear()
                if self._HTBitmap is not None:
                    #Draw the background HT buffer to the foreground HT buffer
                    ForegroundHTdc.DrawBitmap(self._HTBitmap, 0, 0)
            else:
                ForegroundHTdc = None
            self._DrawObjects(dc,
                              self._ForeDrawList,
                              ScreenDC,
                              self.ViewPortBB,
                              ForegroundHTdc)
        if self.GridOver is not None:
            self.GridOver._Draw(dc, self)
        ScreenDC.Blit(0, 0, self.PanelSize[0],self.PanelSize[1], dc, 0, 0)
        # If the canvas is in the middle of a zoom or move,
        # the Rubber Band box needs to be re-drawn
        ##fixme: maybe GUIModes should never be None, and rather have a Do-nothing GUI-Mode.
        if self.GUIMode is not None:
            self.GUIMode.UpdateScreen()

        if self.Debug:
            print("Drawing took %f seconds of CPU time"%(clock()-start))
            if self._HTBitmap is not None:
                self._HTBitmap.SaveFile('junk.png', wx.BITMAP_TYPE_PNG)

        ## Clear the font cache. If you don't do this, the X font server
        ## starts to take up Massive amounts of memory This is mostly a
        ## problem with very large fonts, that you get with scaled text
        ## when zoomed in.
        DrawObject.FontList = {}

    def _ShouldRedraw(DrawList, ViewPortBB):
        # lrk: Returns the objects that should be redrawn
        ## fixme: should this check be moved into the object?
        BB2 = ViewPortBB
        redrawlist = []
        for Object in DrawList:
            if Object.BoundingBox.Overlaps(BB2):
                redrawlist.append(Object)
        return redrawlist
    _ShouldRedraw = staticmethod(_ShouldRedraw)

    def MoveImage(self, shift, CoordType, ReDraw=True):
        """
        Move the image in the window.

        :param tuple `shift`: is an (x, y) tuple defining amount to shift in
         each direction
        :param string `CoordType`: defines what coordinates to use, valid entries
         are:

         ============== ======================================================
         Coordtype      Description
         ============== ======================================================
         `Panel`        shift the image by some fraction of the size of the
                        displayed image
         `Pixel`        shift the image by some number of pixels
         `World`        shift the image by an amount of floating point world
                        coordinates
         ============== ======================================================

        """
        shift = N.asarray(shift,N.float)
        if CoordType == 'Panel':# convert from panel coordinates
            shift = shift * N.array((-1,1),N.float) *self.PanelSize/self.TransformVector
        elif CoordType == 'Pixel': # convert from pixel coordinates
            shift = shift/self.TransformVector
        elif CoordType == 'World': # No conversion
            pass
        else:
            raise FloatCanvasError('CoordType must be either "Panel", "Pixel", or "World"')

        self.ViewPortCenter = self.ViewPortCenter + shift
        self.MapProjectionVector = self.ProjectionFun(self.ViewPortCenter)
        self.TransformVector = N.array((self.Scale,-self.Scale),N.float) * self.MapProjectionVector
        self._BackgroundDirty = True
        if ReDraw:
            self.Draw()

    def Zoom(self, factor, center = None, centerCoords="World", keepPointInPlace=False):
        """
        Zoom(factor, center) changes the amount of zoom of the image by factor.
        If factor is greater than one, the image gets larger.
        If factor is less than one, the image gets smaller.
        :param factor: amount to zoom in or out If factor is greater than one,
                       the image gets larger. If factor is less than one, the
                       image gets smaller.
        :param center: a tuple of (x,y) coordinates of the center of the viewport,
                       after zooming. If center is not given, the center will stay the same.

        :param centerCoords: flag indicating whether the center given is in pixel or world
                             coords. Options are: "world" or "pixel"
        :param keepPointInPlace: boolean flag. If False, the center point is what's given.
                                 If True, the image is shifted so that the given center point
                                 is kept in the same pixel space. This facilitates keeping the
                                 same point under the mouse when zooming with the scroll wheel.
        """
        if center is None:
            center = self.ViewPortCenter
            centerCoords = 'World' #override input if they don't give a center point.

        if centerCoords == "Pixel":
            oldpoint = self.PixelToWorld( center )
        else:
            oldpoint = N.array(center, N.float)

        self.Scale = self.Scale*factor
        if keepPointInPlace:
            self.SetToNewScale(False)

            if centerCoords == "Pixel":
                newpoint = self.PixelToWorld( center )
            else:
                newpoint = N.array(center, N.float)
            delta = (newpoint - oldpoint)
            self.MoveImage(-delta, 'World')
        else:
            self.ViewPortCenter = oldpoint
            self.SetToNewScale()

    def ZoomToBB(self, NewBB=None, DrawFlag=True):

        """

        Zooms the image to the bounding box given, or to the bounding
        box of all the objects on the canvas, if none is given.

        """
        if NewBB is not None:
            BoundingBox = NewBB
        else:
            if self.BoundingBoxDirty:
                self._ResetBoundingBox()
            BoundingBox = self.BoundingBox
        if (BoundingBox is not None) and (not BoundingBox.IsNull()):
            self.ViewPortCenter = N.array(((BoundingBox[0,0]+BoundingBox[1,0])/2,
                                         (BoundingBox[0,1]+BoundingBox[1,1])/2 ),N.float_)
            self.MapProjectionVector = self.ProjectionFun(self.ViewPortCenter)
            # Compute the new Scale
            BoundingBox = BoundingBox*self.MapProjectionVector # this does need to make a copy!
            try:
                self.Scale = min(abs(self.PanelSize[0] / (BoundingBox[1,0]-BoundingBox[0,0])),
                                 abs(self.PanelSize[1] / (BoundingBox[1,1]-BoundingBox[0,1])) )*0.95
            except ZeroDivisionError: # this will happen if the BB has zero width or height
                try: #width == 0
                    self.Scale = (self.PanelSize[0]  / (BoundingBox[1,0]-BoundingBox[0,0]))*0.95
                except ZeroDivisionError:
                    try: # height == 0
                        self.Scale = (self.PanelSize[1]  / (BoundingBox[1,1]-BoundingBox[0,1]))*0.95
                    except ZeroDivisionError: #zero size! (must be a single point)
                        self.Scale = 1

            if DrawFlag:
                self._BackgroundDirty = True
        else:
            # Reset the shifting and scaling to defaults when there is no BB
            self.ViewPortCenter= N.array( (0,0), N.float)
            self.Scale= 1
        self.SetToNewScale(DrawFlag=DrawFlag)

    def SetToNewScale(self, DrawFlag=True):
        """
        Set to the new scale

        :param boolean `DrawFlag`: draw the canvas

        """
        Scale = self.Scale
        if self.MinScale is not None:
            Scale = max(Scale, self.MinScale)
        if self.MaxScale is not None:
            Scale = min(Scale, self.MaxScale)
        self.MapProjectionVector = self.ProjectionFun(self.ViewPortCenter)
        self.TransformVector = N.array((Scale,-Scale),N.float) * self.MapProjectionVector
        self.Scale = Scale
        self._BackgroundDirty = True
        if DrawFlag:
            self.Draw()

    def RemoveObjects(self, Objects):
        """"
        Remove objects from canvas

        :param list `Objects`: a list of :class:`DrawObjects` to remove

        """
        for Object in Objects:
            self.RemoveObject(Object, ResetBB=False)
        self.BoundingBoxDirty = True

    def RemoveObject(self, Object, ResetBB=True):
        """"
        Remove object from canvas

        :param DrawObject `Object`: a :class:`DrawObjects` to remove
        :param boolean `ResetBB`: reset the bounding box

        """
        ##fixme: Using the list.remove method is kind of slow
        if Object.InForeground:
            self._ForeDrawList.remove(Object)
            if not self._ForeDrawList:
                self._ForegroundBuffer = None
                self._ForegroundHTdc = None
        else:
            self._DrawList.remove(Object)
            self._BackgroundDirty = True
        if ResetBB:
            self.BoundingBoxDirty = True

    def ClearAll(self, ResetBB=True):
        """
        ClearAll(ResetBB=True)

        Removes all DrawObjects from the Canvas

        If ResetBB is set to False, the original bounding box will remain

        """
        self._DrawList = []
        self._ForeDrawList = []
        self._BackgroundDirty = True
        self.HitColorGenerator = None
        self.UseHitTest = False
        if ResetBB:
            self._ResetBoundingBox()
        self.MakeNewBuffers()
        self.HitDict = None

    def _ResetBoundingBox(self):
        SetToNull=False
        if self._DrawList or self._ForeDrawList:
            bblist = []
            for obj in self._DrawList + self._ForeDrawList:
                if not obj.BoundingBox.IsNull():
                    bblist.append(obj.BoundingBox)
            if bblist: # if there are only NullBBoxes in DrawLists
                self.BoundingBox = BBox.fromBBArray(bblist)
            else:
                SetToNull = True
            if self.BoundingBox.Width == 0 or self.BoundingBox.Height == 0:
                SetToNull=True
        else:
            SetToNull=True
        if SetToNull:
            self.BoundingBox = BBox.NullBBox()
            self.ViewPortCenter= N.array( (0,0), N.float)
            self.TransformVector = N.array( (1,-1), N.float)
            self.MapProjectionVector = N.array( (1,1), N.float)
            self.Scale = 1
        self.BoundingBoxDirty = False

    def PixelToWorld(self, Points):
        """
        Converts coordinates from Pixel coordinates to world coordinates.

        Points is a tuple of (x,y) coordinates, or a list of such tuples,
        or a NX2 Numpy array of x,y coordinates.

        """
        return  (((N.asarray(Points, N.float) -
                   (self.PanelSize/2))/self.TransformVector) +
                 self.ViewPortCenter)

    def WorldToPixel(self,Coordinates):
        """
        This function will get passed to the drawing functions of the objects,
        to transform from world to pixel coordinates.
        Coordinates should be a NX2 array of (x,y) coordinates, or
        a 2-tuple, or sequence of 2-tuples.
        """
        #Note: this can be called by users code for various reasons, so N.asarray is needed.
        return  (((N.asarray(Coordinates,N.float) -
                   self.ViewPortCenter)*self.TransformVector)+
                 (self.HalfPanelSize)).astype('i')

    def ScaleWorldToPixel(self,Lengths):
        """
        This function will get passed to the drawing functions of the objects,
        to Change a length from world to pixel coordinates.

        Lengths should be a NX2 array of (x,y) coordinates, or
        a 2-tuple, or sequence of 2-tuples.
        """
        return  ( (N.asarray(Lengths, N.float)*self.TransformVector) ).astype('i')

    def ScalePixelToWorld(self,Lengths):
        """
        This function computes a pair of x.y lengths,
        to change then from pixel to world coordinates.

        Lengths should be a NX2 array of (x,y) coordinates, or
        a 2-tuple, or sequence of 2-tuples.
        """
        return  (N.asarray(Lengths,N.float) / self.TransformVector)

    def AddObject(self, obj):
        """
        Add an object to the canvas

        :param DrawObject `obj`: the object to add

        :return: DrawObject

        """
        # put in a reference to the Canvas, so remove and other stuff can work
        obj._Canvas = self
        if  obj.InForeground:
            self._ForeDrawList.append(obj)
            self.UseForeground = True
        else:
            self._DrawList.append(obj)
            self._BackgroundDirty = True
        self.BoundingBoxDirty = True
        return obj

    def AddObjects(self, Objects):
        """
        Add objects to the canvas

        :param list `Objects`: a list of :class:`DrawObject`

        """
        for Object in Objects:
            self.AddObject(Object)

    def _DrawObjects(self, dc, DrawList, ScreenDC, ViewPortBB, HTdc=None):
        """
        This is a convenience function;

        This function takes the list of objects and draws them to specified
        device context.
        """
        dc.SetBackground(self.BackgroundBrush)
        #i = 0
        PanelSize0, PanelSize1 = self.PanelSize # for speed
        WorldToPixel = self.WorldToPixel # for speed
        ScaleWorldToPixel = self.ScaleWorldToPixel # for speed
        Blit = ScreenDC.Blit # for speed
        NumBetweenBlits = self.NumBetweenBlits # for speed
        for i, Object in enumerate(self._ShouldRedraw(DrawList, ViewPortBB)):
            if Object.Visible:
                Object._Draw(dc, WorldToPixel, ScaleWorldToPixel, HTdc)
                if (i+1) % NumBetweenBlits == 0:
                    Blit(0, 0, PanelSize0, PanelSize1, dc, 0, 0)

    def SaveAsImage(self, filename, ImageType=wx.BITMAP_TYPE_PNG):
        """
        Saves the current image as an image file.

        :param string `filename`: the name of the image file
        :param `ImageType`: format to use, see :ref:`wx.BitmapType` and the note in
         :meth:`wx.Bitmap.SaveFile`

        """

        self._Buffer.SaveFile(filename, ImageType)


def _makeFloatCanvasAddMethods(): ## lrk's code for doing this in module __init__
    classnames = ["Circle", "Ellipse", "Arc", "Rectangle", "ScaledText", "Polygon",
                  "Line", "Text", "PointSet","Point", "Arrow", "ArrowLine", "ScaledTextBox",
                  "SquarePoint","Bitmap", "ScaledBitmap", "Spline", "Group"]
    for classname in classnames:
        klass = globals()[classname]
        def getaddshapemethod(klass=klass):
            def addshape(self, *args, **kwargs):
                Object = klass(*args, **kwargs)
                self.AddObject(Object)
                return Object
            return addshape
        addshapemethod = getaddshapemethod()
        methodname = "Add" + classname
        setattr(FloatCanvas, methodname, addshapemethod)
        docstring = "Creates %s and adds its reference to the canvas.\n" % classname
        docstring += "Argument protocol same as %s class" % classname
        if klass.__doc__:
            docstring += ", whose docstring is:\n%s" % klass.__doc__
        FloatCanvas.__dict__[methodname].__doc__ = docstring

_makeFloatCanvasAddMethods()


