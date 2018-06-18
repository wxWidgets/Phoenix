#----------------------------------------------------------------------
# Name:        wx.lib.buttons
# Purpose:     Various kinds of generic buttons, (not native controls but
#              self-drawn.)
#
# Author:      Robin Dunn
#
# Created:     9-Dec-1999
# Copyright:   (c) 1999-2018 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port, unittest, documented
#----------------------------------------------------------------------
# 11/30/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o Updated for wx namespace
# o Tested with updated demo
#

"""
This module implements various forms of generic buttons, meaning that
they are not built on native controls but are self-drawn.


Description
===========

This module implements various forms of generic buttons, meaning that
they are not built on native controls but are self-drawn.
They act like normal buttons but you are able to better control how they look,
bevel width, colours, etc...


Usage
=====

Sample usage::

    import wx
    import wx.lib.buttons as buttons

    class MyFrame(wx.Frame):
        def __init__(self, parent, title):

            wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(400, 300))
            panel = wx.Panel(self)

            # Build a bitmap button and a normal one
            bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
            btn1 = buttons.ThemedGenBitmapButton(panel, -1, bmp, pos=(50, 50))

            btn2 = buttons.GenButton(panel, -1, "Hello World!", pos=(50, 100))


    app = wx.App()
    frame = MyFrame(None, 'wx.lib.buttons Test')
    frame.Show()
    app.MainLoop()

"""

import wx
import wx.lib.imageutils as imageutils


#----------------------------------------------------------------------

class GenButtonEvent(wx.CommandEvent):
    """ Event sent from the generic buttons when the button is activated. """

    def __init__(self, eventType, id):
        """
        Default class constructor.

        :param integer `eventType`: the event type;
        :param integer `id`: the event identifier.
        """

        wx.CommandEvent.__init__(self, eventType, id)
        self.isDown = False
        self.theButton = None


    def SetIsDown(self, isDown):
        """
        Set the button toggle status as 'down' or 'up'.

        :param bool `isDown`: ``True`` if the button is clicked, ``False`` otherwise.
        """

        self.isDown = isDown


    def GetIsDown(self):
        """
        Returns the button toggle status as ``True`` if the button is down, ``False``
        otherwise.

        :rtype: bool
        """

        return self.isDown


    def SetButtonObj(self, btn):
        """
        Sets the event object for the event.

        :param `btn`: the button object, an instance of :class:`GenButton`.
        """

        self.theButton = btn


    def GetButtonObj(self):
        """
        Returns the object associated with this event.

        :return: An instance of :class:`GenButton`.
        """

        return self.theButton


#----------------------------------------------------------------------

