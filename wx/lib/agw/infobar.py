# --------------------------------------------------------------------------- #
# INFOBAR Control wxPython IMPLEMENTATION
# Inspired By And Heavily Based On wxInfoBar.
#
# Python Code By:
#
# Andrea Gavana, @ 12 March 2012
# Latest Revision: 27 Dec 2012, 21.00 GMT
#
#
# TODO List/Caveats
#
# 1. ?
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@gmail.com
# andrea.gavana@maerskoil.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
# Tags:        phoenix-port, unittest, documented, py3-port
#
# End Of Comments
# --------------------------------------------------------------------------- #

"""
An info bar is a transient window shown at top or bottom of its parent window to display
non-critical information to the user.

Description
===========

An info bar is a transient window shown at top or bottom of its parent window to display
non-critical information to the user.

:note:

    The Python implementation of :class:`InfoBar` is a direct translation of the generic C++
    implementation of :class:`InfoBar`.


This class provides another way to show messages to the user, intermediate between message
boxes and status bar messages. The message boxes are modal and thus interrupt the users work
flow and should be used sparingly for this reason. However status bar messages are often
too easy not to notice at all. An info bar provides a way to present the messages which has
a much higher chance to be noticed by the user but without being annoying.

Info bar may show an icon (on the left), text message and, optionally, buttons allowing the
user to react to the information presented. It always has a close button at the right allowing
the user to dismiss it so it isn't necessary to provide a button just to close it.

:class:`InfoBar` calls its parent `Layout()` method (if its parent is **not** managed by :class:`~aui.framemanager`
or :class:`~wx.lib.agw.aui.framemanager.AuiManager`) and assumes that it will change the parent layout appropriately depending
on whether the info bar itself is shown or hidden. Usually this is achieved by simply using a
sizer for the parent window layout and adding wxInfoBar to this sizer as one of the items.
Considering the usual placement of the info bars, normally this sizer should be a vertical
:class:`BoxSizer` and the bar its first or last element.


Base Functionalities
====================

:class:`InfoBar` supports all the :class:`InfoBar` generic implementation functionalities, and in addition
it using :meth:`~InfoBar.AddButton` it is possible to add a button with a bitmap (and not only a plain :class:`Button`).

For example::

    info = InfoBar(parent)
    bitmap = wx.Bitmap('nice_bitmap.png', wx.BITMAP_TYPE_PNG)

    info.AddButton(wx.NewId(), 'New Button', bitmap)



Usage
=====

The simplest possible example of using this class would be::

    import wx
    import wx.lib.agw.infobar as IB

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, 'InfoBar Demo')

            self._infoBar = IB.InfoBar(self)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self._infoBar, wx.SizerFlags().Expand())

            panel = wx.Panel(self)
            sizer.Add(panel, 1, wx.EXPAND)

            # ... Add other frame controls to the sizer ...
            self.SetSizer(sizer)

            wx.CallLater(2000, self.SomeMethod)


        def SomeMethod(self):

            self._infoBar.ShowMessage("Something happened", wx.ICON_INFORMATION)


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()



Supported Platforms
===================

:class:`InfoBar` has been tested on the following platforms:
  * Windows (Vista/7).


Window Styles
=============

`No particular window styles are available for this class.`


Events Processing
=================

This class processes the following events:

================= ==================================================
Event Name        Description
================= ==================================================
``wx.EVT_BUTTON`` Process a `wx.wxEVT_COMMAND_BUTTON_CLICKED` event, when the button is clicked.
================= ==================================================


License And Version
===================

:class:`InfoBar` control is distributed under the wxPython license.

Latest Revision: Andrea Gavana @ 27 Dec 2012, 21.00 GMT

Version 0.3

"""

# Version Info
__version__ = "0.3"

# Start the imports
import wx

