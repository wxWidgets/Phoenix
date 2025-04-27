# --------------------------------------------------------------------------------- #
# HYPERTREELIST wxPython IMPLEMENTATION
# Inspired By And Heavily Based On wx.gizmos.TreeListCtrl in Classic.
#
# Andrea Gavana, @ 08 May 2006
# Latest Revision: 30 Jul 2014, 21.00 GMT
#
#
# TODO List
#
# Almost All The Features Of wx.gizmos.TreeListCtrl Are Available, And There Is
# Practically No Limit In What Could Be Added To This Class. The First Things
# That Comes To My Mind Are:
#
# 1. Add Support For 3-State CheckBoxes (Is That Really Useful?).
#
# 2. Try To Implement A More Flicker-Free Background Image In Cases Like
#    Centered Or Stretched Image (Now HyperTreeList Supports Only Tiled
#    Background Images).
#
# 3. Try To Mimic Windows wx.TreeCtrl Expanding/Collapsing behaviour: HyperTreeList
#    Suddenly Expands/Collapses The Nodes On Mouse Click While The Native Control
#    Has Some Kind Of "Smooth" Expanding/Collapsing, Like A Wave. I Don't Even
#    Know Where To Start To Do That.
#
# 4. Speed Up General OnPaint Things? I Have No Idea, Here HyperTreeList Is Quite
#    Fast, But We Should See On Slower Machines.
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
# --------------------------------------------------------------------------------- #


"""
The ``hypertreelist`` module contains the :class:`~wx.lib.agw.hypertreelist.HyperTreeList` class
that combines the multicolumn features of a :class:`wx.ListCtrl` in report mode
with the hierarchical features of a :class:`wx.TreeCtrl`. Although it looks
more like a :class:`wx.ListCtrl`, the API tends to follow the API of
:class:`wx.TreeCtrl`.

The :class:`~wx.lib.agw.hypertreelist.HyperTreeList` class actually consists of
two sub-windows:

* :class:`TreeListHeaderWindow` displays the column headers.
* :class:`TreeListMainWindow` is the main tree list based off :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl`.

These widgets can be obtained by the :meth:`~HyperTreeList.GetHeaderWindow`
and :meth:`~HyperTreeList.GetMainWindow` methods respectively although this
shouldn't be needed in normal usage because most of the methods of the
sub-windows are monkey-patched and can be called directly from the
:class:`~wx.lib.agw.hypertreelist.HyperTreeList` itself.


Description
===========

:class:`HyperTreeList` was originally inspired from the
``wx.gizmos.TreeListCtrl`` class from Classic wxPython. Now in Phoenix the old
wrapped C++ ``wxTreeListCtrl`` class is gone and this class can be used in its
place. In addition to the features of the old ``wx.gizmos.TreeListCtrl`` this
class supports:

* CheckBox-type items: checkboxes are easy to handle, just selected or unselected
  state with no particular issues in handling the item's children;
* Added support for 3-state value checkbox items;
* RadioButton-type items: since I elected to put radiobuttons in
  :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl`, I needed some way to handle
  them that made sense. So, I used the following approach:

  - All peer-nodes that are radiobuttons will be mutually exclusive. In other words,
    only one of a set of radiobuttons that share a common parent can be checked at
    once. If a radiobutton node becomes checked, then all of its peer radiobuttons
    must be unchecked.
  - If a radiobutton node becomes unchecked, then all of its child nodes will become
    inactive.

* Hyperlink-type items: they look like an hyperlink, with the proper mouse cursor on
  hovering;
* Multiline text items;
* Enabling/disabling items (together with their plain or grayed out icons);
* Whatever non-toplevel widget can be attached next to a tree item;
* Whatever non-toplevel widget can be attached next to a list item;
* Column headers are fully customizable in terms of icons, colour, font, alignment etc...;
* Default selection style, gradient (horizontal/vertical) selection style and Windows
  Vista selection style;
* Customized drag and drop images built on the fly (see :mod:`~wx.lib.agw.customtreectrl` for more info);
* Setting the :class:`HyperTreeList` item buttons to a personalized imagelist;
* Setting the :class:`HyperTreeList` check/radio item icons to a personalized imagelist;
* Changing the style of the lines that connect the items (in terms of :class:`wx.Pen` styles);
* Using an image as a :class:`HyperTreeList` background (currently only in "tile" mode);
* Ellipsization of long items when the horizontal space is low, via the ``TR_ELLIPSIZE_LONG_ITEMS``
  style (`New in version 0.9.3`).
* Hiding items
* Change background colours for each column individually.

And a lot more. Check the demo for an almost complete review of the functionalities.


Base Functionalities
====================

:class:`HyperTreeList` supports all the :mod:`~wx.lib.agw.customtreectrl` styles, except:

- ``TR_EXTENDED``: supports for this style is on the todo list (Am I sure of this?).

Plus it has 3 more styles to handle checkbox-type items:

- ``TR_AUTO_CHECK_CHILD``: automatically checks/unchecks the item children;
- ``TR_AUTO_CHECK_PARENT``: automatically checks/unchecks the item parent;
- ``TR_AUTO_TOGGLE_CHILD``: automatically toggles the item children.

And a style useful to hide the TreeListCtrl header:

- ``TR_NO_HEADER``: hides the :class:`HyperTreeList` header.

And a style related to long items (with a lot of text in them), which can be
ellipsized:

- ``TR_ELLIPSIZE_LONG_ITEMS``: ellipsizes long items when the horizontal space for
  :class:`HyperTreeList` is low (`New in version 0.9.3`).

- ``TR_VIRTUAL``: support is mostly experimental. A TreeCtrl cannot be
  made virtual as easily as a ListCtrl. In a ListCtrl the visible items
  can be determined directly from the scrollbars because all rows are
  the same height and are always visible. In a TreeCtrl the topology of
  the tree can be very complex. Each item can be expanded, collapsed,
  hidden, and even different heights if the ``wx.TR_HAS_VARIABLE_ROW_HEIGHT``
  style is used.

Please note that most TreeCtrl-like APIs are available in this class, although
they may not be visible to IDEs or other tools as they are automatically
delegated to the :class:`CustomTreeCtrl` or other helper classes.


Usage
=====

Usage example::

    import wx
    import wx.lib.agw.hypertreelist as HTL

    class MyFrame(wx.Frame):

        def __init__(self):
            wx.Frame.__init__(self, None, title="HyperTreeList Demo")

            tree = HTL.HyperTreeList(self, agwStyle=wx.TR_DEFAULT_STYLE |
                                     HTL.TR_ELLIPSIZE_LONG_ITEMS)
            tree.AddColumn("Tree Column", width=200)
            tree.AddColumn("Column 1", width=200, flag=wx.ALIGN_LEFT)
            root = tree.AddRoot("Root")

            parent = tree.AppendItem(root, "First child")
            tree.SetItemText(parent, "Child of root", column=1)
            
            child = tree.AppendItem(parent, "First Grandchild")
            tree.SetItemText(child, "Column1 Text", column=1)

            child2 = tree.AppendItem(root, "Second child")
            button = wx.Button(tree.GetMainWindow(), label="Button1")
            tree.SetItemWindow(child2, button, column=1)


    # our normal wxApp-derived class, as usual
    app = wx.App(redirect=False)
    locale = wx.Locale(wx.LANGUAGE_DEFAULT)
    frame = MyFrame()
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()



Events
======

All the events supported by :mod:`~wx.lib.agw.customtreectrl` are also
available in :class:`HyperTreeList`, with a few exceptions:

- ``EVT_TREE_GET_INFO`` (don't know what this means);
- ``EVT_TREE_SET_INFO`` (don't know what this means);
- ``EVT_TREE_ITEM_MIDDLE_CLICK`` (not implemented, but easy to add);
- ``EVT_TREE_STATE_IMAGE_CLICK`` (no need for that, look at the checking events below).

Plus, :class:`HyperTreeList` supports the events related to the checkbutton-type items:

- ``EVT_TREE_ITEM_CHECKING``: an item is being checked;
- ``EVT_TREE_ITEM_CHECKED``: an item has been checked.

And to hyperlink-type items:

- ``EVT_TREE_ITEM_HYPERLINK``: an hyperlink item has been clicked (this event is sent
  after the ``EVT_TREE_SEL_CHANGED`` event).


Supported Platforms
===================

:class:`HyperTreeList` has been tested on the following platforms:
  * Windows
  * Linux
  * Mac


Window Styles
=============

The :class:`HyperTreeList` class takes a regular wxPython ``style`` and an
extended ``agwStyle``. The ``style`` can be used with normal wxPython styles
such as ``wx.WANTS_CHARS`` while the ``agwStyle`` specifies the behavior of the
tree itself. It supports the following ``agwStyle`` flags:

================================= =========== ==================================================
Window agwStyle Flags             Hex Value   Description
================================= =========== ==================================================
**wx.TR_DEFAULT_STYLE**              *varies* The set of flags that are closest to the defaults for the native control for a particular toolkit. Should always be used.
``wx.TR_NO_BUTTONS``                      0x0 For convenience to document that no buttons are to be drawn.
``wx.TR_SINGLE``                          0x0 For convenience to document that only one item may be selected at a time. Selecting another item causes the current selection, if any, to be deselected. This is the default.
``wx.TR_HAS_BUTTONS``                     0x1 Use this style to show + and - buttons to the left of parent items.
``wx.TR_NO_LINES``                        0x4 Use this style to hide vertical level connectors.
``wx.TR_LINES_AT_ROOT``                   0x8 Use this style to show lines between root nodes. Only applicable if ``TR_HIDE_ROOT`` is set and ``TR_NO_LINES`` is not set.
``wx.TR_TWIST_BUTTONS``                  0x10 Use old Mac-twist style buttons.
``wx.TR_MULTIPLE``                       0x20 Use this style to allow a range of items to be selected. If a second range is selected, the current range, if any, is deselected.
``wx.TR_HAS_VARIABLE_ROW_HEIGHT``        0x80 Use this style to cause row heights to be just big enough to fit the content. If not set, all rows use the largest row height. The default is that this flag is unset.
``wx.TR_EDIT_LABELS``                   0x200 Use this style if you wish the user to be able to edit labels in the tree control.
``wx.TR_ROW_LINES``                     0x400 Use this style to draw a contrasting border between displayed rows.
``wx.TR_HIDE_ROOT``                     0x800 Use this style to suppress the display of the root node, effectively causing the first-level nodes to appear as a series of root nodes.
``wx.TR_FULL_ROW_HIGHLIGHT``           0x2000 Use this style to have the background colour and the selection highlight extend over the entire horizontal row of the tree control window. When TR_FILL_WHOLE_COLUMN_BACKGROUND is also set only the selection extends to the whole row, not the background color.
**Styles from hypertreelist:**
``TR_EXTENDED``                          0x40 Use this style to allow disjoint items to be selected. (Only partially implemented; may not work in all cases).
``TR_COLUMN_LINES``                    0x1000 Use this style to draw a contrasting border between displayed columns.
``TR_AUTO_CHECK_CHILD``                0x4000 Only meaningful for checkbox-type items: when a parent item is checked/unchecked its children are checked/unchecked as well.
``TR_AUTO_TOGGLE_CHILD``               0x8000 Only meaningful for checkbox-type items: when a parent item is checked/unchecked its children are toggled accordingly.
``TR_AUTO_CHECK_PARENT``              0x10000 Only meaningful for checkbox-type items: when a child item is checked/unchecked its parent item is checked/unchecked as well.
``TR_ALIGN_WINDOWS``                  0x20000 Has no effect in HyperTreeList.
``TR_NO_HEADER``                      0x40000 Use this style to hide the columns header.
``TR_ELLIPSIZE_LONG_ITEMS``           0x80000 Flag used to ellipsize long items when the horizontal space for :class:`HyperTreeList` columns is low.
``TR_VIRTUAL``                       0x100000 :class:`HyperTreeList` will have virtual behaviour.
``TR_FILL_WHOLE_COLUMN_BACKGROUND``  0x200000 Use this style to fill the whole background of item columns. Modifies behavior of :meth:`SetItemBackgroundColour() <TreeListMainWindow.SetItemBackgroundColour>`.
``TR_LIVE_UPDATE``                   0x400000 Don't draw ``wx.INVERT`` line but resize columns immediately.
================================= =========== ==================================================

See :mod:`~wx.lib.agw.customtreectrl` for more information on styles.


Events Processing
=================

This class processes the following events, Note that these are the same events as ``wx.ListCtrl`` and ``wx.TreeCtrl``:

============================== ==================================================
Event Name                     Description
============================== ==================================================
``EVT_LIST_COL_BEGIN_DRAG``    The user started resizing a column - can be vetoed.
``EVT_LIST_COL_CLICK``         A column has been left-clicked.
``EVT_LIST_COL_DRAGGING``      The divider between columns is being dragged.
``EVT_LIST_COL_END_DRAG``      A column has been resized by the user.
``EVT_LIST_COL_RIGHT_CLICK``   A column has been right-clicked.
``EVT_TREE_BEGIN_DRAG``        Begin dragging with the left mouse button. See :mod:`wx.lib.agw.customtreectrl` Drag/Drop section for more information.
``EVT_TREE_BEGIN_LABEL_EDIT``  Begin editing a label. This can be prevented by calling :meth:`TreeEvent.Veto() <lib.agw.customtreectrl.TreeEvent.Veto>`.
``EVT_TREE_BEGIN_RDRAG``       Begin dragging with the right mouse button.
``EVT_TREE_DELETE_ITEM``       Delete an item.
``EVT_TREE_END_DRAG``          End dragging with the left or right mouse button.
``EVT_TREE_END_LABEL_EDIT``    End editing a label. This can be prevented by calling :meth:`TreeEvent.Veto() <lib.agw.customtreectrl.TreeEvent.Veto>`.
``EVT_TREE_GET_INFO``          Request information from the application (not implemented in :class:`HyperTreeList`).
``EVT_TREE_ITEM_ACTIVATED``    The item has been activated, i.e. chosen by double clicking it with mouse or from keyboard.
``EVT_TREE_ITEM_CHECKED``      A checkbox or radiobox type item has been checked.
``EVT_TREE_ITEM_CHECKING``     A checkbox or radiobox type item is being checked.
``EVT_TREE_ITEM_COLLAPSED``    The item has been collapsed.
``EVT_TREE_ITEM_COLLAPSING``   The item is being collapsed. This can be prevented by calling :meth:`TreeEvent.Veto() <lib.agw.customtreectrl.TreeEvent.Veto>`.
``EVT_TREE_ITEM_EXPANDED``     The item has been expanded.s
``EVT_TREE_ITEM_EXPANDING``    The item is being expanded. This can be prevented by calling :meth:`TreeEvent.Veto() <lib.agw.customtreectrl.TreeEvent.Veto>`.
``EVT_TREE_ITEM_GETTOOLTIP``   The opportunity to set the item tooltip is being given to the application (call :meth:`TreeEvent.SetToolTip() <lib.agw.customtreectrl.CommandTreeEvent.SetToolTip>`).
``EVT_TREE_ITEM_HYPERLINK``    An hyperlink type item has been clicked.
``EVT_TREE_ITEM_MENU``         The context menu for the selected item has been requested, either by a right click or by using the menu key.
``EVT_TREE_ITEM_MIDDLE_CLICK`` The user has clicked the item with the middle mouse button (not implemented in :class:`HyperTreeList`).
``EVT_TREE_ITEM_RIGHT_CLICK``  The user has clicked the item with the right mouse button.
``EVT_TREE_KEY_DOWN``          A key has been pressed.
``EVT_TREE_SEL_CHANGED``       Selection has changed.
``EVT_TREE_SEL_CHANGING``      Selection is changing. This can be prevented by calling :meth:`TreeEvent.Veto() <lib.agw.customtreectrl.TreeEvent.Veto>`.
``EVT_TREE_SET_INFO``          Information is being supplied to the application (not implemented in :class:`HyperTreeList`).
``EVT_TREE_STATE_IMAGE_CLICK`` The state image has been clicked (not implemented in :class:`HyperTreeList`).
============================== ==================================================


License And Version
===================

:class:`HyperTreeList` is distributed under the wxPython license.

Latest Revision: Andrea Gavana @ 30 Jul 2014, 21.00 GMT

Version 1.5

"""
import sys
import wx

from wx.lib.agw.customtreectrl import CustomTreeCtrl
from wx.lib.agw.customtreectrl import DragImage, TreeEvent, GenericTreeItem, ChopText
from wx.lib.agw.customtreectrl import EnsureText, BisectChildren
from wx.lib.agw.customtreectrl import TreeEditTimer as TreeListEditTimer
from wx.lib.agw.customtreectrl import EVT_TREE_ITEM_CHECKING, EVT_TREE_ITEM_CHECKED, EVT_TREE_ITEM_HYPERLINK

import time
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

# Version Info
__version__ = "1.5"

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

_NO_IMAGE = -1

_DEFAULT_COL_WIDTH = 100
_LINEHEIGHT = 10
_LINEATROOT = 5
_MARGIN = 2
_MININDENT = 16
_BTNWIDTH = 9
_BTNHEIGHT = 9
_EXTRA_WIDTH = 4
_EXTRA_HEIGHT = 4

_MAX_WIDTH = 30000  # pixels; used by OnPaint to redraw only exposed items

_DRAG_TIMER_TICKS = 250   # minimum drag wait time in ms
_FIND_TIMER_TICKS = 500   # minimum find wait time in ms
_EDIT_TIMER_TICKS = 250   # minimum edit wait time in ms


# --------------------------------------------------------------------------
# Additional HitTest style
# --------------------------------------------------------------------------
TREE_HITTEST_ONITEMCOLUMN     = 0x2000
""" On the item column. """
TREE_HITTEST_ONITEMCHECKICON  = 0x4000
""" On the check icon, if present. """

# HyperTreeList styles
TR_DEFAULT_STYLE = wx.TR_DEFAULT_STYLE
""" Default style for HyperTreeList. """

TR_NO_BUTTONS = wx.TR_NO_BUTTONS                               # for convenience
""" For convenience to document that no buttons are to be drawn. """
TR_HAS_BUTTONS = wx.TR_HAS_BUTTONS                             # draw collapsed/expanded btns
""" Use this style to show + and - buttons to the left of parent items. """
TR_NO_LINES = wx.TR_NO_LINES                                   # don't draw lines at all
""" Use this style to hide vertical level connectors. """
TR_LINES_AT_ROOT = wx.TR_LINES_AT_ROOT                         # connect top-level nodes
""" Use this style to show lines between root nodes. Only applicable if ``TR_HIDE_ROOT`` is set and ``TR_NO_LINES`` is not set. """
TR_TWIST_BUTTONS = wx.TR_TWIST_BUTTONS                         # still used by wxTreeListCtrl
""" Use old Mac-twist style buttons. """
TR_SINGLE = wx.TR_SINGLE                                       # for convenience
""" For convenience to document that only one item may be selected at a time. Selecting another item causes the current selection, if any, to be deselected. This is the default. """
TR_MULTIPLE = wx.TR_MULTIPLE                                   # can select multiple items
""" Use this style to allow a range of items to be selected. If a second range is selected, the current range, if any, is deselected. """
TR_EXTENDED = 0x40                                             # TODO: allow extended selection
""" Use this style to allow disjoint items to be selected. (Only partially implemented; may not work in all cases). """
TR_HAS_VARIABLE_ROW_HEIGHT = wx.TR_HAS_VARIABLE_ROW_HEIGHT     # what it says
""" Use this style to cause row heights to be just big enough to fit the content. If not set, all rows use the largest row height. The default is that this flag is unset. """
TR_EDIT_LABELS = wx.TR_EDIT_LABELS                             # can edit item labels
""" Use this style if you wish the user to be able to edit labels in the tree control. """
TR_COLUMN_LINES = 0x1000                                       # put column border around items
""" Use this style to draw a contrasting border between displayed columns. """
TR_ROW_LINES = wx.TR_ROW_LINES                                 # put border around items
""" Use this style to draw a contrasting border between displayed rows. """
TR_HIDE_ROOT = wx.TR_HIDE_ROOT                                 # don't display root node
""" Use this style to suppress the display of the root node, effectively causing the first-level nodes to appear as a series of root nodes. """
TR_FULL_ROW_HIGHLIGHT = wx.TR_FULL_ROW_HIGHLIGHT               # highlight full horz space
""" Use this style to have the background colour and the selection highlight extend over the entire horizontal row of the tree control window. """

TR_AUTO_CHECK_CHILD = 0x04000                                  # only meaningful for checkboxes
""" Only meaningful for checkbox-type items: when a parent item is checked/unchecked its children are checked/unchecked as well. """
TR_AUTO_TOGGLE_CHILD = 0x08000                                 # only meaningful for checkboxes
""" Only meaningful for checkbox-type items: when a parent item is checked/unchecked its children are toggled accordingly. """
TR_AUTO_CHECK_PARENT = 0x10000                                 # only meaningful for checkboxes
""" Only meaningful for checkbox-type items: when a child item is checked/unchecked its parent item is checked/unchecked as well. """
TR_ALIGN_WINDOWS = 0x20000                                     # to align windows horizontally for items at the same level
""" Flag used to align windows (in items with windows) at the same horizontal position. """
TR_ELLIPSIZE_LONG_ITEMS = 0x80000                              # to ellipsize long items when horizontal space is low
""" Flag used to ellipsize long items when the horizontal space for :class:`HyperTreeList` columns is low."""
TR_VIRTUAL = 0x100000
""" :class:`HyperTreeList` will have virtual behaviour. """


# --------------------------------------------------------------------------
# Additional HyperTreeList style to hide the header
# --------------------------------------------------------------------------
TR_NO_HEADER = 0x40000
""" Use this style to hide the columns header. """
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Additional HyperTreeList style for filling the whole background of the
# item columns
TR_FILL_WHOLE_COLUMN_BACKGROUND = 0x200000
""" Use this style to fill the whole background of the item columns. """
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Additional HyperTreeList style to do live updates while a column is being
# resized instead of drawing a preview line. The GTK3/MacOS platforms do not
# support the wx.INVERT logical function used to draw the line. Windows 10
# supports it but it is buggy, especially with more than one monitor and
# when the horizontal scrollbar is not at zero.
# Only Windows XP/7 and GTK2 draw the preview line OK.
TR_LIVE_UPDATE = 0x400000
""" Use this style to do live updates while resizing a column. """
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Additional HyperTreeList style autosize the columns based on the widest
# width between column header and cells content
# --------------------------------------------------------------------------
LIST_AUTOSIZE_CONTENT_OR_HEADER = -3
# --------------------------------------------------------------------------


def IsBufferingSupported():
    """
    Utility function which checks if a platform handles correctly double
    buffering for the header. Currently returns ``False`` for all platforms
    except Windows XP.
    """

    if wx.Platform != "__WXMSW__":
        return False

    if wx.App.GetComCtl32Version() >= 600:
        if wx.GetOsVersion()[1] > 5:
            # Windows Vista
            return False

        return True

    return False