class GenButton(wx.Control):
    """ A generic button, and base class for the other generic buttons. """

    labelDelta = 1

    def __init__(self, parent, id=-1, label='',
                 pos = wx.DefaultPosition, size = wx.DefaultSize,
                 style = 0, validator = wx.DefaultValidator,
                 name = "genbutton"):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param string `label`: the button text label;
        :param `pos`: the control position. A value of (-1, -1) indicates a default
         position, chosen by either the windowing system or wxPython, depending on
         platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `style`: the button style;
        :param wx.Validator `validator`: the validator associated with the button;
        :param string `name`: the button name.

        .. seealso:: :class:`wx.Button` for a list of valid window styles.
        """

        cstyle = style
        if cstyle & wx.BORDER_MASK == 0:
            cstyle |= wx.BORDER_NONE

        wx.Control.__init__(self, parent, id, pos, size, cstyle, validator, name)

        self.up = True
        self.hasFocus = False
        self.style = style

        if style & wx.BORDER_NONE:
            self.bezelWidth = 0
            self.useFocusInd = False
        else:
            self.bezelWidth = 2
            self.useFocusInd = True

        self.SetLabel(label)
        self.InheritAttributes()
        self.SetInitialSize(size)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.Bind(wx.EVT_LEFT_DOWN,        self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP,          self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK,      self.OnLeftDown)
        self.Bind(wx.EVT_MOTION,           self.OnMotion)
        self.Bind(wx.EVT_SET_FOCUS,        self.OnGainFocus)
        self.Bind(wx.EVT_KILL_FOCUS,       self.OnLoseFocus)
        self.Bind(wx.EVT_KEY_DOWN,         self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP,           self.OnKeyUp)
        self.Bind(wx.EVT_PAINT,            self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)
        self.Bind(wx.EVT_SIZE,             self.OnSize)
        self.InitOtherEvents()


    def InitOtherEvents(self):
        """
        Override this method in a subclass to initialize any other events that
        need to be bound.  Added so :meth:`__init__` doesn't need to be
        overridden, which is complicated with multiple inheritance.
        """

        pass


    def SetInitialSize(self, size=None):
        """
        Given the current font and bezel width settings, calculate
        and set a good size.

        :param `size`: an instance of :class:`wx.Size` or ``None``,
         in which case the wxPython
         ``wx.DefaultSize`` is used instead.
        """

        if size is None:
            size = wx.DefaultSize

        wx.Control.SetInitialSize(self, size)

    SetBestSize = SetInitialSize


    def DoGetBestSize(self):
        """
        Overridden base class virtual. Determines the best size of the
        button based on the label and bezel size.

        :return: An instance of :class:`wx.Size`.

        .. note:: Overridden from :class:`wx.Control`.
        """

        w, h, useMin = self._GetLabelSize()
        if self.style & wx.BU_EXACTFIT:
            width = w + 2 + 2 * self.bezelWidth + 4 * int(self.useFocusInd)
            height = h + 2 + 2 * self.bezelWidth + 4 * int(self.useFocusInd)
        else:
            defSize = wx.Button.GetDefaultSize()
            width = 12 + w
            if useMin and width < defSize.width:
                width = defSize.width
            height = 11 + h
            if useMin and height < defSize.height:
                height = defSize.height
            width = width + self.bezelWidth - 1
            height = height + self.bezelWidth - 1

        return wx.Size(width, height)


    def AcceptsFocus(self):
        """
        Can this window be given focus by mouse click?

        .. note:: Overridden from :class:`wx.Control`.
        """

        return self.IsShown() and self.IsEnabled()


    def GetDefaultAttributes(self):
        """
        Overridden base class virtual. By default we should use
        the same font/colour attributes as the native :class:`wx.Button`.

        :return: an instance of :class:`wx.VisualAttributes`.

        .. note:: Overridden from :class:`wx.Control`.
        """

        return wx.Button.GetClassDefaultAttributes()


    def ShouldInheritColours(self):
        """
        Overridden base class virtual. Buttons usually don't inherit
        the parent's colours.

        .. note:: Overridden from :class:`wx.Control`.
        """

        return False


    def Enable(self, enable=True):
        """
        Enables/disables the button.

        :param bool `enable`: ``True`` to enable the button, ``False`` to disable it.

        .. note:: Overridden from :class:`wx.Control`.
        """

        if enable != self.IsEnabled():
            wx.Control.Enable(self, enable)
            self.Refresh()


    def SetBezelWidth(self, width):
        """
        Sets the width of the 3D effect.

        :param integer `width`: the 3D border width, in pixels.
        """

        self.bezelWidth = width


    def GetBezelWidth(self):
        """
        Returns the width of the 3D effect, in pixels.

        :rtype: integer
        """

        return self.bezelWidth


    def SetUseFocusIndicator(self, flag):
        """
        Specifies if a focus indicator (dotted line) should be used.

        :param bool `flag`: ``True`` to draw a focus ring, ``False`` otherwise.
        """

        self.useFocusInd = flag


    def GetUseFocusIndicator(self):
        """
        Returns the focus indicator flag, specifying if a focus indicator
        (dotted line) is being used.

        :rtype: bool
        """

        return self.useFocusInd


    def InitColours(self):
        """
        Calculate a new set of highlight and shadow colours based on
        the background colour. Works okay if the colour is dark...
        """

        faceClr = self.GetBackgroundColour()
        r, g, b, a = faceClr
        fr, fg, fb = min(255,r+32), min(255,g+32), min(255,b+32)
        self.faceDnClr = wx.Colour(fr, fg, fb)
        sr, sg, sb = max(0,r-32), max(0,g-32), max(0,b-32)
        self.shadowPenClr = wx.Colour(sr,sg,sb)
        hr, hg, hb = min(255,r+64), min(255,g+64), min(255,b+64)
        self.highlightPenClr = wx.Colour(hr,hg,hb)
        self.focusClr = wx.Colour(hr, hg, hb)


    def SetBackgroundColour(self, colour):
        """
        Sets the :class:`GenButton` background colour.

        :param `colour`: a valid :class:`wx.Colour` object.

        .. note:: Overridden from :class:`wx.Control`.
        """

        wx.Control.SetBackgroundColour(self, colour)
        self.InitColours()


    def SetForegroundColour(self, colour):
        """
        Sets the :class:`wx.GenButton` foreground colour.

        :param `colour`: a valid :class:`wx.Colour` object.

        .. note:: Overridden from :class:`wx.Control`.
        """

        wx.Control.SetForegroundColour(self, colour)
        self.InitColours()


    def SetDefault(self):
        """
        This sets the :class:`GenButton` to be the default item for
        the panel or dialog box.

        .. note:: Under Windows, only dialog box buttons respond to this function.
           As normal under Windows and Motif, pressing return causes the
           default button to be depressed when the return key is pressed. See
           also :meth:`wx.Window.SetFocus` which sets the keyboard focus for
           windows and text panel items, and
           :meth:`wx.TopLevelWindow.SetDefaultItem`.

        .. note:: Note that under Motif, calling this function immediately after
           creation of a button and before the creation of other buttons will
           cause misalignment of the row of buttons, since default buttons are
           larger. To get around this, call :meth:`wx.SetDefault` after you
           have created a row of buttons: wxPython will then set the size of
           all buttons currently on the panel to the same size.
        """

        tlw = wx.GetTopLevelParent(self)
        if hasattr(tlw, 'SetDefaultItem'):
            tlw.SetDefaultItem(self)


    def _GetLabelSize(self):
        """ Used internally. """

        w, h = self.GetTextExtent(self.GetLabel())
        return w, h, True


    def Notify(self):
        """ Actually sends a ``wx.EVT_BUTTON`` event to the listener (if any). """

        evt = GenButtonEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        evt.SetIsDown(not self.up)
        evt.SetButtonObj(self)
        evt.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(evt)


    def DrawBezel(self, dc, x1, y1, x2, y2):
        # draw the upper left sides
        if self.up:
            dc.SetPen(wx.Pen(self.highlightPenClr, 1))
        else:
            dc.SetPen(wx.Pen(self.shadowPenClr, 1))
        for i in range(self.bezelWidth):
            dc.DrawLine(x1+i, y1, x1+i, y2-i)
            dc.DrawLine(x1, y1+i, x2-i, y1+i)

        # draw the lower right sides
        if self.up:
            dc.SetPen(wx.Pen(self.shadowPenClr, 1))
        else:
            dc.SetPen(wx.Pen(self.highlightPenClr, 1))
        for i in range(self.bezelWidth):
            dc.DrawLine(x1+i, y2-i, x2+1, y2-i)
            dc.DrawLine(x2-i, y1+i, x2-i, y2)


    def DrawLabel(self, dc, width, height, dx=0, dy=0):
        dc.SetFont(self.GetFont())
        if self.IsEnabled():
            dc.SetTextForeground(self.GetForegroundColour())
        else:
            dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
        label = self.GetLabel()
        tw, th = dc.GetTextExtent(label)
        if not self.up:
            dx = dy = self.labelDelta
        dc.DrawText(label, (width-tw)/2+dx, (height-th)/2+dy)


    def DrawFocusIndicator(self, dc, w, h):
        bw = self.bezelWidth
        textClr = self.GetForegroundColour()
        focusIndPen  = wx.Pen(textClr, 1, wx.PENSTYLE_USER_DASH)
        focusIndPen.SetDashes([1,1])
        focusIndPen.SetCap(wx.CAP_BUTT)

        if wx.Platform == "__WXMAC__":
            dc.SetLogicalFunction(wx.XOR)
        else:
            focusIndPen.SetColour(self.focusClr)
            dc.SetLogicalFunction(wx.INVERT)
        dc.SetPen(focusIndPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(bw+2,bw+2,  w-bw*2-4, h-bw*2-4)
        dc.SetLogicalFunction(wx.COPY)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`GenButton`.

        :param `event`: a :class:`wx.PaintEvent` event to be processed.
        """

        (width, height) = self.GetClientSize()
        x1 = y1 = 0
        x2 = width-1
        y2 = height-1

        dc = wx.PaintDC(self)
        brush = self.GetBackgroundBrush(dc)
        if brush is not None:
            dc.SetBackground(brush)
            dc.Clear()

        self.DrawBezel(dc, x1, y1, x2, y2)
        self.DrawLabel(dc, width, height)
        if self.hasFocus and self.useFocusInd:
            self.DrawFocusIndicator(dc, width, height)


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`GenButton`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        self.Refresh()
        event.Skip()


    def GetBackgroundBrush(self, dc):
        """
        Returns the current :class:`wx.Brush` to be used to draw the button background.

        :param wx.DC `dc`: the device context used to draw the button background.
        """

        if self.up:
            colBg = self.GetBackgroundColour()
            brush = wx.Brush(colBg)
            if self.style & wx.BORDER_NONE:
                myAttr = self.GetDefaultAttributes()
                parAttr = self.GetParent().GetDefaultAttributes()
                myDef = colBg == myAttr.colBg
                parDef = self.GetParent().GetBackgroundColour() == parAttr.colBg
                if myDef and parDef:
                    if wx.Platform == "__WXMAC__":
                        c = wx.MacThemeColour(1) # 1 == kThemeBrushDialogBackgroundActive
                        brush = wx.Brush(c)
                    elif wx.Platform == "__WXMSW__":
                        if hasattr(self, 'DoEraseBackground') and self.DoEraseBackground(dc):
                            brush = None
                elif myDef and not parDef:
                    colBg = self.GetParent().GetBackgroundColour()
                    brush = wx.Brush(colBg)
        else:
            # this line assumes that a pressed button should be hilighted with
            # a solid colour even if the background is supposed to be transparent
            brush = wx.Brush(self.faceDnClr)
        return brush


    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`GenButton`.

        :param `event`: a :class:`wx.MouseEvent` event to be processed.
        """

        if not self.IsEnabled():
            return

        self.up = False
        self.CaptureMouse()
        self.SetFocus()
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`GenButton`.

        :param `event`: a :class:`wx.MouseEvent` event to be processed.
        """

        if not self.IsEnabled() or not self.HasCapture():
            return

        if self.HasCapture():
            self.ReleaseMouse()
            if not self.up:    # if the button was down when the mouse was released...
                self.Notify()
            self.up = True
            if self:           # in case the button was destroyed in the eventhandler
                self.Refresh()
                event.Skip()


    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`GenButton`.

        :param `event`: a :class:`wx.MouseEvent` event to be processed.
        """

        if not self.IsEnabled() or not self.HasCapture():
            return

        if event.LeftIsDown() and self.HasCapture():
            x,y = event.GetPosition()
            w,h = self.GetClientSize()

            if self.up and x<w and x>=0 and y<h and y>=0:
                self.up = False
                self.Refresh()
                return

            if not self.up and (x<0 or y<0 or x>=w or y>=h):
                self.up = True
                self.Refresh()
                return

        event.Skip()


    def OnGainFocus(self, event):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for :class:`GenButton`.

        :param `event`: a :class:`wx.FocusEvent` event to be processed.
        """

        self.hasFocus = True
        self.Refresh()
        self.Update()


    def OnLoseFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`GenButton`.

        :param `event`: a :class:`wx.FocusEvent` event to be processed.
        """

        self.hasFocus = False
        self.Refresh()
        self.Update()


    def OnKeyDown(self, event):
        """
        Handles the ``wx.EVT_KEY_DOWN`` event for :class:`GenButton`.

        :param `event`: a :class:`wx.KeyEvent` event to be processed.
        """

        if self.hasFocus and event.GetKeyCode() == ord(" "):
            self.up = False
            self.Refresh()

        event.Skip()


    def OnKeyUp(self, event):
        """
        Handles the ``wx.EVT_KEY_UP`` event for :class:`GenButton`.

        :param `event`: a :class:`wx.KeyEvent` event to be processed.
        """

        if self.hasFocus and event.GetKeyCode() == ord(" "):
            self.up = True
            self.Notify()
            self.Refresh()

        event.Skip()


#----------------------------------------------------------------------

class GenBitmapButton(GenButton):
    """ A generic bitmap button. """

    def __init__(self, parent, id=-1, bitmap=wx.NullBitmap,
                 pos = wx.DefaultPosition, size = wx.DefaultSize,
                 style = 0, validator = wx.DefaultValidator,
                 name = "genbutton"):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param wx.Bitmap `bitmap`: the button bitmap;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `style`: the button style;
        :param wx.Validator `validator`: the validator associated to the button;
        :param string `name`: the button name.

        .. seealso:: :class:`wx.Button` for a list of valid window styles.
        """

        self.bmpDisabled = None
        self.bmpFocus = None
        self.bmpSelected = None
        self.SetBitmapLabel(bitmap)
        GenButton.__init__(self, parent, id, "", pos, size, style, validator, name)


    def GetBitmapLabel(self):
        """
        Returns the bitmap for the button's normal state.

        :rtype: :class:`wx.Bitmap`

        .. seealso:: :meth:`SetBitmapLabel`
        """

        return self.bmpLabel


    def GetBitmapDisabled(self):
        """
        Returns the bitmap for the button's disabled state, which may be invalid.

        :rtype: :class:`wx.Bitmap`

        .. seealso:: :meth:`SetBitmapDisabled`
        """

        return self.bmpDisabled


    def GetBitmapFocus(self):
        """
        Returns the bitmap for the button's focused state, which may be invalid.

        :rtype: :class:`wx.Bitmap`

        .. seealso:: :meth:`SetBitmapFocus`
        """

        return self.bmpFocus


    def GetBitmapSelected(self):
        """
        Returns the bitmap for the button's pressed state, which may be invalid.

        :rtype: :class:`wx.Bitmap`

        .. seealso:: :meth:`SetBitmapSelected`
        """

        return self.bmpSelected


    def SetBitmapDisabled(self, bitmap):
        """
        Sets the bitmap for the disabled button appearance.

        :param wx.Bitmap `bitmap`: the bitmap for the disabled button appearance.

        .. seealso::

           :meth:`GetBitmapDisabled`, :meth:`SetBitmapLabel`,
           :meth:`SetBitmapSelected`, :meth:`SetBitmapFocus`

        """

        self.bmpDisabled = bitmap


    def SetBitmapFocus(self, bitmap):
        """
        Sets the bitmap for the focused button appearance.

        :param wx.Bitmap `bitmap`: the bitmap for the focused button appearance.

        .. seealso::

           :meth:`GetBitmapFocus`, :meth:`SetBitmapLabel`,
           :meth:`SetBitmapSelected`, :meth:`SetBitmapDisabled`

        """

        self.bmpFocus = bitmap
        self.SetUseFocusIndicator(False)


    def SetBitmapSelected(self, bitmap):
        """
        Sets the bitmap for the selected (depressed) button appearance.

        :param wx.Bitmap `bitmap`: the bitmap for the selected (depressed) button appearance.

        .. seealso::

           :meth:`GetBitmapSelected`, :meth:`SetBitmapLabel`,
           :meth:`SetBitmapDisabled`, :meth:`SetBitmapFocus`

        """

        self.bmpSelected = bitmap


    def SetBitmapLabel(self, bitmap, createOthers=True):
        """
        Set the bitmap to display normally.
        This is the only one that is required.

        If `createOthers` is ``True``, then the other bitmaps will be generated
        on the fly.  Currently, only the disabled bitmap is generated.

        :param wx.Bitmap `bitmap`: the bitmap for the normal button appearance.

        .. note:: This is the bitmap used for the unselected state, and for all other
           states if no other bitmaps are provided.
        """

        self.bmpLabel = bitmap
        if bitmap is not None and createOthers:
            image = bitmap.ConvertToImage()
            imageutils.grayOut(image)
            self.SetBitmapDisabled(wx.Bitmap(image))


    def _GetLabelSize(self):
        """ Used internally. """

        if not self.bmpLabel:
            return -1, -1, False

        return self.bmpLabel.GetWidth()+2, self.bmpLabel.GetHeight()+2, False


    def DrawLabel(self, dc, width, height, dx=0, dy=0):
        bmp = self.bmpLabel
        if self.bmpDisabled and not self.IsEnabled():
            bmp = self.bmpDisabled
        if self.bmpFocus and self.hasFocus:
            bmp = self.bmpFocus
        if self.bmpSelected and not self.up:
            bmp = self.bmpSelected
        bw,bh = bmp.GetWidth(), bmp.GetHeight()
        if not self.up:
            dx = dy = self.labelDelta
        hasMask = bmp.GetMask() != None
        dc.DrawBitmap(bmp, (width-bw)/2+dx, (height-bh)/2+dy, hasMask)


