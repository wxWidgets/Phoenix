import unittest
import sys
from unittests import wtc
import wx

import wx.lib.agw.customtreectrl as CT

#---------------------------------------------------------------------------

class lib_agw_customtreectrl_Tests(wtc.WidgetTestCase):

    def test_lib_agw_customtreectrlCtor(self):
        tree = CT.CustomTreeCtrl(self.frame)
        self.assertEqual(tree.GetAGWWindowStyleFlag(), CT.TR_DEFAULT_STYLE)
        self.assertEqual(tree.GetCount(), 0)
        self.assertEqual(tree.GetRootItem(), None)

    def test_lib_agw_customtreectrlTreeItem(self):
        tree = CT.CustomTreeCtrl(self.frame)
        root = tree.AddRoot('root item')
        self.assertTrue(isinstance(root, CT.GenericTreeItem))
        self.assertTrue(root.IsOk())

        r = tree.GetRootItem()
        self.assertTrue(r is root)
        self.assertTrue(r == root)

        child = tree.AppendItem(root, 'child item')
        self.assertTrue(child is not root)
        self.assertTrue(child != root)

    def test_lib_agw_customtreectrlTreeItemData(self):
        value = 'Some Python Object'
        tree = CT.CustomTreeCtrl(self.frame)
        root = tree.AddRoot('root item', data=value)
        v = tree.GetItemData(root)
        self.assertTrue(v == value)
        tree.SetItemData(root, None)
        self.assertTrue(tree.GetItemData(root) is None)

    def test_lib_agw_customtreectrlTreeItemPyData(self):
        # ensure that the "Py" versions works as the normal one
        value = 'Some Python Object'
        tree = CT.CustomTreeCtrl(self.frame)
        root = tree.AddRoot('root item')
        tree.SetItemPyData(root, value)

        v = tree.GetItemPyData(root)
        self.assertTrue(v == value)
        tree.SetItemPyData(root, None)
        self.assertTrue(tree.GetItemPyData(root) is None)

    def test_lib_agw_customtreectrlGetSelections(self):
        tree = CT.CustomTreeCtrl(self.frame, agwStyle=CT.TR_MULTIPLE)
        root = tree.AddRoot('root item')
        c1 = tree.AppendItem(root, 'c1')
        c2 = tree.AppendItem(root, 'c2')
        tree.SelectItem(c1)
        tree.SelectItem(c2)
        self.assertTrue(tree.IsSelected(c1))
        self.assertTrue(tree.IsSelected(c2))

        sel = tree.GetSelections()
        self.assertTrue(isinstance(sel, list))
        self.assertTrue(len(sel) == 2)
        self.assertTrue(isinstance(sel[0], CT.GenericTreeItem))

    def test_lib_agw_customtreectrlItemCheck(self):

        tree = CT.CustomTreeCtrl(self.frame)
        root = tree.AddRoot('root item')

        # Checkboxes, there can be more than one checked at the same level
        c1 = tree.AppendItem(root, 'c1', ct_type=1)
        c2 = tree.AppendItem(root, 'c2', ct_type=1)

        tree.CheckItem(c1)
        tree.CheckItem(c2)

        self.assertTrue(tree.IsItemChecked(c1))
        self.assertTrue(tree.IsItemChecked(c2))

        # RadioButtons, there can NOT be more than one checked at the same level
        c1 = tree.AppendItem(root, 'c1', ct_type=2)
        c2 = tree.AppendItem(root, 'c2', ct_type=2)

        tree.CheckItem(c1)
        tree.CheckItem(c2)

        self.assertTrue(not tree.IsItemChecked(c1))
        self.assertTrue(tree.IsItemChecked(c2))

    def test_lib_agw_customtreectrlSetWindow(self):
        tree = CT.CustomTreeCtrl(self.frame, agwStyle=CT.TR_DEFAULT_STYLE|CT.TR_HAS_VARIABLE_ROW_HEIGHT)
        root = tree.AddRoot('root item')
        c1 = tree.AppendItem(root, 'c1')
        c2 = tree.AppendItem(root, 'c2')

        window = wx.TextCtrl(tree, -1, 'Hello World')
        tree.SetItemWindow(c2, window)

        other = tree.GetItemWindow(c2)
        self.assertTrue(window == other)

        tree.DeleteAllItems()
        self.assertTrue(tree.GetCount() == 0)
        if sys.platform == 'darwin':
            # On Mac the scrollbars and the gripper between them on
            # ScrolledWindows are also wx widgets, so they are in the
            # children list.
            self.assertEqual(len(tree.GetChildren()), 3)
        else:
            self.assertEqual(len(tree.GetChildren()), 0)

    def test_lib_agw_customtreectrlConstantsExist(self):
        CT.TR_NO_BUTTONS
        CT.TR_SINGLE
        CT.TR_HAS_BUTTONS
        CT.TR_NO_LINES
        CT.TR_LINES_AT_ROOT
        CT.TR_DEFAULT_STYLE
        CT.TR_TWIST_BUTTONS
        CT.TR_MULTIPLE
        CT.TR_EXTENDED
        CT.TR_HAS_VARIABLE_ROW_HEIGHT
        CT.TR_EDIT_LABELS
        CT.TR_ROW_LINES
        CT.TR_HIDE_ROOT
        CT.TR_FULL_ROW_HIGHLIGHT
        CT.TR_AUTO_CHECK_CHILD
        CT.TR_AUTO_TOGGLE_CHILD
        CT.TR_AUTO_CHECK_PARENT
        CT.TR_ALIGN_WINDOWS
        CT.TR_ALIGN_WINDOWS_RIGHT
        CT.TR_ELLIPSIZE_LONG_ITEMS
        CT.TR_TOOLTIP_ON_LONG_ITEMS

        CT.TreeItemIcon_Normal
        CT.TreeItemIcon_Selected
        CT.TreeItemIcon_Expanded
        CT.TreeItemIcon_SelectedExpanded

        CT.TreeItemIcon_Checked
        CT.TreeItemIcon_NotChecked
        CT.TreeItemIcon_Undetermined
        CT.TreeItemIcon_Flagged
        CT.TreeItemIcon_NotFlagged

        CT.TREE_HITTEST_ABOVE
        CT.TREE_HITTEST_BELOW
        CT.TREE_HITTEST_NOWHERE
        CT.TREE_HITTEST_ONITEMBUTTON
        CT.TREE_HITTEST_ONITEMICON
        CT.TREE_HITTEST_ONITEMINDENT
        CT.TREE_HITTEST_ONITEMLABEL
        CT.TREE_HITTEST_ONITEM
        CT.TREE_HITTEST_ONITEMRIGHT
        CT.TREE_HITTEST_TOLEFT
        CT.TREE_HITTEST_TORIGHT
        CT.TREE_HITTEST_ONITEMUPPERPART
        CT.TREE_HITTEST_ONITEMLOWERPART
        CT.TREE_HITTEST_ONITEMCHECKICON
        CT.TREE_HITTEST_ONITEM

    def test_lib_agw_customtreectrlEventsExist(self):
        CT.wxEVT_TREE_BEGIN_DRAG
        CT.wxEVT_TREE_BEGIN_RDRAG
        CT.wxEVT_TREE_BEGIN_LABEL_EDIT
        CT.wxEVT_TREE_END_LABEL_EDIT
        CT.wxEVT_TREE_DELETE_ITEM
        CT.wxEVT_TREE_GET_INFO
        CT.wxEVT_TREE_SET_INFO
        CT.wxEVT_TREE_ITEM_EXPANDED
        CT.wxEVT_TREE_ITEM_EXPANDING
        CT.wxEVT_TREE_ITEM_COLLAPSED
        CT.wxEVT_TREE_ITEM_COLLAPSING
        CT.wxEVT_TREE_SEL_CHANGED
        CT.wxEVT_TREE_SEL_CHANGING
        CT.wxEVT_TREE_KEY_DOWN
        CT.wxEVT_TREE_ITEM_ACTIVATED
        CT.wxEVT_TREE_ITEM_RIGHT_CLICK
        CT.wxEVT_TREE_ITEM_MIDDLE_CLICK
        CT.wxEVT_TREE_END_DRAG
        CT.wxEVT_TREE_STATE_IMAGE_CLICK
        CT.wxEVT_TREE_ITEM_GETTOOLTIP
        CT.wxEVT_TREE_ITEM_MENU
        CT.wxEVT_TREE_ITEM_CHECKING
        CT.wxEVT_TREE_ITEM_CHECKED
        CT.wxEVT_TREE_ITEM_HYPERLINK

        CT.EVT_TREE_BEGIN_DRAG
        CT.EVT_TREE_BEGIN_LABEL_EDIT
        CT.EVT_TREE_BEGIN_RDRAG
        CT.EVT_TREE_DELETE_ITEM
        CT.EVT_TREE_END_DRAG
        CT.EVT_TREE_END_LABEL_EDIT
        CT.EVT_TREE_GET_INFO
        CT.EVT_TREE_ITEM_ACTIVATED
        CT.EVT_TREE_ITEM_CHECKED
        CT.EVT_TREE_ITEM_CHECKING
        CT.EVT_TREE_ITEM_COLLAPSED
        CT.EVT_TREE_ITEM_COLLAPSING
        CT.EVT_TREE_ITEM_EXPANDED
        CT.EVT_TREE_ITEM_EXPANDING
        CT.EVT_TREE_ITEM_GETTOOLTIP
        CT.EVT_TREE_ITEM_HYPERLINK
        CT.EVT_TREE_ITEM_MENU
        CT.EVT_TREE_ITEM_MIDDLE_CLICK
        CT.EVT_TREE_ITEM_RIGHT_CLICK
        CT.EVT_TREE_KEY_DOWN
        CT.EVT_TREE_SEL_CHANGED
        CT.EVT_TREE_SEL_CHANGING
        CT.EVT_TREE_SET_INFO
        CT.EVT_TREE_STATE_IMAGE_CLICK

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