# These two are needed only to check if the InfoBar parent
# is managed by PyAUI or wx.aui, in which case the handling
# of the showing/dismissing is done a bit differently
CPP_AUI = True
try:
    import wx.aui
except ImportError:
    CPP_AUI = False

from .aui import framemanager as framemanager

# These are for the AutoWrapStaticText class
from wx.lib.wordwrap import wordwrap
from wx.lib.stattext import GenStaticText as StaticText

# Get the translation function
_ = wx.GetTranslation


# Determine the placement of the bar from its position in the containing
# sizer
BarPlacement_Unknown = 0
""" Unknown :class:`InfoBar` placement (not good). """
BarPlacement_Top     = 1
""" :class:`InfoBar` is placed at the top of its parent. """
BarPlacement_Bottom  = 2
""" :class:`InfoBar` is placed at the bottom of its parent. """

# This dictionary is here because wx.ArtProvider.GetMessageBoxIconId(flags)
# doesn't do what I think it should do in wxPython
FLAGS2ART = {wx.ICON_NONE        : wx.ART_MISSING_IMAGE,
             wx.ICON_INFORMATION : wx.ART_INFORMATION,
             wx.ICON_QUESTION    : wx.ART_QUESTION,
             wx.ICON_WARNING     : wx.ART_WARNING,
             wx.ICON_ERROR       : wx.ART_ERROR
             }


# ----------------------------------------------------------------------------
# Local helpers
# ----------------------------------------------------------------------------

def GetCloseButtonBitmap(win, size, colBg, flags=0):
    """
    For platforms supporting it (namely wxMSW and wxMAC), this method uses :class:`RendererNative`
    to draw a natively-looking close button on the :class:`InfoBar` itself.

    :param `win`: the window in which we wish to draw the close button (an instance of
     :class:`InfoBar`);
    :param tuple `size`: the close button size, a tuple of `(width, height)` dimensions in pixels;
    :param `colBg`: the background colour of the parent window, an instance of :class:`wx.Colour`;
    :param integer `flags`: may have the ``wx.CONTROL_PRESSED``, ``wx.CONTROL_CURRENT`` or
     ``wx.CONTROL_ISDEFAULT`` bit set.
    """

    bmp = wx.Bitmap(*size)
    dc = wx.MemoryDC()
    dc.SelectObject(bmp)
    dc.SetBackground(wx.Brush(colBg))
    dc.Clear()

    wx.RendererNative.Get().DrawTitleBarBitmap(win, dc, wx.Rect(size), wx.TITLEBAR_BUTTON_CLOSE, flags)
    dc.SelectObject(wx.NullBitmap)

    return bmp


# ----------------------------------------------------------------------------
# Auto-wrapping static text class
# ----------------------------------------------------------------------------

class AutoWrapStaticText(StaticText):
    """
    A simple class derived from :mod:`lib.stattext` that implements auto-wrapping
    behaviour depending on the parent size.

    .. versionadded:: 0.9.5
    """

    def __init__(self, parent, label):
        """
        Defsult class constructor.

        :param wx.Window parent: a subclass of :class:`wx.Window`, must not be ``None``;
        :param string `label`: the :class:`AutoWrapStaticText` text label.
        """

        StaticText.__init__(self, parent, -1, label, style=wx.ST_NO_AUTORESIZE)

        self.label = label

        colBg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK)
        self.SetBackgroundColour(colBg)
        self.SetOwnForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT))

        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`AutoWrapStaticText`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        event.Skip()
        self.Wrap(event.GetSize().width)


    def Wrap(self, width):
        """
        This functions wraps the controls label so that each of its lines becomes at
        most `width` pixels wide if possible (the lines are broken at words boundaries
        so it might not be the case if words are too long).

        If `width` is negative, no wrapping is done.

        :param integer `width`: the maximum available width for the text, in pixels.

        :note: Note that this `width` is not necessarily the total width of the control,
         since a few pixels for the border (depending on the controls border style) may be added.
        """

        if width < 0:
            return

        self.Freeze()

        dc = wx.ClientDC(self)
        dc.SetFont(self.GetFont())
        text = wordwrap(self.label, width, dc)
        self.SetLabel(text, wrapped=True)

        self.Thaw()


    def SetLabel(self, label, wrapped=False):
        """
        Sets the :class:`AutoWrapStaticText` label.

        All "&" characters in the label are special and indicate that the following character is
        a mnemonic for this control and can be used to activate it from the keyboard (typically
        by using ``Alt`` key in combination with it). To insert a literal ampersand character, you
        need to double it, i.e. use "&&". If this behaviour is undesirable, use :meth:`~Control.SetLabelText` instead.

        :param string `label`: the new :class:`AutoWrapStaticText` text label;
        :param bool `wrapped`: ``True`` if this method was called by the developer using :meth:`~AutoWrapStaticText.SetLabel`,
         ``False`` if it comes from the :meth:`~AutoWrapStaticText.OnSize` event handler.

        :note: Reimplemented from :class:`wx.Control`.
        """

        if not wrapped:
            self.label = label

        StaticText.SetLabel(self, label)


