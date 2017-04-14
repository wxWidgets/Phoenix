# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         buttonbar.py
# Purpose:
#
# Author:       Andrea Gavana <andrea.gavana@gmail.com>
#
# Created:
# Version:
# Date:
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, documented, py3-port
#----------------------------------------------------------------------------
"""
A ribbon button bar is similar to a traditional toolbar.


Description
===========

It contains one or more buttons (button bar buttons, not :class:`Button`), each of which
has a label and an icon. It differs from a :class:`toolbar` in several ways:

- Individual buttons can grow and contract.
- Buttons have labels as well as bitmaps.
- Bitmaps are typically larger (at least 32x32 pixels) on a button bar compared to
  a tool bar (which typically has 16x15).
- There is no grouping of buttons on a button bar
- A button bar typically has a border around each individual button, whereas a tool
  bar typically has a border around each group of buttons.


Events Processing
=================

This class processes the following events:

======================================== ========================================
Event Name                               Description
======================================== ========================================
``EVT_RIBBONBUTTONBAR_CLICKED``          Triggered when the normal (non-dropdown) region of a button on the button bar is clicked.
``EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED`` Triggered when the dropdown region of a button on the button bar is clicked. :meth:`RibbonButtonBarEvent.PopupMenu() <RibbonButtonBarEvent.PopupMenu>` should be called by the event handler if it wants to display a popup menu (which is what most dropdown buttons should be doing).
======================================== ========================================

"""

import wx

import six

from .control import RibbonControl
from .art import *

wxEVT_COMMAND_RIBBONBUTTON_CLICKED = wx.NewEventType()
wxEVT_COMMAND_RIBBONBUTTON_DROPDOWN_CLICKED = wx.NewEventType()

EVT_RIBBONBUTTONBAR_CLICKED = wx.PyEventBinder(wxEVT_COMMAND_RIBBONBUTTON_CLICKED, 1)
EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED = wx.PyEventBinder(wxEVT_COMMAND_RIBBONBUTTON_DROPDOWN_CLICKED, 1)


class RibbonButtonBarButtonSizeInfo(object):

    def __init__(self):

        self.is_supported = True
        self.size = wx.Size()
        self.normal_region = wx.Rect()
        self.dropdown_region = wx.Rect()


class RibbonButtonBarButtonInstance(object):

    def __init__(self):

        self.position = wx.Point()
        self.base = None
        self.size = wx.Size()


class RibbonButtonBarButtonBase(object):

    def __init__(self):

        self.label = ""
        self.help_string = ""
        self.bitmap_large = wx.NullBitmap
        self.bitmap_large_disabled = wx.NullBitmap
        self.bitmap_small = wx.NullBitmap
        self.bitmap_small_disabled = wx.NullBitmap
        self.sizes = [RibbonButtonBarButtonSizeInfo() for i in range(3)]
        self.client_data = None
        self.id = -1
        self.kind = None
        self.state = None


    def NewInstance(self):

        i = RibbonButtonBarButtonInstance()
        i.base = self
        return i


    def GetLargestSize(self):

        if self.sizes[RIBBON_BUTTONBAR_BUTTON_LARGE].is_supported:
            return RIBBON_BUTTONBAR_BUTTON_LARGE
        if self.sizes[RIBBON_BUTTONBAR_BUTTON_MEDIUM].is_supported:
            return RIBBON_BUTTONBAR_BUTTON_MEDIUM

        return RIBBON_BUTTONBAR_BUTTON_SMALL


    def GetSmallerSize(self, size, n=1):

        for i in range(n, 0, -1):

            if size == RIBBON_BUTTONBAR_BUTTON_LARGE:
                if self.sizes[RIBBON_BUTTONBAR_BUTTON_MEDIUM].is_supported:
                    return True, RIBBON_BUTTONBAR_BUTTON_MEDIUM

            elif size == RIBBON_BUTTONBAR_BUTTON_MEDIUM:
                if self.sizes[RIBBON_BUTTONBAR_BUTTON_SMALL].is_supported:
                    return True, RIBBON_BUTTONBAR_BUTTON_SMALL

            else:
                return False, None


class RibbonButtonBarLayout(object):

    def __init__(self):

        self.overall_size = wx.Size()
        self.buttons = []


    def CalculateOverallSize(self):

        self.overall_size = wx.Size(0, 0)

        for instance in self.buttons:
            size = instance.base.sizes[instance.size].size
            right = instance.position.x + size.GetWidth()
            bottom = instance.position.y + size.GetHeight()

            if right > self.overall_size.GetWidth():
                self.overall_size.SetWidth(right)
            if bottom > self.overall_size.GetHeight():
                self.overall_size.SetHeight(bottom)


    def FindSimilarInstance(self, inst):

        if inst is None:
            return None

        for instance in self.buttons:
            if instance.base == inst.base:
                return instance

        return None


