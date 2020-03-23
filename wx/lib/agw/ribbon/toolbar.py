# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         toolbar.py
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
A ribbon tool bar is similar to a traditional toolbar which has no labels.


Description
===========

It contains one or more tool groups, each of which contains one or more tools.
Each tool is represented by a (generally small, i.e. 16x15) bitmap.


Events Processing
=================

This class processes the following events:

====================================== ======================================
Event Name                             Description
====================================== ======================================
``EVT_RIBBONTOOLBAR_CLICKED``          Triggered when the normal (non-dropdown) region of a tool on the tool bar is clicked.
``EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED`` Triggered when the dropdown region of a tool on the tool bar is clicked. LRibbonToolBarEvent.PopupMenu should be called by the event handler if it wants to display a popup menu (which is what most dropdown tools should be doing).
====================================== ======================================

"""

import wx

from .control import RibbonControl
from .panel import RibbonPanel

from .art import *

wxEVT_COMMAND_RIBBONTOOL_CLICKED = wx.NewEventType()
wxEVT_COMMAND_RIBBONTOOL_DROPDOWN_CLICKED = wx.NewEventType()

EVT_RIBBONTOOLBAR_CLICKED = wx.PyEventBinder(wxEVT_COMMAND_RIBBONTOOL_CLICKED, 1)
EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED = wx.PyEventBinder(wxEVT_COMMAND_RIBBONTOOL_DROPDOWN_CLICKED, 1)


def GetSizeInOrientation(size, orientation):

    if orientation == wx.HORIZONTAL:
        return size.GetWidth()

    if orientation == wx.VERTICAL:
        return size.GetHeight()

    if orientation == wx.BOTH:
        return size.GetWidth() * size.GetHeight()

    return 0


class RibbonToolBarEvent(wx.PyCommandEvent):
    """ Handles events related to :class:`RibbonToolBar`. """

    def __init__(self, command_type=None, win_id=0, bar=None):
        """
        Default class constructor.

        :param integer `command_type`: the event type;
        :param integer `win_id`: the event identifier;
        :param `bar`: an instance of :class:`RibbonToolBar`.
        """

        wx.PyCommandEvent.__init__(self, command_type, win_id)
        self._bar = bar


    def GetBar(self):
        """ Returns an instance of :class:`RibbonToolBar`. """

        return self._bar


    def SetBar(self, bar):
        """
        Sets the current :class:`RibbonToolBar` for this event.

        :param `bar`: an instance of :class:`RibbonToolBar`.
        """

        self._bar = bar


    def PopupMenu(self, menu):
        """
        Pops up the given menu and returns control when the user has dismissed the menu.

        If a menu item is selected, the corresponding menu event is generated and will
        be processed as usual.

        :param `menu`: the menu to pop up, an instance of :class:`wx.Menu`.

        :note: Just before the menu is popped up, :meth:`wx.Menu.UpdateUI` is called to ensure
         that the menu items are in the correct state. The menu does not get deleted by
         the window.
        """

        return self._bar.PopupMenu(menu)


class RibbonToolBarToolBase(object):

    def __init__(self):

        self.help_string = ""
        self.bitmap = wx.NullBitmap
        self.bitmap_disabled = wx.NullBitmap
        self.dropdown = wx.Rect()
        self.position = wx.Point()
        self.size = wx.Size()
        self.client_data = None
        self.id = -1
        self.kind = RIBBON_BUTTON_NORMAL
        self.state = None


class RibbonToolBarToolGroup(object):

    def __init__(self):

        # To identify the group as a RibbonToolBarToolBase
        self.dummy_tool = None

        self.tools = []
        self.position = wx.Point()
        self.size = wx.Size()


class RibbonToolBar(RibbonControl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 name="RibbonToolBar"):

        """
        Default class constructor.

        :param `parent`: pointer to a parent window, typically a :class:`~wx.lib.agw.ribbon.panel.RibbonPanel`;
        :param `id`: window identifier. If ``wx.ID_ANY``, will automatically create
         an identifier;
        :param `pos`: window position. ``wx.DefaultPosition`` indicates that wxPython
         should generate a default position for the window;
        :param `size`: window size. ``wx.DefaultSize`` indicates that wxPython should
         generate a default size for the window. If no suitable size can be found, the
         window will be sized to 20x20 pixels so that the window is visible but obviously
         not correctly sized;
        :param `style`: window style, currently unused.
        :param `name`: the window name.

        """

        RibbonControl.__init__(self, parent, id, pos, size, wx.BORDER_NONE, name=name)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.CommonInit(style)


    def CommonInit(self, style):

        self._groups = []

        self.AppendGroup()
        self._hover_tool = None
        self._active_tool = None
        self._nrows_min = 1
        self._nrows_max = 1
        self._sizes = [wx.Size(0, 0)]
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)


    def AddSimpleTool(self, tool_id, bitmap, help_string, kind=RIBBON_BUTTON_NORMAL):
        """
        Add a tool to the tool bar (simple version).

        :param `tool_id`: id of the new tool (used for event callbacks);
        :param `bitmap`: large bitmap of the new button. Must be the same size as all
         other large bitmaps used on the button bar;
        :param `help_string`: the UI help string to associate with the new button;
        :param `kind`: the kind of button to add.

        :see: :meth:`~RibbonToolBar.AddDropdownTool`, :meth:`~RibbonToolBar.AddHybridTool`, :meth:`~RibbonToolBar.AddTool`

        """

        return self.AddTool(tool_id, bitmap, wx.NullBitmap, help_string, kind, None)


    def AddDropdownTool(self, tool_id, bitmap, help_string=""):
        """
        Add a dropdown tool to the tool bar (simple version).

        :param `tool_id`: id of the new tool (used for event callbacks);
        :param `bitmap`: large bitmap of the new button. Must be the same size as all
         other large bitmaps used on the button bar;
        :param `help_string`: the UI help string to associate with the new button.

        :see: :meth:`~RibbonToolBar.AddTool`
        """

        return self.AddTool(tool_id, bitmap, wx.NullBitmap, help_string, RIBBON_BUTTON_DROPDOWN, None)


    def InsertDropdownTool(self, pos, tool_id, bitmap, help_string=""):
        """
        Inserts a dropdown tool in the tool bar at the position specified by `pos`.

        :param `pos`: the position of the new tool in the toolbar (zero-based);
        :param `tool_id`: id of the new tool (used for event callbacks);
        :param `bitmap`: large bitmap of the new button. Must be the same size as all
         other large bitmaps used on the button bar;
        :param `help_string`: the UI help string to associate with the new button.

        :see: :meth:`~RibbonToolBar.AddTool`, :meth:`~RibbonToolBar.InsertTool`

        .. versionadded:: 0.9.5
        """

        return self.InsertTool(pos, tool_id, bitmap, wx.NullBitmap, help_string, RIBBON_BUTTON_DROPDOWN, None)


    def AddHybridTool(self,  tool_id, bitmap, help_string=""):
        """
        Add a hybrid tool to the tool bar (simple version).

        :param `tool_id`: id of the new tool (used for event callbacks);
        :param `bitmap`: large bitmap of the new button. Must be the same size as all
         other large bitmaps used on the button bar;
        :param `help_string`: the UI help string to associate with the new button.

        :see: :meth:`~RibbonToolBar.AddTool`
        """

        return self.AddTool(tool_id, bitmap, wx.NullBitmap, help_string, RIBBON_BUTTON_HYBRID, None)


    def InsertHybridTool(self, pos, tool_id, bitmap, help_string=""):
        """
        Inserts a hybrid tool in the tool bar at the position specified by `pos`.

        :param `pos`: the position of the new tool in the toolbar (zero-based);
        :param `tool_id`: id of the new tool (used for event callbacks);
        :param `bitmap`: large bitmap of the new button. Must be the same size as all
         other large bitmaps used on the button bar;
        :param `help_string`: the UI help string to associate with the new button.

        :see: :meth:`~RibbonToolBar.AddTool`, :meth:`~RibbonToolBar.InsertTool`

        .. versionadded:: 0.9.5
        """

        return self.InsertTool(pos, tool_id, bitmap, wx.NullBitmap, help_string, RIBBON_BUTTON_HYBRID, None)


    def AddToggleTool(self, tool_id, bitmap, help_string=""):
        """
        Add a toggle tool to the tool bar (simple version).

        :param `tool_id`: id of the new tool (used for event callbacks);
        :param `bitmap`: large bitmap of the new button. Must be the same size as all
         other large bitmaps used on the button bar;
        :param `help_string`: the UI help string to associate with the new button.

        :see: :meth:`~RibbonToolBar.AddTool`
        """

        return self.AddTool(tool_id, bitmap, wx.NullBitmap, help_string, RIBBON_BUTTON_TOGGLE, None)


    def InsertToggleTool(self, pos, tool_id, bitmap, help_string=""):
        """
        Inserts a toggle tool in the tool bar at the position specified by `pos`.

        :param `pos`: the position of the new tool in the toolbar (zero-based);
        :param `tool_id`: id of the new tool (used for event callbacks);
        :param `bitmap`: large bitmap of the new button. Must be the same size as all
         other large bitmaps used on the button bar;
        :param `help_string`: the UI help string to associate with the new button.

        :see: :meth:`~RibbonToolBar.AddTool`, :meth:`~RibbonToolBar.InsertTool`

        .. versionadded:: 0.9.5
        """

        return self.InsertTool(pos, tool_id, bitmap, wx.NullBitmap, help_string, RIBBON_BUTTON_TOGGLE, None)


    def AddTool(self, tool_id, bitmap, bitmap_disabled=wx.NullBitmap, help_string="", kind=RIBBON_BUTTON_NORMAL, client_data=None):
        """
        Add a tool to the tool bar.

        :param `tool_id`: id of the new tool (used for event callbacks);
        :param `bitmap`: bitmap to use as the foreground for the new tool. Does not
         have to be the same size as other tool bitmaps, but should be similar as
         otherwise it will look visually odd;
        :param `bitmap_disabled`: bitmap to use when the tool is disabled. If left
         as :class:`NullBitmap`, then a bitmap will be automatically generated from `bitmap`;
        :param `help_string`: the UI help string to associate with the new tool;
        :param `kind`: the kind of tool to add;
        :param `client_data`: client data to associate with the new tool.

        :returns: An opaque pointer which can be used only with other tool bar methods.

        :see: :meth:`~RibbonToolBar.AddDropdownTool`, :meth:`~RibbonToolBar.AddHybridTool`, :meth:`~RibbonToolBar.AddSeparator`
        """

        return self.InsertTool(self.GetToolCount(), tool_id, bitmap, bitmap_disabled,
                               help_string, kind, client_data)


    def InsertTool(self, pos, tool_id, bitmap, bitmap_disabled=wx.NullBitmap, help_string="", kind=RIBBON_BUTTON_NORMAL, client_data=None):
        """
        Inserts a tool in the tool bar at the position specified by `pos`.

        :param `pos`: the position of the new tool in the toolbar (zero-based);
        :param `tool_id`: id of the new tool (used for event callbacks);
        :param `bitmap`: bitmap to use as the foreground for the new tool. Does not
         have to be the same size as other tool bitmaps, but should be similar as
         otherwise it will look visually odd;
        :param `bitmap_disabled`: bitmap to use when the tool is disabled. If left
         as :class:`NullBitmap`, then a bitmap will be automatically generated from `bitmap`;
        :param `help_string`: the UI help string to associate with the new tool;
        :param `kind`: the kind of tool to add;
        :param `client_data`: client data to associate with the new tool.

        :returns: An opaque pointer which can be used only with other tool bar methods.

        :see: :meth:`~RibbonToolBar.AddTool`, :meth:`~RibbonToolBar.AddDropdownTool`, :meth:`~RibbonToolBar.AddHybridTool`, :meth:`~RibbonToolBar.AddSeparator`

        .. versionadded:: 0.9.5
        """

        if not bitmap.IsOk():
            raise Exception("Exception")

        tool = RibbonToolBarToolBase()
        tool.id = tool_id
        tool.bitmap = bitmap

        if bitmap_disabled.IsOk():
            if bitmap.GetSize() != bitmap_disabled.GetSize():
                raise Exception("Exception")

            tool.bitmap_disabled = bitmap_disabled
        else:
            tool.bitmap_disabled = self.MakeDisabledBitmap(bitmap)

        tool.help_string = help_string
        tool.kind = kind
        tool.client_data = client_data
        tool.position = wx.Point(0, 0)
        tool.size = wx.Size(0, 0)
        tool.state = 0

        # Find the position where insert tool
        group_count = len(self._groups)

        for group in self._groups:
            tool_count = len(group.tools)

            if pos <= tool_count:
                group.tools.insert(pos, tool)
                return tool

            pos -= tool_count + 1

        raise Exception("Tool position out of toolbar bounds.")


    def AddSeparator(self):
        """
        Adds a separator to the tool bar.

        Separators are used to separate tools into groups. As such, a separator is not
        explicity drawn, but is visually seen as the gap between tool groups.
        """

        if not self._groups[-1].tools:
            return None

        self.AppendGroup()
        return self._groups[-1].dummy_tool


    def InsertSeparator(self, pos):
        """
        Inserts a separator into the tool bar at the position specified by `pos`.

        Separators are used to separate tools into groups. As such, a separator is not
        explicity drawn, but is visually seen as the gap between tool groups.

        :param `pos`: the position of the new tool in the toolbar (zero-based).

        .. versionadded:: 0.9.5
        """

        for index, group in enumerate(self._groups):
            if pos == 0:
                # Prepend group
                return self.InsertGroup(index).dummy_tool

            if pos >= len(self._groups):
                # Append group
                return self.InsertGroup(index+1).dummy_tool

            tool_count = len(group.tools)

            if pos < tool_count:
                new_group = self.InsertGroup(index+1)

                for t in range(pos, tool_count):
                    new_group.tools.append(group.tools[t])

                group.tools = group.tools[0:pos]
                return group.dummy_tool

            pos -= tool_count + 1

        # Add an empty group at the end of the bar.
        if not self._groups[-1].tools:
            return None

        self.AppendGroup()
        return self._groups[-1].dummy_tool


    def MakeDisabledBitmap(self, original):

        img = original.ConvertToImage()
        return wx.Bitmap(img.ConvertToGreyscale())


    def AppendGroup(self):

        group = RibbonToolBarToolGroup()
        group.position = wx.Point(0, 0)
        group.size = wx.Size(0, 0)
        self._groups.append(group)


    def InsertGroup(self, pos):

        group = RibbonToolBarToolGroup()
        group.position = wx.Point(0, 0)
        group.size = wx.Size(0, 0)
        self._groups.insert(pos, group)

        return group


    def ClearTools(self):
        """
        Deletes all the tools in the toolbar.

        .. versionadded:: 0.9.5
        """

        self._groups = []


    def DeleteTool(self, tool_id):
        """
        Removes the specified tool from the toolbar and deletes it.

        :param `tool_id`: id of the tool to delete.

        :returns: ``True`` if the tool was deleted, ``False`` otherwise.

        :see: :meth:`~RibbonToolBar.DeleteToolByPos`

        .. versionadded:: 0.9.5
        """

        for group in self._groups:
            for tool in group.tools:
                if tool.id == tool_id:
                    group.tools.remove(tool)
                    return True

        return False


    def DeleteToolByPos(self, pos):
        """
        This function behaves like :meth:`~RibbonToolBar.DeleteTool` but it deletes the tool at the
        specified position `pos` and not the one with the given id.

        Useful to delete separators.

        :param `pos`: zero-based position of the tool to delete.

        :returns: ``True`` if the tool was deleted, ``False`` otherwise.

        :see: :meth:`~RibbonToolBar.DeleteTool`

        .. versionadded:: 0.9.5
        """

        for index, group in enumerate(self._groups):
            tool_count = len(group.tools)

            if pos < tool_count:
                # Remove tool
                group.tools.pop(pos)
                return True

            elif pos == tool_count:
                # Remove separator
                if index < len(self._groups) - 1:

                    next_group = self._groups[index+1]

                    for t in range(0, len(next_group.tools)):
                        group.tools.append(next_group.tools[t])

                    self._groups.pop(index+1)

                return True

        return False


    def FindById(self, tool_id):
        """
        Returns a pointer to the tool opaque structure by `tool_id` or ``None`` if
        no corresponding tool is found.

        :param `tool_id`: id of the tool to find.

        .. versionadded:: 0.9.5
        """

        for group in self._groups:
            for tool in group.tools:
                if tool.id == tool_id:
                    return tool

        return None


    def GetToolByPos(self, pos):
        """
        Returns a pointer to the tool opaque structure by `pos` or ``None`` if
        no corresponding tool is found.

        :param `pos`: zero-based position of the tool to retrieve.

        :returns: An instance of :class:`RibbonToolBarToolBase` if the tool was found,
         ``None`` if it was not found.

        .. versionadded:: 0.9.5
        """

        for group in self._groups:
            tool_count = len(group.tools)

            if pos < tool_count:
                return group.tools[pos]

            elif pos >= tool_count:
                return None

        return None


    def GetToolCount(self):
        """
        Returns the number of tools in this :class:`RibbonToolBar`.

        .. versionadded:: 0.9.5
        """

        count = 0
        for group in self._groups:
            count += len(group.tools)

        # There is a splitter in front of every group except for the first
        # If only one group, no separator.
        if len(self._groups) > 1:
            count += len(self._groups) - 1

        return count


    def GetToolId(self, tool):
        """
        Returns the tool id for the specified input `tool`.

        :param `tool`: an instance of :class:`RibbonToolBarToolBase`.

        .. versionadded:: 0.9.5
        """

        return tool.id


    def GetToolClientData(self, tool_id):
        """
        Get any client data associated with the tool.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`.

        :return: Client data (any Python object), or ``None`` if there is none.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        return tool.client_data


    def GetToolEnabled(self, tool_id):
        """
        Called to determine whether a tool is enabled (responds to user input).

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`.

        :return: ``True`` if the tool was found and it is enabled, ``False`` otherwise.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        return (tool.state & RIBBON_TOOLBAR_TOOL_DISABLED) == 0


    def GetToolHelpString(self, tool_id):
        """
        Returns the tool short help string.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        return tool.help_string


    def GetToolKind(self, tool_id):
        """
        Returns the kind of the given tool.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        return tool.kind


    def GetToolPos(self, tool_id):
        """
        Returns the tool position in the toolbar, or ``wx.NOT_FOUND`` if the tool is not found.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`.

        .. versionadded:: 0.9.5
        """

        pos = 0
        for group in self._groups:

            for tool in group.tools:

                if tool.id == tool_id:
                    return pos

                pos += 1

            pos += 1 # Increment pos for group separator.

        return wx.NOT_FOUND


    def GetToolState(self, tool_id):
        """
        Gets the on/off state of a toggle tool.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`.

        :return: ``True`` if the tool is toggled on, ``False`` otherwise.

        :see: :meth:`~RibbonToolBar.ToggleTool`

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        return tool.state & RIBBON_TOOLBAR_TOOL_TOGGLED


    def SetToolClientData(self, tool_id, clientData):
        """
        Sets the client data associated with the tool.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`;
        :param `clientData`: any Python object.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        tool.client_data = clientData


    def SetToolDisabledBitmap(self, tool_id, bitmap):
        """
        Sets the bitmap to be used by the tool with the given ID when the tool is in a disabled state.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`;
        :param `bitmap`: an instance of :class:`wx.Bitmap`.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        tool.bitmap_disabled = bitmap


    def SetToolHelpString(self, tool_id, helpString):
        """
        Sets the tool short help string.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`;
        :param `helpString`: a string for the help.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        tool.help_string = helpString


    def SetToolNormalBitmap(self, tool_id, bitmap):
        """
        Sets the bitmap to be used by the tool with the given ID when the tool is enabled.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`;
        :param `bitmap`: an instance of :class:`wx.Bitmap`.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        tool.bitmap = bitmap


    def EnableTool(self, tool_id, enable=True):
        """
        Enables or disables a single tool on the bar.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`;
        :param `enable`: ``True`` to enable the tool, ``False`` to disable it.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        if enable:

            if tool.state & RIBBON_TOOLBAR_TOOL_DISABLED:
                tool.state &= ~RIBBON_TOOLBAR_TOOL_DISABLED
                self.Refresh()

        else:

            if (tool.state & RIBBON_TOOLBAR_TOOL_DISABLED) == 0:
                tool.state |= RIBBON_TOOLBAR_TOOL_DISABLED
                self.Refresh()


    def ToggleTool(self, tool_id, checked=True):
        """
        Toggles on or off a single tool on the bar.

        :param `tool_id`: id of the tool in question, as passed to :meth:`~RibbonToolBar.AddTool`;
        :param `checked`: ``True`` to toggle on the tool, ``False`` to toggle it off.

        .. versionadded:: 0.9.5
        """

        tool = self.FindById(tool_id)
        if tool is None:
            raise Exception("Invalid tool id")

        if checked:
            if (tool.state & RIBBON_TOOLBAR_TOOL_TOGGLED) == 0:
                tool.state |= RIBBON_TOOLBAR_TOOL_TOGGLED
                self.Refresh()
        else:
            if tool.state & RIBBON_TOOLBAR_TOOL_TOGGLED:
                tool.state &= ~RIBBON_TOOLBAR_TOOL_TOGGLED
                self.Refresh()


    def IsSizingContinuous(self):
        """
        Returns ``True`` if this window can take any size (greater than its minimum size),
        ``False`` if it can only take certain sizes.

        :see: :meth:`RibbonControl.GetNextSmallerSize() <lib.agw.ribbon.control.RibbonControl.GetNextSmallerSize>`,
         :meth:`RibbonControl.GetNextLargerSize() <lib.agw.ribbon.control.RibbonControl.GetNextLargerSize>`
        """

        return False


    def DoGetNextSmallerSize(self, direction, relative_to):
        """
        Implementation of :meth:`RibbonControl.GetNextSmallerSize() <lib.agw.ribbon.control.RibbonControl.GetNextSmallerSize>`.

        Controls which have non-continuous sizing must override this virtual function
        rather than :meth:`RibbonControl.GetNextSmallerSize() <lib.agw.ribbon.control.RibbonControl.GetNextSmallerSize>`.
        """

        result = wx.Size(*relative_to)
        area = 0
        tobreak = False

        for nrows in range(self._nrows_max, self._nrows_min-1, -1):

            size = wx.Size(*self._sizes[nrows - self._nrows_min])
            original = wx.Size(*size)

            if direction == wx.HORIZONTAL:
                if size.GetWidth() < relative_to.GetWidth() and size.GetHeight() <= relative_to.GetHeight():
                    size.SetHeight(relative_to.GetHeight())
                    tobreak = True

            elif direction == wx.VERTICAL:
                if size.GetWidth() <= relative_to.GetWidth() and size.GetHeight() < relative_to.GetHeight():
                    size.SetWidth(relative_to.GetWidth())
                    tobreak = True

            elif direction == wx.BOTH:
                if size.GetWidth() < relative_to.GetWidth() and size.GetHeight() < relative_to.GetHeight():
                    pass

            if GetSizeInOrientation(original, direction) > area:
                result = wx.Size(*size)
                area = GetSizeInOrientation(original, direction)
                if tobreak:
                    break

        return result


    def DoGetNextLargerSize(self, direction, relative_to):
        """
        Implementation of :meth:`RibbonControl.GetNextLargerSize() <lib.agw.ribbon.control.RibbonControl.GetNextLargerSize>`.

        Controls which have non-continuous sizing must override this virtual function
        rather than :meth:`RibbonControl.GetNextLargerSize() <lib.agw.ribbon.control.RibbonControl.GetNextLargerSize>`.
        """

        # Pick the smallest of our sizes which are larger than the given size
        result = wx.Size(*relative_to)
        area = 10000
        tobreak = False

        for nrows in range(self._nrows_min, self._nrows_max+1):

            size = wx.Size(*self._sizes[nrows - self._nrows_min])
            original = wx.Size(*size)

            if direction == wx.HORIZONTAL:
                if size.GetWidth() > relative_to.GetWidth() and size.GetHeight() <= relative_to.GetHeight():
                    size.SetHeight(relative_to.GetHeight())
                    tobreak = True

            elif direction == wx.VERTICAL:
                if size.GetWidth() <= relative_to.GetWidth() and size.GetHeight() > relative_to.GetHeight():
                    size.SetWidth(relative_to.GetWidth())
                    tobreak = True

            elif direction == wx.BOTH:
                if size.GetWidth() > relative_to.GetWidth() and size.GetHeight() > relative_to.GetHeight():
                    tobreak = True

            if GetSizeInOrientation(original, direction) < area:
                result = wx.Size(*size)
                area = GetSizeInOrientation(original, direction)
                if tobreak:
                    break

        return result


    def SetRows(self, nMin, nMax):
        """
        Set the number of rows to distribute tool groups over.

        Tool groups can be distributed over a variable number of rows. The way in which
        groups are assigned to rows is not specificed, and the order of groups may
        change, but they will be distributed in such a way as to minimise the overall
        size of the tool bar.

        :param `nMin`: the minimum number of rows to use;
        :param `nMax`: the maximum number of rows to use (defaults to `nMin`).

        """

        if nMax == -1:
            nMax = nMin

        if nMin < 1:
            raise Exception("Exception")
        if nMin > nMax:
            raise Exception("Exception")

        self._nrows_min = nMin
        self._nrows_max = nMax

        self._sizes = []
        self._sizes = [wx.Size(0, 0) for i in range(self._nrows_min, self._nrows_max + 1)]

        self.Realize()


    def Realize(self):
        """
        Calculates tool layouts and positions.

        Must be called after tools are added to the tool bar, as otherwise the newly
        added tools will not be displayed.

        :note: Reimplemented from :class:`~wx.lib.agw.ribbon.control.RibbonControl`.
        """

        if self._art is None:
            return False

        # Calculate the size of each group and the position/size of each tool
        temp_dc = wx.MemoryDC()
        group_count = len(self._groups)

        for group in self._groups:

            prev = None
            tool_count = len(group.tools)
            tallest = 0

            for t, tool in enumerate(group.tools):

                tool.size, tool.dropdown = self._art.GetToolSize(temp_dc, self, tool.bitmap.GetSize(), tool.kind, t==0, t==(tool_count-1))
                tool.state = tool.state & ~RIBBON_TOOLBAR_TOOL_DISABLED
                if t == 0:
                    tool.state |= RIBBON_TOOLBAR_TOOL_FIRST
                if t == tool_count - 1:
                    tool.state |= RIBBON_TOOLBAR_TOOL_LAST
                if tool.size.GetHeight() > tallest:
                    tallest = tool.size.GetHeight()
                if prev:
                    tool.position = wx.Point(*prev.position)
                    tool.position.x += prev.size.x
                else:
                    tool.position = wx.Point(0, 0)

                prev = tool

            if tool_count == 0:
                group.size = wx.Size(0, 0)
            else:
                group.size = wx.Size(prev.position.x + prev.size.x, tallest)
                for tool in group.tools:
                    tool.size.SetHeight(tallest)

        # Calculate the minimum size for each possible number of rows
        sep = self._art.GetMetric(RIBBON_ART_TOOL_GROUP_SEPARATION_SIZE)
        smallest_area = 10000
        row_sizes = [wx.Size(0, 0) for i in range(self._nrows_max)]
        major_axis = ((self._art.GetFlags() & RIBBON_BAR_FLOW_VERTICAL) and [wx.VERTICAL] or [wx.HORIZONTAL])[0]
        self.SetMinSize(wx.Size(0, 0))

        minSize = wx.Size(10000, 10000)

        # See if we're sizing flexibly (i.e. wrapping), and set min size differently
        sizingFlexibly = False
        panel = self.GetParent()

        if isinstance(panel, RibbonPanel) and (panel.GetFlags() & RIBBON_PANEL_FLEXIBLE):
            sizingFlexibly = True

        # Without this, there will be redundant horizontal space because SetMinSize will
        # use the smallest possible height (and therefore largest width).
        if sizingFlexibly:
            major_axis = wx.HORIZONTAL

        for nrows in range(self._nrows_min, self._nrows_max+1):

            for r in range(nrows):
                row_sizes[r] = wx.Size(0, 0)

            for g in range(group_count):

                group = self._groups[g]
                shortest_row = 0

                for r in range(1, nrows):
                    if row_sizes[r].GetWidth() < row_sizes[shortest_row].GetWidth():
                        shortest_row = r

                row_sizes[shortest_row].x += group.size.x + sep
                if group.size.y > row_sizes[shortest_row].y:
                    row_sizes[shortest_row].y = group.size.y

            size = wx.Size(0, 0)

            for r in range(nrows):
                if row_sizes[r].GetWidth() != 0:
                    row_sizes[r].DecBy(sep, 0)
                if row_sizes[r].GetWidth() > size.GetWidth():
                    size.SetWidth(row_sizes[r].GetWidth())

                size.IncBy(0, row_sizes[r].y)

            self._sizes[nrows - self._nrows_min] = size

            if GetSizeInOrientation(size, major_axis) < smallest_area:
                smallest_area = GetSizeInOrientation(size, major_axis)
                self.SetMinSize(size)

            if sizingFlexibly:
                if size.x < minSize.x:
                    minSize.x = size.x
                if size.y < minSize.y:
                    minSize.y = size.y

        if sizingFlexibly:
            # Give it the min size in either direction regardless of row,
            # so that we're able to vary the size of the panel according to
            # the space the toolbar takes up.
            self.SetMinSize(minSize)

        # Position the groups
        dummy_event = wx.SizeEvent(self.GetSize())
        self.OnSize(dummy_event)

        return True


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`RibbonToolBar`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        if self._art is None:
            return

        # Choose row count with largest possible area
        size = event.GetSize()
        row_count = self._nrows_max
        major_axis = (self._art.GetFlags() & RIBBON_BAR_FLOW_VERTICAL and [wx.VERTICAL] or [wx.HORIZONTAL])[0]

        # See if we're sizing flexibly, and set min size differently
        sizingFlexibly = False
        panel = self.GetParent()

        if isinstance(panel, RibbonPanel) and (panel.GetFlags() & RIBBON_PANEL_FLEXIBLE):
            sizingFlexibly = True

        # Without this, there will be redundant horizontal space because SetMinSize will
        # use the smallest possible height (and therefore largest width).
        if sizingFlexibly:
            major_axis = wx.HORIZONTAL

        bestSize = wx.Size(*self._sizes[0])

        if self._nrows_max != self._nrows_min:
            area = 0
            for i in range(self._nrows_max - self._nrows_min + 1):
                if self._sizes[i].x <= size.x and self._sizes[i].y <= size.y and \
                   GetSizeInOrientation(self._sizes[i], major_axis) > area:
                    area = GetSizeInOrientation(self._sizes[i], major_axis)
                    row_count = self._nrows_min + i
                    bestSize = wx.Size(*self._sizes[i])

        # Assign groups to rows and calculate row widths
        row_sizes = [wx.Size(0, 0) for i in range(row_count)]
        sep = self._art.GetMetric(RIBBON_ART_TOOL_GROUP_SEPARATION_SIZE)

        group_count = len(self._groups)
        for group in self._groups:
            shortest_row = 0
            for r in range(1, row_count):
                if row_sizes[r].GetWidth() < row_sizes[shortest_row].GetWidth():
                    shortest_row = r

            group.position = wx.Point(row_sizes[shortest_row].x, shortest_row)
            row_sizes[shortest_row].x += group.size.x + sep
            if group.size.y > row_sizes[shortest_row].y:
                row_sizes[shortest_row].y = group.size.y

        # Calculate row positions
        total_height = 0
        for r in range(row_count):
            total_height += row_sizes[r].GetHeight()

        rowsep = (size.GetHeight() - total_height) / (row_count + 1)
        rowypos = [0]*row_count
        rowypos[0] = rowsep
        for r in range(1, row_count):
            rowypos[r] = rowypos[r - 1] + row_sizes[r - 1].GetHeight() + rowsep

        # Set group y positions
        for group in self._groups:
            group.position.y = rowypos[group.position.y]


    def GetBestSizeForParentSize(self, parentSize):
        """ Finds the best width and height given the parent's width and height. """

        if not self._sizes:
            return self.GetMinSize()

        # Choose row count with largest possible area
        size = wx.Size(*parentSize)
        row_count = self._nrows_max
        major_axis = (self._art.GetFlags() & RIBBON_BAR_FLOW_VERTICAL and [wx.VERTICAL] or [wx.HORIZONTAL])[0]

        # A toolbar should maximize its width whether vertical or horizontal, so
        # force the major axis to be horizontal. Without this, there will be
        # redundant horizontal space.
        major_axis = wx.HORIZONTAL
        bestSize = wx.Size(*self._sizes[0])

        if self._nrows_max != self._nrows_min:
            area = 0
            for i in range(self._nrows_max - self._nrows_min + 1):

                if self._sizes[i].x <= size.x and self._sizes[i].y <= size.y and \
                   GetSizeInOrientation(self._sizes[i], major_axis) > area:
                    area = GetSizeInOrientation(self._sizes[i], major_axis)
                    row_count = self._nrows_min + i
                    bestSize = wx.Size(*self._sizes[i])

        return bestSize


    def DoGetBestSize(self):
        """
        Gets the size which best suits the window: for a control, it would be the
        minimal size which doesn't truncate the control, for a panel - the same size
        as it would have after a call to `Fit()`.

        :return: An instance of :class:`wx.Size`.

        :note: Overridden from :class:`wx.Control`.
        """

        return self.GetMinSize()


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`RibbonToolBar`.

        :param `event`: a :class:`EraseEvent` event to be processed.
        """

        # All painting done in main paint handler to minimise flicker
        pass


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`RibbonToolBar`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.AutoBufferedPaintDC(self)

        if self._art is None:
            return

        self._art.DrawToolBarBackground(dc, self, wx.Rect(0, 0, *self.GetSize()))

        for group in self._groups:
            tool_count = len(group.tools)

            if tool_count != 0:
                self._art.DrawToolGroupBackground(dc, self, wx.Rect(group.position, group.size))

                for tool in group.tools:
                    rect = wx.Rect(group.position + tool.position, tool.size)

                    if tool.state & RIBBON_TOOLBAR_TOOL_DISABLED:
                        self._art.DrawTool(dc, self, rect, tool.bitmap_disabled, tool.kind, tool.state)
                    else:
                        self._art.DrawTool(dc, self, rect, tool.bitmap, tool.kind, tool.state)


    def OnMouseMove(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`RibbonToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        pos = event.GetPosition()
        new_hover = None

        for group in self._groups:

            if group.position.x <= pos.x and pos.x < group.position.x + group.size.x \
               and group.position.y <= pos.y and pos.y < group.position.y + group.size.y:
                pos -= group.position

                for tool in group.tools:
                    if tool.position.x <= pos.x and pos.x < tool.position.x + tool.size.x \
                       and tool.position.y <= pos.y and pos.y < tool.position.y + tool.size.y:
                        pos -= tool.position
                        new_hover = tool
                        break
                break

        if new_hover and new_hover != self._hover_tool:
            self.SetToolTip(new_hover.help_string)
        elif self.GetToolTip() and new_hover != self._hover_tool:
            self.SetToolTip("")

        if new_hover != self._hover_tool:
            if self._hover_tool:
                self._hover_tool.state &= ~(RIBBON_TOOLBAR_TOOL_HOVER_MASK | RIBBON_TOOLBAR_TOOL_ACTIVE_MASK)

            self._hover_tool = new_hover

            if new_hover:
                what = RIBBON_TOOLBAR_TOOL_NORMAL_HOVERED
                if new_hover.dropdown.Contains(pos):
                    what = RIBBON_TOOLBAR_TOOL_DROPDOWN_HOVERED

                new_hover.state |= what

                if new_hover == self._active_tool:

                    new_hover.state &= ~RIBBON_TOOLBAR_TOOL_ACTIVE_MASK
                    new_hover.state |= (what << 2)

            self.Refresh(False)

        elif self._hover_tool and self._hover_tool.kind == RIBBON_BUTTON_HYBRID:
            newstate = self._hover_tool.state & ~RIBBON_TOOLBAR_TOOL_HOVER_MASK
            what = RIBBON_TOOLBAR_TOOL_NORMAL_HOVERED

            if self._hover_tool.dropdown.Contains(pos):
                what = RIBBON_TOOLBAR_TOOL_DROPDOWN_HOVERED

            newstate |= what

            if newstate != self._hover_tool.state:
                self._hover_tool.state = newstate
                if self._hover_tool == self._active_tool:
                    self._hover_tool.state &= ~RIBBON_TOOLBAR_TOOL_ACTIVE_MASK
                    self._hover_tool.state |= (what << 2)

                self.Refresh(False)


    def OnMouseDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`RibbonToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        self.OnMouseMove(event)

        if self._hover_tool:
            self._active_tool = self._hover_tool
            self._active_tool.state |= (self._active_tool.state & RIBBON_TOOLBAR_TOOL_HOVER_MASK) << 2
            self.Refresh(False)


    def OnMouseLeave(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`RibbonToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self._hover_tool:
            self._hover_tool.state &= ~RIBBON_TOOLBAR_TOOL_HOVER_MASK
            self._hover_tool = None
            self.Refresh(False)


    def OnMouseUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`RibbonToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self._active_tool:
            if self._active_tool.state & RIBBON_TOOLBAR_TOOL_ACTIVE_MASK:
                evt_type = wxEVT_COMMAND_RIBBONTOOL_CLICKED
                if self._active_tool.state & RIBBON_TOOLBAR_TOOL_DROPDOWN_ACTIVE:
                    evt_type = wxEVT_COMMAND_RIBBONTOOL_DROPDOWN_CLICKED

                notification = RibbonToolBarEvent(evt_type, self._active_tool.id)
                notification.SetEventObject(self)
                notification.SetBar(self)
                self.ProcessEvent(notification)

                if self._active_tool.kind == RIBBON_BUTTON_TOGGLE:
                    self._active_tool.state ^= RIBBON_BUTTONBAR_BUTTON_TOGGLED
                    notification.SetInt(self._active_tool.state & RIBBON_BUTTONBAR_BUTTON_TOGGLED)

            # Notice that m_active_tool could have been reset by the event handler
            # above so we need to test it again.
            if self._active_tool:
                self._active_tool.state &= ~RIBBON_TOOLBAR_TOOL_ACTIVE_MASK
                self._active_tool = None
                self.Refresh(False)


    def OnMouseEnter(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` event for :class:`RibbonToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self._active_tool and not event.LeftIsDown():
            self._active_tool = None


    def GetDefaultBorder(self):
        """ Returns the default border style for :class:`RibbonToolBar`. """

        return wx.BORDER_NONE


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
        example of how to call :meth:`~RibbonToolBar.UpdateWindowUI` from an idle function::

            def OnInternalIdle(self):

                if wx.UpdateUIEvent.CanUpdate(self):
                    self.UpdateWindowUI(wx.UPDATE_UI_FROMIDLE)



        .. versionadded:: 0.9.5
        """

        wx.Control.UpdateWindowUI(self, flags)

        # don't waste time updating state of tools in a hidden toolbar
        if not self.IsShown():
            return

        for group in self._groups:
            for tool in group.tools:
                id = tool.id

                event = wx.UpdateUIEvent(id)
                event.SetEventObject(self)

                if self.ProcessWindowEvent(event):
                    if event.GetSetEnabled():
                        self.EnableTool(id, event.GetEnabled())
                    if event.GetSetChecked():
                        self.ToggleTool(id, event.GetChecked())