#----------------------------------------------------------------------


class GenBitmapTextButton(GenBitmapButton):
    """ A generic bitmapped button with text label. """

    def __init__(self, parent, id=-1, bitmap=wx.NullBitmap, label='',
                 pos = wx.DefaultPosition, size = wx.DefaultSize,
                 style = 0, validator = wx.DefaultValidator,
                 name = "genbutton"):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param wx.Bitmap `bitmap`: the button bitmap;
        :param string `label`: the button text label;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `style`: the button style;
        :param wx.Validator `validator`: the validator associated to the button;
        :param string `name`: the button name.

        .. seealso:: :class:`wx.Button` for a list of valid window styles.
        """

        GenBitmapButton.__init__(self, parent, id, bitmap, pos, size, style, validator, name)
        self.SetLabel(label)


    def _GetLabelSize(self):
        """ Used internally. """

        w, h = self.GetTextExtent(self.GetLabel())
        if not self.bmpLabel:
            return w, h, True       # if there isn't a bitmap use the size of the text

        w_bmp = self.bmpLabel.GetWidth()+2
        h_bmp = self.bmpLabel.GetHeight()+2
        width = w + w_bmp
        if h_bmp > h:
            height = h_bmp
        else:
            height = h
        return width, height, True


    def DrawLabel(self, dc, width, height, dx=0, dy=0):
        bmp = self.bmpLabel
        if bmp is not None:     # if the bitmap is used
            if self.bmpDisabled and not self.IsEnabled():
                bmp = self.bmpDisabled
            if self.bmpFocus and self.hasFocus:
                bmp = self.bmpFocus
            if self.bmpSelected and not self.up:
                bmp = self.bmpSelected
            bw,bh = bmp.GetWidth(), bmp.GetHeight()
            if not self.up:
                dx = dy = self.labelDelta
            hasMask = bmp.GetMask() is not None
        else:
            bw = bh = 0     # no bitmap -> size is zero
            hasMask = False

        dc.SetFont(self.GetFont())
        if self.IsEnabled():
            dc.SetTextForeground(self.GetForegroundColour())
        else:
            dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))

        label = self.GetLabel()
        tw, th = dc.GetTextExtent(label)        # size of text
        if not self.up:
            dx = dy = self.labelDelta

        pos_x = (width-bw-tw)/2+dx      # adjust for bitmap and text to centre
        if bmp is not None:
            dc.DrawBitmap(bmp, pos_x, (height-bh)/2+dy, hasMask) # draw bitmap if available
            pos_x = pos_x + 2   # extra spacing from bitmap

        dc.DrawText(label, pos_x + dx+bw, (height-th)/2+dy)      # draw the text


#----------------------------------------------------------------------


class __ToggleMixin(object):
    """
    A mixin that allows to transform :class:`GenButton` in the corresponding
    toggle button.
    """

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
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`GenButton` when used as toggle button.

        :param `event`: a :class:`wx.MouseEvent` event to be processed.
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
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`GenButton` when used as toggle button.

        :param `event`: a :class:`wx.MouseEvent` event to be processed.
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
        Handles the ``wx.EVT_KEY_DOWN`` event for :class:`GenButton` when used as toggle button.

        :param `event`: a :class:`wx.KeyEvent` event to be processed.
        """

        event.Skip()


    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`GenButton` when used as toggle button.

        :param `event`: a :class:`wx.MouseEvent` event to be processed.
        """

        if not self.IsEnabled():
            return

        if event.LeftIsDown() and self.HasCapture():
            x,y = event.GetPosition()
            w,h = self.GetClientSize()

            if x<w and x>=0 and y<h and y>=0:
                self.up = not self.saveUp
                self.Refresh()
                return

            if (x<0 or y<0 or x>=w or y>=h):
                self.up = self.saveUp
                self.Refresh()
                return

        event.Skip()


    def OnKeyUp(self, event):
        """
        Handles the ``wx.EVT_KEY_UP`` event for :class:`GenButton` when used as toggle button.

        :param `event`: a :class:`wx.KeyEvent` event to be processed.
        """

        if self.hasFocus and event.GetKeyCode() == ord(" "):
            self.up = not self.up
            self.Notify()
            self.Refresh()
        event.Skip()




class GenToggleButton(__ToggleMixin, GenButton):
    """ A generic toggle button. """
    pass

class GenBitmapToggleButton(__ToggleMixin, GenBitmapButton):
    """ A generic toggle bitmap button. """
    pass

class GenBitmapTextToggleButton(__ToggleMixin, GenBitmapTextButton):
    """ A generic toggle bitmap button with text label. """
    pass

#----------------------------------------------------------------------


class __ThemedMixin(object):
    """ Uses the native renderer to draw the bezel, also handle mouse-overs. """


    def InitOtherEvents(self):
        """ Initializes other events needed for themed buttons. """

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouse)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouse)


    def OnMouse(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` and ``wx.EVT_LEAVE_WINDOW`` events for
        :class:`GenButton` when used as a themed button.

        :param `event`: a :class:`wx.MouseEvent` event to be processed.
        """

        self.Refresh()
        event.Skip()


    def DrawBezel(self, dc, x1, y1, x2, y2):

        rect = wx.Rect(x1, y1, x2, y2)
        if self.up:
            state = 0
        else:
            state = wx.CONTROL_PRESSED | wx.CONTROL_SELECTED
        if not self.IsEnabled():
            state = wx.CONTROL_DISABLED
        pt = self.ScreenToClient(wx.GetMousePosition())
        if self.GetClientRect().Contains(pt):
            state |= wx.CONTROL_CURRENT
        wx.RendererNative.Get().DrawPushButton(self, dc, rect, state)



class ThemedGenButton(__ThemedMixin, GenButton):
    """ A themed generic button. """
    pass

class ThemedGenBitmapButton(__ThemedMixin, GenBitmapButton):
    """ A themed generic bitmap button. """
    pass

class ThemedGenBitmapTextButton(__ThemedMixin, GenBitmapTextButton):
    """ A themed generic bitmapped button with text label. """
    pass

class ThemedGenToggleButton(__ThemedMixin, GenToggleButton):
    """ A themed generic toggle button. """
    pass

class ThemedGenBitmapToggleButton(__ThemedMixin, GenBitmapToggleButton):
    """ A themed generic toggle bitmap button. """
    pass

class ThemedGenBitmapTextToggleButton(__ThemedMixin, GenBitmapTextToggleButton):
    """ A themed generic toggle bitmap button with text label. """
    pass


#----------------------------------------------------------------------