class RibbonButtonBarEvent(wx.PyCommandEvent):
    """
    Event used to indicate various actions relating to a button on a :class:`RibbonButtonBar`.

    .. seealso:: :class:`RibbonButtonBar` for available event types.
    """

    def __init__(self, command_type=None, win_id=0, bar=None):
        """
        Default class constructor.

        :param integer `command_type`: the event type;
        :param integer `win_id`: the event identifier;
        :param `bar`: an instance of :class:`RibbonButtonBar`.
        """

        wx.PyCommandEvent.__init__(self, command_type, win_id)
        self._bar = bar


    def GetBar(self):
        """
        Returns the bar which contains the button which the event relates to.

        :returns: An instance of :class:`RibbonButtonBar`.
        """

        return self._bar


    def SetBar(self, bar):
        """
        Sets the button bar relating to this event.

        :param `bar`: an instance of :class:`RibbonButtonBar`.

        """

        self._bar = bar


    def PopupMenu(self, menu):
        """
        Display a popup menu as a result of this (dropdown clicked) event.

        :param `menu`: an instance of :class:`wx.Menu`.
        """

        pos = wx.Point()

        if self._bar._active_button:
            size = self._bar._active_button.base.sizes[self._bar._active_button.size]
            btn_rect = wx.Rect()
            btn_rect.SetTopLeft(self._bar._layout_offset + self._bar._active_button.position)
            btn_rect.SetSize(wx.Size(*size.size))
            pos = btn_rect.GetBottomLeft()
            pos.y += 1

        return self._bar.PopupMenu(menu, pos)


