# --------------------------------------------------------------------------------- #
# AQUABUTTON wxPython IMPLEMENTATION
#
# Andrea Gavana, @ 07 October 2008
# Latest Revision: 27 Dec 2012, 21.00 GMT
#
#
# TODO List
#
# 1) Anything to do?
#
#
# For all kind of problems, requests of enhancements and bug reports, please
# write to me at:
#
# andrea.gavana@gmail.com
# andrea.gavana@maerskoil.com
#
# Or, obviously, to the wxPython mailing list!!!
#
# Tags:        phoenix-port, unittest, documented, py3-port
#
# End Of Comments
# --------------------------------------------------------------------------------- #

"""
:class:`~wx.lib.agw.aquabutton.AquaButton` is another custom-drawn button class which *approximatively* mimics
the behaviour of Aqua buttons on the Mac.


Description
===========

:class:`AquaButton` is another custom-drawn button class which *approximatively* mimics
the behaviour of Aqua buttons on the Mac. At the moment this class supports:

* Bubble and shadow effects;
* Customizable background, foreground and hover colours;
* Rounded-corners buttons;
* Text-only or image+text buttons;
* Pulse effect on gaining focus.

And a lot more. Check the demo for an almost complete review of the functionalities.


Usage
=====

Sample usage::

    import wx
    import wx.lib.agw.aquabutton as AB

    app = wx.App(0)

    frame = wx.Frame(None, -1, "AquaButton Test")

    mainPanel = wx.Panel(frame)
    mainPanel.SetBackgroundColour(wx.WHITE)

    # Initialize AquaButton 1 (with image)
    bitmap = wx.Bitmap("my_button_bitmap.png", wx.BITMAP_TYPE_PNG)
    btn1 = AB.AquaButton(mainPanel, -1, bitmap, "AquaButton")

    # Initialize AquaButton 2 (no image)
    btn2 = AB.AquaButton(mainPanel, -1, None, "Hello World!")

    frame.Show()

    app.MainLoop()


Supported Platforms
===================

AquaButton has been tested on the following platforms:
  * Windows (Windows XP);
  * Linux Ubuntu (10.10).


Window Styles
=============

`No particular window styles are available for this class.`


Events Processing
=================

This class processes the following events:

================= ==================================================
Event Name        Description
================= ==================================================
``wx.EVT_BUTTON`` Process a `wxEVT_COMMAND_BUTTON_CLICKED` event, when the button is clicked.
================= ==================================================


License And Version
===================

:class:`AquaButton` control is distributed under the wxPython license.

Latest Revision: Andrea Gavana @ 27 Dec 2012, 21.00 GMT

Version 0.4

"""

import wx

# Constants for the hovering and clicking effects
HOVER = 1
""" Indicates that the mouse is hovering over :class:`AquaButton` """
CLICK = 2
""" Indicates that :class:`AquaButton` has been clicked """


class AquaButtonEvent(wx.PyCommandEvent):
    """ Event sent from the :class:`AquaButton` buttons when the button is activated. """

    def __init__(self, eventType, eventId):
        """
        Default class constructor.

        :param integer `eventType`: the event type;
        :param integer `eventId`: the event identifier.
        """

        wx.PyCommandEvent.__init__(self, eventType, eventId)
        self.isDown = False
        self.theButton = None


    def SetButtonObj(self, btn):
        """
        Sets the event object for the event.

        :param `btn`: the button object, an instance of :class:`AquaButton`.
        """

        self.theButton = btn


    def GetButtonObj(self):
        """
        Returns the object associated with this event.

        :return: An instance of :class:`AquaButton`.
        """

        return self.theButton