class TreeListColumnInfo(object):
    """
    Class used to store information (width, alignment flags, colours, etc...) about a
    :class:`HyperTreeList` column header.
    """

    def __init__(self, input="", width=_DEFAULT_COL_WIDTH, flag=wx.ALIGN_LEFT,
                 image=-1, shown=True, colour=None, edit=False):
        """
        Default class constructor.

        :param `input`: can be a string (representing the column header text) or
         another instance of :class:`TreeListColumnInfo`. In the latter case, all the
         other input parameters are not used;
        :param `width`: the column width in pixels;
        :param `flag`: the column alignment flag, one of ``wx.ALIGN_LEFT``,
         ``wx.ALIGN_RIGHT``, ``wx.ALIGN_CENTER``;
        :param `image`: an index within the normal image list assigned to
         :class:`HyperTreeList` specifying the image to use for the column;
        :param `shown`: ``True`` to show the column, ``False`` to hide it;
        :param `colour`: a valid :class:`wx.Colour`, representing the text foreground colour
         for the column;
        :param `edit`: ``True`` to set the column as editable, ``False`` otherwise.
        """

        if isinstance(input, str):
            self._text = input
            self._width = width
            self._flag = flag
            self._image = image
            self._selected_image = -1
            self._shown = shown
            self._edit = edit
            self._font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            if colour is None:
                self._colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
            else:
                self._colour = colour

        else:

            self._text = input._text
            self._width = input._width
            self._flag = input._flag
            self._image = input._image
            self._selected_image = input._selected_image
            self._shown = input._shown
            self._edit = input._edit
            self._colour = input._colour
            self._font = input._font
        self._sort_icon = wx.HDR_SORT_ICON_NONE
        self._sort_icon_colour = None

    # get/set
    def GetText(self):
        """ Returns the column header label. """

        return self._text


    def SetText(self, text) -> Self:
        """
        Sets the column header label.

        :param `text`: the new column header text.
        """

        self._text = text
        return self


    def GetWidth(self):
        """ Returns the column header width in pixels. """

        return self._width


    def SetWidth(self, width) -> Self:
        """
        Sets the column header width.

        :param `width`: the column header width, in pixels.
        """

        self._width = width
        return self


    def GetAlignment(self):
        """ Returns the column text alignment. """

        return self._flag


    def SetAlignment(self, flag) -> Self:
        """
        Sets the column text alignment.

        :param `flag`: the alignment flag, one of ``wx.ALIGN_LEFT``, ``wx.ALIGN_RIGHT``,
         ``wx.ALIGN_CENTER``.
        """

        self._flag = flag
        return self


    def GetColour(self):
        """ Returns the column text colour. """

        return self._colour


    def SetColour(self, colour) -> Self:
        """
        Sets the column text colour.

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._colour = colour
        return self


    def GetImage(self):
        """ Returns the column image index. """

        return self._image


    def SetImage(self, image) -> Self:
        """
        Sets the column image index.

        :param `image`: an index within the normal image list assigned to
         :class:`HyperTreeList` specifying the image to use for the column.
        """

        self._image = image
        return self


    def GetSelectedImage(self):
        """ Returns the column image index in the selected state. """

        return self._selected_image


    def SetSelectedImage(self, image) -> Self:
        """
        Sets the column image index in the selected state.

        :param `image`: an index within the normal image list assigned to
         :class:`HyperTreeList` specifying the image to use for the column when in
         selected state.
        """

        self._selected_image = image
        return self


    def IsEditable(self):
        """ Returns ``True`` if the column is editable, ``False`` otherwise. """

        return self._edit


    def SetEditable(self, edit) -> Self:
        """
        Sets the column as editable or non-editable.

        :param `edit`: ``True`` if the column should be editable, ``False`` otherwise.
        """

        self._edit = edit
        return self


    def IsShown(self):
        """ Returns ``True`` if the column is shown, ``False`` if it is hidden. """

        return self._shown


    def SetShown(self, shown) -> Self:
        """
        Sets the column as shown or hidden.

        :param `shown`: ``True`` if the column should be shown, ``False`` if it
         should be hidden.
        """

        self._shown = shown
        return self


    def SetFont(self, font) -> Self:
        """
        Sets the column text font.

        :param `font`: a valid :class:`wx.Font` object.
        """

        self._font = font
        return self


    def GetFont(self):
        """ Returns the column text font. """

        return self._font


    def GetSortIcon(self):
        """ Returns the column sort icon displayed in the header. """

        return self._sort_icon


    def SetSortIcon(self, sortIcon, colour=None) -> Self:
        """
        Sets the column sort icon displayed in the header.

        :param `sortIcon`: the sort icon to display, one of ``wx.HDR_SORT_ICON_NONE``,
         ``wx.HDR_SORT_ICON_UP``, ``wx.HDR_SORT_ICON_DOWN``.
        :param `colour`: the colour of the sort icon as a wx.Colour. Optional.
         Set to ``None`` to restore native colour.
        """
    
        self._sort_icon = sortIcon
        self._sort_icon_colour = colour
        return self


    def GetSortIconColour(self):
        """Return the colour of the sort icon (``None`` = Default). """

        return self._sort_icon_colour


#-----------------------------------------------------------------------------
#  TreeListHeaderWindow (internal)
#-----------------------------------------------------------------------------

class TreeListHeaderWindow(wx.Window):
    """ A window which holds the header of :class:`HyperTreeList`. """

    def __init__(self, parent, id=wx.ID_ANY, owner=None, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name="wxtreelistctrlcolumntitles"):
        """
        Default class constructor.

        :param `parent`: the window parent. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `owner`: the window owner, in this case an instance of :class:`TreeListMainWindow`;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the window style;
        :param `name`: the window name.
        """

        wx.Window.__init__(self, parent, id, pos, size, style, name=name)

        self._owner = owner
        self._currentCursor = wx.Cursor(wx.CURSOR_DEFAULT)
        self._resizeCursor = wx.Cursor(wx.CURSOR_SIZEWE)
        self._isDragging = False
        self._dragStart = 0
        self._dirty = False
        self._total_col_width = 0
        self._hotTrackCol = -1
        self._columns = []
        self._headerCustomRenderer = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)


    def SetBuffered(self, buffered):
        """
        Sets/unsets the double buffering for the header.

        :param `buffered`: ``True`` to use double-buffering, ``False`` otherwise.

        :note: Currently double-buffering is only enabled by default for Windows XP.
        """

        self._buffered = buffered


    # total width of all columns
    def GetWidth(self):
        """ Returns the total width of all columns. """

        return self._total_col_width


    # column manipulation
    def GetColumnCount(self):
        """ Returns the total number of columns. """

        return len(self._columns)


    # column information manipulation
    def GetColumn(self, column):
        """
        Returns a column item, an instance of :class:`TreeListItem`.

        :param `column`: an integer specifying the column index.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column]


    def GetColumnText(self, column):
        """
        Returns the column text label.

        :param `column`: an integer specifying the column index.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column].GetText()


    def SetColumnText(self, column, text):
        """
        Sets the column text label.

        :param `column`: an integer specifying the column index;
        :param `text`: the new column label.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column].SetText(text)


    def GetColumnAlignment(self, column):
        """
        Returns the column text alignment.

        :param `column`: an integer specifying the column index.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column].GetAlignment()


    def SetColumnAlignment(self, column, flag):
        """
        Sets the column text alignment.

        :param `column`: an integer specifying the column index;
        :param `flag`: the new text alignment flag.

        :see: :meth:`TreeListColumnInfo.SetAlignment() <TreeListColumnInfo.SetAlignment>` for a list of valid alignment
         flags.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column].SetAlignment(flag)


    def GetColumnWidth(self, column):
        """
        Returns the column width, in pixels.

        :param `column`: an integer specifying the column index.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column].GetWidth()


    def GetColumnColour(self, column):
        """
        Returns the column text colour.

        :param `column`: an integer specifying the column index.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column].GetColour()


    def SetColumnColour(self, column, colour):
        """
        Sets the column text colour.

        :param `column`: an integer specifying the column index;
        :param `colour`: a valid :class:`wx.Colour` object.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column].SetColour(colour)


    def IsColumnEditable(self, column):
        """
        Returns ``True`` if the column is editable, ``False`` otherwise.

        :param `column`: an integer specifying the column index.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column].IsEditable()


    def IsColumnShown(self, column):
        """
        Returns ``True`` if the column is shown, ``False`` if it is hidden.

        :param `column`: an integer specifying the column index.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        return self._columns[column].IsShown()


    # shift the DC origin to match the position of the main window horz
    # scrollbar: this allows us to always use logical coords
    def AdjustDC(self, dc):
        """
        Shifts the :class:`wx.DC` origin to match the position of the main window horizontal
        scrollbar: this allows us to always use logical coordinates.

        :param `dc`: an instance of :class:`wx.DC`.
        """

        xpix, dummy = self._owner.GetScrollPixelsPerUnit()
        x, dummy = self._owner.GetViewStart()

        # account for the horz scrollbar offset
        dc.SetDeviceOrigin(-x * xpix, 0)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`TreeListHeaderWindow`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        if self._buffered:
            dc = wx.BufferedPaintDC(self)
        else:
            dc = wx.PaintDC(self)

        self.AdjustDC(dc)

        x = 0

        # width and height of the entire header window
        w, h = self.GetClientSize()
        w, dummy = self._owner.CalcUnscrolledPosition(w, 0)
        dc.SetBackgroundMode(wx.TRANSPARENT)

        numColumns = self.GetColumnCount()

        for i in range(numColumns):

            if x >= w:
                break

            if not self.IsColumnShown(i):
                continue    # do next column if not shown

            params = wx.HeaderButtonParams()

            column = self.GetColumn(i)
            params.m_labelColour = column.GetColour()
            params.m_labelFont = column.GetFont()

            wCol = column.GetWidth()
            flags = 0
            rect = wx.Rect(x, 0, wCol, h)
            x += wCol

            if i == self._hotTrackCol:
                flags |= wx.CONTROL_CURRENT

            params.m_labelText = column.GetText()
            params.m_labelAlignment = column.GetAlignment()
            sortIcon = column.GetSortIcon()
            sortIconColour = column.GetSortIconColour()
            if sortIconColour:
                params.m_arrowColour = sortIconColour

            image = column.GetImage()
            imageList = self._owner.GetImageList()

            if image != -1 and imageList:
                params.m_labelBitmap = imageList.GetBitmap(image)

            if self._headerCustomRenderer is not None:
                self._headerCustomRenderer.DrawHeaderButton(dc, rect, flags, params)
            else:
                wx.RendererNative.Get().DrawHeaderButton(self, dc, rect, flags,
                                                         sortIcon, params)

        # Fill up any unused space to the right of the columns
        if x < w:
            rect = wx.Rect(x, 0, w - x, h)
            if self._headerCustomRenderer is not None:
                self._headerCustomRenderer.DrawHeaderButton(dc, rect)
            else:
                wx.RendererNative.Get().DrawHeaderButton(self, dc, rect)


    def DrawCurrent(self):
        """ Draws the column resize line on a :class:`ScreenDC`. """

        x1, y1 = self._currentX, 0
        x1, y1 = self.ClientToScreen((x1, y1))
        # GTK2 needs x2 offset by 1 to draw 2-pixel wide line. Windows does not.
        x2 = self._currentX - 1
        if wx.Platform == "__WXMSW__":
            # Undo 1 pixel slant added in previous line under Windows.
            x2 += 1

        y2 = 0
        dummy, y2 = self._owner.GetClientSize()
        x2, y2 = self._owner.ClientToScreen((x2, y2))

        dc = wx.ScreenDC()
        dc.SetLogicalFunction(wx.INVERT)
        dc.SetPen(wx.Pen(wx.BLACK, 2, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        self.AdjustDC(dc)
        dc.DrawLine(x1, y1, x2, y2)
        dc.SetLogicalFunction(wx.COPY)


    def SetCustomRenderer(self, renderer=None):
        """
        Associate a custom renderer with the header - all columns will use it

        :param `renderer`: a class able to correctly render header buttons

        :note: the renderer class **must** implement the method `DrawHeaderButton`
        """

        self._headerCustomRenderer = renderer


    def XToCol(self, x):
        """
        Returns the column that corresponds to the logical input `x` coordinate.

        :param `x`: the `x` position to evaluate.

        :return: The column that corresponds to the logical input `x` coordinate,
         or ``wx.NOT_FOUND`` if there is no column at the `x` position.
        """

        colLeft = 0
        numColumns = self.GetColumnCount()
        for col in range(numColumns):

            if not self.IsColumnShown(col):
                continue

            column = self.GetColumn(col)

            if x < (colLeft + column.GetWidth()):
                return col

            colLeft += column.GetWidth()

        return wx.NOT_FOUND


    def RefreshColLabel(self, col):
        """
        Redraws the column.

        :param `col`: the index of the column to redraw.
        """

        if col >= self.GetColumnCount():
            return

        x = idx = width = 0
        while idx <= col:

            if not self.IsColumnShown(idx):
                idx += 1
                continue

            column = self.GetColumn(idx)
            x += width
            width = column.GetWidth()
            idx += 1

        x, dummy = self._owner.CalcScrolledPosition(x, 0)
        self.RefreshRect(wx.Rect(x, 0, width, self.GetSize().GetHeight()))


    def OnMouse(self, event):
        """
        Handles the ``wx.EVT_MOUSE_EVENTS`` event for :class:`TreeListHeaderWindow`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        # we want to work with logical coords
        x, dummy = self._owner.CalcUnscrolledPosition(event.GetX(), 0)
        y = event.GetY()

        if event.Moving():

            col = self.XToCol(x)
            if col != self._hotTrackCol:

                # Refresh the col header so it will be painted with hot tracking
                # (if supported by the native renderer.)
                self.RefreshColLabel(col)

                # Also refresh the old hot header
                if self._hotTrackCol >= 0:
                    self.RefreshColLabel(self._hotTrackCol)

                self._hotTrackCol = col

        if event.Leaving() and self._hotTrackCol >= 0:

            # Leaving the window so clear any hot tracking indicator that may be present
            self.RefreshColLabel(self._hotTrackCol)
            self._hotTrackCol = -1

        if self._isDragging:

            # User is dragging the column header separator. Send event.
            self.SendListEvent(wx.wxEVT_COMMAND_LIST_COL_DRAGGING, event.GetPosition())

            # Calculate time elapsed for this drag, and new/old column sizes.
            elapsed_ms = abs(time.time() - self._dragStart) * 1000
            new_width = self._currentX - self._minX
            old_width = self.GetColumnWidth(self._column)

            # Live updates or old preview line?
            if self._owner.HasAGWFlag(TR_LIVE_UPDATE):
                # Avoid making change on first click of double-click.
                if elapsed_ms > 333 or abs(new_width - old_width) > 3:
                    self.SetColumnWidth(self._column, new_width)
                    self.Refresh()
                    self.Update()
            else:
                # Don't draw line beyond our window but allow dragging it there.
                w, dummy = self.GetClientSize()
                w, dummy = self._owner.CalcUnscrolledPosition(w, 0)
                w -= 6
                # Erase the preview line if it was drawn.
                if self._currentX < w:
                    self.DrawCurrent()

            if event.ButtonUp():
                self._isDragging = False
                if self.HasCapture():
                    self.ReleaseMouse()
                self._dirty = True
                # Avoid making change on first click of double-click.
                if elapsed_ms > 333 or abs(new_width - old_width) > 3:
                    self.SetColumnWidth(self._column, new_width)
                    self.Refresh()
                    self.SendListEvent(wx.wxEVT_COMMAND_LIST_COL_END_DRAG,
                                       event.GetPosition())
            else:
                # Update the new column preview position.
                self._currentX = max(self._minX + 7, x)
                # Draw the preview line in the new location.
                if not self._owner.HasAGWFlag(TR_LIVE_UPDATE):
                    if self._currentX < w:
                        self.DrawCurrent()

        else:
            # Not dragging (column resizing)
            self._minX = 0
            hit_border = False

            # end of the current column
            xpos = 0

            # find the column where this event occurred
            countCol = self.GetColumnCount()

            for column in range(countCol):

                if not self.IsColumnShown(column):
                    continue    # do next if not shown

                xpos += self.GetColumnWidth(column)
                self._column = column
                if abs(x - xpos) < 3 and y < 22:
                    # near the column border
                    hit_border = True
                    break

                if x < xpos:
                    # inside the column
                    break

                self._minX = xpos

            if event.LeftDown() or event.RightUp():
                if hit_border and event.LeftDown():
                    self._isDragging = True
                    self._dragStart = time.time()
                    if not self.HasCapture():
                        self.CaptureMouse()
                    self._currentX = x
                    if not self._owner.HasAGWFlag(TR_LIVE_UPDATE):
                        self.DrawCurrent()
                    self.SendListEvent(wx.wxEVT_COMMAND_LIST_COL_BEGIN_DRAG, event.GetPosition())
                else:   # click on a column
                    evt = (event.LeftDown() and [wx.wxEVT_COMMAND_LIST_COL_CLICK] or [wx.wxEVT_COMMAND_LIST_COL_RIGHT_CLICK])[0]
                    self.SendListEvent(evt, event.GetPosition())

            elif event.LeftDClick() and hit_border:
                best_width = self._owner.GetBestColumnWidth(self._column)
                self.SetColumnWidth(self._column, best_width)
                self.Refresh()

            elif event.Moving():

                if hit_border:
                    setCursor = self._currentCursor == wx.STANDARD_CURSOR
                    self._currentCursor = self._resizeCursor
                else:
                    setCursor = self._currentCursor != wx.STANDARD_CURSOR
                    self._currentCursor = wx.STANDARD_CURSOR

                if setCursor:
                    self.SetCursor(self._currentCursor)


    def OnSetFocus(self, event):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for :class:`TreeListHeaderWindow`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        self._owner.SetFocus()


    def SendListEvent(self, evtType, pos):
        """
        Sends a :class:`ListEvent` for the parent window.

        :param `evtType`: the event type;
        :param `pos`: an instance of :class:`wx.Point`.
        """

        parent = self.GetParent()
        le = wx.ListEvent(evtType, parent.GetId())
        le.SetEventObject(parent)
        le.m_pointDrag = pos

        # the position should be relative to the parent window, not
        # this one for compatibility with MSW and common sense: the
        # user code doesn't know anything at all about this header
        # window, so why should it get positions relative to it?
        le.m_pointDrag.y -= self.GetSize().y
        le.m_col = self._column
        # Set point/column with Setters for Phoenix compatibility.
        le.SetPoint(le.m_pointDrag)
        le.SetColumn(self._column)
        parent.GetEventHandler().ProcessEvent(le)


    def AddColumnInfo(self, colInfo):
        """
        Appends a column to the :class:`TreeListHeaderWindow`.

        :param `colInfo`: an instance of :class:`TreeListColumnInfo`.
        """

        self._columns.append(colInfo)
        self._total_col_width += colInfo.GetWidth()
        self._owner.AdjustMyScrollbars()
        self._owner._dirty = True


    def AddColumn(self, text, width=_DEFAULT_COL_WIDTH, flag=wx.ALIGN_LEFT,
                  image=-1, shown=True, colour=None, edit=False):
        """
        Appends a column to the :class:`TreeListHeaderWindow`.

        :param `text`: the column text label;
        :param `width`: the column width in pixels;
        :param `flag`: the column alignment flag, one of ``wx.ALIGN_LEFT``,
         ``wx.ALIGN_RIGHT``, ``wx.ALIGN_CENTER``;
        :param `image`: an index within the normal image list assigned to
         :class:`HyperTreeList` specifying the image to use for the column;
        :param `shown`: ``True`` to show the column, ``False`` to hide it;
        :param `colour`: a valid :class:`wx.Colour`, representing the text foreground colour
         for the column;
        :param `edit`: ``True`` to set the column as editable, ``False`` otherwise.
        """

        colInfo = TreeListColumnInfo(text, width, flag, image, shown, colour, edit)
        self.AddColumnInfo(colInfo)


    def SetColumnWidth(self, column, width):
        """
        Sets the column width, in pixels.

        :param `column`: an integer specifying the column index;
        :param `width`: the new width for the column, in pixels.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        self._total_col_width -= self._columns[column].GetWidth()
        self._columns[column].SetWidth(width)
        self._total_col_width += width
        #self._owner.AdjustMyScrollbars()   # Setting dirty does this now.
        self._owner._dirty = True


    def InsertColumnInfo(self, before, colInfo):
        """
        Inserts a column to the :class:`TreeListHeaderWindow` at the position specified
        by `before`.

        :param `before`: the index at which we wish to insert the new column;
        :param `colInfo`: an instance of :class:`TreeListColumnInfo`.
        """

        if before < 0 or before >= self.GetColumnCount():
            raise Exception("Invalid column")

        self._columns.insert(before, colInfo)
        self._total_col_width += colInfo.GetWidth()
        self._owner.AdjustMyScrollbars()
        self._owner._dirty = True


    def InsertColumn(self, before, text, width=_DEFAULT_COL_WIDTH,
                     flag=wx.ALIGN_LEFT, image=-1, shown=True, colour=None,
                     edit=False):
        """
        Inserts a column to the :class:`TreeListHeaderWindow` at the position specified
        by `before`.

        :param `before`: the index at which we wish to insert the new column;
        :param `text`: the column text label;
        :param `width`: the column width in pixels;
        :param `flag`: the column alignment flag, one of ``wx.ALIGN_LEFT``,
         ``wx.ALIGN_RIGHT``, ``wx.ALIGN_CENTER``;
        :param `image`: an index within the normal image list assigned to
         :class:`HyperTreeList` specifying the image to use for the column;
        :param `shown`: ``True`` to show the column, ``False`` to hide it;
        :param `colour`: a valid :class:`wx.Colour`, representing the text foreground colour
         for the column;
        :param `edit`: ``True`` to set the column as editable, ``False`` otherwise.
        """

        colInfo = TreeListColumnInfo(text, width, flag, image, shown, colour,
                                     edit)
        self.InsertColumnInfo(before, colInfo)


    def RemoveColumn(self, column):
        """
        Removes a column from the :class:`TreeListHeaderWindow`.

        :param `column`: an integer specifying the column index.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        self._total_col_width -= self._columns[column].GetWidth()
        self._columns.pop(column)
        self._owner.AdjustMyScrollbars()
        self._owner._dirty = True


    def SetColumn(self, column, info):
        """
        Sets a column using an instance of :class:`TreeListColumnInfo`.

        :param `column`: an integer specifying the column index;
        :param `info`: an instance of :class:`TreeListColumnInfo`.
        """

        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        w = self._columns[column].GetWidth()
        self._columns[column] = info

        if w != info.GetWidth():
            self._total_col_width += info.GetWidth() - w
            self._owner.AdjustMyScrollbars()

        self._owner._dirty = True


    def SetSortIcon(self, column, sortIcon, colour=None):
        """
        Sets the sort icon to be displayed in the column header.

        The sort icon will be displayed in the specified column number
        and all other columns will have the sort icon cleared.

        :param `column`: an integer specifying the column index;
        :param `sortIcon`: the sort icon to display, one of ``wx.HDR_SORT_ICON_NONE``,
         ``wx.HDR_SORT_ICON_UP``, ``wx.HDR_SORT_ICON_DOWN``.
        :param `colour`: the colour of the sort icon as a wx.Colour. Optional.
         Set to ``None`` to restore native colour.
        """
        if column < 0 or column >= self.GetColumnCount():
            raise Exception("Invalid column")

        for num in range(self.GetColumnCount()):
            if num == column:
                self.GetColumn(num).SetSortIcon(sortIcon, colour)
            else:
                self.GetColumn(num).SetSortIcon(wx.HDR_SORT_ICON_NONE, colour)
        self.Refresh()