class RibbonButtonBar(RibbonControl):
    """ A ribbon button bar is similar to a traditional toolbar. """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, agwStyle=0):
        """
        Default class constructor.

        :param `parent`: pointer to a parent window, typically a :class:`~wx.lib.agw.ribbon.panel.RibbonPanel`;
        :type `parent`: :class:`wx.Window`
        :param integer `id`: window identifier. If ``wx.ID_ANY``, will automatically create
         an identifier;
        :param `pos`: window position. ``wx.DefaultPosition`` indicates that wxPython
         should generate a default position for the window;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: window size. ``wx.DefaultSize`` indicates that wxPython should
         generate a default size for the window. If no suitable size can be found, the
         window will be sized to 20x20 pixels so that the window is visible but obviously
         not correctly sized;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `agwStyle`: the AGW-specific window style, currently unused.
        """

        RibbonControl.__init__(self, parent, id, pos, size, style=wx.BORDER_NONE)

        self._layouts_valid = False
        self.CommonInit(agwStyle)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)


    def AddButton(self, button_id, label, bitmap, bitmap_small=wx.NullBitmap, bitmap_disabled=wx.NullBitmap,
                  bitmap_small_disabled=wx.NullBitmap, kind=RIBBON_BUTTON_NORMAL, help_string="", client_data=None):
        """
        Add a button to the button bar.

        :param integer `button_id`: id of the new button (used for event callbacks);
        :param string `label`: label of the new button;
        :param `bitmap`: large bitmap of the new button, an instance of :class:`wx.Bitmap`. Must be the same size as
         all other large bitmaps used on the button bar;
        :param `bitmap_small`: small bitmap of the new button, an instance of :class:`wx.Bitmap`. If left as :class:`NullBitmap`,
         then a small bitmap will be automatically generated. Must be the same size
         as all other small bitmaps used on the button bar;
        :param `bitmap_disabled`: large bitmap of the new button when it is disabled, an instance of :class:`wx.Bitmap`.
         If left as :class:`NullBitmap`, then a bitmap will be automatically generated from `bitmap`;
        :param `bitmap_small_disabled`: small bitmap of the new button when it is disabled, an instance of :class:`wx.Bitmap`.
         If left as :class:`NullBitmap`, then a bitmap will be automatically generated from `bitmap_small`;
        :param integer `kind`: the kind of button to add, one of the following values:

         ========================================== =========== ==========================================
         Button Kind                                Hex Value   Description
         ========================================== =========== ==========================================
         ``RIBBON_BUTTON_NORMAL``                           0x1 Normal button or tool with a clickable area which causes some generic action.
         ``RIBBON_BUTTON_DROPDOWN``                         0x2 Dropdown button or tool with a clickable area which typically causes a dropdown menu.
         ``RIBBON_BUTTON_HYBRID``                           0x3 Button or tool with two clickable areas - one which causes a dropdown menu, and one which causes a generic action.
         ``RIBBON_BUTTON_TOGGLE``                           0x4 Normal button or tool with a clickable area which toggles the button between a pressed and unpressed state.
         ========================================== =========== ==========================================

        :param string `help_string`: the UI help string to associate with the new button;
        :param object `client_data`: client data to associate with the new button (any Python object).

        :returns: An opaque pointer which can be used only with other button bar methods.

        :see: :meth:`~RibbonButtonBar.InsertButton`, :meth:`~RibbonButtonBar.AddDropdownButton`, :meth:`~RibbonButtonBar.AddHybridButton`
        """

        return self.InsertButton(self.GetButtonCount(), button_id, label, bitmap,
                                 bitmap_small, bitmap_disabled, bitmap_small_disabled, kind, help_string,
                                 client_data)


    def AddSimpleButton(self, button_id, label, bitmap, help_string, kind=RIBBON_BUTTON_NORMAL):
        """
        Add a button to the button bar (simple version).

        :param integer `button_id`: id of the new button (used for event callbacks);
        :param string `label`: label of the new button;
        :param `bitmap`: large bitmap of the new button, an instance of :class:`wx.Bitmap`. Must be the same size as
         all other large bitmaps used on the button bar;
        :param string `help_string`: the UI help string to associate with the new button;
        :param integer `kind`: the kind of button to add.

        :returns: An opaque pointer which can be used only with other button bar methods.

        :see: :meth:`~RibbonButtonBar.AddButton` for a list of valid button `kind` values.
        """

        return self.AddButton(button_id, label, bitmap, wx.NullBitmap, wx.NullBitmap,
                              wx.NullBitmap, kind, help_string)


    def InsertButton(self, pos, button_id, label, bitmap, bitmap_small=wx.NullBitmap, bitmap_disabled=wx.NullBitmap,
                     bitmap_small_disabled=wx.NullBitmap, kind=RIBBON_BUTTON_NORMAL, help_string="", client_data=None):

        """
        Inserts a button in the button bar at the position specified by `pos`.

        :param integer `pos`: the position at which the new button must be inserted (zero-based);
        :param integer `button_id`: id of the new button (used for event callbacks);
        :param string `label`: label of the new button;
        :param `bitmap`: large bitmap of the new button, an instance of :class:`wx.Bitmap`. Must be the same size as
         all other large bitmaps used on the button bar;
        :param `bitmap_small`: small bitmap of the new button, an instance of :class:`wx.Bitmap`. If left as :class:`NullBitmap`,
         then a small bitmap will be automatically generated. Must be the same size
         as all other small bitmaps used on the button bar;
        :param `bitmap_disabled`: large bitmap of the new button when it is disabled, an instance of :class:`wx.Bitmap`.
         If left as :class:`NullBitmap`, then a bitmap will be automatically generated from `bitmap`;
        :param `bitmap_small_disabled`: small bitmap of the new button when it is disabled, an instance of :class:`wx.Bitmap`.
         If left as :class:`NullBitmap`, then a bitmap will be automatically generated from `bitmap_small`;
        :param integer `kind`: the kind of button to add;
        :param string `help_string`: the UI help string to associate with the new button;
        :param object `client_data`: client data to associate with the new button.

        :returns: An opaque pointer which can be used only with other button bar methods.

        :raise: `Exception` if both `bitmap` and `bitmap_small` are invalid or if the input `help_string` is not
         a valid Python `basestring`.

        :see: :meth:`~RibbonButtonBar.AddDropdownButton`, :meth:`~RibbonButtonBar.AddHybridButton` and :meth:`~RibbonButtonBar.AddButton` for a list of valid button `kind` values.

        .. versionadded:: 0.9.5
        """

        if not bitmap.IsOk() and not bitmap_small.IsOk():
            raise Exception("Invalid main bitmap")

        if not isinstance(help_string, six.string_types):
            raise Exception("Invalid help string parameter")

        if not self._buttons:
            if bitmap.IsOk():

                self._bitmap_size_large = bitmap.GetSize()
                if not bitmap_small.IsOk():
                    w, h = self._bitmap_size_large
                    self._bitmap_size_small = wx.Size(0.5*w, 0.5*h)

            if bitmap_small.IsOk():

                self._bitmap_size_small = bitmap_small.GetSize()
                if not bitmap.IsOk():
                    w, h = self._bitmap_size_small
                    self._bitmap_size_large = wx.Size(2*w, 2*h)

        base = RibbonButtonBarButtonBase()
        base.id = button_id
        base.label = label
        base.bitmap_large = bitmap

        if not base.bitmap_large.IsOk():
            base.bitmap_large = self.MakeResizedBitmap(base.bitmap_small, self._bitmap_size_large)

        elif base.bitmap_large.GetSize() != self._bitmap_size_large:
            base.bitmap_large = self.MakeResizedBitmap(base.bitmap_large, self._bitmap_size_large)

        base.bitmap_small = bitmap_small

        if not base.bitmap_small.IsOk():
            base.bitmap_small = self.MakeResizedBitmap(base.bitmap_large, self._bitmap_size_small)

        elif base.bitmap_small.GetSize() != self._bitmap_size_small:
            base.bitmap_small = self.MakeResizedBitmap(base.bitmap_small, self._bitmap_size_small)

        base.bitmap_large_disabled = bitmap_disabled

        if not base.bitmap_large_disabled.IsOk():
            base.bitmap_large_disabled = self.MakeDisabledBitmap(base.bitmap_large)

        base.bitmap_small_disabled = bitmap_small_disabled

        if not base.bitmap_small_disabled.IsOk():
            base.bitmap_small_disabled = self.MakeDisabledBitmap(base.bitmap_small)

        base.kind = kind
        base.help_string = help_string
        base.client_data = client_data
        base.state = 0

        temp_dc = wx.ClientDC(self)
        self.FetchButtonSizeInfo(base, RIBBON_BUTTONBAR_BUTTON_SMALL, temp_dc)
        self.FetchButtonSizeInfo(base, RIBBON_BUTTONBAR_BUTTON_MEDIUM, temp_dc)
        self.FetchButtonSizeInfo(base, RIBBON_BUTTONBAR_BUTTON_LARGE, temp_dc)

        self._buttons.insert(pos, base)
        self._layouts_valid = False

        return base


    def AddDropdownButton(self, button_id, label, bitmap, help_string=""):
        """
        Add a dropdown button to the button bar (simple version).

        :param integer `button_id`: id of the new button (used for event callbacks);
        :param string `label`: label of the new button;
        :param `bitmap`: large bitmap of the new button, an instance of :class:`wx.Bitmap`. Must be the same size as
         all other large bitmaps used on the button bar;
        :param string `help_string`: the UI help string to associate with the new button.

        :returns: An opaque pointer which can be used only with other button bar methods.

        :see: :meth:`~RibbonButtonBar.AddButton`, :meth:`~RibbonButtonBar.InsertDropdownButton`, :meth:`~RibbonButtonBar.InsertButton`
        """

        return self.AddSimpleButton(button_id, label, bitmap, kind=RIBBON_BUTTON_DROPDOWN, help_string=help_string)


    def InsertDropdownButton(self, pos, button_id, label, bitmap, help_string=""):
        """
        Inserts a dropdown button in the button bar at the position specified by `pos`.

        :param integer `pos`: the position at which the new button must be inserted (zero-based);
        :param integer `button_id`: id of the new button (used for event callbacks);
        :param string `label`: label of the new button;
        :param `bitmap`: large bitmap of the new button, an instance of :class:`wx.Bitmap`. Must be the same size as
         all other large bitmaps used on the button bar;
        :param string `help_string`: the UI help string to associate with the new button.

        :returns: An opaque pointer which can be used only with other button bar methods.

        :see: :meth:`~RibbonButtonBar.AddButton`, :meth:`~RibbonButtonBar.InsertButton`, :meth:`~RibbonButtonBar.AddDropdownButton`

        .. versionadded:: 0.9.5
        """

        return self.InsertButton(pos, button_id, label, bitmap, kind=RIBBON_BUTTON_DROPDOWN, help_string=help_string)


    def AddToggleButton(self, button_id, label, bitmap, help_string=""):
        """
        Add a toggle button to the button bar.

        :param integer `button_id`: id of the new button (used for event callbacks);
        :param string `label`: label of the new button;
        :param `bitmap`: large bitmap of the new button, an instance of :class:`wx.Bitmap`. Must be the same size as
         all other large bitmaps used on the button bar;
        :param string `help_string`: the UI help string to associate with the new button.

        :returns: An opaque pointer which can be used only with other button bar methods.

        :see: :meth:`~RibbonButtonBar.AddButton`, :meth:`~RibbonButtonBar.InsertButton`, :meth:`~RibbonButtonBar.InsertToggleButton`
        """

        return self.AddButton(button_id, label, bitmap, kind=RIBBON_BUTTON_TOGGLE, help_string=help_string)


    def InsertToggleButton(self, pos, button_id, label, bitmap, help_string=""):
        """
        Inserts a toggle button in the button bar at the position specified by `pos`.

        :param integer `pos`: the position at which the new button must be inserted (zero-based);
        :param integer `button_id`: id of the new button (used for event callbacks);
        :param string `label`: label of the new button;
        :param `bitmap`: large bitmap of the new button, an instance of :class:`wx.Bitmap`. Must be the same size as
         all other large bitmaps used on the button bar;
        :param string `help_string`: the UI help string to associate with the new button.

        :returns: An opaque pointer which can be used only with other button bar methods.

        :see: :meth:`~RibbonButtonBar.AddButton`, :meth:`~RibbonButtonBar.InsertButton`, :meth:`~RibbonButtonBar.AddToggleButton`

        .. versionadded:: 0.9.5
        """

        return self.InsertButton(pos, button_id, label, bitmap, kind=RIBBON_BUTTON_TOGGLE, help_string=help_string)


    def AddHybridButton(self, button_id, label, bitmap, help_string=""):
        """
        Add a hybrid button to the button bar (simple version).

        :param integer `button_id`: id of the new button (used for event callbacks);
        :param string `label`: label of the new button;
        :param `bitmap`: large bitmap of the new button, an instance of :class:`wx.Bitmap`. Must be the same size as
         all other large bitmaps used on the button bar;
        :param string `help_string`: the UI help string to associate with the new button.

        :returns: An opaque pointer which can be used only with other button bar methods.

        :see: :meth:`~RibbonButtonBar.AddButton`, :meth:`~RibbonButtonBar.InsertButton`, :meth:`~RibbonButtonBar.InsertHybridButton`
        """

        return self.AddSimpleButton(button_id, label, bitmap, kind=RIBBON_BUTTON_HYBRID, help_string=help_string)


    def InsertHybridButton(self, pos, button_id, label, bitmap, help_string=""):
        """
        Inserts a hybrid button in the button bar at the position specified by `pos`.

        :param integer `pos`: the position at which the new button must be inserted (zero-based);
        :param integer `button_id`: id of the new button (used for event callbacks);
        :param string `label`: label of the new button;
        :param `bitmap`: large bitmap of the new button, an instance of :class:`wx.Bitmap`. Must be the same size as
         all other large bitmaps used on the button bar;
        :param string `help_string`: the UI help string to associate with the new button.

        :returns: An opaque pointer which can be used only with other button bar methods.

        :see: :meth:`~RibbonButtonBar.AddButton`, :meth:`~RibbonButtonBar.InsertButton`, :meth:`~RibbonButtonBar.AddHybridButton`

        .. versionadded:: 0.9.5
        """

        return self.InsertButton(pos, button_id, label, bitmap, kind=RIBBON_BUTTON_HYBRID, help_string=help_string)


    def FetchButtonSizeInfo(self, button, size, dc):

        info = button.sizes[size]

        if self._art:

            info.is_supported, info.size, info.normal_region, info.dropdown_region = \
                               self._art.GetButtonBarButtonSize(dc, self, button.kind, size, button.label,
                                                                self._bitmap_size_large, self._bitmap_size_small)

        else:
            info.is_supported = False


    def MakeResizedBitmap(self, original, size):
        """
        Resize and scale the `original` bitmap to the dimensions specified in `size`.

        :param `original`: the original bitmap, an instance of :class:`wx.Bitmap`;
        :param `size`: the size to which the input bitmap must be rescaled, an instance of :class:`wx.Size`.

        :return: A scaled representation of the input bitmap.
        """

        img = original.ConvertToImage()
        img.Rescale(size.GetWidth(), size.GetHeight(), wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(img)


    def MakeDisabledBitmap(self, original):
        """
        Converts the `original` bitmap into a visually-looking disabled one.

        :param `original`: the original bitmap, an instance of :class:`wx.Bitmap`.

        :return: A visually-looking disabled representation of the input bitmap.
        """

        img = original.ConvertToImage()
        return wx.Bitmap(img.ConvertToGreyscale())


    def Realize(self):
        """
        Calculate button layouts and positions.

        Must be called after buttons are added to the button bar, as otherwise the newly
        added buttons will not be displayed. In normal situations, it will be called
        automatically when :meth:`RibbonBar.Realize() <lib.agw.ribbon.bar.RibbonBar.Realize>` is called.

        :note: Reimplemented from :class:`~wx.lib.agw.ribbon.control.RibbonControl`.
        """

        if not self._layouts_valid:
            self.MakeLayouts()
            self._layouts_valid = True

        return True


    def ClearButtons(self):
        """
        Delete all buttons from the button bar.

        :see: :meth:`~RibbonButtonBar.DeleteButton`
        """

        self._layouts_valid = False
        self._buttons = []
        self.Realize()


    def DeleteButton(self, button_id):
        """
        Delete a single button from the button bar.

        :param integer `button_id`: id of the button to delete.

        :return: ``True`` if the button has been found and successfully deleted, ``False`` otherwise.

        :see: :meth:`~RibbonButtonBar.ClearButtons`
        """

        for button in self._buttons:
            if button.id == button_id:
                self._layouts_valid = False
                self._buttons.pop(button)
                self.Realize()
                self.Refresh()
                return True

        return False


    def EnableButton(self, button_id, enable=True):
        """
        Enable or disable a single button on the bar.

        :param integer `button_id`: id of the button to enable or disable;
        :param bool `enable`: ``True`` to enable the button, ``False`` to disable it.

        :raise: `Exception` when the input `button_id` could not be associated
         with a :class:`RibbonButtonBar` button.
        """

        for button in self._buttons:
            if button.id == button_id:
                if enable:
                    if button.state & RIBBON_BUTTONBAR_BUTTON_DISABLED:
                        button.state &= ~RIBBON_BUTTONBAR_BUTTON_DISABLED
                        self.Refresh()
                else:
                    if button.state & RIBBON_BUTTONBAR_BUTTON_DISABLED == 0:
                        button.state |= RIBBON_BUTTONBAR_BUTTON_DISABLED
                        self.Refresh()

                return

        raise Exception('Invalid button id specified.')


    def ToggleButton(self, button_id, checked=True):
        """
        Toggles/untoggles a :class:`RibbonButtonBar` toggle button.

        :param integer `button_id`: id of the button to be toggles/untoggled;
        :param bool `checked`: ``True`` to toggle the button, ``False`` to untoggle it.

        :raise: `Exception` when the input `button_id` could not be associated
         with a :class:`RibbonButtonBar` button.
        """

        for button in self._buttons:
            if button.id == button_id:
                if checked:
                    if button.state & RIBBON_BUTTONBAR_BUTTON_TOGGLED == 0:
                        button.state |= RIBBON_BUTTONBAR_BUTTON_TOGGLED
                        self.Refresh()
                else:
                    if button.state & RIBBON_BUTTONBAR_BUTTON_TOGGLED:
                        button.state &= ~RIBBON_BUTTONBAR_BUTTON_TOGGLED
                        self.Refresh()

                return

        raise Exception('Invalid button id specified.')


    def IsButtonEnabled(self, button_id):
        """
        Returns whether a button in the bar is enabled or not.

        :param integer `button_id`: id of the button to check.

        :return: ``True`` if the button is enabled, ``False`` otherwise.

        :raise: `Exception` when the input `button_id` could not be associated
         with a :class:`RibbonButtonBar` button.
        """

        for button in self._buttons:
            if button.id == button_id:
                if button.state & RIBBON_BUTTONBAR_BUTTON_DISABLED:
                    return False
                return True

        raise Exception('Invalid button id specified.')


    def GetButtonCount(self):
        """
        Returns the number of buttons in this :class:`RibbonButtonBar`.

        .. versionadded:: 0.9.5
        """

        return len(self._buttons)


    def SetArtProvider(self, art):
        """
        Set the art provider to be used.

        In many cases, setting the art provider will also set the art provider on all
        child windows which extend :class:`~wx.lib.agw.ribbon.control.RibbonControl`. In most cases, controls will not
        take ownership of the given pointer, with the notable exception being
        :meth:`RibbonBar.SetArtProvider() <lib.agw.ribbon.bar.RibbonBar.SetArtProvider>`.

        :param `art`: an art provider.
        """

        if art == self._art:
            return

        RibbonControl.SetArtProvider(self, art)

        temp_dc = wx.ClientDC(self)
        for base in self._buttons:
            self.FetchButtonSizeInfo(base, RIBBON_BUTTONBAR_BUTTON_SMALL, temp_dc)
            self.FetchButtonSizeInfo(base, RIBBON_BUTTONBAR_BUTTON_MEDIUM, temp_dc)
            self.FetchButtonSizeInfo(base, RIBBON_BUTTONBAR_BUTTON_LARGE, temp_dc)

        self._layouts_valid = False
        self.Realize()


    def IsSizingContinuous(self):
        """
        Returns ``True`` if this window can take any size (greater than its minimum size),
        ``False`` if it can only take certain sizes.

        :see: :meth:`RibbonControl.GetNextSmallerSize() <lib.agw.ribbon.control.RibbonControl.GetNextSmallerSize>`,
         :meth:`RibbonControl.GetNextLargerSize() <lib.agw.ribbon.control.RibbonControl.GetNextLargerSize>`
        """

        return False


    def DoGetNextSmallerSize(self, direction, _result):
        """
        Implementation of :meth:`RibbonControl.GetNextSmallerSize() <lib.agw.ribbon.control.RibbonControl.GetNextSmallerSize>`.

        Controls which have non-continuous sizing must override this virtual function
        rather than :meth:`RibbonControl.GetNextSmallerSize() <lib.agw.ribbon.control.RibbonControl.GetNextSmallerSize>`.

        :return: An instance of :class:`wx.Size`.
        """

        result = wx.Size(*_result)

        for i, layout in enumerate(self._layouts):
            size = wx.Size(*layout.overall_size)

            if direction == wx.HORIZONTAL:
                if size.x < result.x and size.y <= result.y:
                    result.x = size.x
                    break

            elif direction == wx.VERTICAL:
                if size.x <= result.x and size.y < result.y:
                    result.y = size.y
                    break

            elif direction == wx.BOTH:
                if size.x < result.x and size.y < result.y:
                    result = size
                    break

        return result


    def DoGetNextLargerSize(self, direction, _result):
        """
        Implementation of :meth:`RibbonControl.GetNextLargerSize() <lib.agw.ribbon.control.RibbonControl.GetNextLargerSize>`.

        Controls which have non-continuous sizing must override this virtual function
        rather than :meth:`RibbonControl.GetNextLargerSize() <lib.agw.ribbon.control.RibbonControl.GetNextLargerSize>`.

        :return: An instance of :class:`wx.Size`.
        """

        nlayouts = i = len(self._layouts)
        result = wx.Size(*_result)

        while 1:
            i -= 1
            layout = self._layouts[i]
            size = wx.Size(*layout.overall_size)

            if direction == wx.HORIZONTAL:
                if size.x > result.x and size.y <= result.y:
                    result.x = size.x
                    break

            elif direction == wx.VERTICAL:
                if size.x <= result.x and size.y > result.y:
                    result.y = size.y
                    break

            elif direction == wx.BOTH:
                if size.x > result.x and size.y > result.y:
                    result = size
                    break

            if i <= 0:
                break

        return result


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`RibbonButtonBar`.

        :param `event`: a :class:`EraseEvent` event to be processed.
        """

        # All painting done in main paint handler to minimise flicker
        pass


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`RibbonButtonBar`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.AutoBufferedPaintDC(self)
        self._art.DrawButtonBarBackground(dc, self, wx.Rect(0, 0, *self.GetSize()))

        layout = self._layouts[self._current_layout]

        for button in layout.buttons:
            base = button.base

            bitmap = base.bitmap_large
            bitmap_small = base.bitmap_small

            if base.state & RIBBON_BUTTONBAR_BUTTON_DISABLED:
                bitmap = base.bitmap_large_disabled
                bitmap_small = base.bitmap_small_disabled

            rect = wx.Rect(button.position + self._layout_offset, base.sizes[button.size].size)
            self._art.DrawButtonBarButton(dc, self, rect, base.kind, base.state | button.size, base.label, bitmap, bitmap_small)


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`RibbonButtonBar`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        new_size = event.GetSize()
        layout_count = len(self._layouts)
        self._current_layout = layout_count - 1

        for layout_i in range(layout_count):

            layout_size = self._layouts[layout_i].overall_size
            if layout_size.x <= new_size.x and layout_size.y <= new_size.y:
                self._layout_offset.x = (new_size.x - layout_size.x)/2
                self._layout_offset.y = (new_size.y - layout_size.y)/2
                self._current_layout = layout_i
                break

        self._hovered_button = self._layouts[self._current_layout].FindSimilarInstance(self._hovered_button)
        self.Refresh()


    def UpdateWindowUI(self, flags):
        """
        This function sends one or more :class:`UpdateUIEvent` to the window.

        The particular implementation depends on the window; for example a :class:`ToolBar` will
        send an update UI event for each toolbar button, and a :class:`wx.Frame` will send an
        update UI event for each menubar menu item.

        You can call this function from your application to ensure that your UI is up-to-date
        at this point (as far as your :class:`UpdateUIEvent` handlers are concerned). This may be
        necessary if you have called :meth:`UpdateUIEvent.SetMode` or :meth:`UpdateUIEvent.SetUpdateInterval`
        to limit the overhead that wxWidgets incurs by sending update UI events in idle time.

        :param integer `flags`: should be a bitlist of one or more of ``wx.UPDATE_UI_NONE``,
         ``wx.UPDATE_UI_RECURSE`` or ``wx.UPDATE_UI_FROMIDLE``.

        If you are calling this function from an `OnInternalIdle` or `OnIdle` function, make sure
        you pass the ``wx.UPDATE_UI_FROMIDLE`` flag, since this tells the window to only update
        the UI elements that need to be updated in idle time. Some windows update their elements
        only when necessary, for example when a menu is about to be shown. The following is an
        example of how to call :meth:`~RibbonButtonBar.UpdateWindowUI` from an idle function::

            def OnInternalIdle(self):

                if wx.UpdateUIEvent.CanUpdate(self):
                    self.UpdateWindowUI(wx.UPDATE_UI_FROMIDLE)



        .. versionadded:: 0.9.5
        """

        wx.Control.UpdateWindowUI(self, flags)

        # don't waste time updating state of tools in a hidden toolbar
        if not self.IsShown():
            return

        rerealize = False

        for button in self._buttons:

            id = button.id
            event = wx.UpdateUIEvent(id)
            event.SetEventObject(self)

            if self.ProcessWindowEvent(event):
                if event.GetSetEnabled():
                    self.EnableButton(id, event.GetEnabled())
                if event.GetSetChecked():
                    self.ToggleButton(id, event.GetChecked())
                if event.GetSetText():
                    button.label = event.GetText()
                    rerealize = True

        if rerealize:
            self.Realize()


    def CommonInit(self, agwStyle):
        """
        Common initialization procedures.

        :param integer `agwStyle`: the AGW-specific window style, currently unused.
        """

        self._bitmap_size_large = wx.Size(32, 32)
        self._bitmap_size_small = wx.Size(16, 16)

        self._layouts = []
        self._buttons = []

        placeholder_layout = RibbonButtonBarLayout()
        placeholder_layout.overall_size = wx.Size(20, 20)
        self._layouts.append(placeholder_layout)
        self._current_layout = 0
        self._layout_offset = wx.Point(0, 0)
        self._hovered_button = None
        self._active_button = None
        self._lock_active_state = False

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)


    def GetMinSize(self):
        """
        Returns the minimum size of the window, an indication to the sizer layout mechanism
        that this is the minimum required size.

        This method normally just returns the value set by `SetMinSize`, but it can be
        overridden to do the calculation on demand.

        :return: An instance of :class:`wx.Size`.
        """

        return wx.Size(*self._layouts[-1].overall_size)


    def DoGetBestSize(self):
        """
        Gets the size which best suits the window: for a control, it would be the
        minimal size which doesn't truncate the control, for a panel - the same size
        as it would have after a call to `Fit()`.

        :return: An instance of :class:`wx.Size`.

        :note: Overridden from :class:`wx.Control`.
        """

        return wx.Size(*self._layouts[0].overall_size)


    def MakeLayouts(self):

        if self._layouts_valid or self._art == None:
            return

        # Clear existing layouts
        if self._hovered_button:
            self._hovered_button.base.state &= ~RIBBON_BUTTONBAR_BUTTON_HOVER_MASK
            self._hovered_button = None

        if self._active_button:
            self._active_button.base.state &= ~RIBBON_BUTTONBAR_BUTTON_ACTIVE_MASK
            self._active_button = None

        self._layouts = []

        # Best layout : all buttons large, stacking horizontally
        layout = RibbonButtonBarLayout()
        cursor = wx.Point(0, 0)
        layout.overall_size.SetHeight(0)

        for button in self._buttons:
            instance = button.NewInstance()
            instance.position = wx.Point(*cursor)
            instance.size = button.GetLargestSize()
            size = wx.Size(*button.sizes[instance.size].size)
            cursor.x += size.GetWidth()
            layout.overall_size.SetHeight(max(layout.overall_size.GetHeight(), size.GetHeight()))
            layout.buttons.append(instance)

        layout.overall_size.SetWidth(cursor.x)
        self._layouts.append(layout)

        if len(self._buttons) >= 2:
            # Collapse the rightmost buttons and stack them vertically
            iLast = len(self._buttons) - 1
            result = True

            while result and iLast > 0:
                result, iLast = self.TryCollapseLayout(self._layouts[-1], iLast)
                iLast -= 1


    def TryCollapseLayout(self, original, first_btn, last_button=None):

        btn_count = len(self._buttons)
        used_height = 0
        used_width = 0
        available_width = 0
        available_height = 0

        count = first_btn + 1

        while 1:
            count -= 1

            button = self._buttons[count]
            large_size_class = button.GetLargestSize()
            large_size = button.sizes[large_size_class].size
            t_available_height = max(available_height, large_size.GetHeight())
            t_available_width = available_width + large_size.GetWidth()
            small_size_class = large_size_class

            result, small_size_class = button.GetSmallerSize(small_size_class)
            if not result:
                return False, count

            small_size = button.sizes[small_size_class].size
            t_used_height = used_height + small_size.GetHeight()
            t_used_width = max(used_width, small_size.GetWidth())

            if t_used_height > t_available_height:
                count += 1
                break

            else:
                used_height = t_used_height
                used_width = t_used_width
                available_width = t_available_width
                available_height = t_available_height

            if count <= 0:
                break

        if count >= first_btn or used_width >= available_width:
            return False, count

        if last_button != None:
            last_button = count

        layout = RibbonButtonBarLayout()
        for indx, button in enumerate(original.buttons):
            instance = RibbonButtonBarButtonInstance()
            instance.position = wx.Point(*button.position)
            instance.size = button.size
            instance.base = self._buttons[indx]
            layout.buttons.append(instance)

        cursor = wx.Point(*layout.buttons[count].position)
        preserve_height = False

        if count == 0:
            # If height isn't preserved (i.e. it is reduced), then the minimum
            # size for the button bar will decrease, preventing the original
            # layout from being used (in some cases).
            # It may be a good idea to always preverse the height, but for now
            # it is only done when the first button is involved in a collapse.
            preserve_height = True

        for btn_i in range(count, first_btn+1):
            instance = layout.buttons[btn_i]
            result, instance.size = instance.base.GetSmallerSize(instance.size)
            instance.position = wx.Point(*cursor)
            cursor.y += instance.base.sizes[instance.size].size.GetHeight()

        x_adjust = available_width - used_width

        for btn_i in range(first_btn+1, btn_count):
            instance = layout.buttons[btn_i]
            instance.position.x -= x_adjust

        layout.CalculateOverallSize()

##        # Sanity check
##        if layout.overall_size.GetWidth() >= original.overall_size.GetWidth() or \
##           layout.overall_size.GetHeight() > original.overall_size.GetHeight():
##
##            del layout
##            return False, count

        if preserve_height:
            layout.overall_size.SetHeight(original.overall_size.GetHeight())

        self._layouts.append(layout)
        return True, count


    def OnMouseMove(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`RibbonButtonBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        cursor = event.GetPosition()
        new_hovered = None
        new_hovered_state = 0

        layout = self._layouts[self._current_layout]

        for instance in layout.buttons:
            size = instance.base.sizes[instance.size]
            btn_rect = wx.Rect()
            btn_rect.SetTopLeft(self._layout_offset + instance.position)
            btn_rect.SetSize(size.size)

            if btn_rect.Contains(cursor) and self.IsButtonEnabled(instance.base.id):
                new_hovered = instance
                new_hovered_state = instance.base.state
                new_hovered_state &= ~RIBBON_BUTTONBAR_BUTTON_HOVER_MASK
                offset = wx.Point(*cursor)
                offset -= btn_rect.GetTopLeft()
                if size.normal_region.Contains(offset):
                    new_hovered_state |= RIBBON_BUTTONBAR_BUTTON_NORMAL_HOVERED

                if size.dropdown_region.Contains(offset):
                    new_hovered_state |= RIBBON_BUTTONBAR_BUTTON_DROPDOWN_HOVERED

                break

        if new_hovered == None and self.GetToolTip():
            self.SetToolTip("")

        if new_hovered != self._hovered_button or (self._hovered_button != None and \
                                                   new_hovered_state != self._hovered_button.base.state):

            if self._hovered_button != None:
                self._hovered_button.base.state &= ~RIBBON_BUTTONBAR_BUTTON_HOVER_MASK

            self._hovered_button = new_hovered
            if self._hovered_button != None:
                self._hovered_button.base.state = new_hovered_state
                self.SetToolTip(self._hovered_button.base.help_string)

            self.Refresh(False)

        if self._active_button and not self._lock_active_state:

            new_active_state = self._active_button.base.state
            new_active_state &= ~RIBBON_BUTTONBAR_BUTTON_ACTIVE_MASK
            size = self._active_button.base.sizes[self._active_button.size]
            btn_rect = wx.Rect()
            btn_rect.SetTopLeft(self._layout_offset + self._active_button.position)
            btn_rect.SetSize(size.size)

            if btn_rect.Contains(cursor):

                offset = wx.Point(*cursor)
                offset -= btn_rect.GetTopLeft()

                if size.normal_region.Contains(offset):
                    new_active_state |= RIBBON_BUTTONBAR_BUTTON_NORMAL_ACTIVE

                if size.dropdown_region.Contains(offset):
                    new_active_state |= RIBBON_BUTTONBAR_BUTTON_DROPDOWN_ACTIVE

            if new_active_state != self._active_button.base.state:
                self._active_button.base.state = new_active_state
                self.Refresh(False)


    def OnMouseDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`RibbonButtonBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        cursor = event.GetPosition()
        self._active_button = None

        layout = self._layouts[self._current_layout]

        for instance in layout.buttons:

            size = instance.base.sizes[instance.size]
            btn_rect = wx.Rect()
            btn_rect.SetTopLeft(self._layout_offset + instance.position)
            btn_rect.SetSize(size.size)

            if btn_rect.Contains(cursor) and self.IsButtonEnabled(instance.base.id):
                self._active_button = instance
                cursor -= btn_rect.GetTopLeft()
                state = 0
                if size.normal_region.Contains(cursor):
                    state = RIBBON_BUTTONBAR_BUTTON_NORMAL_ACTIVE
                elif size.dropdown_region.Contains(cursor):
                    state = RIBBON_BUTTONBAR_BUTTON_DROPDOWN_ACTIVE
                instance.base.state |= state
                self.Refresh(False)
                break


    def OnMouseUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`RibbonButtonBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        cursor = event.GetPosition()

        if self._active_button:

            size = self._active_button.base.sizes[self._active_button.size]
            btn_rect = wx.Rect()
            btn_rect.SetTopLeft(self._layout_offset + self._active_button.position)
            btn_rect.SetSize(size.size)

            if btn_rect.Contains(cursor):
                id = self._active_button.base.id
                cursor -= btn_rect.GetTopLeft()

                while 1:
                    if size.normal_region.Contains(cursor):
                        event_type = wxEVT_COMMAND_RIBBONBUTTON_CLICKED
                    elif size.dropdown_region.Contains(cursor):
                        event_type = wxEVT_COMMAND_RIBBONBUTTON_DROPDOWN_CLICKED
                    else:
                        break

                    notification = RibbonButtonBarEvent(event_type, id)

                    if self._active_button.base.kind == RIBBON_BUTTON_TOGGLE:
                        self._active_button.base.state ^= RIBBON_BUTTONBAR_BUTTON_TOGGLED
                        notification.SetInt(self._active_button.base.state & RIBBON_BUTTONBAR_BUTTON_TOGGLED)

                    notification.SetEventObject(self)
                    notification.SetBar(self)
                    self._lock_active_state = True
                    self.GetEventHandler().ProcessEvent(notification)
                    self._lock_active_state = False
                    break

                if self._active_button: # may have been Noneed by event handler
                    self._active_button.base.state &= ~RIBBON_BUTTONBAR_BUTTON_ACTIVE_MASK
                    self._active_button = None

                self.Refresh()


    def OnMouseEnter(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` event for :class:`RibbonButtonBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self._active_button and not event.LeftIsDown():
            self._active_button = None


    def OnMouseLeave(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`RibbonButtonBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        repaint = False
        if self._hovered_button != None:
            self._hovered_button.base.state &= ~RIBBON_BUTTONBAR_BUTTON_HOVER_MASK
            self._hovered_button = None
            repaint = True

        if self._active_button != None and not self._lock_active_state:
            self._active_button.base.state &= ~RIBBON_BUTTONBAR_BUTTON_ACTIVE_MASK
            repaint = True

        if repaint:
            self.Refresh(False)


    def GetDefaultBorder(self):
        """ Returns the default border style for :class:`RibbonButtonBar`. """

        return wx.BORDER_NONE


