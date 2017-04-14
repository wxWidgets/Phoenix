#----------------------------------------------------------------------------
# Name:         ColourSelect.py
# Purpose:      Colour Box Selection Control
#
# Author:       Lorne White, Lorne.White@telusplanet.net
#
# Created:      Feb 25, 2001
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, documented
#----------------------------------------------------------------------------

# creates a colour wxButton with selectable color
# button click provides a colour selection box
# button colour will change to new colour
# GetColour method to get the selected colour

# Updates:
# call back to function if changes made

# Cliff Wells, logiplexsoftware@earthlink.net:
# - Made ColourSelect into "is a button" rather than "has a button"
# - Added label parameter and logic to adjust the label colour according to the background
#   colour
# - Added id argument
# - Rearranged arguments to more closely follow wx conventions
# - Simplified some of the code

# Cliff Wells, 2002/02/07
# - Added ColourSelect Event

# 12/01/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o Updated for 2.5 compatibility.
#

"""
Provides a :class:`wx.ColourSelect` button that, when clicked, will display a
colour selection dialog.


Description
===========

This module provides a :class:`wx.ColourSelect` button that, when clicked, will display a
colour selection dialog. The selected colour is displayed on the button itself.


Usage
=====

Sample usage::

    import wx
    import wx.lib.colourselect as csel

    class MyFrame(wx.Frame):

        def __init__(self, parent, title):

            wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(400, 300))
            self.panel = wx.Panel(self)

            colour_button = csel.ColourSelect(self.panel, -1, "Choose...", wx.WHITE)
            colour_button.Bind(csel.EVT_COLOURSELECT, self.OnChooseBackground)

        def OnChooseBackground(self, event):

            col1 = event.GetValue()
            self.panel.SetBackgroundColour(col1)
            event.Skip()

    app = wx.App()
    frame = MyFrame(None, 'Select a colour')
    frame.Show()
    app.MainLoop()

"""

#----------------------------------------------------------------------------

import wx
import wx.lib.buttons
import functools

#----------------------------------------------------------------------------

wxEVT_COMMAND_COLOURSELECT = wx.NewEventType()

class ColourSelectEvent(wx.PyCommandEvent):
    """
    :class:`wx.ColourSelectEvent` is a special subclassing of :class:`wx.CommandEvent`
    and it provides for a custom event sent every time the user chooses a colour.
    """

    def __init__(self, id, value):
        """
        Default class constructor.

        :param integer `id`: the event identifier;
        :param wx.Colour `value`: the colour currently selected.
        """

        wx.PyCommandEvent.__init__(self, id = id)
        self.SetEventType(wxEVT_COMMAND_COLOURSELECT)
        self.value = value


    def GetValue(self):
        """
        Returns the currently selected colour.

        :rtype: :class:`wx.Colour`
        """

        return self.value


EVT_COLOURSELECT = wx.PyEventBinder(wxEVT_COMMAND_COLOURSELECT, 1)


#----------------------------------------------------------------------------

class CustomColourData(object):
    """
    A simple container for tracking custom colours to be shown in the colour
    dialog, and which facilitates reuse of this collection across multiple
    instances or multiple invocations of the :class:`ColourSelect` button.
    """
    COUNT = 16

    def __init__(self):
        self._customColours = [None] * self.COUNT


    @property
    def Colours(self):
        return self._customColours

    @Colours.setter
    def Colours(self, value):
        # slice it into the current list to keep the same list instance
        if isinstance(value, CustomColourData):
            value = value.Colours
        self._customColours[:] = value


#----------------------------------------------------------------------------