class AquaButton(wx.Control):
    """ This is the main class implementation of :class:`AquaButton`. """

    def __init__(self, parent, id=wx.ID_ANY, bitmap=None, label="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="aquabutton"):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param wx.Bitmap `bitmap`: the button bitmap (if any);
        :param string `label`: the button text label;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `style`: the button style (unused);
        :param wx.Validator `validator`: the validator associated to the button;
        :param string `name`: the button name.
        """

        wx.Control.__init__(self, parent, id, pos, size, style, validator, name)

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_SET_FOCUS, self.OnGainFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocus)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.Bind(wx.EVT_TIMER, self.OnPulseTimer)

        if "__WXMSW__" in wx.PlatformInfo:
            self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDown)

        self._mouseAction = None
        self.SetBitmapLabel(bitmap)
        self._hasFocus = False
        self._saveBitmap = True
        self._storedBitmap = wx.NullBitmap
        self._pulseOnFocus = False
        self._gammaFactor = 1.0
        self._gammaIncrement = 0.1

        self._timer = wx.Timer(self, wx.ID_ANY)

        self.SetLabel(label)
        self.InheritAttributes()
        self.SetInitialSize(size)

        # The following defaults are better suited to draw the text outline
        if "__WXMAC__" in wx.PlatformInfo:
            self._backColour = wx.Colour(147, 202, 255)
            self._hoverColour = self.LightColour(self._backColour, 30)
            self._focusColour = self.LightColour(self._backColour, 40)
            self._disableColour = self.LightColour(self._backColour, 70)
            self._textColour = wx.BLACK
            self._shadowColour = wx.Colour("grey")
            self._rectColour = self.GetParent().GetBackgroundColour()
        else:
            self._backColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
            self._hoverColour = self.LightColour(self._backColour, 30)
            self._focusColour = self.LightColour(self._backColour, 40)
            self._disableColour = self.LightColour(self._backColour, 70)
            self._textColour = wx.WHITE
            self._shadowColour = wx.Colour("grey")
            self._rectColour = self.GetParent().GetBackgroundColour()


    def SetBitmapLabel(self, bitmap):
        """
        Sets the bitmap label for the button.

        :param `bitmap`: the bitmap label to set, an instance of :class:`wx.Bitmap`.
        """

        self._bitmap = bitmap
        self.Refresh()


    def LightColour(self, colour, percent):
        """
        Return light contrast of `colour`. The colour returned is from the scale of
        `colour` ==> white.

        :param `colour`: the input colour to be brightened, a valid instance of :class:`wx.Colour`;
        :param integer `percent`: determines how light the colour will be. `percent` = ``100``
         returns white, `percent` = ``0`` returns `colour`.

        :return: A light contrast of the input `colour`, an instance of :class:`wx.Colour`.
        """

        end_colour = wx.WHITE
        rd = end_colour.Red() - colour.Red()
        gd = end_colour.Green() - colour.Green()
        bd = end_colour.Blue() - colour.Blue()
        high = 100

        # We take the percent way of the colour from colour ==> white
        i = percent
        r = colour.Red() + ((i*rd*100)/high)/100
        g = colour.Green() + ((i*gd*100)/high)/100
        b = colour.Blue() + ((i*bd*100)/high)/100
        a = colour.Alpha()

        return wx.Colour(int(r), int(g), int(b), int(a))


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`AquaButton`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        xpos, ypos, width, height = self.GetClientRect()

        dc.SetBackground(wx.Brush(self._rectColour))
        dc.Clear()
        gc.SetBrush(wx.WHITE_BRUSH)

        shadowOffset = 5
        btnOffset = 0
        clr = self._backColour

        if self._mouseAction == CLICK:
            shadowOffset = 3
            clr = self._hoverColour
            btnOffset = 2

        elif self._mouseAction == HOVER:
            clr = self._hoverColour

        elif self._hasFocus:
            clr = self._focusColour

        elif not self.IsEnabled():
            clr = self._disableColour

        rc1 = wx.Rect(btnOffset, btnOffset, width-8-btnOffset, height-8-btnOffset)
        path1 = self.GetPath(gc, rc1, 10)
        br1 = gc.CreateLinearGradientBrush(0, 0, 0, rc1.height+6, clr, wx.WHITE)

        # Create shadow
        rc2 = wx.Rect(*rc1)
        rc2.Offset((shadowOffset, shadowOffset))
        path2 = self.GetPath(gc, rc2, 10)
        br2 = gc.CreateRadialGradientBrush(rc2.x, rc2.y,
                                           rc2.x+rc2.width, rc2.y+rc2.height,
                                           rc2.width, self._shadowColour, wx.WHITE)

        # Create top water colour to give "aqua" effect
        rc3 = wx.Rect(*rc1)
        rc3.Inflate(-5, -5)
        rc3.height = 15
        path3 = self.GetPath(gc, rc3, 10)

        br3 = gc.CreateLinearGradientBrush(rc3.x, rc3.y, rc3.x, rc3.y+rc3.height,
                                           wx.WHITE, wx.TransparentColour)

        # draw shapes
        gc.SetBrush(br2)
        gc.FillPath(path2)  #draw shadow
        gc.SetBrush(br1)
        gc.FillPath(path1) #draw main
        gc.SetBrush(br3)
        gc.FillPath(path3) #draw top bubble

        font = gc.CreateFont(self.GetFont(), self._textColour)

        gc.SetFont(font)
        label = self.GetLabel()
        tw, th = gc.GetTextExtent(label)

        if self._bitmap:
            bw, bh = self._bitmap.GetWidth(), self._bitmap.GetHeight()
        else:
            bw = bh = 0

        pos_x = (width-bw-tw)/2+btnOffset-shadowOffset      # adjust for bitmap and text to centre
        if self._bitmap:
            pos_y =  (height-bh-shadowOffset)/2+btnOffset
            gc.DrawBitmap(self._bitmap, pos_x, pos_y, bw, bh) # draw bitmap if available
            pos_x = pos_x + 2   # extra spacing from bitmap

        # Create a Path to draw the text
        gc.DrawText(label, pos_x + bw + btnOffset, (height-th-shadowOffset)/2+btnOffset)      # draw the text

        if self._saveBitmap:
            # Save the bitmap using wx.MemoryDC for later use
            self._saveBitmap = False
            memory = wx.MemoryDC()
            self._storedBitmap = wx.Bitmap.FromRGBA(max(width, 1), max(height, 1))
            memory.SelectObject(self._storedBitmap)

            gcMemory = wx.GraphicsContext.Create(memory)

            gcMemory.SetBrush(br1)
            gcMemory.FillPath(path1) #draw main
            gcMemory.SetBrush(br3)
            gcMemory.FillPath(path3) #draw top bubble

            if self._bitmap:
                gcMemory.DrawBitmap(self._bitmap, pos_x - 2, pos_y, bw, bh)

            gcMemory.SetFont(font)
            gcMemory.DrawText(label, pos_x + bw + btnOffset, (height-th-shadowOffset)/2+btnOffset)

            memory.SelectObject(wx.NullBitmap)
            self._storedBitmap = self._storedBitmap.ConvertToImage()


    def GetPath(self, gc, rc, r):
        """
        Returns a rounded :class:`GraphicsPath` rectangle.

        :param `gc`: an instance of :class:`GraphicsContext`;
        :param wx.Rect `rc`: a client rectangle;
        :param float `r`: the radius of the rounded part of the rectangle.

        :return: A rounded rectangle, an instance of :class:`GraphicsPath`.
        """

        x, y, w, h = rc
        path = gc.CreatePath()
        path.AddRoundedRectangle(x, y, w, h, r)
        path.CloseSubpath()
        return path


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`AquaButton`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        self.Invalidate()


    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`AquaButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self.IsEnabled():
            return

        self._mouseAction = CLICK
        self.CaptureMouse()
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`AquaButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self.IsEnabled() or not self.HasCapture():
            return

        pos = event.GetPosition()
        rect = self.GetClientRect()

        if self.HasCapture():
            self.ReleaseMouse()

        if rect.Contains(pos):
            self._mouseAction = HOVER
            self.Notify()
        else:
            self._mouseAction = None

        self.Refresh()
        event.Skip()


    def OnMouseEnter(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` event for :class:`AquaButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self.IsEnabled():
            return

        self._mouseAction = HOVER
        self.Refresh()
        event.Skip()


    def OnMouseLeave(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`AquaButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        self._mouseAction = None
        self.Refresh()
        event.Skip()


    def OnGainFocus(self, event):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for :class:`AquaButton`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        self._hasFocus = True
        self.Refresh()
        self.Update()

        if self._pulseOnFocus:
            self._gammaFactor = 1.0
            self._timer.Start(100)


    def OnLoseFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`AquaButton`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        if self._pulseOnFocus:
            self._gammaFactor = 1.0
            self._timer.Stop()

        self._hasFocus = False
        self.Refresh()
        self.Update()


    def OnKeyDown(self, event):
        """
        Handles the ``wx.EVT_KEY_DOWN`` event for :class:`AquaButton`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        if self._hasFocus and event.GetKeyCode() == ord(" "):
            self._mouseAction = HOVER
            self.Refresh()
        event.Skip()


    def OnKeyUp(self, event):
        """
        Handles the ``wx.EVT_KEY_UP`` event for :class:`AquaButton`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        if self._hasFocus and event.GetKeyCode() == ord(" "):
            self._mouseAction = HOVER
            self.Notify()
            self.Refresh()
        event.Skip()


    def OnPulseTimer(self, event):
        """
        Handles the ``wx.EVT_TIMER`` event for :class:`AquaButton`.

        :param `event`: a :class:`TimerEvent` event to be processed.

        :note: This method is only invoked when `pulseOnFocus` is ``True``.
        """

        if not self._storedBitmap.IsOk():
            self._timer.Stop()
            return

        xpos, ypos, width, height = self.GetClientRect()
        gamma = self._gammaFactor

        if gamma >= 1.3:
            self._gammaIncrement = -self._gammaIncrement
        elif gamma < 0.7:
            self._gammaIncrement = abs(self._gammaIncrement)

        self._gammaFactor += self._gammaIncrement

        image = self._storedBitmap.AdjustChannels(gamma, gamma, gamma, 1.0)
        dc = wx.ClientDC(self)
        dc.SetClippingRegion(wx.Rect(xpos, ypos, width-8, height-8))
        dc.DrawBitmap(image.ConvertToBitmap(), xpos, ypos, True)


    def SetInitialSize(self, size=None):
        """
        Given the current font and bezel width settings, calculate
        and set a good size.

        :param `size`: an instance of :class:`wx.Size` or ``None``, in which case the wxWidgets
         :class:`DefaultSize` is used instead.
        """

        if size is None:
            size = wx.DefaultSize
        wx.Control.SetInitialSize(self, size)

    SetBestSize = SetInitialSize


    def AcceptsFocus(self):
        """
        Can this window be given focus by mouse click?

        :note: Overridden from :class:`wx.Control`.
        """

        return self.IsShown() and self.IsEnabled()


    def GetDefaultAttributes(self):
        """
        Overridden base class virtual. By default we should use
        the same font/colour attributes as the native :class:`Button`.

        :return: an instance of :class:`VisualAttributes`.

        :note: Overridden from :class:`wx.Control`.
        """

        return wx.Button.GetClassDefaultAttributes()


    def ShouldInheritColours(self):
        """
        Overridden base class virtual. Buttons usually don't inherit
        the parent's colours.

        :note: Overridden from :class:`wx.Control`.
        """

        return False


    def Enable(self, enable=True):
        """
        Enables/disables the button.

        :param bool `enable`: ``True`` to enable the button, ``False`` to disable it.

        :note: Overridden from :class:`wx.Control`.
        """

        wx.Control.Enable(self, enable)
        self.Refresh()


    def SetPulseOnFocus(self, pulse):
        """
        Sets whether to enable the pulsing effect on gaining focus or not.

        :param bool `pulse`: ``True`` to enable pulsing when the :class:`AquaButton` gains focus,
         ``False`` to disable this effect.
        """

        if pulse == self._pulseOnFocus:
            return

        self._pulseOnFocus = pulse
        self.Invalidate()


    def GetPulseOnFocus(self):
        """
        Returns whether the pulsing effect is active.

        :return: ``True`` if the pulsing effect is active, ``False`` otherwise.
        """

        return self._pulseOnFocus


    def DoGetBestSize(self):
        """
        Overridden base class virtual. Determines the best size of the
        button based on the label and bezel size.

        :return: An instance of :class:`wx.Size`.

        :note: Overridden from :class:`wx.Control`.
        """

        label = self.GetLabel()
        if not label:
            return wx.Size(112, 48)

        dc = wx.ClientDC(self)
        dc.SetFont(self.GetFont())
        retWidth, retHeight = dc.GetTextExtent(label)

        bmpWidth = bmpHeight = 0
        constant = 24
        if self._bitmap:
            bmpWidth, bmpHeight = self._bitmap.GetWidth()+10, self._bitmap.GetHeight()
            retWidth += bmpWidth
            retHeight = max(bmpHeight, retHeight)
            constant = 24

        return wx.Size(retWidth+constant, retHeight+constant)


    def DoEnable(self, enable):
        """
        Overridden base class virtual.

        Need to Refresh otherwise Enable state change done from a
        `wx.EVT_UPDATE_UI` will not show.
        """
        self.Refresh()


    def SetBackgroundColour(self, colour):
        """
        Sets the :class:`AquaButton` background colour.

        :param `colour`: a valid :class:`wx.Colour` object.

        :note: Overridden from :class:`wx.Control`.
        """

        wx.Control.SetBackgroundColour(self, colour)
        self._backColour = colour
        self.Invalidate()


    def GetBackgroundColour(self):
        """
        Returns the button colour when the mouse is not hovering on the button.

        :return: An instance of :class:`wx.Colour`.

        :note: Overridden from :class:`wx.Control`.
        """

        return self._backColour


    def SetHoverColour(self, colour):
        """
        Sets the button colour when the mouse is hovering on the button.

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._hoverColour = colour
        self.Invalidate()


    def GetHoverColour(self):
        """
        Returns the button colour when the mouse is hovering on the button.

        :return: An instance of :class:`wx.Colour`.
        """

        return self._hoverColour


    def SetDisabledColour(self, colour):
        """
        Sets the button colour when it is disabled.

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._disableColour = colour
        self.Invalidate()


    def GetDisabledColour(self):
        """
        Returns the button colour when it is disabled.

        :return: An instance of :class:`wx.Colour`.
        """

        return self._disableColour


    def SetShadowColour(self, colour):
        """
        Sets the button shadow colour.

        :param `colour`: a valid :class:`wx.Colour` object.

        .. versionadded:: 0.9.7
        """

        self._shadowColour = colour
        self.Invalidate()


    def GetShadowColour(self):
        """
        Returns the button shadow colour.

        :return: An instance of :class:`wx.Colour`.

        .. versionadded:: 0.9.7
        """

        return self._shadowColour


    def SetRectColour(self, colour):
        """
        Sets the button rectangular background colour.

        :param `colour`: a valid :class:`wx.Colour` object.

        .. versionadded:: 0.9.7
        """

        self._rectColour = colour
        self.Invalidate()


    def GetRectColour(self):
        """
        Returns the button rectangular background colour.

        :return: An instance of :class:`wx.Colour`.

        .. versionadded:: 0.9.7
        """

        return self._rectColour


    SetBackgroundColor = SetBackgroundColour
    SetHoverColor = SetHoverColour
    GetHoverColor = GetHoverColour
    SetDisabledColor = SetDisabledColour
    GetDisabledColor = GetDisabledColour
    SetShadowColor = SetShadowColour
    GetShadowColor = SetShadowColour
    SetRectColor = SetRectColour
    GetRectColor = SetRectColour


    def SetForegroundColour(self, colour):
        """
        Sets the :class:`AquaButton` foreground (text) colour.

        :param `colour`: a valid :class:`wx.Colour` object.

        :note: Overridden from :class:`wx.Control`.
        """

        wx.Control.SetForegroundColour(self, colour)
        self._textColour = colour
        self.Invalidate()


    def GetForegroundColour(self):
        """
        Returns the text colour for :class:`AquaButton`.

        :return: An instance of :class:`wx.Colour`.

        :note: Overridden from :class:`wx.Control`.
        """

        return self._textColour


    def SetFocusColour(self, colour):
        """
        Sets the button colour when the button has focus.

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._focusColour = colour
        self.Invalidate()


    def GetFocusColour(self):
        """
        Returns the button colour when the button has focus.

        :return: An instance of :class:`wx.Colour`.
        """

        return self._hoverColour


    def Invalidate(self):
        """ Invalidate the saved bitmap and refresh the button. """

        self._saveBitmap = True
        self._storedBitmap = wx.NullBitmap

        self.Refresh()


    def SetDefault(self):
        """
        This sets the :class:`AquaButton` to be the default item for the panel or dialog box.

        :note: Under Windows, only dialog box buttons respond to this function. As normal
         under Windows and Motif, pressing return causes the default button to be depressed
         when the return key is pressed. See also :meth:`wx.Window.SetFocus` which sets the
         keyboard focus for windows and text panel items, and :meth:`TopLevelWindow.SetDefaultItem`.

        :note: Note that under Motif, calling this function immediately after creation of a button
         and before the creation of other buttons will cause misalignment of the row of buttons,
         since default buttons are larger. To get around this, call :meth:`SetDefault` after you
         have created a row of buttons: wxPython will then set the size of all buttons currently
         on the panel to the same size.
        """

        tlw = wx.GetTopLevelParent(self)
        if hasattr(tlw, 'SetDefaultItem'):
            tlw.SetDefaultItem(self)


    def Notify(self):
        """ Actually sends a ``wx.EVT_BUTTON`` event to the listener (if any). """

        evt = AquaButtonEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        evt.SetButtonObj(self)
        evt.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(evt)


class __ToggleMixin(object):
    """
    A mixin that allows to transform :class:`AquaButton` in the corresponding toggle button.
    """

    up = True

    def SetToggle(self, flag):
        """
        Sets the button as toggled/not toggled.

        :param bool `flag`: ``True`` to set the button as toggled, ``False`` otherwise.
        """

        self.up = not flag
        self.Refresh()

    SetValue = SetToggle


    def GetToggle(self):
        """
        Returns the toggled state of a button.

        :return: ``True`` is the button is toggled, ``False`` if it is not toggled.
        """

        return not self.up

    GetValue = GetToggle


    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`AquaButton` when used as toggle button.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self.IsEnabled():
            return

        self.saveUp = self.up
        self.up = not self.up
        self.CaptureMouse()
        self.SetFocus()
        self.Refresh()


    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`AquaButton` when used as toggle button.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            self.Refresh()
            if self.up != self.saveUp:
                self.Notify()


    def OnKeyDown(self, event):
        """
        Handles the ``wx.EVT_KEY_DOWN`` event for :class:`AquaButton` when used as toggle button.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        event.Skip()


    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`AquaButton` when used as toggle button.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self.IsEnabled():
            return

        if event.LeftIsDown() and self.HasCapture():
            x, y = event.GetPosition()
            w, h = self.GetClientSize()

            if x < w and x >= 0 and y < h and y >= 0:
                self.up = not self.saveUp
                self.Refresh()
                return

            if x < 0 or y < 0 or x >= w or y >= h:
                self.up = self.saveUp
                self.Refresh()
                return

        event.Skip()


    def OnKeyUp(self, event):
        """
        Handles the ``wx.EVT_KEY_UP`` event for :class:`AquaButton` when used as toggle button.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        if self.hasFocus and event.GetKeyCode() == ord(" "):
            self.up = not self.up
            self.Notify()
            self.Refresh()

        event.Skip()


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`AquaButton` when used as toggle button.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        xpos, ypos, width, height = self.GetClientRect()

        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        gc.SetBrush(wx.WHITE_BRUSH)

        shadowOffset = 5
        btnOffset = 0
        clr = self._backColour

        if not self.up:
            shadowOffset = 3
            clr = self._hoverColour
            btnOffset = 2

        if self._mouseAction == HOVER:
            clr = self._hoverColour

        rc1 = wx.Rect(btnOffset, btnOffset, width-8-btnOffset, height-8-btnOffset)
        path1 = self.GetPath(gc, rc1, 10)
        br1 = gc.CreateLinearGradientBrush(0, 0, 0, rc1.height+6, clr, wx.WHITE)

        # Create shadow
        rc2 = wx.Rect(*rc1)
        rc2.Offset((shadowOffset, shadowOffset))
        path2 = self.GetPath(gc, rc2, 10)
        br2 = gc.CreateRadialGradientBrush(rc2.x, rc2.y,
                                           rc2.x+rc2.width, rc2.y+rc2.height,
                                           rc2.width, wx.Colour("grey"), wx.WHITE)

        # Create top water colour to give "aqua" effect
        rc3 = wx.Rect(*rc1)
        rc3.Inflate(-5, -5)
        rc3.height = 15
        path3 = self.GetPath(gc, rc3, 10)

        br3 = gc.CreateLinearGradientBrush(rc3.x, rc3.y, rc3.x, rc3.y+rc3.height,
                                           wx.WHITE, wx.TransparentColour)

        # draw shapes
        gc.SetBrush(br2)
        gc.FillPath(path2)  #draw shadow
        gc.SetBrush(br1)
        gc.FillPath(path1) #draw main
        gc.SetBrush(br3)
        gc.FillPath(path3) #draw top bubble

        font = gc.CreateFont(self.GetFont(), self._textColour)

        gc.SetFont(font)
        label = self.GetLabel()
        tw, th = gc.GetTextExtent(label)

        if self._bitmap:
            bw, bh = self._bitmap.GetWidth(), self._bitmap.GetHeight()
        else:
            bw = bh = 0

        pos_x = (width-bw-tw)/2+btnOffset-shadowOffset      # adjust for bitmap and text to centre
        if self._bitmap:
            pos_y =  (height-bh-shadowOffset)/2+btnOffset
            gc.DrawBitmap(self._bitmap, pos_x, pos_y, bw, bh) # draw bitmap if available
            pos_x = pos_x + 2   # extra spacing from bitmap

        # Create a Path to draw the text
        gc.DrawText(label, pos_x + bw + btnOffset, (height-th-shadowOffset)/2+btnOffset)      # draw the text

        if self._saveBitmap:
            # Save the bitmap using wx.MemoryDC for later use
            self._saveBitmap = False
            memory = wx.MemoryDC()
            self._storedBitmap = wx.Bitmap.FromRGBA(max(width, 1), max(height, 1))
            memory.SelectObject(self._storedBitmap)

            gcMemory = wx.GraphicsContext.Create(memory)

            gcMemory.SetBrush(br1)
            gcMemory.FillPath(path1) #draw main
            gcMemory.SetBrush(br3)
            gcMemory.FillPath(path3) #draw top bubble

            if self._bitmap:
                gcMemory.DrawBitmap(self._bitmap, pos_x - 2, pos_y, bw, bh)

            gcMemory.SetFont(font)
            gcMemory.DrawText(label, pos_x + bw + btnOffset, (height-th-shadowOffset)/2+btnOffset)

            memory.SelectObject(wx.NullBitmap)
            self._storedBitmap = self._storedBitmap.ConvertToImage()


class AquaToggleButton(__ToggleMixin, AquaButton):
    """ An :class:`AquaButton` toggle button. """
    pass