# ============================================================================
# Implementation
# ============================================================================

class InfoBar(wx.Control):
    """
    An info bar is a transient window shown at top or bottom of its parent window to display
    non-critical information to the user.

    This is the main class implementation, plainly translated from C++.
    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, name='InfoBar'):
        """
        Default class constructor.

        :param `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `style`: the :class:`InfoBar` style (unused at present);
        :param string `name`: the control name.
        """

        wx.Control.__init__(self, parent, id, pos, size, style|wx.BORDER_NONE, name=name)

        self.SetInitialSize(size)
        self.Init()

        # calling Hide() before Create() ensures that we're created initially
        # hidden
        self.Hide()

        # use special, easy to notice, colours
        colBg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK)
        self.SetBackgroundColour(colBg)
        self.SetOwnForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT))

        # create the controls: icon,text and the button to dismiss the
        # message.

        # the icon is not shown unless it's assigned a valid bitmap
        self._icon = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap)
        self._text = AutoWrapStaticText(self, "")

        if wx.Platform == '__WXGTK__':
            bmp = wx.ArtProvider.GetBitmap(wx.ART_CLOSE, wx.ART_BUTTON)
        else:
            # THIS CRASHES PYTHON ALTOGETHER!!
            # sizeBmp = wx.ArtProvider.GetSizeHint(wx.ART_BUTTON)
            sizeBmp = (16, 16)
            bmp = GetCloseButtonBitmap(self, sizeBmp, colBg)

        self._button = wx.BitmapButton(self, wx.ID_ANY, bmp, style=wx.BORDER_NONE)

        if wx.Platform != '__WXGTK__':
            self._button.SetBitmapPressed(GetCloseButtonBitmap(self, sizeBmp, colBg, wx.CONTROL_PRESSED))
            self._button.SetBitmapCurrent(GetCloseButtonBitmap(self, sizeBmp, colBg, wx.CONTROL_CURRENT))

        self._button.SetBackgroundColour(colBg)
        self._button.SetToolTip(_("Hide this notification message."))

        # center the text inside the sizer with an icon to the left of it and a
        # button at the very right
        #
        # NB: AddButton() relies on the button being the last control in the sizer
        #     and being preceded by a spacer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._icon, wx.SizerFlags().Centre().Border())
        sizer.Add(self._text, 200, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self._button, wx.SizerFlags().Centre().Border())
        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.OnButton)


    def Init(self):
        """ Common initialization code. """

        self._icon = None
        self._text = None
        self._button = None
        self._showEffect = wx.SHOW_EFFECT_MAX
        self._hideEffect = wx.SHOW_EFFECT_MAX

        # use default effect duration
        self._effectDuration = 0


    def SetFont(self, font):
        """
        Overridden base class methods changes the font of the text message.

        :class:`InfoBar` overrides this method to use the font passed to it for its text
        message part. By default a larger and bold version of the standard font is used.

        :param `font`: a valid instance of :class:`wx.Font`.

        :note: Reimplemented from :class:`wx.Window`.
        """

        if not wx.Control.SetFont(self, font):
            return False

        # check that we're not called before Create()
        if self._text:
            self._text.SetFont(font)

        return True


    def GetBarPlacement(self):
        """
        Determines the placement of the bar from its position in the containing
        sizer.

        :return: One of these integer bits:

         ========================== =========== ==================================================
         Placement Flag             Hex Value   Description
         ========================== =========== ==================================================
         ``BarPlacement_Unknown``           0x0 Unknown placement of :class:`InfoBar` (not good).
         ``BarPlacement_Top``               0x1 :class:`InfoBar` is placed at the top of its parent.
         ``BarPlacement_Bottom``            0x2 :class:`InfoBar` is placed at the bottom of its parent.
         ========================== =========== ==================================================

        """

        sizer = self.GetContainingSizer()

        if not sizer:
            return BarPlacement_Unknown

        siblings = sizer.GetChildren()
        lSib = len(siblings) - 1

        if siblings[0].GetWindow() == self:
            return BarPlacement_Top
        elif siblings[lSib].GetWindow()== self:
            return BarPlacement_Bottom
        else:
            return BarPlacement_Unknown


    def GetShowEffect(self):
        """
        Return the effect currently used for showing the bar.

        :return: One of the following integer bits:

         ================================== =========== ==================================================
         `ShowEffect` Flag                  Hex Value   Description
         ================================== =========== ==================================================
         ``wx.SHOW_EFFECT_NONE``                    0x0 No effect, equivalent to normal `Show()` or `Hide()` call.
         ``wx.SHOW_EFFECT_SLIDE_TO_TOP``            0x7 Slide the :class:`InfoBar` window to the top.
         ``wx.SHOW_EFFECT_SLIDE_TO_BOTTOM``         0x8 Slide the :class:`InfoBar` window to the bottom.
         ================================== =========== ==================================================

        """

        if self._showEffect != wx.SHOW_EFFECT_MAX:
            return self._showEffect

        placement = self.GetBarPlacement()

        if placement == BarPlacement_Top:
            return wx.SHOW_EFFECT_SLIDE_TO_BOTTOM

        elif placement == BarPlacement_Bottom:
            return wx.SHOW_EFFECT_SLIDE_TO_TOP

        elif placement == BarPlacement_Unknown:
            return wx.SHOW_EFFECT_NONE

        else:
            raise Exception("unknown info bar placement")


    def GetHideEffect(self):
        """
        Return the effect currently used for hiding the bar.

        :return: One of the following integer bits:

         ================================== =========== ==================================================
         `ShowEffect` Flag                  Hex Value   Description
         ================================== =========== ==================================================
         ``wx.SHOW_EFFECT_NONE``                    0x0 No effect, equivalent to normal `Show()` or `Hide()` call.
         ``wx.SHOW_EFFECT_SLIDE_TO_TOP``            0x7 Slide the :class:`InfoBar` window to the top.
         ``wx.SHOW_EFFECT_SLIDE_TO_BOTTOM``         0x8 Slide the :class:`InfoBar` window to the bottom.
         ================================== =========== ==================================================

        """

        if self._hideEffect != wx.SHOW_EFFECT_MAX:
            return self._hideEffect

        placement = self.GetBarPlacement()

        if placement == BarPlacement_Top:
            return wx.SHOW_EFFECT_SLIDE_TO_TOP

        elif placement == BarPlacement_Bottom:
            return wx.SHOW_EFFECT_SLIDE_TO_BOTTOM

        elif placement == BarPlacement_Unknown:
            return wx.SHOW_EFFECT_NONE

        else:
            raise Exception("unknown info bar placement")


    def GetDefaultBorder(self):
        """ Returns the default border style for :class:`InfoBar`. """

        return wx.BORDER_NONE


    def UpdateParent(self):
        """
        Updates the parent layout appearance, but only if this :class:`InfoBar` parent is **not** managed
        by :class:`framemanager` or :class:`~wx.lib.agw.aui.framemanager.AuiManager`.
        """

        parent = self.GetParent()
        parent.Layout()
        parent.Refresh()


    def DoHide(self):
        """ Hides this :class:`InfoBar` with whatever hiding effect has been chosen. """

        self.HideWithEffect(self.GetHideEffect(), self.GetEffectDuration())

        handler = self.GetParent().GetEventHandler()
        if CPP_AUI:
            managers = (framemanager.AuiManager, wx.aui.AuiManager)
        else:
            managers = (framemanager.AuiManager, )

        if not isinstance(handler, managers):
            self.UpdateParent()
        else:
            pane = handler.GetPane(self)
            pane.Show(False)
            handler.Update()


    def DoShow(self):
        """ Shows this :class:`InfoBar` with whatever showing effect has been chosen. """

        # re-layout the parent first so that the window expands into an already
        # unoccupied by the other controls area: for this we need to change our
        # internal visibility flag to force Layout() to take us into account(an
        # alternative solution to this hack would be to temporarily set
        # wx.RESERVE_SPACE_EVEN_IF_HIDDEN flag but it's not really better)

        # just change the internal flag indicating that the window is visible,
        # without really showing it
        self.GetParent().Freeze()

        wx.Control.Show(self)

        # adjust the parent layout to account for us
        self.UpdateParent()

        # reset the flag back before really showing the window or it wouldn't be
        # shown at all because it would believe itself already visible
        wx.Control.Show(self, False)
        self.GetParent().Thaw()

        # finally do really show the window.
        self.ShowWithEffect(self.GetShowEffect(), self.GetEffectDuration())

        handler = self.GetParent().GetEventHandler()

        if CPP_AUI:
            managers = (framemanager.AuiManager, wx.aui.AuiManager)
        else:
            managers = (framemanager.AuiManager, )

        if isinstance(handler, managers):
            pane = handler.GetPane(self)
            pane.Show(True)
            handler.Update()


    def ShowMessage(self, msg, flags=wx.ICON_INFORMATION):
        """
        Show a message in the bar.

        If the bar is currently hidden, it will be shown. Otherwise its message will be updated in place.

        :param string `msg`: the text of the message;
        :param integer `flags`: one of ``wx.ICON_NONE``, ``wx.ICON_INFORMATION`` (default), ``wx.ICON_QUESTION``,
         ``wx.ICON_WARNING`` or ``wx.ICON_ERROR`` values.

         :note: These flags have the same meaning as in :class:`MessageDialog` for the generic version, i.e.
          show (or not, in case of ``wx.ICON_NONE``) the corresponding icon in the bar but can be interpreted
          by the native versions. For example, the GTK+ native implementation doesn't show icons at all but
          uses this parameter to select the appropriate background colour for the notification.
        """

        # first update the controls
        icon = flags & wx.ICON_MASK
        iconSize = 0

        if not icon or icon == wx.ICON_NONE:
            self._icon.Hide()

        else: # do show an icon
            bitmap = wx.ArtProvider.GetBitmap(FLAGS2ART[flags], wx.ART_BUTTON)
            iconSize = bitmap.GetWidth() + wx.SizerFlags().Border().GetDefaultBorder()
            self._icon.SetBitmap(bitmap)
            self._icon.Show()

        # notice the use of EscapeMnemonics() to ensure that "&" come through
        # correctly
        self._text.SetLabel(wx.Control.EscapeMnemonics(msg))

        parentSize = self.GetParent().GetSize()
        self._text.Wrap(parentSize.x - iconSize - wx.SizerFlags().Border().GetDefaultBorder())

        # then show this entire window if not done yet
        if not self.IsShown():
            self.DoShow()

        self.Layout()


    def Dismiss(self):
        """
        Hides the :class:`InfoBar` window.

        This method hides the window and lays out the parent window to account for
        its disappearance (unlike a simple `Hide()`), but only if this :class:`InfoBar`
        parent is **not** managed by :class:`framemanager` or :class:`~wx.lib.agw.aui.framemanager.AuiManager`.
        """

        self.DoHide()


    def AddButton(self, btnid, label='', bitmap=wx.NullBitmap):
        """
        Adds a button to be shown in the info bar.

        The button added by this method will be shown to the right of the text (in LTR layout),
        with each successive button being added to the right of the previous one. If any buttons
        are added to the info bar using this method, the default `Close` button is not shown
        as it is assumed that the extra buttons already allow the user to close it.

        Clicking the button will generate a normal ``wx.wxEVT_COMMAND_BUTTON_CLICKED`` event which
        can be handled as usual. The default handler in :class:`InfoBar` itself closes the window
        whenever a button in it is clicked so if you wish the info bar to be hidden when the button
        is clicked, simply call `event.Skip()` in the button handler to let the base class handler
        do it (calling :meth:`~InfoBar.Dismiss` explicitly works too, of course). On the other hand, if you don't
        skip the event, the info bar will remain opened so make sure to do it for at least some
        buttons to allow the user to close it.

        :param integer `btnid`: id of the button. It will be used in the button message clicking
         this button will generate;
        :param string `label`: the label of the button. It may only be empty if `btnid` is one of
         the stock ids in which case the corresponding stock label will be used;
        :param `bitmap`: if not equal to :class:`NullBitmap`, a valid :class:`wx.Bitmap` image to show beside
         the button text.

        :note:

             Notice that the generic :class:`InfoBar` implementation handles the button events itself
             and so they are not propagated to the info bar parent and you need to either inherit from
             :class:`InfoBar` and handle them in your derived class or use `self.Bind(...)` to handle the
             button events in the parent frame.

        """

        sizer = self.GetSizer()

        if not sizer:
            raise Exception("must be created first")

        # user-added buttons replace the standard close button so remove it if we
        # hadn't done it yet
        if sizer.Detach(self._button):
            self._button.Hide()

        button = wx.Button(self, btnid, label)

        if bitmap.IsOk():
            # Add the bitmap to the button
            button.SetBitmap(bitmap, wx.LEFT)
            button.SetBitmapMargins((2, 2)) # default is 4 but that seems too big to me.

        if wx.Platform == '__WXMAC__':
            # smaller buttons look better in the(narrow)info bar under OS X
            button.SetWindowVariant(wx.WINDOW_VARIANT_SMALL)

        sizer.Add(button, wx.SizerFlags().Centre().DoubleBorder())

        if self.IsShown():
            self.UpdateParent()


    def RemoveButton(self, btnid):
        """
        Remove a button previously added by :meth:`~InfoBar.AddButton`.

        :param integer `btnid`: id of the button to remove. If more than one button with the
         same id is used in the :class:`InfoBar` (which is in any case not recommended), the last,
         i.e. most recently added, button with this `id` is removed.
        """

        sizer = self.GetSizer()

        if not sizer:
            raise Exception("must be created first")

        # iterate over the sizer items in reverse order to find the last added
        # button with this id(ids of all buttons should be unique anyhow but if
        # they are repeated removing the last added one probably makes more sense)
        items = sizer.GetChildren()

        for item in reversed(items):
            # if we reached the spacer separating the buttons from the text
            # preceding them without finding our button,it must mean it's not
            # there at all
            if item.IsSpacer():
                raise Exception("button with id %d not found"%btnid)

            # check if we found our button
            window = item.GetWindow()
            if window.GetId() == btnid:
                sizer.Detach(window)
                window.Destroy()
                break

        # check if there are any custom buttons left
        if list(sizer.GetChildren())[-1].IsSpacer():
            # if the last item is the spacer,none are left so restore the
            # standard close button
            sizer.Add(self._button, wx.SizerFlags().Centre().DoubleBorder())
            self._button.Show()


    def OnButton(self, event):
        """
        Default event handler for the `Close` button in :class:`InfoBar`.

        :param `event`: a :class:`CommandEvent` to be processed.

        :note:

             Notice that the generic :class:`InfoBar` implementation handles the button events itself
             and so they are not propagated to the info bar parent and you need to either inherit from
             :class:`InfoBar` and handle them in your derived class or use `self.Bind(...)` to handle the
             button events in the parent frame.
        """

        self.DoHide()


    def SetShowHideEffects(self, showEffect, hideEffect):
        """
        Set the effects to use when showing and hiding the bar.

        Either or both of the parameters can be set to ``wx.SHOW_EFFECT_NONE`` to disable using
        effects entirely.

        By default, the info bar uses ``wx.SHOW_EFFECT_SLIDE_TO_BOTTOM`` effect for showing itself
        and ``wx.SHOW_EFFECT_SLIDE_TO_TOP`` for hiding if it is the first element of the containing
        sizer and reverse effects if it's the last one. If it is neither the first nor the last element,
        no effect is used to avoid the use of an inappropriate one and this function must be called
        if an effect is desired.

        :param integer `showEffect`: the effect to use when showing the bar;
        :param integer `hideEffect`: the effect to use when hiding the bar.

        The `showEffect` and `hideEffect` parameters can take one of the following bit:

        ==================================== ===========================================================
        `ShowEffect` Flag                    Description
        ==================================== ===========================================================
        ``SHOW_EFFECT_NONE``                 No effect, equivalent to normal `Show()` or `Hide()` call.
        ``SHOW_EFFECT_ROLL_TO_LEFT``         Roll window to the left.
        ``SHOW_EFFECT_ROLL_TO_RIGHT``        Roll window to the right.
        ``SHOW_EFFECT_ROLL_TO_TOP``          Roll window to the top.
        ``SHOW_EFFECT_ROLL_TO_BOTTOM``       Roll window to the bottom.
        ``SHOW_EFFECT_SLIDE_TO_LEFT``        Slide window to the left.
        ``SHOW_EFFECT_SLIDE_TO_RIGHT``       Slide window to the right.
        ``SHOW_EFFECT_SLIDE_TO_TOP``         Slide window to the top.
        ``SHOW_EFFECT_SLIDE_TO_BOTTOM``      Slide window to the bottom.
        ``SHOW_EFFECT_BLEND``                Fade in or out effect.
        ``SHOW_EFFECT_EXPAND``               Expanding or collapsing effect.
        ==================================== ===========================================================

        """

        self._showEffect = showEffect
        self._hideEffect = hideEffect


    def SetEffectDuration(self, duration):
        """
        Sets the duration of the animation used when showing or hiding the bar.

        By default, 500ms duration is used.

        :param integer `duration`: duration of the animation, in milliseconds.
        """

        self._effectDuration = duration


    def GetEffectDuration(self):
        """ Return the effect animation duration currently used, in milliseconds. """

        return self._effectDuration


if __name__ == '__main__':

    import wx

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, 'InfoBar Demo')

            self._infoBar = InfoBar(self)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self._infoBar, wx.SizerFlags().Expand())

            panel = wx.Panel(self)
            sizer.Add(panel, 1, wx.EXPAND)

            # ... Add other frame controls to the sizer ...
            self.SetSizer(sizer)

            wx.CallLater(2000, self.SomeMethod)


        def SomeMethod(self):

            self._infoBar.ShowMessage("Something happened", wx.ICON_INFORMATION)


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()