class ColourSelect(wx.lib.buttons.GenBitmapButton):
    """
    A subclass of :class:`wx.BitmapButton` that, when clicked, will
    display a colour selection dialog.
    """

    def __init__(self, parent, id=wx.ID_ANY, label="", colour=wx.BLACK,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 callback=None, style=0):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param string `label`: the button text label;
        :param wx.Colour: a valid :class:`wx.Colour` instance, which will be the default initial
         colour for this button;
        :type `colour`: :class:`wx.Colour` or tuple
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param PyObject `callback`: a callable method/function that will be called every time
         the user chooses a new colour;
        :param integer `style`: the button style.
        """

        size = wx.Size(*size)
        if label:
            mdc = wx.MemoryDC(wx.Bitmap(1,1))
            w, h = mdc.GetTextExtent(label)
            w += 8
            h += 8
        else:
            w, h = 22, 22

        size.width = size.width if size.width != -1 else w
        size.height = size.height if size.height != -1 else h
        super(ColourSelect, self).__init__(parent, id, wx.Bitmap(w,h),
                                 pos=pos, size=size, style=style,
                                 name='ColourSelect')

        if type(colour) == type( () ):
            colour = wx.Colour(*colour)

        self.colour = colour
        self.SetLabel(label)
        self.callback = callback
        bmp = self.MakeBitmap()
        self.SetBitmap(bmp)
        self.customColours = None
        parent.Bind(wx.EVT_BUTTON, self.OnClick, self)


    def GetColour(self):
        """
        Returns the current colour set for the :class:`ColourSelect`.

        :rtype: :class:`wx.Colour`
        """

        return self.colour


    def GetValue(self):
        """
        Returns the current colour set for the :class:`ColourSelect`.
        Same as :meth:`~ColourSelect.GetColour`.

        :rtype: :class:`wx.Colour`
        """

        return self.colour


    def SetValue(self, colour):
        """
        Sets the current colour for :class:`ColourSelect`.  Same as
        :meth:`~ColourSelect.SetColour`.

        :param `colour`: the new colour for :class:`ColourSelect`.
        :type `colour`: tuple or string or :class:`wx.Colour`
        """

        self.SetColour(colour)


    def SetColour(self, colour):
        """
        Sets the current colour for :class:`ColourSelect`.

        :param `colour`: the new colour for :class:`ColourSelect`.
        :type `colour`: tuple or string or :class:`wx.Colour`
        """

        self.colour = wx.Colour(colour)  # use the typmap or copy an existing colour object
        bmp = self.MakeBitmap()
        self.SetBitmap(bmp)


    def SetLabel(self, label):
        """
        Sets the new text label for :class:`wx.ColourSelect`.

        :param string `label`: the new text label for :class:`ColourSelect`.
        """

        self.label = label


    def GetLabel(self):
        """
        Returns the current text label for the :class:`ColourSelect`.

        :rtype: string
        """

        return self.label


    def GetCustomColours(self):
        """
        Returns the current set of custom colour values to be shown in the
        colour dialog, if supported.

        :rtype: :class:`CustomColourData`
        """
        return self.customColours


    def SetCustomColours(self, colours):
        """
        Sets the list of custom colour values to be shown in colour dialog, if
        supported.

        :param `colours`: An instance of :class:`CustomColourData` or a 16
        element list of ``None`` or :class:`wx.Colour` values.
        """
        if isinstance(colours, CustomColourData):
            colours = colours.Colours
        if self.customColours is None:
            self.customColours = CustomColourData()
        self.customColours.Colours = colours


    Colour = property(GetColour, SetColour)
    Value = property(GetValue, SetValue)
    Label = property(GetLabel, SetLabel)
    CustomColours = property(GetCustomColours, SetCustomColours)


    def MakeBitmap(self):
        """ Creates a bitmap representation of the current selected colour. """

        bdr = 8
        width, height = self.GetSize()

        # yes, this is weird, but it appears to work around a bug in wxMac
        if "wxMac" in wx.PlatformInfo and width == height:
            height -= 1

        bmp = wx.Bitmap(width-bdr, height-bdr)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetFont(self.GetFont())
        label = self.GetLabel()
        # Just make a little colored bitmap
        dc.SetBackground(wx.Brush(self.colour))
        dc.Clear()

        if label:
            # Add a label to it
            avg = functools.reduce(lambda a, b: a + b, self.colour.Get()) / 3
            fcolour = avg > 128 and wx.BLACK or wx.WHITE
            dc.SetTextForeground(fcolour)
            dc.DrawLabel(label, (0,0, width-bdr, height-bdr),
                         wx.ALIGN_CENTER)

        dc.SelectObject(wx.NullBitmap)
        return bmp


    def SetBitmap(self, bmp):
        """
        Sets the bitmap representation of the current selected colour to the button.

        :param wx.Bitmap `bmp`: the new bitmap.
        """

        self.SetBitmapLabel(bmp)
        self.Refresh()


    def OnChange(self):
        """ Fires the ``EVT_COLOURSELECT`` event, as the user has changed the current colour. """

        evt = ColourSelectEvent(self.GetId(), self.GetValue())
        evt.SetEventObject(self)
        wx.PostEvent(self, evt)
        if self.callback is not None:
            self.callback()


    def OnClick(self, event):
        """
        Handles the ``wx.EVT_BUTTON`` event for :class:`ColourSelect`.

        :param `event`: a :class:`wx.CommandEvent` event to be processed.
        """

        data = wx.ColourData()
        data.SetChooseFull(True)
        data.SetColour(self.colour)
        if self.customColours:
            for idx, clr in enumerate(self.customColours.Colours):
                if clr is not None:
                    data.SetCustomColour(idx, clr)

        dlg = wx.ColourDialog(wx.GetTopLevelParent(self), data)
        changed = dlg.ShowModal() == wx.ID_OK

        if changed:
            data = dlg.GetColourData()
            self.SetColour(data.GetColour())
            if self.customColours:
                self.customColours.Colours = \
                    [data.GetCustomColour(idx) for idx in range(0, 16)]

        dlg.Destroy()

        # moved after dlg.Destroy, since who knows what the callback will do...
        if changed:
            self.OnChange()