# ---------------------------------------------------------------------------
# TreeListItem
# ---------------------------------------------------------------------------
class TreeListItem(GenericTreeItem):
    """
    This class holds all the information and methods for every single item in
    :class:`HyperTreeList`.

    :note: Subclassed from :class:`~wx.lib.agw.customtreectrl.GenericTreeItem`.
    """

    def __init__(self, mainWin, parent, text="", ct_type=0, wnd=None, image=-1, selImage=-1, data=None):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param `mainWin`: the main :class:`HyperTreeList` window, in this case an instance
         of :class:`TreeListMainWindow`;
        :param `parent`: the tree item parent (may be ``None`` for root items);
        :param `text`: the tree item text;
        :param `ct_type`: the tree item kind. May be one of the following integers:

         =============== ==========================
         `ct_type` Value Description
         =============== ==========================
                0        A normal item
                1        A checkbox-like item
                2        A radiobutton-type item
         =============== ==========================

        :param `wnd`: if not ``None``, a non-toplevel window to be displayed next to
         the item;
        :param `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param `data`: associate the given Python object `data` with the item.

        :note: Regarding radiobutton-type items (with `ct_type` = 2), the following
         approach is used:

         - All peer-nodes that are radiobuttons will be mutually exclusive. In other words,
           only one of a set of radiobuttons that share a common parent can be checked at
           once. If a radiobutton node becomes checked, then all of its peer radiobuttons
           must be unchecked.
         - If a radiobutton node becomes unchecked, then all of its child nodes will become
           inactive.
        """

        self._col_images = []
        self._owner = mainWin

        # We don't know the height here yet.
        self._text_x = 0

        GenericTreeItem.__init__(self, parent, text, ct_type, wnd, image, selImage, data)

        self._wnd = [None]             # are we holding a window?
        self._bgColour = [None]
        self._extents = None           # Cached text extents

        if wnd:
            self.SetWindow(wnd)


    def DeleteChildren(self, tree):
        """
        Deletes the item children.

        :param `tree`: the main :class:`TreeListMainWindow` instance.
        """
        # Iterate over copy of self._children as tree.Delete() will modify it.
        for child in list(self._children):
            child.DeleteChildren(tree)
            if tree:
                tree.Delete(child)

            if child == tree._selectItem:
                tree._selectItem = None

            # We have to destroy the associated window
            for wnd in child._wnd:
                if wnd:
                    wnd.Hide()
                    wnd.Destroy()

            child._wnd = []

            if child in tree._itemWithWindow:
                tree._itemWithWindow.remove(child)

            del child

        self._children = []


    def HitTest(self, point, theCtrl, flags, column, level):
        """
        HitTest method for an item. Called from the main window HitTest.

        :param `point`: the point to test for the hit (an instance of :class:`wx.Point`);
        :param `theCtrl`: the main :class:`TreeListMainWindow` tree;
        :param `flags`: a bitlist of hit locations;
        :param `column`: an integer specifying the column index;
        :param `level`: the item's level inside the tree hierarchy.

        :see: :meth:`TreeListMainWindow.HitTest() <TreeListMainWindow.HitTest>` method for the flags explanation.

        :return: A 3-tuple of (item, flags, column). The item may be ``None``.
        """
        # Hidden items are never evaluated.
        if self.IsHidden():
            return None, flags, wx.NOT_FOUND

        # for a hidden root node, don't evaluate it, but do evaluate children
        if level > 0 or not theCtrl.HasAGWFlag(wx.TR_HIDE_ROOT):

            # reset any previous hit infos
            flags = 0
            column = -1
            header_win = theCtrl._owner.GetHeaderWindow()

            # check for right of all columns (outside)
            if point.x > header_win.GetWidth():
                return None, flags, wx.NOT_FOUND

            # evaluate if y-pos is okay
            h = theCtrl.GetLineHeight(self)

            if point.y >= self._y and point.y <= self._y + h:

                maincol = theCtrl.GetMainColumn()

                # check for above/below middle
                y_mid = self._y + h // 2
                if point.y < y_mid:
                    flags |= wx.TREE_HITTEST_ONITEMUPPERPART
                else:
                    flags |= wx.TREE_HITTEST_ONITEMLOWERPART

                # check for button hit
                if self.HasPlus() and theCtrl.HasButtons():
                    bntX = self._x - theCtrl._btnWidth2
                    bntY = y_mid - theCtrl._btnHeight2
                    if ((point.x >= bntX) and (point.x <= (bntX + theCtrl._btnWidth)) and
                        (point.y >= bntY) and (point.y <= (bntY + theCtrl._btnHeight))):
                        flags |= wx.TREE_HITTEST_ONITEMBUTTON
                        column = maincol
                        return self, flags, column

                # check for hit on the check icons
                if self.GetType() != 0:
                    imageWidth = 0
                    numberOfMargins = 1
                    if self.GetCurrentImage() != _NO_IMAGE:
                        imageWidth = theCtrl._imgWidth
                        numberOfMargins += 1
                    chkX = self._text_x - imageWidth - numberOfMargins * _MARGIN - theCtrl._checkWidth
                    chkY = y_mid - theCtrl._checkHeight2
                    if ((point.x >= chkX) and (point.x <= (chkX + theCtrl._checkWidth)) and
                        (point.y >= chkY) and (point.y <= (chkY + theCtrl._checkHeight))):
                        flags |= TREE_HITTEST_ONITEMCHECKICON
                        return self, flags, maincol

                # check for image hit
                if self.GetCurrentImage() != _NO_IMAGE:
                    imgX = self._text_x - theCtrl._imgWidth - _MARGIN
                    imgY = y_mid - theCtrl._imgHeight2
                    if ((point.x >= imgX) and (point.x <= (imgX + theCtrl._imgWidth)) and
                        (point.y >= imgY) and (point.y <= (imgY + theCtrl._imgHeight))):
                        flags |= wx.TREE_HITTEST_ONITEMICON
                        column = maincol
                        return self, flags, column

                # check for label hit
                if ((point.x >= self._text_x) and (point.x <= (self._text_x + self._width))):
                    flags |= wx.TREE_HITTEST_ONITEMLABEL
                    column = maincol
                    return self, flags, column

                # check for indent hit after button and image hit
                if point.x < self._x:
                    flags |= wx.TREE_HITTEST_ONITEMINDENT
                    column = -1     # considered not belonging to main column
                    return self, flags, column

                # check for right of label
                end = 0
                for i in range(maincol):
                    end += header_win.GetColumnWidth(i)
                    if ((point.x > (self._text_x + self._width)) and (point.x <= end)):
                        flags |= wx.TREE_HITTEST_ONITEMRIGHT
                        column = -1     # considered not belonging to main column
                        return self, flags, column

                # else check for each column except main
                x = 0
                for j in range(theCtrl.GetColumnCount()):
                    if not header_win.IsColumnShown(j):
                        continue
                    w = header_win.GetColumnWidth(j)
                    if ((j != maincol) and (point.x >= x and point.x < x + w)):
                        flags |= TREE_HITTEST_ONITEMCOLUMN
                        column = j
                        return self, flags, column

                    x += w

                # no special flag or column found
                return self, flags, column

            # if children are expanded, fall through to evaluate them
            if not self.IsExpanded():
                # Item is not expanded (or hidden). Return no item found.
                return None, flags, wx.NOT_FOUND

        # Binary search for last child that is before the point's Y.
        lo = BisectChildren(self._children, point[1])
        hi = len(self._children)

        # Now hit test only against prospective children.
        for index in range(lo, hi):
            child = self._children[index]
            hit, flags, column = child.HitTest(point, theCtrl, flags, column, level + 1)
            if hit:
                return hit, flags, column
            if child.GetY() > point[1]:
                break   # Early exit (we're past the point)

        # not found
        return None, flags, wx.NOT_FOUND


    def HasExtents(self, column=None):
        """
        Returns whether the text extents are calculated for this item.

        :param `column`: The column to check for extents. If it is ``None``,
         check that all columns have extents.

        :return: ``True`` if extents are calculated, ``False`` otherwise.
        """

        if not self._extents:
            return False
        if len(self._extents) < self._owner.GetColumnCount():
            # Only partial extents list is present.
            if column is None or column >= len(self._extents):
                return False
        if column is None:
            # All extents must be present.
            return True if all(self._extents) else False
        # Return specific extent for column number.
        return self._extents[column] is not None


    def GetExtents(self, dc=None, column=None):
        """
        Calculate text extents of this item using the given ClientDc.

        :param `dc`: an instance of :class:`wx.DC` to use to calculate
         text extent if it has not been cached yet. The proper font
         should have been already set in the device context.

        :param `column`: The column to get extents for. If it is ``None``,
         return the width of the main column and maximum height of all
         the columns (``dc`` is required in this case).

        :return: A 2-tuple of (width, height). If `dc` was not provided
         could return `None`.
        """
        # Make sure self._extents array is fully setup.
        if self._extents is None:
            self._extents = [None] * self._owner.GetColumnCount()
        elif len(self._extents) < self._owner.GetColumnCount():
            self._extents.extend([None] * (self._owner.GetColumnCount() - len(self._extents)))
        # Are we grabbing all extents?
        if column is None:
            # Scan all extents.
            main_width, max_height = (0, 0)
            main_column = self._owner.GetMainColumn()
            for column, extent in enumerate(self._extents):
                if extent is None:
                    text = self.GetText(column)
                    if text or column == main_column:
                        # Always get extents for main column, even if blank.
                        width, height, hl = dc.GetFullMultiLineTextExtent(text)
                    else:
                        # Blank text, no need for extents.
                        width = height = 0
                    self._extents[column] = (width, height)
                else:
                    width, height = extent
                if column == main_column:
                    main_width = width
                max_height = height if height > max_height else max_height
            # Return main column width and max height amonst all columns.
            return main_width, max_height
        elif column < len(self._extents):
            if self._extents[column] is None and dc is not None:
                # Need to calculate
                text = self.GetText(column)
                width, height, dummy = dc.GetFullMultiLineTextExtent(text)
                self._extents[column] = (width, height)
            return self._extents[column]
        return None


    def GetText(self, column=None):
        """
        Returns the item text label.

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        column = self._owner.GetMainColumn() if column is None else column

        if len(self._text) > 0:
            if self._owner.IsVirtual():
                return self._owner.GetItemText(self._data, column)
            else:
                return self._text[column]

        return ""


    def GetImage(self, which=wx.TreeItemIcon_Normal, column=None):
        """
        Returns the item image for a particular item state.

        :param `which`: can be one of the following bits:

         ================================= ========================
         Item State                        Description
         ================================= ========================
         ``TreeItemIcon_Normal``           To get the normal item image
         ``TreeItemIcon_Selected``         To get the selected item image (i.e. the image which is shown when the item is currently selected)
         ``TreeItemIcon_Expanded``         To get the expanded image (this only makes sense for items which have children - then this image is shown when the item is expanded and the normal image is shown when it is collapsed)
         ``TreeItemIcon_SelectedExpanded`` To get the selected expanded image (which is shown when an expanded item is currently selected)
         ================================= ========================

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.

        :return: An integer index that can be used to retrieve the item
         image inside a :class:`wx.ImageList`.
        """

        column = self._owner.GetMainColumn() if column is None else column

        if column == self._owner.GetMainColumn():
            return self._images[which]

        if column < len(self._col_images):
            return self._col_images[column]

        return _NO_IMAGE


    def GetCurrentImage(self, column=None):
        """
        Returns the current item image.

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        if column is None or column == self._owner.GetMainColumn():
            # Main column image depends on item state. Use base class method.
            return GenericTreeItem.GetCurrentImage(self)
        # Return column image.
        return self.GetImage(column=column)


    def SetText(self, column, text):
        """
        Sets the item text label.

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used;
        :param `text`: a string specifying the new item label.
        
        :note: Call :meth:`~TreeListMainWindow.SetItemText` instead to refresh the tree properly.
        """
        column = self._owner.GetMainColumn() if column is None else column

        if column < self._owner.GetColumnCount():
            if column >= len(self._text):
                self._text.extend([""] * (column - len(self._text) + 1))
            self._text[column] = text
            # Set dirty flag and clear extents for this column.
            self._dirty = True
            if self._extents and column < len(self._extents):
                self._extents[column] = None


    def SetImage(self, column, image, which):
        """
        Sets the item image for a particular item state.

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used;
        :param `image`: an index within the normal image list specifying the image to use;
        :param `which`: The item state for which this image applies. One
         of wx.TreeItemIcon_Xxx. Only valid for the main column.

        :see: :meth:`~TreeListItem.GetImage` for a list of valid item states.
        
        :note: Call :meth:`~TreeListMainWindow.SetItemImage` instead to refresh the tree properly.
        """

        if column is None or column == self._owner.GetMainColumn():
            # Set tree column image (one of 4 wx.TreeItemIcon.XXX states).
            if self._images[which] != image:
                # Only set image if different.
                self._images[which] = image
                # Only go dirty if the current image state was modified.
                if which == self.GetCurrentImageState():
                    self._dirty = True
        elif column < self._owner.GetColumnCount():
            # Set column image.
            if column >= len(self._col_images):
                self._col_images.extend([_NO_IMAGE] * (column - len(self._col_images) + 1))
            if self._col_images[column] != image:
                # Only set image if different.
                self._col_images[column] = image
                self._dirty = True


    def GetTextX(self):
        """ Returns the `x` position of the item text. """

        return self._text_x


    def SetTextX(self, text_x):
        """
        Sets the `x` position of the item text. Used internally to position
        text according to column alignment.

        :param `text_x`: the `x` position of the item text.
        """

        self._text_x = text_x


    def SetWindow(self, wnd, column=None):
        """
        Sets the window associated to the item. Internal use only.

        :param `wnd`: a non-toplevel window to be displayed next to the item;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
         
        :note: Always use :meth:`~TreeListMainWindow.SetItemWindow` instead to update the tree properly.
        """

        column = self._owner.GetMainColumn() if column is None else column
        if column < 0 or column >= self._owner.GetColumnCount():
            # Invalid column number.
            return

        if type(self._wnd) is not list:
            # Convert self._wnd to array, putting window in main column.
            main_wnd = self._wnd
            self._wnd = [None] * self._owner.GetColumnCount()
            self._wnd[self._owner.GetMainColumn()] = main_wnd
        elif len(self._wnd) < self._owner.GetColumnCount():
            # Extend array to owner's column count size.
            self._wnd.extend([None] * (self._owner.GetColumnCount() - len(self._wnd)))

        self._wnd[column] = wnd
        self._dirty = True

        if self not in self._owner._itemWithWindow:
            self._owner._itemWithWindow.add(self)

        # We have to bind the wx.EVT_SET_FOCUS for the associated window
        # No other solution to handle the focus changing from an item in
        # HyperTreeList and the window associated to an item
        # Do better strategies exist?
        wnd.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

        ## Hide the window since the position isn't correct yet. It will
        ## be shown and positioned when the tree is calculated.
        wnd.Show(False)

        # The window is enabled only if the item is enabled
        wnd.Enable(self._enabled)


    def OnSetFocus(self, event):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for a window associated to an item.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        treectrl = self._owner
        select = treectrl.GetSelection()
        # Refresh header window since child focus could have moved scrollbars.
        treectrl.GetParent().GetHeaderWindow().Refresh()

        # If the window is associated to an item that currently is selected
        # (has focus) we don't kill the focus. Otherwise we do it.
        if select != self:
            treectrl._hasFocus = False
        else:
            treectrl._hasFocus = True

        event.Skip()


    def GetWindow(self, column=None):
        """
        Returns the window associated to the item.

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        column = self._owner.GetMainColumn() if column is None else column

        if column >= len(self._wnd):
            return None

        return self._wnd[column]


    def DeleteWindow(self, column=None):
        """
        Deletes the window associated to the item (if any).

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        column = self._owner.GetMainColumn() if column is None else column

        if column >= len(self._wnd):
            return

        wnd = self._wnd[column]
        if wnd:
            wnd.Destroy()
            self._wnd[column] = None
            self._dirty = True
            if not any(self._wnd) and self in self._owner._itemWithWindow:
                self._owner._itemWithWindow.remove(self)


    def GetWindowEnabled(self, column=None):
        """
        Returns whether the window associated with an item is enabled or not.

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        column = self._owner.GetMainColumn() if column is None else column

        if not self._wnd[column]:
            raise Exception("\nERROR: This Item Has No Window Associated At Column %s" % column)

        return self._wnd[column].IsEnabled()


    def SetWindowEnabled(self, enable=True, column=None):
        """
        Sets whether the window associated with an item is enabled or not.

        :param `enable`: ``True`` to enable the associated window, ``False`` to disable it;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        column = self._owner.GetMainColumn() if column is None else column

        if not self._wnd[column]:
            raise Exception("\nERROR: This Item Has No Window Associated At Column %s" % column)

        self._wnd[column].Enable(enable)


    def GetWindowSize(self, column=None):
        """
        Returns the associated window size.

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        column = self._owner.GetMainColumn() if column is None else column

        if not self._wnd[column]:
            raise Exception("\nERROR: This Item Has No Window Associated At Column %s" % column)

        return self._wnd[column].GetSize()


    def GetWindows(self):
        """Returns a list of all associated windows. May be empty list."""
        return [wnd for wnd in self._wnd if wnd] if self._wnd else []


    def GetBackgroundColour(self, column=0):
        """
        Returns the associated background colour

        :param `column` an integer specifying the column index.
        """

        if column >= len(self._bgColour):
            return None

        return self._bgColour[column]

    def SetBackgroundColour(self, colour, column=0):
        """
        Sets the associated background colour

        :param `colour`: a valid :class:`wx.Colour` instance.
        :param integer `column`
        """

        if type(self._bgColour) is not list:
            self._bgColour = [self._bgColour]

        if column < len(self._bgColour):
            self._bgColour[column] = colour
        elif column < self._owner.GetColumnCount():
            self._bgColour.extend([None] * (column - len(self._bgColour) + 1))
            self._bgColour[column] = colour


#-----------------------------------------------------------------------------
# EditTextCtrl (internal)
#-----------------------------------------------------------------------------


class EditCtrl(object):
    """
    Base class for controls used for in-place edit.
    """

    def __init__(self, parent, id=wx.ID_ANY, item=None, column=None, owner=None,
                 value="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 validator=wx.DefaultValidator, name="editctrl", **kwargs):
        """
        Default class constructor.

        :param `parent`: the window parent. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used;
        :param `owner`: the window owner, in this case an instance of :class:`TreeListMainWindow`;
        :param `value`: the initial value in the control;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the window style;
        :param `validator`: the window validator;
        :param `name`: the window name.
        """
        self._owner = owner
        self._startValue = value
        self._itemEdited = item
        self._finished = False

        column = (column is not None and [column] or [self._owner.GetMainColumn()])[0]

        self._column = column

        w = self._itemEdited.GetWidth()
        h = self._itemEdited.GetHeight()

        wnd = self._itemEdited.GetWindow(column)
        if wnd:
            w = w - self._itemEdited.GetWindowSize(column)[0]
            h = 0

        x = item.GetX()

        if column > 0:
            x = 0

        for i in range(column):
            if not self._owner.GetParent()._header_win.IsColumnShown(i):
                continue    # do next column if not shown

            col = self._owner.GetParent()._header_win.GetColumn(i)
            wCol = col.GetWidth()
            x += wCol

        x, y = self._owner.CalcScrolledPosition(x + 2, item.GetY())

        image_w = image_h = wcheck = hcheck = 0
        image = item.GetCurrentImage(column)

        if image != _NO_IMAGE:

            if self._owner._imageListNormal:
                image_w, image_h = self._owner._imageListNormal.GetSize(image)
                image_w += 2 * _MARGIN

            else:

                raise Exception("\n ERROR: You Must Create An Image List To Use Images!")

        if column > 0:
            checkimage = item.GetCurrentCheckedImage()
            if checkimage is not None:
                wcheck, hcheck = self._owner._imageListCheck.GetSize(checkimage)
                wcheck += 2 * _MARGIN

        if wnd:
            h = max(hcheck, image_h)
            dc = wx.ClientDC(self._owner)
            h = max(h, dc.GetTextExtent("Aq")[1])
            h = h + 2

        # FIXME: what are all these hardcoded 4, 8 and 11s really?
        x += image_w + wcheck
        w -= image_w + 2 * _MARGIN + wcheck

        super(EditCtrl, self).__init__(parent, id, value, wx.Point(x, y),
                                       wx.Size(w + 15, h),
                                       style=style | wx.SIMPLE_BORDER,
                                       name=name, **kwargs)

        if wx.Platform == "__WXMAC__":
            self.SetFont(owner.GetFont())
            bs = self.GetBestSize()
            self.SetSize((-1, bs.height))

        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)


    def item(self):
        """Returns the item currently edited."""

        return self._itemEdited


    def column(self):
        """Returns the column currently edited."""

        return self._column


    def StopEditing(self):
        """Suddenly stops the editing."""

        self._owner.OnCancelEdit()
        self.Finish()


    def Finish(self):
        """Finish editing."""

        if not self._finished:

            self._finished = True
            self._owner.SetFocusIgnoringChildren()
            self._owner.ResetEditControl()


    def AcceptChanges(self):
        """Accepts/refuses the changes made by the user."""

        value = self.GetValue()

        if value == self._startValue:
            # nothing changed, always accept
            # when an item remains unchanged, the owner
            # needs to be notified that the user decided
            # not to change the tree item label, and that
            # the edit has been cancelled
            self._owner.OnCancelEdit()
            return True
        else:
            return self._owner.OnAcceptEdit(value)


    def OnKillFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`EditCtrl`

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        # We must let the native control handle focus, too, otherwise
        # it could have problems with the cursor (e.g., in wxGTK).
        event.Skip()



class EditTextCtrl(EditCtrl, wx.TextCtrl):
    """
    Text control used for in-place edit.
    """

    def __init__(self, parent, id=wx.ID_ANY, item=None, column=None, owner=None,
                 value="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 validator=wx.DefaultValidator, name="edittextctrl", **kwargs):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param `parent`: the window parent. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used;
        :param `owner`: the window owner, in this case an instance of :class:`TreeListMainWindow`;
        :param `value`: the initial value in the text control;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the window style;
        :param `validator`: the window validator;
        :param `name`: the window name.
        """

        super(EditTextCtrl, self).__init__(parent, id, item, column, owner,
                                           value, pos, size, style, validator,
                                           name, **kwargs)
        self.SelectAll()

        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)


    def OnChar(self, event):
        """
        Handles the ``wx.EVT_CHAR`` event for :class:`EditTextCtrl`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        keycode = event.GetKeyCode()

        if keycode in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER] and not event.ShiftDown():
            # Notify the owner about the changes
            self.AcceptChanges()
            # Even if vetoed, close the control (consistent with MSW)
            wx.CallAfter(self.Finish)

        elif keycode == wx.WXK_ESCAPE:
            # This calls self.Finish() which calls _owner.ResetEditControl()
            # which calls Destroy() on this EditCtrl. We cannot destroy this
            # edit control while handing an event for it otherwise wxWidgets
            # v3.1+ on GTK2/3 will seg fault. So we must use wx.CallAfter.
            wx.CallAfter(self.StopEditing)

        else:
            event.Skip()


    def OnKeyUp(self, event):
        """
        Handles the ``wx.EVT_KEY_UP`` event for :class:`EditTextCtrl`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        if not self._finished:

            # auto-grow the textctrl:
            parentSize = self._owner.GetSize()
            myPos = self.GetPosition()
            mySize = self.GetSize()

            sx, sy = self.GetTextExtent(self.GetValue() + "M")
            if myPos.x + sx > parentSize.x:
                sx = parentSize.x - myPos.x
            if mySize.x > sx:
                sx = mySize.x

            self.SetSize((sx, -1))

        event.Skip()



# ---------------------------------------------------------------------------
# TreeListMainWindow implementation
# ---------------------------------------------------------------------------

class TreeListMainWindow(CustomTreeCtrl):
    """
    This class represents the main window (and thus the main column) in :class:`HyperTreeList`.

    :note: This is a subclass of :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl`.
    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, agwStyle=wx.TR_DEFAULT_STYLE, validator=wx.DefaultValidator,
                 name="wxtreelistmainwindow"):
        """
        Default class constructor.

        :param `parent`: parent window. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the underlying :class:`ScrolledWindow` style;
        :param `agwStyle`: can be a combination of various bits. See
         :mod:`~wx.lib.agw.hypertreelist` for a full list of flags.
        :param `validator`: window validator;
        :param `name`: window name.
        """

        self._buffered = False

        CustomTreeCtrl.__init__(self, parent, id, pos, size, style, agwStyle, validator, name)

        self._shiftItem = None
        self._editItem = None
        ## Note: self._selectItem currently does nothing. It appears to
        ## have been an abandoned attempt to replicate the logic that
        ## customtreectrl subclass uses self._select_me for.
        self._selectItem = None

        self._curColumn = -1    # no current column
        self._owner = parent
        self._main_column = 0
        self._dragItem = None

        self._imgWidth = self._imgWidth2 = 0
        self._imgHeight = self._imgHeight2 = 0
        self._btnWidth = self._btnWidth2 = 0
        self._btnHeight = self._btnHeight2 = 0
        self._checkWidth = self._checkWidth2 = 0
        self._checkHeight = self._checkHeight2 = 0
        self._agwStyle = agwStyle
        self._current = None

        # TextCtrl initial settings for editable items
        self._editTimer = TreeListEditTimer(self)
        self._left_down_selection = False

        self._dragTimer = wx.Timer(self)
        self._findTimer = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.Bind(wx.EVT_SCROLLWIN, self.OnScroll)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, lambda evt: None)

        # Sets the focus to ourselves: this is useful if you have items
        # with associated widgets.
        self.SetFocus()
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)


    def SetBuffered(self, buffered):
        """
        Sets/unsets the double buffering for the main window.

        :param `buffered`: ``True`` to use double-buffering, ``False`` otherwise.

        :note: Currently we are using double-buffering only on Windows XP.
        """

        self._buffered = buffered
        if buffered:
            self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        else:
            self.SetBackgroundStyle(wx.BG_STYLE_ERASE)


    def IsVirtual(self):
        """ Returns ``True`` if :class:`TreeListMainWindow` has the ``TR_VIRTUAL`` flag set. """

        return self.HasAGWFlag(TR_VIRTUAL)


