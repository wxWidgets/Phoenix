"""
A throbber displays an animated image that can be
started, stopped, reversed, etc.  Useful for showing
an ongoing process (like most web browsers use) or
simply for adding eye-candy to an application.

Throbbers utilize a wxTimer so that normal processing
can continue unencumbered.
"""

#
# throbber.py - Cliff Wells <clifford.wells@comcast.net>
#
# Thanks to Harald Massa <harald.massa@suedvers.de> for
# suggestions and sample code.
#
#
# 12/12/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 compatibility update.
#
# Tags:        phoenix-port, unittest, py3-port, documented


import os
import wx

# ------------------------------------------------------------------------------

THROBBER_EVENT = wx.NewEventType()
EVT_UPDATE_THROBBER = wx.PyEventBinder(THROBBER_EVENT, 0)

class UpdateThrobberEvent(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(THROBBER_EVENT)

# ------------------------------------------------------------------------------

class Throbber(wx.Panel):
    """
    The first argument is either the name of a file that will be split into frames
    (a composite image) or a list of  strings of image names that will be treated
    as individual frames.  If a single (composite) image is given, then additional
    information must be provided: the number of frames in the image and the width
    of each frame.  The first frame is treated as the "at rest" frame (it is not
    shown during animation, but only when Throbber.Rest() is called.
    A second, single image may be optionally specified to overlay on top of the
    animation. A label may also be specified to show on top of the animation.
    """
    def __init__(self, parent, id,
                 bitmap,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 frameDelay = 0.1,
                 frames = 0,
                 frameWidth = 0,
                 label = None,
                 overlay = None,
                 reverse = 0,
                 style = 0,
                 name = "throbber",
                 rest = 0,
                 current = 0,
                 direction = 1,
                 sequence = None
                 ):
        """
        Default class constructor.

        :param `parent`: parent window, must not be ``None``
        :param integer `id`: window identifier. A value of -1 indicates a default value
        :param `bitmap`: a :class:`wx.Bitmap` to be used
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform
        :param `frameDelay`: time delay between frames
        :param `frames`: number of frames (only necessary for composite image)
        :param `frameWidth`: width of each frame (only necessary for composite image)
        :param string `label`: optional text to be displayed
        :param `overlay`: optional :class:`wx.Bitmap` to overlay on animation
        :param boolean `reverse`: reverse direction at end of animation
        :param integer `style`: the underlying :class:`wx.Control` style
        :param string `name`: the widget name.
        :param `rest`: the rest frame
        :param `current`: the current frame
        :param `direction`: 1 advances = -1 reverses
        :param `sequence`: sequence of frames, defaults to range(self.frames)

        """

        super(Throbber, self).__init__(parent, id, pos, size, style, name)
        self.name = name
        self.label = label
        self.running = (1 != 1)
        _seqTypes = (type([]), type(()))

        # set size, guessing if necessary
        width, height = size
        if width == -1:
            if type(bitmap) in _seqTypes:
                width = bitmap[0].GetWidth()
            else:
                if frameWidth:
                    width = frameWidth
        if height == -1:
            if type(bitmap) in _seqTypes:
                height = bitmap[0].GetHeight()
            else:
                height = bitmap.GetHeight()
        self.width, self.height = width, height

        # double check it
        assert width != -1 and height != -1, "Unable to guess size"

        if label:
            extentX, extentY = self.GetTextExtent(label)
            self.labelX = (width - extentX)/2
            self.labelY = (height - extentY)/2
        self.frameDelay = frameDelay
        self.rest = rest
        self.current = current
        self.direction = direction
        self.autoReverse = reverse
        self.overlay = overlay
        if overlay is not None:
            self.overlay = overlay
            self.overlayX = (width - self.overlay.GetWidth()) / 2
            self.overlayY = (height - self.overlay.GetHeight()) / 2
        self.showOverlay = overlay is not None
        self.showLabel = label is not None

        # do we have a sequence of images?
        if type(bitmap) in _seqTypes:
            self.submaps = bitmap
            self.frames = len(self.submaps)
        # or a composite image that needs to be split?
        else:
            self.frames = frames
            self.submaps = []
            for chunk in range(frames):
                rect = (chunk * frameWidth, 0, width, height)
                self.submaps.append(bitmap.GetSubBitmap(rect))

        # self.sequence can be changed, but it's not recommended doing it
        # while the throbber is running.  self.sequence[0] should always
        # refer to whatever frame is to be shown when 'resting' and be sure
        # that no item in self.sequence >= self.frames or < 0!!!
        self.SetSequence(sequence)

        self.SetClientSize((width, height))

        timerID  = wx.NewIdRef()
        self.timer = wx.Timer(self, timerID)

        self.Bind(EVT_UPDATE_THROBBER, self.Update)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroyWindow)


    def DoGetBestSize(self):
        """
        Get the best size of the widget.

        :returns: the width and height

        """
        return (self.width, self.height)


    def OnTimer(self, event):
        """
        Handles the ``wx.EVT_TIMER`` event for :class:`Throbber`.

        :param `event`: a :class:`TimerEvent` event to be processed.

        """
        wx.PostEvent(self, UpdateThrobberEvent())


    def OnDestroyWindow(self, event):
        """
        Handles the ``wx.EVT_WINDOW_DESTROY`` event for :class:`Throbber`.

        :param `event`: a :class:`wx.WindowDestroyEvent` event to be processed.

        """
        self.Stop()
        event.Skip()


    def Draw(self, dc):
        """
        Draw the widget.

        :param `dc`: the :class:`wx.DC` to draw on

        """
        dc.DrawBitmap(self.submaps[self.sequence[self.current]], 0, 0, True)
        if self.overlay and self.showOverlay:
            dc.DrawBitmap(self.overlay, self.overlayX, self.overlayY, True)
        if self.label and self.showLabel:
            dc.DrawText(self.label, self.labelX, self.labelY)
            dc.SetTextForeground(wx.WHITE)
            dc.DrawText(self.label, self.labelX-1, self.labelY-1)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`Throbber`.

        :param `event`: a :class:`PaintEvent` event to be processed.

        """
        self.Draw(wx.PaintDC(self))
        event.Skip()


    def Update(self, event):
        """
        Handles the ``EVT_UPDATE_THROBBER`` event for :class:`ResizeWidget`.

        :param `event`: a :class:`UpdateThrobberEvent` event to be processed.

        """
        self.Next()


    def Wrap(self):
        """Wrap the throbber around."""
        if self.current >= len(self.sequence):
            if self.autoReverse:
                self.Reverse()
                self.current = len(self.sequence) - 1
            else:
                self.current = 0
        if self.current < 0:
            if self.autoReverse:
                self.Reverse()
                self.current = 0
            else:
                self.current = len(self.sequence) - 1
        self.Draw(wx.ClientDC(self))


    # --------- public methods ---------
    def SetFont(self, font):
        """
        Set the font for the label.

        :param `font`: the :class:`wx.Font` to use

        """
        wx.Panel.SetFont(self, font)
        self.SetLabel(self.label)
        self.Draw(wx.ClientDC(self))


    def Rest(self):
        """Stop the animation and return to frame 0."""
        self.Stop()
        self.current = self.rest
        self.Draw(wx.ClientDC(self))


    def Reverse(self):
        """Change the direction of the animation."""
        self.direction = -self.direction


    def Running(self):
        """Returns True if the animation is running."""
        return self.running


    def Start(self):
        """Start the animation."""
        if not self.running:
            self.running = not self.running
            self.timer.Start(int(self.frameDelay * 1000))


    def Stop(self):
        """Stop the animation."""
        if self.running:
            self.timer.Stop()
            self.running = not self.running


    def SetCurrent(self, current):
        """
        Set current image.

        :param int `current`: the index to the current image

        """
        running = self.Running()
        if not running:
            #FIXME: need to make sure value is within range!!!
            self.current = current
            self.Draw(wx.ClientDC(self))


    def SetRest(self, rest):
        """
        Set rest image.

        :param int `rest`: the index for the rest frame.

        """
        self.rest = rest


    def SetSequence(self, sequence = None):
        """
        Order to display images in.

        :param `sequence`: a sequence containing the order to display images in.

        """

        # self.sequence can be changed, but it's not recommended doing it
        # while the throbber is running.  self.sequence[0] should always
        # refer to whatever frame is to be shown when 'resting' and be sure
        # that no item in self.sequence >= self.frames or < 0!!!

        running = self.Running()
        self.Stop()

        if sequence is not None:
            #FIXME: need to make sure values are within range!!!
            self.sequence = sequence
        else:
            self.sequence = list(range(self.frames))

        if running:
            self.Start()


    def Increment(self):
        """Display next image in sequence."""
        self.current += 1
        self.Wrap()


    def Decrement(self):
        """Display previous image in sequence."""
        self.current -= 1
        self.Wrap()


    def Next(self):
        """Display next image in sequence according to direction."""
        self.current += self.direction
        self.Wrap()


    def Previous(self):
        """Display previous image in sequence according to direction."""
        self.current -= self.direction
        self.Wrap()


    def SetFrameDelay(self, frameDelay = 0.05):
        """
        Delay between each frame.

        :param float `frameDelay`: the delay between frames.

        """
        self.frameDelay = frameDelay
        if self.running:
            self.Stop()
            self.Start()


    def ToggleOverlay(self, state = None):
        """
        Toggle the overlay image.

        :param boolean `state`: set the overlay state or if None toggle state.

        """
        if state is None:
            self.showOverlay = not self.showOverlay
        else:
            self.showOverlay = state
        self.Draw(wx.ClientDC(self))


    def ToggleLabel(self, state = None):
        """
        Toggle the label.

        :param boolean `state`: set the label state or if None toggle state.

        """
        if state is None:
            self.showLabel = not self.showLabel
        else:
            self.showLabel = state
        self.Draw(wx.ClientDC(self))


    def SetLabel(self, label):
        """
        Change the text of the label.

        :param string `label`: the label text.

        """
        self.label = label
        if label:
            extentX, extentY = self.GetTextExtent(label)
            self.labelX = (self.width - extentX)/2
            self.labelY = (self.height - extentY)/2
        self.Draw(wx.ClientDC(self))



# ------------------------------------------------------------------------------

