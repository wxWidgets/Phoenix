
#
#  **** THIS IS STILL A WIP ****
#

#----------------------------------------------------------------------
# Name:        wx.lib.gizmos.treelistctrl
# Purpose:     A simple derivation from wx.lib.agw.hypertreelist.HyperTreeListCtrl
#              to provide a class that is mostly compatible with the
#              TreeListCtrl class from the old gizmos module and the
#              wxCode library.
#
# Author:      Robin Dunn
#
# Created:     16-Nov-2017
# Copyright:   (c) 2018 by Total Control Software
# Licence:     wxWindows license
# Tags:
#----------------------------------------------------------------------
"""
A generic widget that combines the multicolumn features of a :class:`wx.ListCtrl`
with the hierarchical features of a :class:`wx.TreeCtrl`.

This implementation is based on :class:`~wx.lib.agw.hypertreelist.HyperTreeList`
"""

import wx
import wx.lib.agw.hypertreelist as HTL


#--------------------------------------------------------------------------
# Styles and flags
#
# Most of these are the same as what's in the wx module, but a few are
# specific to HyperTreeList so replicate them all here so they are easier to
# find and use.

TREE_HITTEST_ONITEMCOLUMN = HTL.TREE_HITTEST_ONITEMCOLUMN
TREE_HITTEST_ONITEMCHECKICON = HTL.TREE_HITTEST_ONITEMCHECKICON

TR_DEFAULT_STYLE = HTL.TR_DEFAULT_STYLE
TR_NO_BUTTONS = HTL.TR_NO_BUTTONS
TR_HAS_BUTTONS = HTL.TR_HAS_BUTTONS
TR_NO_LINES = HTL.TR_NO_LINES
TR_LINES_AT_ROOT = HTL.TR_LINES_AT_ROOT
TR_TWIST_BUTTONS = HTL.TR_TWIST_BUTTONS
TR_SINGLE = HTL.TR_SINGLE
TR_MULTIPLE = HTL.TR_MULTIPLE
TR_EXTENDED = HTL.TR_EXTENDED
TR_HAS_VARIABLE_ROW_HEIGHT = HTL.TR_HAS_VARIABLE_ROW_HEIGHT
TR_EDIT_LABELS = HTL.TR_EDIT_LABELS
TR_COLUMN_LINES = HTL.TR_COLUMN_LINES
TR_ROW_LINES = HTL.TR_ROW_LINES
TR_HIDE_ROOT = HTL.TR_HIDE_ROOT
TR_FULL_ROW_HIGHLIGHT = HTL.TR_FULL_ROW_HIGHLIGHT
TR_AUTO_CHECK_CHILD = HTL.TR_AUTO_CHECK_CHILD
TR_AUTO_TOGGLE_CHILD = HTL.TR_AUTO_TOGGLE_CHILD
TR_AUTO_CHECK_PARENT = HTL.TR_AUTO_CHECK_PARENT
TR_ALIGN_WINDOWS = HTL.TR_ALIGN_WINDOWS
TR_ELLIPSIZE_LONG_ITEMS = HTL.TR_ELLIPSIZE_LONG_ITEMS
TR_VIRTUAL = HTL.TR_VIRTUAL
TR_NO_HEADER = HTL.TR_NO_HEADER
LIST_AUTOSIZE_CONTENT_OR_HEADER = HTL.LIST_AUTOSIZE_CONTENT_OR_HEADER



#--------------------------------------------------------------------------

class TreeListCtrl(HTL.HyperTreeList):
    """
    See documentation for :class:`~wx.lib.agw.hypertreelist.HyperTreeList` and
    :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl`. This class is just a
    simple derivation of the former in order to provide a mostly compatible
    class to replace the C++ TreeListCtrl class in Classic, and most
    CustomTreeCtrl methods are available here as well via monkey-patched
    delegates.
    """
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, agwStyle=wx.TR_DEFAULT_STYLE,
                 validator=wx.DefaultValidator, name="treelistctrl"):
        super(TreeListCtrl, self).__init__(parent, id, pos, size, style,
                                           agwStyle, validator, name)



#-------------------------------------------------------------------------