#-----------------------------------------------------------------------------
# functions to work with tree items
#-----------------------------------------------------------------------------

    def GetItemImage(self, item, column=None, which=wx.TreeItemIcon_Normal):
        """
        Returns the item image.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used;
        :param `which`: can be one of the following bits:

         ================================= ========================
         Item State                        Description
         ================================= ========================
         ``TreeItemIcon_Normal``           To get the normal item image
         ``TreeItemIcon_Selected``         To get the selected item image (i.e. the image which is shown when the item is currently selected)
         ``TreeItemIcon_Expanded``         To get the expanded image (this only makes sense for items which have children - then this image is shown when the item is expanded and the normal image is shown when it is collapsed)
         ``TreeItemIcon_SelectedExpanded`` To get the selected expanded image (which is shown when an expanded item is currently selected)
         ================================= ========================
        """
        # wx.lib.mixins.TreeAPIHarmonizer uses -1 for default column!
        column = self._main_column if column in (None, -1) else column

        return item.GetImage(which, column)


    def SetItemImage(self, item, image, column=None, which=wx.TreeItemIcon_Normal):
        """
        Sets the item image for a particular item state.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `image`: an index within the normal image list specifying the image to use;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used;
        :param `which`: the item state.

        :see: :meth:`~TreeListMainWindow.GetItemImage` for a list of valid item states.
        """
        # wx.lib.mixins.TreeAPIHarmonizer uses -1 for default column!
        column = self._main_column if column in (None, -1) else column
        # Force 'image' to integer index and set (flag errors now).
        image = _NO_IMAGE if image is None else int(image)
        item.SetImage(column, image, which)
        # Calculate new size of item, if dirty.
        if not self._dirty and item.IsDirty() and self.IsItemShown(item):
            # Calculate item size to see if it changed height.
            old_height = self.GetLineHeight(item)
            dc = self._freezeDC if self._freezeDC else wx.ClientDC(self)
            self.CalculateSize(item, dc)
            # If the height changes, we need to recalculate the tree.
            if self.GetLineHeight(item) != old_height:
                self._dirty = True
            else:
                self.RefreshLine(item)


    def GetItemWindowEnabled(self, item, column=None):
        """
        Returns whether the window associated with an item is enabled or not.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        return item.GetWindowEnabled(column)


    def GetItemWindow(self, item, column=None):
        """
        Returns the window associated with an item.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        return item.GetWindow(column)


    def SetItemWindow(self, item, window, column=None):
        """
        Sets the window associated to an item.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `wnd`: a non-toplevel window to be displayed next to the item;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.

        :note: The window being added should have its parent set to the :class:`TreeListMainWindow`
         which can be obtained with :meth:`~HyperTreeList.GetHeaderWindow`. If this is not the case
         the window will be re-parented which may cause some flicker.
        """

        # Reparent the window to ourselves
        if window.GetParent() != self:
            window.Reparent(self)

        item.SetWindow(window, column)
        if window:
            self._hasWindows = True

        # Recalculate tree during idle time.
        if item.IsDirty():
            self._dirty = True

    def SetItemWindowEnabled(self, item, enable=True, column=None):
        """
        Sets whether the window associated with an item is enabled or not.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `enable`: ``True`` to enable the associated window, ``False`` to disable it;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        item.SetWindowEnabled(enable, column)

    def DeleteItemWindow(self, item, column=None):
        """
        Deletes the window in the column associated to an item (if any).

        :param `item`: an instance of :class:`GenericTreeItem`.
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """
        item.DeleteWindow(column=column)

    def GetItemBackgroundColour(self, item, column=0):
        """
        Returns the column background colour of the item

        :param `item`: an instance of :class:`TreeListItem`
        :param integer `column`
        """

        return item.GetBackgroundColour(column)

    def SetItemBackgroundColour(self, item, colour, column=0):
        """
        Sets the column background colour of the item

        :param `item`: an instance of :class:`TreeListItem`
        :param `colour`: a valid :class:`wx.Colour` instance.
        :param integer `column`
        """

        item.SetBackgroundColour(colour, column)

        if column == 0:
            item.Attr().SetBackgroundColour(colour)

        self.RefreshLine(item)

# ----------------------------------------------------------------------------
# navigation
# ----------------------------------------------------------------------------

    def IsItemVisible(self, item):
        """
        Returns whether the item is visible or not.

        :param `item`: an instance of :class:`TreeListItem`;
        
        :note: This method is renamed from :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.IsVisible`
        """
        return self.IsVisible(item)


    def GetPrevChild(self, item, cookie):
        """
        Returns the previous child of an item.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `cookie`: a parameter which is opaque for the application but is necessary
         for the library to make these functions reentrant (i.e. allow more than one
         enumeration on one and the same object simultaneously).

        :note: This method returns ``None`` if there are no further siblings.
        """

        children = item.GetChildren()

        if cookie >= 0:
            return children[cookie], cookie - 1
        else:
            # there are no more of them
            return None, cookie


    def GetFirstExpandedItem(self):
        """ Returns the first item which is in the expanded state. """

        return self.GetNextExpanded(self.GetRootItem())


    def GetNextExpanded(self, item):
        """
        Returns the next expanded item after the input one.

        :param `item`: an instance of :class:`TreeListItem`.
        """

        return CustomTreeCtrl.GetNextExpanded(self, item)


    def GetPrevExpanded(self, item):
        """
        Returns the previous expanded item before the input one.

        :param `item`: an instance of :class:`TreeListItem`.
        """

        return CustomTreeCtrl.GetPrevExpanded(self, item)


    def GetFirstVisibleItem(self):
        """ Returns the first visible item. """

        root = self.GetRootItem()
        if not root:
            return None

        if not self.HasAGWFlag(TR_HIDE_ROOT):
            if self.IsItemVisible(root):
                return root

        return self.GetNextVisible(root)


    def GetPrevVisible(self, item):
        """
        Returns the previous visible item before the input one.

        :param `item`: an instance of :class:`TreeListItem`.
        """

        i = self.GetPrev(item)
        while i:
            if self.IsItemVisible(i):
                return i
            i = self.GetPrev(i)

        return None


# ----------------------------------------------------------------------------
# operations
# ----------------------------------------------------------------------------

    def DoInsertItem(self, parent, previous, text, ct_type=0, wnd=None, image=-1, selImage=-1, data=None, *ignored_args):
        """
        Actually inserts an item in the tree.

        :param `parentId`: an instance of :class:`TreeListItem` representing the
         item's parent;
        :param `previous`: the index at which we should insert the item;
        :param `text`: the item text label;
        :param `ct_type`: the item type (see :meth:`CustomTreeCtrl.SetItemType() <lib.agw.customtreectrl.CustomTreeCtrl.SetItemType>` for a list of valid
         item types);
        :param `wnd`: if not ``None``, a non-toplevel window to show next to the item;
        :param `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param `data`: associate the given Python object `data` with the item.
        :param `ignored_args`: unused at the moment, this parameter is present to comply with
         :meth:`CustomTreeCtrl.DoInsertItem() <lib.agw.customtreectrl.CustomTreeCtrl.DoInsertItem>` changed API.
        """

        self._dirty = True  # do this first so stuff below doesn't cause flicker

        # Tree strings must be valid utf8 or we will crash on GetExtent calls.
        text = EnsureText(text)

        arr = [""] * self.GetColumnCount()
        arr[self._main_column] = text

        if not parent:
            # should we give a warning here?
            return self.AddRoot(text, ct_type, wnd, image, selImage, data)

        self._dirty = True     # do this first so stuff below doesn't cause flicker

        item = TreeListItem(self, parent, arr, ct_type, wnd, image, selImage, data)

        if wnd is not None:
            self._hasWindows = True
            self._itemWithWindow.add(item)

        parent.Insert(item, previous)

        return item


    def AddRoot(self, text, ct_type=0, wnd=None, image=-1, selImage=-1, data=None):
        """
        Adds a root item to the :class:`TreeListMainWindow`.

        :param `text`: the item text label;
        :param `ct_type`: the item type (see :meth:`CustomTreeCtrl.SetItemType() <lib.agw.customtreectrl.CustomTreeCtrl.SetItemType>`
         for a list of valid item types);
        :param `wnd`: if not ``None``, a non-toplevel window to show next to the item;
        :param `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param `data`: associate the given Python object `data` with the item.

        .. warning::

           Only one root is allowed to exist in any given instance of :class:`TreeListMainWindow`.

        """

        if self._anchor:
            raise Exception("\nERROR: Tree Can Have Only One Root")

        if wnd is not None and not (self._agwStyle & wx.TR_HAS_VARIABLE_ROW_HEIGHT):
            raise Exception("\nERROR: In Order To Append/Insert Controls You Have To Use The Style TR_HAS_VARIABLE_ROW_HEIGHT")

        if text.find("\n") >= 0 and not (self._agwStyle & wx.TR_HAS_VARIABLE_ROW_HEIGHT):
            raise Exception("\nERROR: In Order To Append/Insert A MultiLine Text You Have To Use The Style TR_HAS_VARIABLE_ROW_HEIGHT")

        if ct_type < 0 or ct_type > 2:
            raise Exception("\nERROR: Item Type Should Be 0 (Normal), 1 (CheckBox) or 2 (RadioButton). ")

        self._dirty = True     # do this first so stuff below doesn't cause flicker
        arr = [""] * self.GetColumnCount()
        arr[self._main_column] = text
        self._anchor = TreeListItem(self, None, arr, ct_type, wnd, image, selImage, data)

        if wnd is not None:
            self._hasWindows = True
            self._itemWithWindow.add(self._anchor)

        if self.HasAGWFlag(wx.TR_HIDE_ROOT):
            # if root is hidden, make sure we can navigate
            # into children
            self._anchor.SetHasPlus()
            self._anchor.Expand()
            self.CalculatePositions()

        if not self.HasAGWFlag(wx.TR_MULTIPLE):
            self._current = self._key_current = self._selectItem = self._anchor
            self.SetItemHilight(self._anchor, True)

        return self._anchor


    def Delete(self, item):
        """
        Deletes an item.

        :param `item`: an instance of :class:`TreeListItem`.
        """

        if not item:
            raise Exception("\nERROR: Invalid Tree Item. ")

        self._dirty = True     # do this first so stuff below doesn't cause flicker

        if self._editCtrl is not None and self.IsDescendantOf(item, self._editCtrl.item()):
            # can't delete the item being edited, cancel editing it first
            self._editCtrl.StopEditing()

        # don't stay with invalid self._shiftItem or we will crash in the next call to OnChar()
        changeKeyCurrent = False
        itemKey = self._shiftItem

        while itemKey:
            if itemKey == item:  # self._shiftItem is a descendant of the item being deleted
                changeKeyCurrent = True
                break

            itemKey = itemKey.GetParent()

        parent = item.GetParent()
        if parent:
            parent.GetChildren().remove(item)  # remove by value

        if changeKeyCurrent:
            self._shiftItem = parent

        self.SendDeleteEvent(item)
        if self._selectItem == item:
            self._selectItem = None

        # Remove the item with window
        if item in self._itemWithWindow:
            for wnd in item._wnd:
                if wnd:
                    wnd.Hide()
                    wnd.Destroy()

            item._wnd = []
            self._itemWithWindow.remove(item)

        item.DeleteChildren(self)
        del item


    # Don't leave edit or selection on a child which is about to disappear
    def ChildrenClosing(self, item):
        """
        We are about to destroy the item's children.

        :param `item`: an instance of :class:`TreeListItem`.
        """
        # If editing a descendant of this item, stop editing before collapsing.
        if (self._editCtrl is not None and item != self._editCtrl.item() and
            self.IsDescendantOf(item, self._editCtrl.item())):
            self._editCtrl.StopEditing()

        # self._selectItem is currently not used. This logic does nothing.
        if self.IsDescendantOf(item, self._selectItem):
            self._selectItem = item

        # If a descendant is currently selected, select the item instead.
        if item != self._current and self.IsDescendantOf(item, self._current):
            # Deselect the currently selected descendant.
            self.SetItemHilight(self._current, False)
            self._current = None
            # Flag item to be selected in the next idle handler.
            self._select_me = item


    def DeleteRoot(self):
        """
        Removes the tree root item (and subsequently all the items in
        :class:`TreeListMainWindow`.
        """

        if self._anchor:

            self._dirty = True
            self._anchor.DeleteChildren(self)
            self.Delete(self._anchor)

            self.SendDeleteEvent(self._anchor)
            self._current = None
            self._selectItem = None
            del self._anchor
            self._anchor = None


    def DeleteAllItems(self):
        """ Delete all items in the :class:`TreeListMainWindow`. """

        self.DeleteRoot()


    def HideWindows(self):
        """Scans all item windows in the tree and hides those whose items
        they belong to are not currently visible. Used internally. """

        for child in self._itemWithWindow:
            if not self.IsItemVisible(child):
                for column in range(self.GetColumnCount()):
                    wnd = child.GetWindow(column)
                    if wnd and wnd.IsShown():
                        wnd.Hide()


    def HideItemWindows(self, item):
        """Hides all windows belonging to given item and its children."""
        # Hide windows for this item.
        for wnd in item.GetWindows():
            if wnd.IsShown():
                wnd.Hide()
        # Hide its child windows.
        for child in item.GetChildren():
            self.HideItemWindows(child)


    def EnableItem(self, item, enable=True, torefresh=True):
        """
        Enables/disables an item.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `enable`: ``True`` to enable the item, ``False`` otherwise;
        :param `torefresh`: whether to redraw the item or not.
        """

        if item.IsEnabled() == enable:
            return

        if not enable and item.IsSelected():
            self.DoSelectItem(item, not self.HasAGWFlag(wx.TR_MULTIPLE))

        item.Enable(enable)

        for column in range(self.GetColumnCount()):
            wnd = item.GetWindow(column)

            # Handles the eventual window associated to the item
            if wnd:
                wnd.Enable(enable)

        if torefresh:
            # We have to refresh the item line
            dc = self._freezeDC if self._freezeDC else wx.ClientDC(self)
            self.CalculateSize(item, dc)
            self.RefreshLine(item)


    def IsItemEnabled(self, item):
        """
        Returns whether an item is enabled or disabled.

        :param `item`: an instance of :class:`TreeListItem`.
        """

        return item.IsEnabled()


    def GetCurrentItem(self):
        """Returns the current item.

        This is the same as :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetSelection`.
        """

        return self.GetSelection()


    def GetColumnCount(self):
        """ Returns the total number of columns. """

        return self._owner.GetHeaderWindow().GetColumnCount()


    def SetMainColumn(self, column):
        """
        Sets the :class:`HyperTreeList` main column (i.e. the position of the underlying
        :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl`.

        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        if column >= 0 and column < self.GetColumnCount():
            self._main_column = column


    def GetMainColumn(self):
        """
        Returns the :class:`HyperTreeList` main column (i.e. the position of the underlying
        :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl`.
        """

        return self._main_column


    def ScrollTo(self, item):
        """
        Scrolls the specified item into view.

        :param `item`: an instance of :class:`TreeListItem`.
        """

        if not item:
            return

        # ensure that the position of the item it calculated in any case
        if self._dirty:
            self.CalculatePositions()

        # now scroll to the item
        item_y = item.GetY()
        xUnit, yUnit = self.GetScrollPixelsPerUnit()
        start_x, start_y = self.GetViewStart()
        start_y *= yUnit
        client_w, client_h = self.GetClientSize()

        x = self._owner.GetHeaderWindow().GetWidth()
        x_pos = self.GetScrollPos(wx.HORIZONTAL)

        ## Note: The Scroll() method updates all child window positions
        ##       while the SetScrollBars() does not (on most platforms).
        if item_y < start_y + 3:
            # going down, item should appear at top
            self.Scroll(x_pos, (item_y // yUnit) if yUnit > 0 else 0)

        elif item_y + self.GetLineHeight(item) > start_y + client_h:
            # going up, item should appear at bottom
            item_y += yUnit + 2
            self.Scroll(x_pos, ((item_y + self.GetLineHeight(item) - client_h) // yUnit) if yUnit > 0 else 0)


    def SetDragItem(self, item):
        """
        Sets the specified item as member of a current drag and drop operation.

        :param `item`: an instance of :class:`TreeListItem`.
        """

        prevItem = self._dragItem
        self._dragItem = item
        if prevItem:
            self.RefreshLine(prevItem)
        if self._dragItem:
            self.RefreshLine(self._dragItem)


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

    def AdjustMyScrollbars(self, tree_size=None):
        """Internal method used to adjust the :class:`ScrolledWindow` scrollbars.

        This method is always called at the end of CalculatePositions() if the
        tree size has changed.

        :param `tree_size`: The full size of the current tree as a wx.Size or
         (width, height) tuple. If not specified it will be calculated.
        """
        if self._freezeCount:
            # Skip if frozen. Set dirty flag to adjust when thawed.
            self._dirty = True
            return
        
        if self._anchor:
            if tree_size is not None:
                x, y = tree_size
            else:
                x, y = self._anchor.GetSize(0, 0, self)
            xUnit, yUnit = self.GetScrollPixelsPerUnit()
            if xUnit == 0:
                xUnit = self.GetCharWidth()
            if yUnit == 0:
                yUnit = self._lineHeight
            y += yUnit + 2  # one more scrollbar unit + 2 pixels
            x_pos = self.GetScrollPos(wx.HORIZONTAL)
            y_pos = self.GetScrollPos(wx.VERTICAL)
            x = self._owner.GetHeaderWindow().GetWidth() + 2
            if x < self.GetClientSize().GetWidth():
                x_pos = 0

            self.SetScrollbars(xUnit, yUnit, x // xUnit, y // yUnit, x_pos, y_pos)
        else:
            # No root item. Reset scrollbars.
            self.SetScrollbars(0, 0, 0, 0)


    def PaintItem(self, item, dc):
        """
        Actually draws an item.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `dc`: an instance of :class:`wx.DC`.
        """

        def _paintText(text, textrect, alignment):
            """
            Sub-function to draw multi-lines text label aligned correctly.

            :param `text`: the item text label (possibly multiline);
            :param `textrect`: the label client rectangle;
            :param `alignment`: the alignment for the text label, one of ``wx.ALIGN_LEFT``,
             ``wx.ALIGN_RIGHT``, ``wx.ALIGN_CENTER``.
            """

            txt = text.splitlines()
            if alignment != wx.ALIGN_LEFT and len(txt):
                yorigin = textrect.Y
                for t in txt:
                    w, h = dc.GetTextExtent(t)
                    plus = textrect.Width - w
                    if alignment == wx.ALIGN_CENTER:
                        plus //= 2
                    dc.DrawLabel(t, wx.Rect(textrect.X + plus, yorigin, w, yorigin + h))
                    yorigin += h
                return
            dc.DrawLabel(text, textrect)

        # Set the font for this item.
        attr = item.GetAttributes()
        if item.IsHyperText():
            dc.SetFont(self.GetHyperTextFont())
            if item.GetVisited():
                dc.SetTextForeground(self.GetHyperTextVisitedColour())
            else:
                dc.SetTextForeground(self.GetHyperTextNewColour())
        elif attr and attr.HasFont():
            dc.SetFont(attr.GetFont())
        elif item.IsBold():
            dc.SetFont(self._boldFont)
        elif item.IsItalic():
            dc.SetFont(self._italicFont)
        else:
            dc.SetFont(self._normalFont)

        colText = wx.Colour(*dc.GetTextForeground())

        if item.IsSelected():
            colTextHilight = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)

        else:
            attr = item.GetAttributes()
            if attr and attr.HasTextColour():
                colText = attr.GetTextColour()

        if self._vistaselection:
            colText = colTextHilight = wx.BLACK

        total_w = self._owner.GetHeaderWindow().GetWidth()
        total_h = self.GetLineHeight(item)
        off_h = (self.HasAGWFlag(TR_ROW_LINES) and [1] or [0])[0]
        off_w = (self.HasAGWFlag(TR_COLUMN_LINES) and [1] or [0])[0]
##        clipper = wx.DCClipper(dc, 0, item.GetY(), total_w, total_h) # only within line

        text_w, text_h, dummy = dc.GetFullMultiLineTextExtent(item.GetText(self.GetMainColumn()))

        drawItemBackground = False
        # determine background and show it
        if attr and attr.HasBackgroundColour():
            colBg = attr.GetBackgroundColour()
            drawItemBackground = True
        else:
            colBg = self._backgroundColour

        dc.SetBrush(wx.Brush(colBg))
        if attr and attr.HasBorderColour():
            colBorder = attr.GetBorderColour()
            dc.SetPen(wx.Pen(colBorder, 1))
        else:
            dc.SetPen(wx.TRANSPARENT_PEN)

        if self.HasAGWFlag(wx.TR_FULL_ROW_HIGHLIGHT):
            # Draw any highlight or background across entire row.
            itemrect = wx.Rect(0, item.GetY() + off_h, total_w - 1, total_h - off_h)

            if item == self._dragItem:
                dc.SetBrush(self._hilightBrush)
                if wx.Platform == "__WXMAC__":
                    dc.SetPen((item == self._dragItem) and [wx.BLACK_PEN] or [wx.TRANSPARENT_PEN])[0]

                dc.SetTextForeground(colTextHilight)

            elif item.IsSelected():
                # Draw selection rectangle over entire row (all columns)
                wnd = item.GetWindow(self._main_column)
                wndx = 0
                if wnd:
                    wndx, wndy = item.GetWindowSize(self._main_column)

                itemrect = wx.Rect(0, item.GetY() + off_h, total_w - 1, total_h - off_h)

                if self._usegradients:
                    if self._gradientstyle == 0:   # Horizontal
                        self.DrawHorizontalGradient(dc, itemrect, self._hasFocus)
                    else:                          # Vertical
                        self.DrawVerticalGradient(dc, itemrect, self._hasFocus)
                elif self._vistaselection:
                    self.DrawVistaRectangle(dc, itemrect, self._hasFocus)
                else:
                    if wx.Platform in ["__WXGTK2__", "__WXMAC__"]:
                        flags = wx.CONTROL_SELECTED
                        if self._hasFocus:
                            flags = flags | wx.CONTROL_FOCUSED
                        wx.RendererNative.Get().DrawItemSelectionRect(self._owner, dc, itemrect, flags)
                    else:
                        dc.SetBrush((self._hasFocus and [self._hilightBrush] or [self._hilightUnfocusedBrush])[0])
                        dc.SetPen((self._hasFocus and [self._borderPen] or [wx.TRANSPARENT_PEN])[0])
                        dc.DrawRectangle(itemrect)

                dc.SetTextForeground(colTextHilight)

            # On GTK+ 2, drawing a 'normal' background is wrong for themes that
            # don't allow backgrounds to be customized. Not drawing the background,
            # except for custom item backgrounds, works for both kinds of theme.
            elif drawItemBackground and not self.HasAGWFlag(TR_FILL_WHOLE_COLUMN_BACKGROUND):
                # Draw background color under all columns only if TR_FILL_WHOLE_COLUMN_BACKGROUND is not set.
                itemrect = wx.Rect(0, item.GetY() + off_h, total_w - 1, total_h - off_h)
                dc.SetBrush(wx.Brush(colBg))
                dc.DrawRectangle(itemrect)
                dc.SetTextForeground(colText)

            else:
                dc.SetTextForeground(colText)

        else:

            dc.SetTextForeground(colText)

        text_extraH = (total_h > text_h and [(total_h - text_h) // 2] or [0])[0]
        img_extraH = (total_h > self._imgHeight and [(total_h - self._imgHeight) // 2] or [0])[0]
        x_colstart = 0

        # Draw all columns for this item.
        for i in range(self.GetColumnCount()):
            if not self._owner.GetHeaderWindow().IsColumnShown(i):
                continue

            col_w = self._owner.GetHeaderWindow().GetColumnWidth(i)
            dc.SetClippingRegion(x_colstart, item.GetY(), col_w, total_h)   # only within column

            image = _NO_IMAGE
            x = image_w = wcheck = hcheck = 0

            if i == self.GetMainColumn():
                x = item.GetX() + _MARGIN
                if self.HasButtons():
                    x += (self._btnWidth - self._btnWidth2) + _LINEATROOT
                else:
                    x -= self._indent // 2

                if self._imageListNormal:
                    image = item.GetCurrentImage(i)

                if item.GetType() != 0 and self._imageListCheck:
                    checkimage = item.GetCurrentCheckedImage()
                    wcheck, hcheck = self._imageListCheck.GetSize(item.GetType())
                else:
                    wcheck, hcheck = 0, 0

            else:
                x = x_colstart + _MARGIN
                image = item.GetImage(column=i)

            if image != _NO_IMAGE:
                image_w = self._imgWidth + _MARGIN

            # honor text alignment
            text = item.GetText(i)
            alignment = self._owner.GetHeaderWindow().GetColumn(i).GetAlignment()

            text_w, dummy, dummy = dc.GetFullMultiLineTextExtent(text)

            left_x = x + (2 * _MARGIN if image_w == 0 and wcheck else 0)
            if alignment == wx.ALIGN_RIGHT:
                w = col_w - (image_w + wcheck + text_w + off_w + _MARGIN + 1)
                x += (w > 0 and [w] or [0])[0]

            elif alignment == wx.ALIGN_CENTER:
                w = (col_w - (image_w + wcheck + text_w + off_w + _MARGIN)) // 2
                x += (w > 0 and [w] or [0])[0]
            else:
                x = left_x

            text_x = x + image_w + wcheck + 1
            left_x = left_x + image_w + wcheck + 1

            if i == self.GetMainColumn():
                item.SetTextX(text_x)

            if not self.HasAGWFlag(wx.TR_FULL_ROW_HIGHLIGHT):
                # Draw item background for column i with FULL_ROW_HIGHLIGHT off.
                dc.SetBrush((self._hasFocus and [self._hilightBrush] or [self._hilightUnfocusedBrush])[0])
                dc.SetPen((self._hasFocus and [self._borderPen] or [wx.TRANSPARENT_PEN])[0])
                if i == self.GetMainColumn():
                    # Main column (Tree).
                    if item == self._dragItem:
                        if wx.Platform == "__WXMAC__":  # don't draw rect outline if we already have the background colour
                            dc.SetPen((item == self._dragItem and [wx.BLACK_PEN] or [wx.TRANSPARENT_PEN])[0])

                        dc.SetTextForeground(colTextHilight)

                    elif item.IsSelected():
                        # If fill whole column background set, draw background
                        # before selection, since selection covers only text.
                        if drawItemBackground and self.HasAGWFlag(TR_FILL_WHOLE_COLUMN_BACKGROUND):
                            itemrect = wx.Rect(x_colstart, item.GetY() + off_h, col_w, total_h - off_h)
                            dc.SetBrush(wx.Brush(colBg))
                            dc.SetPen(wx.TRANSPARENT_PEN)
                            dc.DrawRectangle(itemrect)
                            dc.SetBrush(self._hilightBrush if self._hasFocus else self._hilightUnfocusedBrush)
                            dc.SetPen(self._borderPen if self._hasFocus else wx.TRANSPARENT_PEN)

                        # Draw selection over text only.
                        itemrect = wx.Rect(text_x - 2, item.GetY() + off_h, text_w + 2 * _MARGIN, total_h - off_h)
                        if self._usegradients:
                            if self._gradientstyle == 0:   # Horizontal
                                self.DrawHorizontalGradient(dc, itemrect, self._hasFocus)
                            else:                          # Vertical
                                self.DrawVerticalGradient(dc, itemrect, self._hasFocus)
                        elif self._vistaselection:
                            self.DrawVistaRectangle(dc, itemrect, self._hasFocus)
                        else:
                            if wx.Platform in ["__WXGTK2__", "__WXMAC__"]:
                                flags = wx.CONTROL_SELECTED
                                if self._hasFocus:
                                    flags = flags | wx.CONTROL_FOCUSED
                                wx.RendererNative.Get().DrawItemSelectionRect(self._owner, dc, itemrect, flags)
                            else:
                                dc.DrawRectangle(itemrect)
                        dc.SetTextForeground(colTextHilight)

                    elif item == self._current:
                        dc.SetPen((self._hasFocus and [wx.BLACK_PEN] or [wx.TRANSPARENT_PEN])[0])

                    # On GTK+ 2, drawing a 'normal' background is wrong for themes that
                    # don't allow backgrounds to be customized. Not drawing the background,
                    # except for custom item backgrounds, works for both kinds of theme.
                    elif drawItemBackground:

                        if self.HasAGWFlag(TR_FILL_WHOLE_COLUMN_BACKGROUND):
                            # Draw background under entire main tree width.
                            itemrect = wx.Rect(x_colstart, item.GetY() + off_h, col_w, total_h - off_h)
                        else:
                            # Draw background only behind the text.
                            itemrect = wx.Rect(text_x - 2, item.GetY() + off_h, text_w + 2 * _MARGIN, total_h - off_h)
                        dc.SetBrush(wx.Brush(colBg))
                        dc.SetPen(wx.TRANSPARENT_PEN)
                        dc.DrawRectangle(itemrect)

                    else:
                        dc.SetTextForeground(colText)

                else:
                    # Regular column (non-tree).
                    if self.HasAGWFlag(TR_FILL_WHOLE_COLUMN_BACKGROUND):
                        itemrect = wx.Rect(x_colstart, item.GetY() + off_h, col_w, total_h - off_h)
                    else:
                        itemrect = wx.Rect(text_x - 2, item.GetY() + off_h, text_w + 2 * _MARGIN, total_h - off_h)
                    colBgX = item.GetBackgroundColour(i)

                    if colBgX is not None and i != 0:
                        dc.SetBrush(wx.Brush(colBgX, wx.SOLID))
                        dc.SetPen(wx.TRANSPARENT_PEN)
                        dc.DrawRectangle(itemrect)

                    dc.SetTextForeground(colText)

            else:
                # TR_FULL_ROW_HIGHLIGHT is ON. The background has already been
                # drawn for selected items. If TR_FILL_WHOLE_COLUMN_BACKGROUND
                # is not set, it has also been drawn for all columns.
                if not item.IsSelected():
                    itemrect = None
                    if self.HasAGWFlag(TR_FILL_WHOLE_COLUMN_BACKGROUND):
                        # Full-row highlight has been suppressed. Draw background for entire column.
                        itemrect = wx.Rect(x_colstart, item.GetY() + off_h, col_w, total_h - off_h)
                    elif i != self.GetMainColumn():
                        # Allow column-specific backgrounds to draw overtop of any full row highlight.
                        itemrect = wx.Rect(text_x - 2, item.GetY() + off_h, text_w + 2 * _MARGIN, total_h - off_h)
                    colBgX = item.GetBackgroundColour(i)
                    if itemrect is not None and colBgX is not None:
                        dc.SetBrush(wx.Brush(colBgX, wx.SOLID))
                        dc.SetPen(wx.TRANSPARENT_PEN)
                        dc.DrawRectangle(itemrect)


            if self.HasAGWFlag(TR_COLUMN_LINES):  # vertical lines between columns
                pen = wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT), 1, wx.PENSTYLE_SOLID)
                dc.SetPen((self.GetBackgroundColour() == wx.WHITE and [pen] or [wx.WHITE_PEN])[0])
                dc.DrawLine(x_colstart + col_w - 1, item.GetY(), x_colstart + col_w - 1, item.GetY() + total_h)

            dc.SetBackgroundMode(wx.TRANSPARENT)

            if image != _NO_IMAGE:
                y = item.GetY() + img_extraH
                if wcheck:
                    x += wcheck

                if item.IsEnabled():
                    imglist = self._imageListNormal
                else:
                    imglist = self._grayedImageList

                imglist.Draw(image, dc, x, y, wx.IMAGELIST_DRAW_TRANSPARENT)

            if wcheck:
                if item.IsEnabled():
                    imglist = self._imageListCheck
                else:
                    imglist = self._grayedCheckList

                if self.HasButtons():  # should the item show a button?
                    btnWidth = self._btnWidth
                else:
                    btnWidth = -self._btnWidth

                imglist.Draw(checkimage, dc,
                             item.GetX() + btnWidth + _MARGIN,
                             item.GetY() + ((total_h > hcheck) and [(total_h - hcheck) // 2] or [0])[0] + 1,
                             wx.IMAGELIST_DRAW_TRANSPARENT)

            if self.HasAGWFlag(TR_ELLIPSIZE_LONG_ITEMS):
                if i == self.GetMainColumn():
                    maxsize = col_w - text_x - _MARGIN
                else:
                    maxsize = col_w - (wcheck + image_w + _MARGIN)

                text = ChopText(dc, text, maxsize)

            text_w, text_h, dummy = dc.GetFullMultiLineTextExtent(text)
            text_extraH = (total_h > text_h and [(total_h - text_h) // 2] or [0])[0]
            text_y = item.GetY() + text_extraH
            textrect = wx.Rect(text_x, text_y, text_w, text_h)

            if not item.IsEnabled():
                foreground = dc.GetTextForeground()
                dc.SetTextForeground(self._disabledColour)
                _paintText(text, textrect, alignment)
                dc.SetTextForeground(foreground)
            else:
                if (wx.Platform == "__WXMAC__" and item.IsSelected() and
                    self._hasFocus and i == self.GetMainColumn()):
                    # Use white on Macs, but only on the primary column if
                    # TR_FULL_ROW_HIGHLIGHT is NOT turned on.
                    dc.SetTextForeground(wx.WHITE)
                _paintText(text, textrect, alignment)

            wnd = item.GetWindow(i)
            if wnd:
                if text_w == 0:
                    # No text. Honor column alignment for window.
                    if alignment == wx.ALIGN_RIGHT:
                        # text_x = right edge of window
                        wndx = text_x - wnd.GetSize().width
                    elif alignment == wx.ALIGN_CENTER:
                        # text_x = center of window
                        wndx = text_x - (wnd.GetSize().width // 2)
                    else:
                        # text_x = left of window (default).
                        wndx = text_x
                else:
                    if alignment == wx.ALIGN_RIGHT:
                        # Place window left of text with 2*_MARGIN in between.
                        wndx = text_x - 2 * _MARGIN - wnd.GetSize().width
                    else:
                        # Place window at end of text plus 2*_MARGIN (default).
                        wndx = text_x + text_w + 2 * _MARGIN
                xa, ya = self.CalcScrolledPosition(0, item.GetY())
                wndx += xa
                if item.GetHeight() > item.GetWindowSize(i)[1]:
                    ya += (item.GetHeight() - item.GetWindowSize(i)[1]) // 2

                if wnd.GetPosition() != (wndx, ya):
                    wnd.Move(wndx, ya, flags=wx.SIZE_ALLOW_MINUS_ONE)
                # Force window visible after any position changes were made.
                if not wnd.IsShown():
                    wnd.Show()

            x_colstart += col_w
            dc.DestroyClippingRegion()


    # Now y stands for the top of the item, whereas it used to stand for middle !
    def PaintLevel(self, item, dc, level, y, x_maincol):
        """
        Paint a level in the hierarchy of :class:`TreeListMainWindow`.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `dc`: an instance of :class:`wx.DC`;
        :param `level`: the item level in the tree hierarchy;
        :param `y`: the current vertical position in the :class:`ScrolledWindow`;
         It is no longer used. Instead each item's Y position is set by
         the CalculatePositions() method.
        :param `x_maincol`: the horizontal position of the main column.
        """
        # Don't paint hidden items.
        if item.IsHidden():
            return y, x_maincol

        # Get this item's X,Y position.
        x = item.GetX()
        y = item.GetY()

        # Handle hide root (only level 0)
        if level == 0 and self.HasAGWFlag(wx.TR_HIDE_ROOT):
            # Always expand hidden root.
            children = item.GetChildren()
            for child in children:
                y, x_maincol = self.PaintLevel(child, dc, 1, y, x_maincol)

            ## TODO: This is where we would draw the vertical line for
            ## TR_HIDE_ROOT trees if TR_LINES_AT_ROOT style is set.
            ## CustomTreeCtrl does this but it was never implemented here?

            # end after expanding root
            return y, x_maincol

        h = self.GetLineHeight(item)
        y_top = y
        y_mid = y_top + (h // 2)
        y += h

        exposed_x = dc.LogicalToDeviceX(0)
        exposed_y = dc.LogicalToDeviceY(y_top)

        # horizontal lines between rows?
        draw_row_lines = self.HasAGWFlag(TR_ROW_LINES)

        if self.IsExposed(exposed_x, exposed_y, _MAX_WIDTH, h + int(draw_row_lines)):
            # Save window text color.
            prevText = wx.Colour(*dc.GetTextForeground())

            # draw item
            self.PaintItem(item, dc)

            # restore DC objects
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.SetPen(self._dottedPen)

            # clip to the column width
            clip_width = self._owner.GetHeaderWindow().GetColumn(self._main_column).GetWidth()
##            clipper = wx.DCClipper(dc, x_maincol, y_top, clip_width, 10000)

            if not self.HasAGWFlag(wx.TR_NO_LINES):  # connection lines

                # draw the horizontal line here
                dc.SetPen(self._dottedPen)
                x2 = x - self._indent
                if x2 < (x_maincol + _MARGIN):
                    x2 = x_maincol + _MARGIN
                x3 = x + (self._btnWidth - self._btnWidth2)
                if self.HasButtons():
                    if item.HasPlus():
                        dc.DrawLine(x2, y_mid, x - self._btnWidth2, y_mid)
                        dc.DrawLine(x3, y_mid, x3 + _LINEATROOT, y_mid)
                    else:
                        dc.DrawLine(x2, y_mid, x3 + _LINEATROOT, y_mid)
                else:
                    dc.DrawLine(x2, y_mid, x - self._indent // 2, y_mid)

            if item.HasPlus() and self.HasButtons():  # should the item show a button?

                if self._imageListButtons:

                    # draw the image button here
                    image = wx.TreeItemIcon_Normal
                    if item.IsExpanded():
                        image = wx.TreeItemIcon_Expanded
                    if item.IsSelected():
                        image += wx.TreeItemIcon_Selected - wx.TreeItemIcon_Normal
                    xx = x - self._btnWidth2 + _MARGIN
                    yy = y_mid - self._btnHeight2
                    dc.SetClippingRegion(xx, yy, self._btnWidth, self._btnHeight)
                    self._imageListButtons.Draw(image, dc, xx, yy, wx.IMAGELIST_DRAW_TRANSPARENT)
                    dc.DestroyClippingRegion()

                elif self.HasAGWFlag(wx.TR_TWIST_BUTTONS):

                    # draw the twisty button here
                    dc.SetPen(wx.BLACK_PEN)
                    dc.SetBrush(self._hilightBrush)
                    button = [wx.Point() for j in range(3)]
                    if item.IsExpanded():
                        button[0].x = x - (self._btnWidth2 + 1)
                        button[0].y = y_mid - (self._btnHeight // 3)
                        button[1].x = x + (self._btnWidth2 + 1)
                        button[1].y = button[0].y
                        button[2].x = x
                        button[2].y = button[0].y + (self._btnHeight2 + 1)
                    else:
                        button[0].x = x - (self._btnWidth // 3)
                        button[0].y = y_mid - (self._btnHeight2 + 1)
                        button[1].x = button[0].x
                        button[1].y = y_mid + (self._btnHeight2 + 1)
                        button[2].x = button[0].x + (self._btnWidth2 + 1)
                        button[2].y = y_mid

                    dc.SetClippingRegion(x_maincol + _MARGIN, y_top, clip_width, h)
                    dc.DrawPolygon(button)
                    dc.DestroyClippingRegion()

                else:# if (HasAGWFlag(wxTR_HAS_BUTTONS))

                    rect = wx.Rect(x - self._btnWidth2, y_mid - self._btnHeight2, self._btnWidth, self._btnHeight)
                    flag = (item.IsExpanded() and [wx.CONTROL_EXPANDED] or [0])[0]
                    wx.RendererNative.GetDefault().DrawTreeItemButton(self, dc, rect, flag)

            if draw_row_lines:
                total_width = self._owner.GetHeaderWindow().GetWidth()
                # if the background colour is white, choose a
                # contrasting colour for the lines
                pen = wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT), 1, wx.PENSTYLE_SOLID)
                dc.SetPen((self.GetBackgroundColour() == wx.WHITE and [pen] or [wx.WHITE_PEN])[0])
                dc.DrawLine(0, y_top, total_width, y_top)
                dc.DrawLine(0, y_top + h, total_width, y_top + h)

            # restore DC objects
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.SetPen(self._dottedPen)
            dc.SetTextForeground(prevText)

        # If this item is expanded, handle its children.
        if item.IsExpanded():
            children = item.GetChildren()
            count = len(children)

            if count > 0:
                # Item has children. Draw only those that are visible.
                n = 0

                # Calculate start and end of client area in logical Y coordinates.
                width, height = self.GetClientSize()
                start_y = self.CalcUnscrolledPosition(0, 0)[1]
                last_y = self.CalcUnscrolledPosition(0, height)[1]

                # If this item is off the bottom of the screen, do nothing.
                if y_top > last_y:
                    return y, x_maincol  # Early exit (for TR_HIDE_ROOT only)

                # Binary search for first child that is within our draw area.
                n = BisectChildren(children, start_y)

                # Now paint only prospective children
                while n < count:
                    y, x_maincol = self.PaintLevel(children[n], dc, level + 1, y, x_maincol)
                    n = n + 1
                    if y > last_y:
                        break   # Early exit
                    
                if not self.HasAGWFlag(wx.TR_NO_LINES) and children:
                    # Draw vertical tree line down to middle of last child.
                    lastY = children[-1].GetY()
                    lastY += self.GetLineHeight(children[-1]) // 2

                    if self.HasButtons():
                        topY = y_mid + self._btnHeight2  # Half of ButtonHeight
                    else:
                        topY = y_mid + h // 2            # Half of LineHeight

                    # Clip the vertical line to only the visible portion.
                    # Required speedup since the default _dottedPen is a
                    # USER_DASH style that draws very slow on some platforms.
                    xOrigin, yOrigin = dc.GetDeviceOrigin()
                    yOrigin = abs(yOrigin)

                    # Move end points to the begining/end of the view?
                    if topY < yOrigin:
                        topY = yOrigin
                    if lastY > yOrigin + height:
                        lastY = yOrigin + height

                    # after the adjustments if topY is larger than lastY
                    # then the line isn't visible at all so don't draw anything
                    if topY < lastY:
                        dc.SetPen(self._dottedPen)
                        dc.DrawLine(x, topY, x, lastY)

        return y, x_maincol


# ----------------------------------------------------------------------------
# wxWindows callbacks
# ----------------------------------------------------------------------------

    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`TreeListMainWindow`.

        :param `event`: a :class:`EraseEvent` event to be processed.
        """

        # do not paint the background separately in buffered mode.
        if not self._buffered:
            CustomTreeCtrl.OnEraseBackground(self, event)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`TreeListMainWindow`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        if self._buffered:

            # paint the background
            dc = wx.BufferedPaintDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRegion(rect)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            if self._backgroundImage:
                self.TileBackground(dc)
            else:
                dc.Clear()

        else:
            dc = wx.PaintDC(self)

        self.PrepareDC(dc)

        if not self._anchor or self._freezeCount or self.GetColumnCount() <= 0:
            return

        # If the tree is dirty, recalculate it. Required for paint.
        if self._dirty is True:
            self.CalculatePositions()

        # Paint the tree.
        x_maincol = self._x_maincol
        y = 2
        y, x_maincol = self.PaintLevel(self._anchor, dc, 0, y, x_maincol)


    def HitTest(self, point, flags=0):
        """
        Calculates which (if any) item is under the given point, returning the tree item
        at this point plus extra information flags plus the item's column.

        :param `point`: an instance of :class:`wx.Point`, a point to test for hits;
        :param `flags`: a bitlist of the following values:

         ================================== =============== =================================
         HitTest Flags                      Hex Value       Description
         ================================== =============== =================================
         ``TREE_HITTEST_ABOVE``                         0x1 Above the client area
         ``TREE_HITTEST_BELOW``                         0x2 Below the client area
         ``TREE_HITTEST_NOWHERE``                       0x4 No item has been hit
         ``TREE_HITTEST_ONITEMBUTTON``                  0x8 On the button associated to an item
         ``TREE_HITTEST_ONITEMICON``                   0x10 On the icon associated to an item
         ``TREE_HITTEST_ONITEMINDENT``                 0x20 On the indent associated to an item
         ``TREE_HITTEST_ONITEMLABEL``                  0x40 On the label (string) associated to an item
         ``TREE_HITTEST_ONITEM``                       0x50 Anywhere on the item
         ``TREE_HITTEST_ONITEMRIGHT``                  0x80 On the right of the label associated to an item
         ``TREE_HITTEST_TOLEFT``                      0x200 On the left of the client area
         ``TREE_HITTEST_TORIGHT``                     0x400 On the right of the client area
         ``TREE_HITTEST_ONITEMUPPERPART``             0x800 On the upper part (first half) of the item
         ``TREE_HITTEST_ONITEMLOWERPART``            0x1000 On the lower part (second half) of the item
         ``TREE_HITTEST_ONITEMCHECKICON``            0x2000 On the check/radio icon, if present
         ================================== =============== =================================

        :return: the item (if any, ``None`` otherwise), the `flags` and the column are always
         returned as a tuple.
        """

        w, h = self.GetSize()
        column = -1

        if not isinstance(point, wx.Point):
            point = wx.Point(*point)

        if point.x < 0:
            flags |= wx.TREE_HITTEST_TOLEFT
        if point.x > w:
            flags |= wx.TREE_HITTEST_TORIGHT
        if point.y < 0:
            flags |= wx.TREE_HITTEST_ABOVE
        if point.y > h:
            flags |= wx.TREE_HITTEST_BELOW
        if flags:
            return None, flags, column

        if not self._anchor:
            flags = wx.TREE_HITTEST_NOWHERE
            column = -1
            return None, flags, column

        pt = wx.Point(self.CalcUnscrolledPosition(point.x, point.y))
        hit, flags, column = self._anchor.HitTest(pt, self, flags, column, 0)
        if not hit:
            flags = wx.TREE_HITTEST_NOWHERE
            column = -1
            return None, flags, column

        return hit, flags, column


    def EditLabel(self, item, column=None):
        """
        Starts editing an item label.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        if not item:
            return

        column = (column is not None and [column] or [self._main_column])[0]

        if column < 0 or column >= self.GetColumnCount():
            return

        self._curColumn = column
        self._editItem = item

        te = TreeEvent(wx.wxEVT_COMMAND_TREE_BEGIN_LABEL_EDIT, self._owner.GetId())
        te.SetItem(self._editItem)
        te.SetInt(column)
        te.SetEventObject(self._owner)
        self._owner.GetEventHandler().ProcessEvent(te)

        if not te.IsAllowed():
            return

        # ensure that the position of the item it calculated in any case
        if self._dirty:
            self.CalculatePositions()

        if self._editCtrl is not None and (item != self._editCtrl.item() or column != self._editCtrl.column()):
            self._editCtrl.StopEditing()

        self._editCtrl = self._owner.CreateEditCtrl(item, column)
        self._editCtrl.SetFocus()


    def OnEditTimer(self):
        """ The timer for editing has expired. Start editing. """

        self.EditLabel(self._current, self._curColumn)


    def OnAcceptEdit(self, value):
        """
        Called by :class:`EditTextCtrl`, to accept the changes and to send the
        ``EVT_TREE_END_LABEL_EDIT`` event.

        :param `value`: the new value of the item label.
        """

        # TODO if the validator fails this causes a crash
        le = TreeEvent(wx.wxEVT_COMMAND_TREE_END_LABEL_EDIT, self._owner.GetId())
        le.SetItem(self._editItem)
        le.SetEventObject(self._owner)
        le.SetLabel(value)
        le.SetInt(self._curColumn if self._curColumn >= 0 else 0)
        le._editCancelled = False
        self._owner.GetEventHandler().ProcessEvent(le)

        if not le.IsAllowed():
            return

        if self._curColumn == -1:
            self._curColumn = 0

        self.SetItemText(self._editItem, str(value), self._curColumn)


    def OnCancelEdit(self):
        """
        Called by :class:`EditCtrl`, to cancel the changes and to send the
        ``EVT_TREE_END_LABEL_EDIT`` event.
        """

        # let owner know that the edit was cancelled
        le = TreeEvent(wx.wxEVT_COMMAND_TREE_END_LABEL_EDIT, self._owner.GetId())
        le.SetItem(self._editItem)
        le.SetEventObject(self._owner)
        le.SetLabel("")
        le._editCancelled = True

        self._owner.GetEventHandler().ProcessEvent(le)


    def OnMouse(self, event):
        """
        Handles the ``wx.EVT_MOUSE_EVENTS`` event for :class:`TreeListMainWindow`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self._anchor:
            return

        # we process left mouse up event (enables in-place edit), right down
        # (pass to the user code), left dbl click (activate item) and
        # dragging/moving events for items drag-and-drop
        if not (event.LeftDown() or event.LeftUp() or event.RightDown() or
                event.RightUp() or event.LeftDClick() or event.Dragging() or
                event.GetWheelRotation() != 0 or event.Moving()):
            self._owner.GetEventHandler().ProcessEvent(event)
            return


        # set focus if window clicked
        if event.LeftDown() or event.RightDown():
            self._hasFocus = True
            self.SetFocusIgnoringChildren()

        # determine event
        p = wx.Point(event.GetX(), event.GetY())
        flags = 0
        pt = wx.Point(self.CalcUnscrolledPosition(p.x, p.y))
        item, flags, column = self._anchor.HitTest(pt, self, flags, self._curColumn, 0)

        underMouse = item
        underMouseChanged = underMouse != self._underMouse

        if underMouse and (flags & wx.TREE_HITTEST_ONITEM) and not event.LeftIsDown() and \
           not self._isDragging and (not self._editTimer or not self._editTimer.IsRunning()):
            underMouse = underMouse
        else:
            underMouse = None

        if underMouse != self._underMouse:
            if self._underMouse:
                # unhighlight old item
                self._underMouse = None

            self._underMouse = underMouse

        # Determines what item we are hovering over and need a tooltip for
        hoverItem = item

        if (event.LeftDown() or event.LeftUp() or event.RightDown() or
            event.RightUp() or event.LeftDClick() or event.Dragging()):
            if self._editCtrl is not None and (item != self._editCtrl.item() or column != self._editCtrl.column()):
                self._editCtrl.StopEditing()

        # We do not want a tooltip if we are dragging, or if the edit timer is running
        if underMouseChanged and not self._isDragging and (not self._editTimer or not self._editTimer.IsRunning()):

            if hoverItem is not None:
                # Ask the tree control what tooltip (if any) should be shown
                hevent = TreeEvent(wx.wxEVT_COMMAND_TREE_ITEM_GETTOOLTIP, self.GetId())
                hevent.SetItem(hoverItem)
                hevent.SetEventObject(self)

                if self.GetEventHandler().ProcessEvent(hevent) and hevent.IsAllowed():
                    self.SetToolTip(hevent._label)

                if hoverItem.IsHyperText() and (flags & wx.TREE_HITTEST_ONITEMLABEL) and hoverItem.IsEnabled():
                    self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
                    self._isonhyperlink = True
                else:
                    if self._isonhyperlink:
                        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
                        self._isonhyperlink = False

        # we only process dragging here
        if event.Dragging():

            if self._isDragging:
                if not self._dragImage:
                    # Create the custom draw image from the icons and the text of the item
                    self._dragImage = DragImage(self, self._current or item)
                    # BeginDrag captures mouse. GTK cannot capture mouse twice.
                    if self.HasCapture() is True:
                        self.ReleaseMouse()
                    self._dragImage.BeginDrag(wx.Point(0, 0), self, fullScreen=self._dragFullScreen)
                    self._dragImage.Show()

                self._dragImage.Move(p)

                if self._dragFullScreen is True:
                    # Don't highlight target items if dragging full-screen.
                    return

                if self._countDrag == 0 and item:
                    self._oldItem = self._current
                    self._oldSelection = self._current

                if item != self._dropTarget:

                    # unhighlight the previous drop target
                    if self._dropTarget:
                        self.SetItemHilight(self._dropTarget, False)
                        self.RefreshLine(self._dropTarget)
                    if item:
                        self.SetItemHilight(item, True)
                        self.RefreshLine(item)
                        self._countDrag = self._countDrag + 1
                    self._dropTarget = item

                    self.Update()

                if self._countDrag >= 3 and self._oldItem is not None:
                    # Here I am trying to avoid ugly repainting problems... hope it works
                    self.RefreshLine(self._oldItem)
                    self._countDrag = 0

                return  # nothing to do, already done

            if item is None:
                return  # we need an item to dragging

            # determine drag start
            if self._dragCount == 0:
                self._dragTimer.Start(_DRAG_TIMER_TICKS, wx.TIMER_ONE_SHOT)

            self._dragCount += 1
            if self._dragCount < 3:
                return  # minimum drag 3 pixel
            if self._dragTimer.IsRunning():
                return

            # we're going to drag
            self._dragCount = 0

            # send drag start event
            command = (event.LeftIsDown() and [wx.wxEVT_COMMAND_TREE_BEGIN_DRAG] or [wx.wxEVT_COMMAND_TREE_BEGIN_RDRAG])[0]
            nevent = TreeEvent(command, self._owner.GetId())
            nevent.SetEventObject(self._owner)
            nevent.SetItem(self._current)   # the dragged item
            nevent.SetPoint(p)
            nevent.Veto()         # dragging must be explicit allowed!

            if self.GetEventHandler().ProcessEvent(nevent) and nevent.IsAllowed():

                # we're going to drag this item
                self._isDragging = True
                self._left_down_selection = True    # Stop DoSelect on drag end.
                if not self.HasCapture():
                    self.CaptureMouse()
                self.RefreshSelected()

                # in a single selection control, hide the selection temporarily
                if not (self._agwStyle & wx.TR_MULTIPLE):
                    if self._oldSelection:

                        self.SetItemHilight(self._oldSelection, False)
                        self.RefreshLine(self._oldSelection)
                else:
                    selections = self.GetSelections()
                    if len(selections) == 1:
                        self._oldSelection = selections[0]
                        self.SetItemHilight(self._oldSelection, False)
                        self.RefreshLine(self._oldSelection)

        elif self._isDragging:  # any other event but not event.Dragging()

            # end dragging
            self._dragCount = 0
            self._isDragging = False
#            if self.HasCapture():
#                self.ReleaseMouse()
            self.RefreshSelected()

            # send drag end event event
            nevent = TreeEvent(wx.wxEVT_COMMAND_TREE_END_DRAG, self._owner.GetId())
            nevent.SetEventObject(self._owner)
            nevent.SetItem(item)    # the item the drag is started
            nevent.SetPoint(p)
            self._owner.GetEventHandler().ProcessEvent(nevent)

            if self._dragImage:
                self._dragImage.EndDrag()

            if self._dropTarget:
                self.SetItemHilight(self._dropTarget, False)
                self.RefreshLine(self._dropTarget)

            if self._oldSelection:
                self.SetItemHilight(self._oldSelection, True)
                self.RefreshLine(self._oldSelection)
                self._oldSelection = None

            self._isDragging = False
            self._dropTarget = None
            if self._dragImage:
                self._dragImage = None

            self.Refresh()

        elif self._dragCount > 0:  # just in case dragging is initiated

            # end dragging
            self._dragCount = 0

        # we process only the messages which happen on tree items
        if (item is None or not self.IsItemEnabled(item)) and not event.GetWheelRotation():
            self._owner.GetEventHandler().ProcessEvent(event)
            return

        # remember item at shift down
        if event.ShiftDown():
            if not self._shiftItem:
                self._shiftItem = self._current
        else:
            self._shiftItem = None

        if event.RightUp():

            self.SetFocus()
            nevent = TreeEvent(wx.wxEVT_COMMAND_TREE_ITEM_RIGHT_CLICK, self._owner.GetId())
            nevent.SetEventObject(self._owner)
            nevent.SetItem(item)    # the item clicked
            nevent.SetInt(self._curColumn)  # the column clicked
            nevent.SetPoint(p)
            self._owner.GetEventHandler().ProcessEvent(nevent)

        elif event.LeftUp():

            if self._lastOnSame:
                if (item == self._current and self._curColumn != -1 and
                    self._owner.GetHeaderWindow().IsColumnEditable(self._curColumn) and
                    flags & (wx.TREE_HITTEST_ONITEMLABEL | TREE_HITTEST_ONITEMCOLUMN) and
                    ((self._editCtrl is not None and column != self._editCtrl.column()) or self._editCtrl is None)):
                    self._editTimer.Start(_EDIT_TIMER_TICKS, wx.TIMER_ONE_SHOT)

                self._lastOnSame = False

            if (((flags & wx.TREE_HITTEST_ONITEMBUTTON) or (flags & wx.TREE_HITTEST_ONITEMICON)) and
                self.HasButtons() and item.HasPlus()):

                # only toggle the item for a single click, double click on
                # the button doesn't do anything (it toggles the item twice)
                if event.LeftDown():
                    self.Toggle(item)

                # don't select the item if the button was clicked
                return

            # determine the selection if not done by left down
            if not self._left_down_selection:
                unselect_others = not ((event.ShiftDown() or event.CmdDown()) and self.HasAGWFlag(wx.TR_MULTIPLE))
                self.DoSelectItem(item, unselect_others, event.ShiftDown())
                self.EnsureVisible(item)
                self._current = self._key_current = item    # make the new item the current item
            else:
                self._left_down_selection = False

        elif event.LeftDown() or event.RightDown() or event.LeftDClick():

            if column >= 0:
                self._curColumn = column

            if event.LeftDown() or event.RightDown():
                self.SetFocus()
                self._lastOnSame = item == self._current

            if (((flags & wx.TREE_HITTEST_ONITEMBUTTON) or (flags & wx.TREE_HITTEST_ONITEMICON)) and
                self.HasButtons() and item.HasPlus()):

                # only toggle the item for a single click, double click on
                # the button doesn't do anything (it toggles the item twice)
                if event.LeftDown():
                    self.Toggle(item)

                # don't select the item if the button was clicked
                return

            if flags & TREE_HITTEST_ONITEMCHECKICON and event.LeftDown():
                if item.GetType() > 0:
                    if self.IsItem3State(item):
                        checked = self.GetItem3StateValue(item)
                        checked = (checked + 1) % 3
                    else:
                        checked = not self.IsItemChecked(item)

                    self.CheckItem(item, checked)
                    return

            # determine the selection if the current item is not selected
            if not item.IsSelected():
                unselect_others = not ((event.ShiftDown() or event.CmdDown()) and self.HasAGWFlag(wx.TR_MULTIPLE))
                self.DoSelectItem(item, unselect_others, event.ShiftDown())
                self.EnsureVisible(item)
                self._current = self._key_current = item    # make the new item the current item
                self._left_down_selection = True

            # For some reason, Windows isn't recognizing a left double-click,
            # so we need to simulate it here.  Allow 200 milliseconds for now.
            if event.LeftDClick():

                # double clicking should not start editing the item label
                self._editTimer.Stop()
                self._lastOnSame = False

                # send activate event first
                nevent = TreeEvent(wx.wxEVT_COMMAND_TREE_ITEM_ACTIVATED, self._owner.GetId())
                nevent.SetEventObject(self._owner)
                nevent.SetItem(item)    # the item clicked
                nevent.SetInt(self._curColumn)  # the column clicked
                nevent.SetPoint(p)
                if not self._owner.GetEventHandler().ProcessEvent(nevent):

                    # if the user code didn't process the activate event,
                    # handle it ourselves by toggling the item when it is
                    # double clicked
                    if item.HasPlus():
                        self.Toggle(item)

        else:
            # Any other event skip just in case.
            event.Skip()


    def OnScroll(self, event):
        """
        Handles the ``wx.EVT_SCROLLWIN`` event for :class:`TreeListMainWindow`.

        :param `event`: a :class:`ScrollEvent` event to be processed.
        """

        def _updateHeaderWindow(header):
            header.Refresh()
            header.Update()

        # Update the header window after this scroll event has fully finished
        # processing, and the scroll action is complete.
        if event.GetOrientation() == wx.HORIZONTAL:
            wx.CallAfter(_updateHeaderWindow, self._owner.GetHeaderWindow())
        event.Skip()


    def CalculateSize(self, item, dc):
        """
        Calculates overall position and size of an item.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `dc`: an instance of :class:`wx.DC`.
        """

        # Clear dirty flag.
        item.SetDirty(False)

        # Hidden items have a height of 0 and width is irrelevant.
        if item.IsHidden():
            item.SetHeight(0)
            return
        
        # Calcualte text width
        if item.HasExtents() is False:
            # Avoid this stuff unless necessary.
            attr = item.GetAttributes()
            if item.IsHyperText():
                font = self.GetHyperTextFont()  # Hypertext font.
            elif attr and attr.HasFont():
                font = attr.GetFont()           # User-defined font.
            elif item.IsBold():
                font = self._boldFont           # Bold font.
            elif item.IsItalic():
                font = self._italicFont         # Italics font.
            else:
                font = self._normalFont         # Default font.
            dc.SetFont(font)

        text_w, text_h = item.GetExtents(dc)
        text_h += 2

        wnd_w = wnd_h = 0
        for wnd in item.GetWindows():
            wnd_h = max(wnd_h, wnd.GetSize()[1])
        wnd = item.GetWindow(self._main_column)
        if wnd:
            wnd_w = wnd.GetSize()[0]

        image_w, image_h = 0, 0
        image = item.GetCurrentImage()
        if image != _NO_IMAGE:
            image_w = self._imgWidth + 2 * _MARGIN
            image_h = self._imgHeight
        total_h = image_h if image_h > text_h else text_h

        checkimage = item.GetCurrentCheckedImage()
        if checkimage is not None:
            wcheck, hcheck = self._checkWidth, self._checkHeight
            wcheck += 2 * _MARGIN
        else:
            wcheck = 0

        if total_h < 30:
            total_h += 2            # at least 2 pixels
        else:
            total_h += total_h // 10   # otherwise 10% extra spacing

        if total_h > self._lineHeight:
            self._lineHeight = max(total_h, wnd_h + 2)

        item.SetWidth(image_w + text_w + wcheck + 2 + wnd_w)
        item.SetHeight(max(total_h, wnd_h + 2))


    def CalculateLevel(self, item, dc, level, y, x_colstart):
        """
        Calculates the level of an item inside the tree hierarchy.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `dc`: an instance of :class:`wx.DC`;
        :param `level`: the item level in the tree hierarchy;
        :param `y`: the current vertical position in the :class:`ScrolledWindow`;
        :param `x_maincol`: the horizontal position of the main column.
        """

        # Indent according to level
        x = x_colstart + level * self._indent

        # Calculate the width and height of this item only if required.
        if item.IsDirty():
            self.CalculateSize(item, dc)

        # set its position
        item.SetX(x)
        item.SetY(y)

        # hidden items don't get a height (height=0).
        if item.IsHidden():
            return y
        height = self.GetLineHeight(item)

        for wnd in item.GetWindows():
            # Reposition all item windows.
            xa, ya = self.CalcScrolledPosition((0, y))
            wndx, wndy, wndWidth, wndHeight = wnd.GetRect()
            if height > wndHeight:
                ya += (height - wndHeight) // 2
            if wndy != ya:
                wnd.Move(wndx, ya, flags=wx.SIZE_ALLOW_MINUS_ONE)
            
        # Advance Y to next item and update tree width.
        y += height
        self._width = max(self._width, x + item.GetWidth())

        if not item.IsExpanded():
            # We don't need to calculate collapsed branches
            return y

        level = level + 1
        for child in item.GetChildren():
            y = self.CalculateLevel(child, dc, level, y, x_colstart)  # recurse

        return y


    def CalculatePositions(self):
        """Calculates the positions of all items in the tree.

        Used internally. Called to clear the self._dirty flag.
        """

        if not self._anchor:
            return
        if self._freezeCount:
            # Skip calculate if frozen. Set dirty flag to do this when thawed.
            self._dirty = True
            return

        dc = wx.ClientDC(self)
        self.PrepareDC(dc)

        # Save old tree dimensions. Reset width as CalculateLevel updates it.
        old_width, old_height = self._width, self._height
        self._width = 0

        # pre-calculate tree button size
        if self._imageListButtons:
            self._btnWidth, self._btnHeight = self._imageListButtons.GetSize(0)
        elif self.HasButtons():
            self._btnWidth = _BTNWIDTH
            self._btnHeight = _BTNHEIGHT
        self._btnWidth2 = self._btnWidth // 2
        self._btnHeight2 = self._btnHeight // 2

        # pre-calculate image size
        if self._imageListNormal:
            self._imgWidth, self._imgHeight = self._imageListNormal.GetSize(0)
        self._imgWidth2 = self._imgWidth // 2
        self._imgHeight2 = self._imgHeight // 2

        # pre-calculate checkbox/radio button size
        if self._imageListCheck:
            self._checkWidth, self._checkHeight = self._imageListCheck.GetSize(0)
        self._checkWidth2 = self._checkWidth // 2
        self._checkHeight2 = self._checkHeight // 2

        # pre-calculate indent size
        if self._imageListButtons:
            self._indent = max(_MININDENT, self._btnWidth + _MARGIN)
        elif self.HasButtons():
            self._indent = max(_MININDENT, self._btnWidth + _LINEATROOT)

        # Chintzy speedup for GetLineHeight() because it is called so often.
        if self.GetAGWWindowStyleFlag() & TR_HAS_VARIABLE_ROW_HEIGHT:
            self.GetLineHeight = lambda item: item.GetHeight()
        else:
            self.GetLineHeight = lambda item: self._lineHeight

        # Calculate X column start.
        x_colstart = 0
        for i in range(self.GetMainColumn()):
            if not self._owner.GetHeaderWindow().IsColumnShown(i):
                continue
            x_colstart += self._owner.GetHeaderWindow().GetColumnWidth(i)
        # Save parameter for use by OnPaint.
        self._x_maincol = x_colstart

        # Adjust x_colstart for margin size.
        x_colstart += _MARGIN  # start of column
        if self.HasAGWFlag(wx.TR_LINES_AT_ROOT):
            x_colstart += _LINEATROOT     # space for lines at root
        if self.HasButtons():
            x_colstart += (self._btnWidth - self._btnWidth2)    # half button
        else:
            x_colstart += (self._indent - self._indent // 2)

        # Calculate size of entire tree recursively.
        y = 2
        if not self.HasAGWFlag(TR_HIDE_ROOT):
            # Calculate tree from root.
            y = self.CalculateLevel(self._anchor, dc, 0, y, x_colstart)
        else:
            # A hidden root is not evaluated, but its children are.
            for child in self._anchor.GetChildren():
                y = self.CalculateLevel(child, dc, 0, y, x_colstart)
        self._height = y

        # Always update our scrollbars in case the header window size changed.
        self.AdjustMyScrollbars(tree_size=(self._width, self._height))

        # Clear tree dirty flag.
        self._dirty = False
        # Refresh entire window
        self.Refresh()


    def SetItemText(self, item, text, column=None):
        """
        Sets the item text label.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `text`: a string specifying the new item label;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        column = self.GetMainColumn() if column is None else column
        # Tree strings must be valid utf8 or we will crash on GetExtent calls.
        text = EnsureText(text)

        # Save old size and set item's text.
        old_size = item.GetExtents(column=column)
        item.SetText(column, text)

        # If tree already dirty don't attempt to refresh line.
        if self._dirty:
            return
        
        # Calculate new size of item's text.
        dc = self._freezeDC if self._freezeDC else wx.ClientDC(self)
        new_size = item.GetExtents(dc, column)
        # If text height changed (number of lines) we need to recalculate tree.
        if old_size is None or new_size[1] != old_size[1]:
            self._dirty = True
        else:
            self.RefreshLine(item)


    def GetItemText(self, item, column=None):
        """
        Returns the item text label.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: if not ``None``, an integer specifying the column index.
         If it is ``None``, the main column index is used.
        """

        if self.IsVirtual():
            return self._owner.OnGetItemText(item, column)
        else:
            return item.GetText(column)


    def GetItemWidth(self, item, column):
        """
        Returns the item width.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: an integer specifying the column index.
        """

        if not item:
            return 0

        if column == self.GetMainColumn():
            # Main column (tree). Calculate item size, if necessary.
            if item.IsDirty():
                dc = self._freezeDC if self._freezeDC else wx.ClientDC(self)
                self.CalculateSize(item, dc)
            width = item.GetX() - self._x_maincol + item.GetWidth() + _MARGIN + 1
            if self.HasButtons():
                width += (self._btnWidth - self._btnWidth2) + _LINEATROOT
            else:
                width -= self._indent // 2
        else:
            # Normal column
            if item.HasExtents(column) is False:
                # Avoid this stuff unless necessary.
                attr = item.GetAttributes()
                if item.IsHyperText():
                    font = self.GetHyperTextFont()  # Hypertext font.
                elif attr and attr.HasFont():
                    font = attr.GetFont()           # User-defined font.
                elif item.IsBold():
                    font = self._boldFont           # Bold font.
                elif item.IsItalic():
                    font = self._italicFont         # Italics font.
                else:
                    font = self._normalFont         # Default font.
                dc = self._freezeDC if self._freezeDC else wx.ClientDC(self)
                dc.SetFont(font)
            else:
                dc = None
            width, height = item.GetExtents(dc, column)
            width += 4 * _MARGIN
            # If this column has a window, factor that into its width.
            wnd = item.GetWindow(column)
            if wnd:
                width += wnd.GetSize()[0] + 2 * _MARGIN
        return width


    def GetBestColumnWidth(self, column, parent=None):
        """
        Returns the best column's width based on the items width in this column.

        :param `column`: an integer specifying the column index;
        :param `parent`: an instance of :class:`TreeListItem`.
        """

        maxWidth, h = self.GetClientSize()
        width = 0

        if maxWidth < 5:
            # Not shown on screen
            maxWidth = 1000

        # get root, if on item
        if not parent:
            parent = self.GetRootItem()

        # add root width
        if not self.HasAGWFlag(wx.TR_HIDE_ROOT):
            w = self.GetItemWidth(parent, column)
            if width < w:
                width = w
            if width > maxWidth:
                return maxWidth

        item, cookie = self.GetFirstChild(parent)
        while item:
            if item.IsHidden() is False:
                w = self.GetItemWidth(item, column)
                if width < w:
                    width = w
                if width > maxWidth:
                    return maxWidth

                # Recursively check expanded children of this item.
                if item.IsExpanded():
                    w = self.GetBestColumnWidth(column, item)
                    if width < w:
                        width = w
                    if width > maxWidth:
                        return maxWidth

            # next sibling
            item, cookie = self.GetNextChild(parent, cookie)

        return max(10, width)   # Prevent zero column width


#----------------------------------------------------------------------------
# TreeListCtrl - the multicolumn tree control
#----------------------------------------------------------------------------

## Monkey patch methods. Be sure to modify the docstring for HyperTreeList
## to reflect any changes to this list.
_methods = ["GetIndent", "SetIndent", "GetSpacing", "SetSpacing", "GetImageList", "GetStateImageList",
            "GetButtonsImageList", "AssignImageList", "AssignStateImageList", "AssignButtonsImageList",
            "SetImageList", "SetButtonsImageList", "SetStateImageList",
            "GetItemText", "GetItemImage", "GetItemPyData", "GetPyData", "GetItemTextColour",
            "GetItemBackgroundColour", "GetItemFont", "SetItemText", "SetItemImage", "SetItemPyData", "SetPyData",
            "SetItemHasChildren", "SetItemBackgroundColour", "SetItemFont", "IsItemVisible", "HasChildren",
            "IsExpanded", "IsSelected", "IsBold", "GetCount", "GetChildrenCount", "GetRootItem", "GetSelection", "GetSelections",
            "GetItemParent", "GetFirstChild", "GetNextChild", "GetPrevChild", "GetLastChild", "GetNextSibling",
            "GetPrevSibling", "GetNext", "GetFirstExpandedItem", "GetNextExpanded", "GetPrevExpanded", "GetFocusedItem",
            "GetFirstVisibleItem", "GetNextVisible", "GetPrevVisible", "AddRoot", "PrependItem", "InsertItem",
            "AppendItem", "Delete", "DeleteChildren", "DeleteRoot", "Expand", "ExpandAll", "ExpandAllChildren",
            "Collapse", "CollapseAndReset", "Toggle", "Unselect", "UnselectAll", "SelectItem", "SelectAll",
            "EnsureVisible", "ScrollTo", "HitTest", "GetBoundingRect", "EditLabel", "FindItem", "SelectAllChildren",
            "SetDragItem", "GetColumnCount", "SetMainColumn", "GetHyperTextFont", "SetHyperTextFont",
            "SetHyperTextVisitedColour", "GetHyperTextVisitedColour", "SetHyperTextNewColour", "GetHyperTextNewColour",
            "SetItemVisited", "GetItemVisited", "SetHilightFocusColour", "GetHilightFocusColour", "SetHilightNonFocusColour",
            "GetHilightNonFocusColour", "SetFirstGradientColour", "GetFirstGradientColour", "SetSecondGradientColour",
            "GetSecondGradientColour", "EnableSelectionGradient", "SetGradientStyle", "GetGradientStyle",
            "EnableSelectionVista", "SetBorderPen", "GetBorderPen", "SetConnectionPen", "GetConnectionPen",
            "SetBackgroundImage", "GetBackgroundImage", "SetImageListCheck", "GetImageListCheck", "EnableChildren",
            "EnableItem", "IsItemEnabled", "GetDisabledColour", "SetDisabledColour", "IsItemChecked",
            "UnCheckRadioParent", "CheckItem", "CheckItem2", "AutoToggleChild", "AutoCheckChild", "AutoCheckParent",
            "CheckChilds", "CheckSameLevel", "GetItemWindowEnabled", "SetItemWindowEnabled", "GetItemType",
            "IsDescendantOf", "SetItemHyperText", "IsItemHyperText", "SetItemBold", "SetItemDropHighlight", "SetItemItalic",
            "GetEditControl", "ShouldInheritColours", "GetItemWindow", "SetItemWindow", "DeleteItemWindow", "SetItemTextColour",
            "HideItem", "DeleteAllItems", "ItemHasChildren", "ToggleItemSelection", "SetItemType", "GetDragFullScreen", "SetDragFullScreen",
            "GetCurrentItem", "SetItem3State", "SetItem3StateValue", "GetItem3StateValue", "IsItem3State", "GetPrev",
            "GetNextShown", "GetPrevShown", "SetItemData", "GetItemData", "IsVisible", "EnableBellOnNoMatch"]


class HyperTreeList(wx.Control):
    """
    :class:`HyperTreeList` is a generic widget that combines the multicolumn
    features of a :class:`wx.ListCtrl` with the hierarchical features of a
    :class:`wx.TreeCtrl` This class does not rely on native native controls,
    as it is a full owner-drawn tree-list control.

    It manages two widgets internally:

    * :class:`TreeListHeaderWindow` displays the column headers.
    * :class:`TreeListMainWindow` is the main tree list based off :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl`.

    These widgets can be obtained by the :meth:`~HyperTreeList.GetHeaderWindow`
    and :meth:`~HyperTreeList.GetMainWindow` methods respectively although this
    shouldn't be needed in normal usage.

    Please note that in addition to the defined methods of :class:`HyperTreeList`
    many more methods are delegated to the internal :class:`TreeListMainWindow`
    and its subclass :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl`. These
    methods can be called directly from the ``HyperTreeList`` class:
    
    ================================================================================ ==================================================================================
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.AddRoot`                     Adds a root item to the :class:`TreeListMainWindow`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.AppendItem`                     Appends an item as a last child of its parent.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.AssignButtonsImageList`         Assigns the button image list.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.AssignImageList`                Assigns the normal image list.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.AssignStateImageList`           Assigns the state image list.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.AutoCheckChild`                 Transverses the tree and checks/unchecks the items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.AutoCheckParent`                Traverses up the tree and checks/unchecks parent items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.AutoToggleChild`                Transverses the tree and toggles the items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.CheckChilds`                    Programmatically check/uncheck item children.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.CheckItem`                      Actually checks/uncheks an item, sending the two related events.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.CheckItem2`                     Used internally to avoid ``EVT_TREE_ITEM_CHECKED`` events.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.CheckSameLevel`                 Uncheck radio items which are on the same level of the checked one.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.Collapse`                       Collapse an item, sending the two related events.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.CollapseAndReset`               Collapse the given item and deletes its children.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.Delete`                      Deletes an item.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.DeleteAllItems`              Delete all items in the :class:`TreeListMainWindow`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.DeleteChildren`                 Delete all the item's children.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.DeleteItemWindow`            Deletes the window in the column associated to an item (if any).
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.DeleteRoot`                  Removes the tree root item (and subsequently all the items in the tree).
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.EditLabel`                   Starts editing an item label.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.EnableChildren`                 Enables/disables the item children.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.EnableItem`                  Enables/disables an item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.EnableSelectionGradient`        Globally enables/disables drawing of gradient selections.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.EnableSelectionVista`           Globally enables/disables drawing of Windows Vista selections.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.EnsureVisible`                  Scrolls and/or expands items to ensure that the given item is visible.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.Expand`                         Expands an item, sending the two related events.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.ExpandAll`                      Expands all :class:`TreeListMainWindow` items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.ExpandAllChildren`              Expands all the items children of the input item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.FindItem`                       Finds the first item starting with the given prefix after the given parent.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetBackgroundImage`             Returns the :class:`TreeListMainWindow` background image (if any).
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetBorderPen`                   Returns the pen used to draw the selected item border.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetBoundingRect`                Retrieves the rectangle bounding the item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetButtonsImageList`            Returns the buttons image list associated with :class:`TreeListMainWindow`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetChildrenCount`               Returns the item children count.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetColumnCount`              Returns the total number of columns.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetConnectionPen`               Returns the pen used to draw the connecting lines between items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetCount`                       Returns the global number of items in the tree.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetCurrentItem`              Returns the current item. Simply calls :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetSelection`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetDisabledColour`              Returns the colour for items in a disabled state.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetDragFullScreen`              Returns whether built-in drag/drop will be full screen or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetEditControl`                 Returns a reference to the edit :class:`~wx.lib.agw.customtreectrl.TreeTextCtrl` if the item is being edited.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetFirstChild`                  Returns the item's first child and an integer value 'cookie'.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetFirstExpandedItem`        Returns the first item which is in the expanded state.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetFirstGradientColour`         Returns the first gradient colour for gradient-style selections.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetFirstVisibleItem`         Returns the first visible item.
    GetFocusedItem                                                                   Another name for :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetSelection`
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetGradientStyle`               Returns the gradient style for gradient-style selections.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetHilightFocusColour`          Returns the colour used to highlight focused selected items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetHilightNonFocusColour`       Returns the colour used to highlight unfocused selected items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetHyperTextFont`               Returns the font used to render hypertext items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetHyperTextNewColour`          Returns the colour used to render a non-visited hypertext item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetHyperTextVisitedColour`      Returns the colour used to render a visited hypertext item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetImageList`                   Returns the normal image list associated with :class:`TreeListMainWindow`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetImageListCheck`              Returns the ``wx.ImageList`` used for the check/radio buttons in :class:`TreeListMainWindow`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetIndent`                      Returns the item indentation, in pixels.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetItem3StateValue`             Gets the state of a 3-state checkbox item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetItemBackgroundColour`        Returns the item background colour.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetItemFont`                    Returns the item font.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetItemImage`                Returns the item image.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetItemParent`                  Returns the item parent (can be ``None`` for root items).
    GetItemPyData                                                                    Another name for :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetPyData`
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetItemText`                 Returns the item text label.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetItemTextColour`              Returns the item text colour or separator horizontal line colour.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetItemType`                    Returns the item type.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetItemVisited`                 Returns whether an hypertext item was visited.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetItemWindow`               Returns the window associated with an item.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetItemWindowEnabled`        Returns whether the window associated with an item is enabled or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetLastChild`                   Returns the item last child.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetNext`                        Returns the next item. Only for internal use right now.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetNextChild`                   Returns the item's next child.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetNextExpanded`             Returns the next expanded item after the input one.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetNextShown`                   Returns the next displayed item in the tree, visible or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetNextSibling`                 Returns the next sibling of an item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetNextVisible`                 Returns the next item that is visible to the user.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetPrev`                        Returns the previous item. Only for internal use right now.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetPrevChild`                Returns the previous child of an item.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetPrevExpanded`             Returns the previous expanded item before the input one.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetPrevShown`                   Returns the previous displayed item in the tree, visible or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetPrevSibling`                 Returns the previous sibling of an item.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.GetPrevVisible`              Returns the previous item visible to the user.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetPyData`                      Returns the data associated to an item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetRootItem`                    Returns the root item, an instance of :class:`GenericTreeItem`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetSecondGradientColour`        Returns the second gradient colour for gradient-style selections.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetSelection`                   Returns the current selection.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetSelections`                  Returns a list of selected items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetSpacing`                     Returns the spacing between the start and the text, in pixels.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.GetStateImageList`              Returns the state image list associated with :class:`TreeListMainWindow`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.HasChildren`                    Returns whether an item has children or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.HideItem`                       Hides/shows an item.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.HitTest`                     Finds which (if any) item is under the given point, returning the item plus flags.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.InsertItem`                     Inserts an item after the given previous.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.IsBold`                         Returns whether the item font is bold or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.IsDescendantOf`                 Checks if the given item is under another one in the tree hierarchy.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.IsExpanded`                     Returns whether the item is expanded or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.IsItem3State`                   Returns whether or not the checkbox item is a 3-state checkbox.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.IsItemChecked`                  Returns whether an item is checked or not.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.IsItemEnabled`               Returns whether an item is enabled or disabled.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.IsItemHyperText`                Returns whether an item is hypertext or not.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.IsItemVisible`               Returns whether the item is visible or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.IsSelected`                     Returns whether the item is selected or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.ItemHasChildren`                Returns whether the item has children or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.PrependItem`                    Prepends an item as a first child of parent.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.ScrollTo`                    Scrolls the specified item into view.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SelectAll`                      Selects all the item in the tree.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SelectAllChildren`              Selects all the children of the given item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SelectItem`                     Selects/deselects an item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetBackgroundImage`             Sets the :class:`TreeListMainWindow` background image.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetBorderPen`                   Sets the pen used to draw the selected item border.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetButtonsImageList`            Sets the buttons image list for :class:`TreeListMainWindow`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetConnectionPen`               Sets the pen used to draw the connecting lines between items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetDisabledColour`              Sets the colour for items in a disabled state.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetDragFullScreen`              Sets whether a drag operation will be performed full screen or not.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.SetDragItem`                 Sets the specified item as member of a current drag and drop operation.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetFirstGradientColour`         Sets the first gradient colour for gradient-style selections.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetGradientStyle`               Sets the gradient style for gradient-style selections.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetHilightFocusColour`          Sets the colour used to highlight focused selected items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetHilightNonFocusColour`       Sets the colour used to highlight unfocused selected items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetHyperTextFont`               Sets the font used to render hypertext items.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetHyperTextNewColour`          Sets the colour used to render a non-visited hypertext item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetHyperTextVisitedColour`      Sets the colour used to render a visited hypertext item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetImageList`                   Sets the normal image list for :class:`TreeListMainWindow`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetImageListCheck`              Sets the checkbox/radiobutton image list.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetIndent`                      Currently has no effect on ``HyperTreeList``. The indent is auto-calculated.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItem3State`                  Sets whether the item has a 3-state value checkbox assigned to it or not.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItem3StateValue`             Sets the checkbox item to the given `state`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemBackgroundColour`        Sets the item background colour.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemBold`                    Sets the item font as bold/unbold.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemDropHighlight`           Gives the item the visual feedback for drag and drop operations.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemFont`                    Sets the item font.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemHasChildren`             Forces the appearance/disappearance of the button next to the item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemHyperText`               Sets whether the item is hypertext or not.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.SetItemImage`                Sets the item image for a particular item state.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemItalic`                  Sets the item font as italic/non-italic.
    SetItemPyData                                                                    Another name for :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetPyData`
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.SetItemText`                 Sets the item text label.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemTextColour`              Sets the item text colour or separator horizontal line colour.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemType`                    Sets the item type.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetItemVisited`                 Sets whether an hypertext item was visited.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.SetItemWindow`               Sets the window associated to an item.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.SetItemWindowEnabled`        Sets whether the window associated with an item is enabled or not.
    :meth:`~wx.lib.agw.hypertreelist.TreeListMainWindow.SetMainColumn`               Sets the :class:`HyperTreeList` main column (i.e. the column of the tree).
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetPyData`                      Sets the data associated to an item.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetSecondGradientColour`        Sets the second gradient colour for gradient-style selections.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetSpacing`                     Currently has no effect on ``HyperTreeList``.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.SetStateImageList`              Sets the state image list for :class:`TreeListMainWindow`
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.ShouldInheritColours`           Return ``True`` to allow the window colours to be changed by `InheritAttributes`.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.Toggle`                         Toggles the item state (collapsed/expanded).
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.ToggleItemSelection`            Toggles the item selection.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.UnCheckRadioParent`             Used internally to handle radio node parent correctly.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.Unselect`                       Unselects the current selection.
    :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.UnselectAll`                    Unselect all the items.
    ================================================================================ ==================================================================================
    
    
    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, agwStyle=wx.TR_DEFAULT_STYLE, validator=wx.DefaultValidator,
                 name="HyperTreeList"):
        """
        Default class constructor.

        :param `parent`: parent window. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the underlying :class:`wx.Control` style;
        :param `agwStyle`: the AGW-specific :class:`HyperTreeList` window style.
         see :mod:`~wx.lib.agw.hypertreelist` for a full list of flags.
        :param `validator`: window validator;
        :param `name`: window name.
        """

        wx.Control.__init__(self, parent, id, pos, size, style, validator, name)

        self._header_win = None
        self._main_win = None
        self._headerHeight = 0
        self._attr_set = False

        main_style = style & ~(wx.SIMPLE_BORDER | wx.SUNKEN_BORDER |
                               wx.DOUBLE_BORDER | wx.RAISED_BORDER |
                               wx.STATIC_BORDER)

        self._agwStyle = agwStyle

        self._main_win = TreeListMainWindow(self, -1, wx.Point(0, 0), size, main_style, agwStyle, validator)
        self._main_win._buffered = False

        self._header_win = TreeListHeaderWindow(self, -1, self._main_win, wx.Point(0, 0),
                                                wx.DefaultSize, wx.TAB_TRAVERSAL)
        self._header_win._buffered = False

        self.CalculateAndSetHeaderHeight()
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnHTLFocus)

        self.SetBuffered(IsBufferingSupported())
        self._main_win.SetAGWWindowStyleFlag(agwStyle)


    def SetBuffered(self, buffered):
        """
        Sets/unsets the double buffering for the header and the main window.

        :param `buffered`: ``True`` to use double-buffering, ``False`` otherwise.

        :note: Currently we are using double-buffering only on Windows XP.
        """

        self._main_win.SetBuffered(buffered)
        self._header_win.SetBuffered(buffered)


    def Freeze(self):
        """
        Freeze :class:`HyperTreeList` to allow rapid changes to the tree.
        
        Freezes the HyperTreeList main (tree) and and header windows.
        This prevents any re-calculation or updates from taking place
        allowing mass updates to the tree very quickly. :meth:`~Thaw`
        must be called to re-enable updates. Calls to these two
        functions may be nested.
        """
        self._main_win.Freeze()
        self._header_win.Freeze()


    def Thaw(self):
        """
        Thaw :class:`HyperTreeList`.

        Re-enables updates to the main (tree) and header windows after a
        previous call to :meth:`~Freeze`. To really thaw the control, it
        must be called exactly the same number of times as :meth:`~Freeze`.
        When fully thawed the tree will re-calculate and update itself.

        :raise: `Exception` if :meth:`~Thaw` has been called without an un-matching :meth:`~Freeze`.
        """
        self._main_win.Thaw()
        self._header_win.Thaw()

        
    def CalculateAndSetHeaderHeight(self):
        """ Calculates the best header height and stores it. """

        if self._header_win:
            h = wx.RendererNative.Get().GetHeaderButtonHeight(self._header_win)
            # only update if changed
            if h != self._headerHeight:
                self._headerHeight = h
                self.DoHeaderLayout()


    def DoHeaderLayout(self):
        """ Layouts the header control. """

        w, h = self.GetClientSize()
        has_header = self._agwStyle & TR_NO_HEADER == 0

        if self._header_win and has_header:
            self._header_win.SetSize(0, 0, w, self._headerHeight)
            self._header_win.Refresh()
        else:
            self._header_win.SetSize(0, 0, 0, 0)

        if self._main_win and has_header:
            self._main_win.SetSize(0, self._headerHeight + 1, w, h - self._headerHeight - 1)
        else:
            self._main_win.SetSize(0, 0, w, h)


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`HyperTreeList`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        self.DoHeaderLayout()


    def OnHTLFocus(self, event):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for :class:`HyperTreeList`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """
        # Pass focus to TreeListMainWindow so keyboard controls work.
        self.GetMainWindow().SetFocus()


    def SetFont(self, font):
        """
        Sets the default font for the header window and the main window.

        :param `font`: a valid :class:`wx.Font` object.
        """

        if self._header_win:
            self._header_win.SetFont(font)
            self.CalculateAndSetHeaderHeight()
            self._header_win.Refresh()

        if self._main_win:
            return self._main_win.SetFont(font)
        else:
            return False


    def SetHeaderFont(self, font):
        """
        Sets the default font for the header window..

        :param `font`: a valid :class:`wx.Font` object.
        """

        if not self._header_win:
            return

        for column in range(self.GetColumnCount()):
            self._header_win.SetColumn(column, self.GetColumn(column).SetFont(font))

        self._header_win.Refresh()


    def SetHeaderCustomRenderer(self, renderer=None):
        """
        Associate a custom renderer with the header - all columns will use it

        :param `renderer`: a class able to correctly render header buttons

        :note: the renderer class **must** implement the method `DrawHeaderButton`
        """

        self._header_win.SetCustomRenderer(renderer)


    def SetAGWWindowStyleFlag(self, agwStyle):
        """
        Sets the window style for :class:`HyperTreeList`.

        :param `agwStyle`: can be a combination of various bits. See
         :mod:`~wx.lib.agw.hypertreelist` for a full list of flags.

        :note: Please note that some styles cannot be changed after the window creation
         and that `Refresh()` might need to be be called after changing the others for
         the change to take place immediately.
        """

        if self._main_win:
            self._main_win.SetAGWWindowStyleFlag(agwStyle)

        tmp = self._agwStyle
        self._agwStyle = agwStyle
        if abs(agwStyle - tmp) & TR_NO_HEADER:
            self.DoHeaderLayout()


    def GetAGWWindowStyleFlag(self):
        """
        Returns the :class:`HyperTreeList` window style flag.

        :see: :meth:`~HyperTreeList.SetAGWWindowStyleFlag` for a list of valid window styles.
        """

        agwStyle = self._agwStyle
        if self._main_win:
            agwStyle |= self._main_win.GetAGWWindowStyleFlag()

        return agwStyle


    def HasAGWFlag(self, flag):
        """
        Returns whether a flag is present in the :class:`HyperTreeList` style.

        :param `flag`: one of the possible :class:`HyperTreeList` window styles.

        :see: :meth:`~HyperTreeList.SetAGWWindowStyleFlag` for a list of possible window style flags.
        """

        agwStyle = self.GetAGWWindowStyleFlag()
        res = bool(agwStyle & flag)
        return res


    def SetBackgroundColour(self, colour):
        """
        Changes the background colour of :class:`HyperTreeList`.

        :param `colour`: the colour to be used as the background colour, pass
         :class:`NullColour` to reset to the default colour.

        :note: The background colour is usually painted by the default :class:`EraseEvent`
         event handler function under Windows and automatically under GTK.

        :note: Setting the background colour does not cause an immediate refresh, so
         you may wish to call :meth:`wx.Window.ClearBackground` or :meth:`wx.Window.Refresh` after
         calling this function.

        :note: Overridden from :class:`wx.Control`.
        """

        if not self._main_win:
            return False

        return self._main_win.SetBackgroundColour(colour)


    def SetForegroundColour(self, colour):
        """
        Changes the foreground colour of :class:`HyperTreeList`.

        :param `colour`: the colour to be used as the foreground colour, pass
         :class:`NullColour` to reset to the default colour.

        :note: Overridden from :class:`wx.Control`.
        """

        if not self._main_win:
            return False

        return self._main_win.SetForegroundColour(colour)


    def SetColumnWidth(self, column, width):
        """
        Sets the column width, in pixels.

        :param `column`: an integer specifying the column index;
        :param `width`: the new column width, in pixels.
        """

        if width == wx.LIST_AUTOSIZE_USEHEADER:

            font = self._header_win.GetFont()
            dc = wx.ClientDC(self._header_win)
            width, dummy = dc.GetMultiLineTextExtent(self._header_win.GetColumnText(column))
            # Search TreeListHeaderWindow.OnPaint to understand this:
            width += 2 * _EXTRA_WIDTH + _MARGIN

        elif width == wx.LIST_AUTOSIZE:

            width = self._main_win.GetBestColumnWidth(column)

        elif width == LIST_AUTOSIZE_CONTENT_OR_HEADER:

            width1 = self._main_win.GetBestColumnWidth(column)
            font = self._header_win.GetFont()
            dc = wx.ClientDC(self._header_win)
            width2, dummy = dc.GetMultiLineTextExtent(self._header_win.GetColumnText(column))

            width2 += 2 * _EXTRA_WIDTH + _MARGIN
            width = max(width1, width2)


        self._header_win.SetColumnWidth(column, width)
        self._header_win.Refresh()


    def GetColumnWidth(self, column):
        """
        Returns the column width, in pixels.

        :param `column`: an integer specifying the column index.
        """

        return self._header_win.GetColumnWidth(column)


    def SetColumnText(self, column, text):
        """
        Sets the column text label.

        :param `column`: an integer specifying the column index;
        :param `text`: the new column label.
        """

        self._header_win.SetColumnText(column, text)
        self._header_win.Refresh()


    def GetColumnText(self, column):
        """
        Returns the column text label.

        :param `column`: an integer specifying the column index.
        """

        return self._header_win.GetColumnText(column)


    def AddColumn(self, text, width=_DEFAULT_COL_WIDTH, flag=wx.ALIGN_LEFT,
                  image=-1, shown=True, colour=None, edit=False):
        """
        Appends a column to the :class:`HyperTreeList`.

        :param `text`: the column text label;
        :param `width`: the column width in pixels;
        :param `flag`: the column alignment flag, one of ``wx.ALIGN_LEFT``,
         ``wx.ALIGN_RIGHT``, ``wx.ALIGN_CENTER``;
        :param `image`: an index within the normal image list assigned to
         :class:`HyperTreeList` specifying the image to use for the column;
        :param `shown`: ``True`` to show the column, ``False`` to hide it;
        :param `colour`: a valid :class:`wx.Colour`, representing the text foreground colour
         for the column;
        :param `edit`: ``True`` to set the column as editable, ``False`` otherwise.
        """

        self._header_win.AddColumn(text, width, flag, image, shown, colour, edit)
        self.DoHeaderLayout()


    def AddColumnInfo(self, colInfo):
        """
        Appends a column to the :class:`HyperTreeList`.

        :param `colInfo`: an instance of :class:`TreeListColumnInfo`.
        """

        self._header_win.AddColumnInfo(colInfo)
        self.DoHeaderLayout()


    def InsertColumnInfo(self, before, colInfo):
        """
        Inserts a column to the :class:`HyperTreeList` at the position specified
        by `before`.

        :param `before`: the index at which we wish to insert the new column;
        :param `colInfo`: an instance of :class:`TreeListColumnInfo`.
        """

        self._header_win.InsertColumnInfo(before, colInfo)
        self._header_win.Refresh()


    def InsertColumn(self, before, text, width=_DEFAULT_COL_WIDTH,
                     flag=wx.ALIGN_LEFT, image=-1, shown=True, colour=None,
                     edit=False):
        """
        Inserts a column to the :class:`HyperTreeList` at the position specified
        by `before`.

        :param `before`: the index at which we wish to insert the new column;
        :param `text`: the column text label;
        :param `width`: the column width in pixels;
        :param `flag`: the column alignment flag, one of ``wx.ALIGN_LEFT``,
         ``wx.ALIGN_RIGHT``, ``wx.ALIGN_CENTER``;
        :param `image`: an index within the normal image list assigned to
         :class:`HyperTreeList` specifying the image to use for the column;
        :param `shown`: ``True`` to show the column, ``False`` to hide it;
        :param `colour`: a valid :class:`wx.Colour`, representing the text foreground colour
         for the column;
        :param `edit`: ``True`` to set the column as editable, ``False`` otherwise.
        """

        self._header_win.InsertColumn(before, text, width, flag, image,
                                      shown, colour, edit)
        self._header_win.Refresh()


    def RemoveColumn(self, column):
        """
        Removes a column from the :class:`HyperTreeList`.

        :param `column`: an integer specifying the column index.
        """

        self._header_win.RemoveColumn(column)
        self._header_win.Refresh()


    def SetColumn(self, column, colInfo):
        """
        Sets a column using an instance of :class:`TreeListColumnInfo`.

        :param `column`: an integer specifying the column index;
        :param `info`: an instance of :class:`TreeListColumnInfo`.
        """

        self._header_win.SetColumn(column, colInfo)
        self._header_win.Refresh()


    def GetColumn(self, column):
        """
        Returns an instance of :class:`TreeListColumnInfo` containing column information.

        :param `column`: an integer specifying the column index.
        """

        return self._header_win.GetColumn(column)


    def SetColumnImage(self, column, image):
        """
        Sets an image on the specified column.

        :param `column`: an integer specifying the column index.
        :param `image`: an index within the normal image list assigned to
         :class:`HyperTreeList` specifying the image to use for the column.
        """

        self._header_win.SetColumn(column, self.GetColumn(column).SetImage(image))
        self._header_win.Refresh()


    def GetColumnImage(self, column):
        """
        Returns the image assigned to the specified column.

        :param `column`: an integer specifying the column index.
        """

        return self._header_win.GetColumn(column).GetImage()


    def SetColumnEditable(self, column, edit):
        """
        Sets the column as editable or non-editable.

        :param `column`: an integer specifying the column index;
        :param `edit`: ``True`` if the column should be editable, ``False`` otherwise.
        """

        self._header_win.SetColumn(column, self.GetColumn(column).SetEditable(edit))


    def SetColumnShown(self, column, shown):
        """
        Sets the column as shown or hidden.

        :param `column`: an integer specifying the column index;
        :param `shown`: ``True`` if the column should be shown, ``False`` if it
         should be hidden.
        """

        if self._main_win.GetMainColumn() == column:
            shown = True    # Main column cannot be hidden

        self.SetColumn(column, self.GetColumn(column).SetShown(shown))


    def IsColumnEditable(self, column):
        """
        Returns ``True`` if the column is editable, ``False`` otherwise.

        :param `column`: an integer specifying the column index.
        """

        return self._header_win.GetColumn(column).IsEditable()


    def IsColumnShown(self, column):
        """
        Returns ``True`` if the column is shown, ``False`` otherwise.

        :param `column`: an integer specifying the column index.
        """

        return self._header_win.GetColumn(column).IsShown()


    def SetColumnAlignment(self, column, flag):
        """
        Sets the column text alignment.

        :param `column`: an integer specifying the column index;
        :param `flag`: the alignment flag, one of ``wx.ALIGN_LEFT``, ``wx.ALIGN_RIGHT``,
         ``wx.ALIGN_CENTER``.
        """

        self._header_win.SetColumn(column, self.GetColumn(column).SetAlignment(flag))
        self._header_win.Refresh()


    def GetColumnAlignment(self, column):
        """
        Returns the column text alignment.

        :param `column`: an integer specifying the column index.
        """

        return self._header_win.GetColumn(column).GetAlignment()


    def SetColumnColour(self, column, colour):
        """
        Sets the column text colour.

        :param `column`: an integer specifying the column index;
        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._header_win.SetColumn(column, self.GetColumn(column).SetColour(colour))
        self._header_win.Refresh()


    def GetColumnColour(self, column):
        """
        Returns the column text colour.

        :param `column`: an integer specifying the column index.
        """

        return self._header_win.GetColumn(column).GetColour()


    def SetColumnFont(self, column, font):
        """
        Sets the column text font.

        :param `column`: an integer specifying the column index;
        :param `font`: a valid :class:`wx.Font` object.
        """

        self._header_win.SetColumn(column, self.GetColumn(column).SetFont(font))
        self._header_win.Refresh()


    def GetColumnFont(self, column):
        """
        Returns the column text font.

        :param `column`: an integer specifying the column index.
        """

        return self._header_win.GetColumn(column).GetFont()


    def SetColumnSortIcon(self, column, sortIcon, colour=None):
        """
        Sets the sort icon to be displayed in the column header.

        The sort icon will be displayed in the specified column number
        and all other columns will have the sort icon cleared.

        :param `column`: an integer specifying the column index;
        :param `sortIcon`: the sort icon to display, one of ``wx.HDR_SORT_ICON_NONE``,
         ``wx.HDR_SORT_ICON_UP``, ``wx.HDR_SORT_ICON_DOWN``.
        :param `colour`: the colour of the sort icon as a wx.Colour. Optional.
         Set to ``None`` to restore native colour.
        """
        return self._header_win.SetSortIcon(column, sortIcon, colour)


    def Refresh(self, erase=True, rect=None):
        """
        Causes this window, and all of its children recursively (except under wxGTK1
        where this is not implemented), to be repainted.

        :param `erase`: If ``True``, the background will be erased;
        :param `rect`: If not ``None``, only the given rectangle will be treated as damaged.

        :note: Note that repainting doesn't happen immediately but only during the next
         event loop iteration, if you need to update the window immediately you should
         use `Update` instead.

        :note: Overridden from :class:`wx.Control`.
        """

        self._main_win.Refresh(erase, rect)
        self._header_win.Refresh(erase, rect)


    def SetFocus(self):
        """ This sets the window to receive keyboard input. """

        self._main_win.SetFocus()


    def GetHeaderWindow(self):
        """ Returns the header window, an instance of :class:`TreeListHeaderWindow`. """

        return self._header_win


    def GetMainWindow(self):
        """ Returns the main window, an instance of :class:`TreeListMainWindow`. """

        return self._main_win


    def DoGetBestSize(self):
        """
        Gets the size which best suits the window: for a control, it would be the
        minimal size which doesn't truncate the control, for a panel - the same size
        as it would have after a call to `Fit()`.

        :note: Overridden from :class:`wx.Control`.
        """

        # something is better than nothing...
        return wx.Size(200, 200)    # but it should be specified values! FIXME


    def OnGetItemText(self, item, column):
        """
        If the ``TR_VIRTUAL`` style is set this function **must** be overloaded
        in the derived class. It should return the string containing the text
        of the given column for the specified item.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: an integer specifying the column index.
        """

        return ""


    def SortChildren(self, item):
        """
        Sorts the children of the given item using :meth:`~HyperTreeList.OnCompareItems` method of :class:`HyperTreeList`.
        You should override that method to change the sort order (the default is ascending
        case-sensitive alphabetical order).

        :param `item`: an instance of :class:`TreeListItem`;
        """

        if not self._attr_set:
            setattr(self._main_win, "OnCompareItems", self.OnCompareItems)
            self._attr_set = True

        self._main_win.SortChildren(item)


    def OnCompareItems(self, item1, item2):
        """
        Returns the comparison of two items. Used for sorting.

        Override this function in the derived class to change the sort order of the items
        in the :class:`HyperTreeList`. The function should return a negative, zero or positive
        value if the first item is less than, equal to or greater than the second one.

        :param `item1`: an instance of :class:`TreeListItem`;
        :param `item2`: another instance of :class:`TreeListItem`.

        :note: The base class version compares items alphabetically.
        """

        # do the comparison here, and not delegate to self._main_win, in order
        # to let the user override it

        return self.GetItemText(item1) == self.GetItemText(item2)


    def CreateEditCtrl(self, item, column):
        """
        Create an edit control for editing a label of an item. By default, this
        returns a text control.

        Override this function in the derived class to return a different type
        of control.

        :param `item`: an instance of :class:`TreeListItem`;
        :param `column`: an integer specifying the column index.
        """

        return EditTextCtrl(self.GetMainWindow(), -1, item, column,
                            self.GetMainWindow(), item.GetText(column),
                            style=self.GetTextCtrlStyle(column))


    def GetTextCtrlStyle(self, column):
        """
        Return the style to use for the text control that is used to edit
        labels of items.

        Override this function in the derived class to support a different
        style, e.g. ``wx.TE_MULTILINE``.

        :param `column`: an integer specifying the column index.
        """

        return self.GetTextCtrlAlignmentStyle(column) | wx.TE_PROCESS_ENTER


    def GetTextCtrlAlignmentStyle(self, column):
        """
        Return the alignment style to use for the text control that is used
        to edit labels of items. The alignment style is derived from the
        column alignment.

        :param `column`: an integer specifying the column index.
        """

        header_win = self.GetHeaderWindow()
        alignment = header_win.GetColumnAlignment(column)
        return {wx.ALIGN_LEFT: wx.TE_LEFT,
                wx.ALIGN_RIGHT: wx.TE_RIGHT,
                wx.ALIGN_CENTER: wx.TE_CENTER}[alignment]


    def GetClassDefaultAttributes(self):
        """
        Returns the default font and colours which are used by the control. This is
        useful if you want to use the same font or colour in your own control as in
        a standard control -- which is a much better idea than hard coding specific
        colours or fonts which might look completely out of place on the users system,
        especially if it uses themes.

        This static method is "overridden'' in many derived classes and so calling,
        for example, :meth:`Button.GetClassDefaultAttributes` () will typically return the
        values appropriate for a button which will be normally different from those
        returned by, say, :meth:`ListCtrl.GetClassDefaultAttributes` ().

        :note: The :class:`VisualAttributes` structure has at least the fields `font`,
         `colFg` and `colBg`. All of them may be invalid if it was not possible to
         determine the default control appearance or, especially for the background
         colour, if the field doesn't make sense as is the case for `colBg` for the
         controls with themed background.
        """

        attr = wx.VisualAttributes()
        attr.colFg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        attr.colBg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
        attr.font  = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        return attr

    GetClassDefaultAttributes = classmethod(GetClassDefaultAttributes)


def create_delegator_for(method):
    """
    Creates a method that forwards calls to `self._main_win` (an instance of :class:`TreeListMainWindow`).

    :param `method`: one method inside the :class:`TreeListMainWindow` local scope.
    """

    def delegate(self, *args, **kwargs):
        return getattr(self._main_win, method)(*args, **kwargs)
    return delegate

# Create methods that delegate to self._main_win. This approach allows for
# overriding these methods in possible subclasses of HyperTreeList
for method in _methods:
    setattr(HyperTreeList, method, create_delegator_for(method))


if __name__ == '__main__':

    import wx
    import wx.lib.agw.hypertreelist as HTL

    class MyFrame(wx.Frame):
        COLUMNS = (("Main Tree", 320, wx.ALIGN_LEFT),
                   ("Column 1", 320, wx.ALIGN_LEFT),
                   ("Column 2", 100, wx.ALIGN_CENTER),
                   ("Column 3", 100, wx.ALIGN_RIGHT))
        NUMBERS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six',
                   'seven', 'eight', 'nine']

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, size=(800, 600),
                              title="HyperTreeList Demo")
            self.spin_parent = None
            self.spin_count = 0
            self.hidden = False

            panel = wx.Panel(self)
            sizer = wx.BoxSizer(orient=wx.VERTICAL)

            # Create a HyperTreeList instance in our panel.
            self.tree = HTL.HyperTreeList(panel, agwStyle=wx.TR_DEFAULT_STYLE |
                                          HTL.TR_HAS_VARIABLE_ROW_HEIGHT |
                                          TR_COLUMN_LINES |
#                                          TR_LIVE_UPDATE |
                                          wx.TR_MULTIPLE |
                                          0)
            # Create columns
            for title, width, alignment in self.COLUMNS:
                self.tree.AddColumn(text=title, width=width, flag=alignment)
            self.tree.SetMainColumn(0)
            #self.tree.SetBuffered(True)
            
            # Create an image list to add icons next to an item
            size, client = (16, 16), wx.ART_OTHER
            il = wx.ImageList(*size)
            imgFolder = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NEW_DIR, client, size))
            imgOpen = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, client, size))
            imgFile = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, client, size))
            imgExe = il.Add(wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, client, size))
            il.Add(wx.ArtProvider.GetBitmap(wx.ART_COPY, client, size))
            il.Add(wx.ArtProvider.GetBitmap(wx.ART_CUT, client, size))
            il.Add(wx.ArtProvider.GetBitmap(wx.ART_PASTE, client, size))
            il.Add(wx.ArtProvider.GetBitmap(wx.ART_UNDO, client, size))
            self.tree.SetImageList(il)

            # Create root node.
            root = self.tree.AddRoot("Root", image=imgFolder, selImage=imgOpen)
            self.tree.SetItemBold(root)

            # Freeze tree then populate items.
            self.tree.Freeze()
            start = time.time()
            count = 0
            for x in range(5):
                child = self.tree.AppendItem(root, "Item %d" % x)
                self.tree.SetItemText(child, self.NUMBERS[x], column=1)
                self.tree.SetItemImage(child, imgFolder, which=wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(child, imgOpen, which=wx.TreeItemIcon_Expanded)
                self.tree.SetItemImage(child, imgFile, which=wx.TreeItemIcon_Selected)
                self.tree.SetItemImage(child, imgExe, which=wx.TreeItemIcon_SelectedExpanded)
                if x == 1:
                    self.spin_parent = child
                for y in range(5000):
                    last = self.tree.AppendItem(child, "item %d-%d" % (x, y))
                    self.tree.SetItemText(last, "Column 1", column=1)
                    self.tree.SetItemText(last, "0x%04x" % y, column=2)
                    self.tree.SetItemText(last, format(y, ','), column=3)
                    self.tree.SetItemImage(last, imgFolder, which=wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(last, imgOpen, which=wx.TreeItemIcon_Expanded)
                    if x < 2 and y == 0:
                        button = wx.Button(self.tree, label="Show Windows")
                        self.tree.SetItemWindow(last, button)
                        button.Bind(wx.EVT_BUTTON, lambda evt, item=child:
                                    self.OnShowButton(evt, item))
                    for z in range(5):
                        item = self.tree.AppendItem(last, "Subordinate-item %d-%d-%s" %
                                                    (x, y, chr(ord("a") + z)), 1)
                        self.tree.SetItemImage(item, imgFolder, which=wx.TreeItemIcon_Normal)
                        count += 1
                    count += 1
                count += 1
            for x in range(2):
                name = "Disable" if x == 1 else "Hide"
                child = self.tree.AppendItem(root, "Parent %s %d" % (name, x))
                self.tree.SetItemText(child, self.NUMBERS[x + 5], column=1)
                self.tree.SetItemImage(child, imgFolder, which=wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(child, imgOpen, which=wx.TreeItemIcon_Expanded)
                for y in range(10000):
                    last = self.tree.AppendItem(child, "%s item %d-%d" % (name, x, y))
                    self.tree.SetItemImage(last, imgFolder, which=wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(last, imgOpen, which=wx.TreeItemIcon_Expanded)
                    if y > 4 and x == 1:
                        self.tree.EnableItem(last, True if y & 0x20 else False)
                    elif y > 4 and x != 1:
                        self.tree.HideItem(last)
                    count += 1
                count += 1
            elapsed = abs(time.time() - start) * 1000
            print("Tree populate %s items took %.3fms" % (count, elapsed))
            start = time.time()
            self.tree.Thaw()
            elapsed = abs(time.time() - start) * 1000
            print("Thaw took %.3fms" % elapsed)
            start = time.time()
            self.tree.Expand(root)
            elapsed = abs(time.time() - start) * 1000
            print("Expand root took %.3fms" % elapsed)

            sizer.Add(self.tree, proportion=1, flag=wx.EXPAND)

            # Create tree test button row.
            row = wx.BoxSizer(orient=wx.HORIZONTAL)
            spin_button = wx.ToggleButton(panel, label="Spin")
            spin_button.Bind(wx.EVT_TOGGLEBUTTON, self.OnSpinButton)
            row.Add(spin_button, flag=wx.RIGHT, border=20)
            unhide_button = wx.Button(panel, label="Unhide")
            unhide_button.Bind(wx.EVT_BUTTON, self.OnUnhide)
            row.Add(unhide_button, flag=wx.RIGHT, border=20)
            getsel_button = wx.Button(panel, label="GetSelections")
            getsel_button.Bind(wx.EVT_BUTTON, self.OnGetSelections)
            row.Add(getsel_button, flag=wx.RIGHT, border=20)
            sizer.Add(row, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

            panel.SetSizer(sizer)
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.OnTimer, source=self.timer)
            self.Bind(wx.EVT_CLOSE, self.OnClose)

        def OnSpinButton(self, event):
            if self.timer.IsRunning():
                self.timer.Stop()
            if event.GetEventObject().GetValue():
                self.timer.Start(milliseconds=300)
            
        def OnShowButton(self, event, parent):
            # Add windows to first 100 items in this branch.
            self.tree.Freeze()
            self.Freeze()
            size, client = (16, 16), wx.ART_OTHER
            bitmap = wx.ArtProvider.GetBitmap(wx.ART_COPY, client, size)
            hypertree = self.tree.GetMainWindow()
            count = len(hypertree._itemWithWindow)
            start = time.time()
            for index, child in enumerate(parent.GetChildren()):
                if not self.tree.GetItemWindow(child, column=3):
                    widget = wx.StaticBitmap(hypertree, bitmap=bitmap)
                    self.tree.SetItemWindow(child, widget, column=3)
                if index > 100:
                    break
            self.Thaw()
            self.tree.Thaw()
            elapsed = abs(time.time() - start) * 1000
            print("Added %d windows in %.3fms" % (len(hypertree._itemWithWindow) - count, elapsed))

        def OnHideButton(self, event):
            start = time.time()
            windows = self.tree.GetMainWindow()._itemWithWindow
            for item in windows:
                for wnd in item.GetWindows():
                    wnd.Hide()
            elapsed = abs(time.time() - start) * 1000
            print("Hid %d windows in %.3fms" % (len(windows), elapsed))

        def OnGetSelections(self, event):
            start = time.time()
            selections = self.tree.GetSelections()
            elapsed = abs(time.time() - start) * 1000
            print("Got %d selections in %.3fms" % (len(selections), elapsed))
            
        def OnUnhide(self, event):
            # Recursively hide/unhide items with "Hidden" in their text.
            start = time.time()
            self.item_count = 0
            self.DoHideUnhide(self.tree.GetRootItem(), self.hidden)
            elapsed = abs(time.time() - start) * 1000
            print("Changed hide state in %.3fms (%d items scanned)" %
                  (elapsed, self.item_count))
            self.hidden = not self.hidden
            event.GetEventObject().SetLabel("Hide" if self.hidden else "Unhide")

        def DoHideUnhide(self, item, hide):
            self.item_count += 1
            text = item.GetText()
            if len(text) > 13 and text.startswith('Hide'):
                self.tree.HideItem(item, hide)
            for child in item.GetChildren():
                self.DoHideUnhide(child, hide)

        def OnTimer(self, event):
            self.spin_count = (self.spin_count + 1) % 8
            if self.spin_parent:
                start = time.time()
                self.tree.Freeze()
                children = self.spin_parent.GetChildren()
                for child in children:
                    self.tree.SetItemImage(child, self.spin_count, which=0)
                self.tree.Thaw()
                elapsed = abs(time.time() - start) * 1000
                print("Spun %d items in %.3fms" % (len(children), elapsed))

        def OnClose(self, event):
            if self.timer.IsRunning() is True:
                self.timer.Stop()
            event.Skip()

    # our normal wxApp-derived class, as usual
    app = wx.App(False)
    locale = wx.Locale(wx.LANGUAGE_DEFAULT)
    frame = MyFrame(None)
    frame.Show()

    app.MainLoop()
