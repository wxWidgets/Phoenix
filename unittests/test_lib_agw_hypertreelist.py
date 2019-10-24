import unittest
from unittests import wtc
import wx

import wx.lib.agw.hypertreelist as HTL
import wx.lib.agw.customtreectrl as CT

#---------------------------------------------------------------------------

class lib_agw_hypertreelist_Tests(wtc.WidgetTestCase):

    def test_lib_agw_hypertreelistCtor(self):
        tree = HTL.HyperTreeList(self.frame)
        self.assertEqual(tree.GetAGWWindowStyleFlag(), CT.TR_DEFAULT_STYLE)
        self.assertEqual(tree.GetRootItem(), None)

    def test_lib_agw_hypertreelistTreeItem(self):
        tree = HTL.HyperTreeList(self.frame)
        tree.AddColumn("First column")

        root = tree.AddRoot('root item')
        self.assertTrue(isinstance(root, CT.GenericTreeItem))
        self.assertTrue(root.IsOk())

        r = tree.GetRootItem()
        self.assertTrue(r is root)
        self.assertTrue(r == root)

        child = tree.AppendItem(root, 'child item')
        self.assertTrue(child is not root)
        self.assertTrue(child != root)

    def test_lib_agw_hypertreelistColumns(self):
        tree = HTL.HyperTreeList(self.frame)
        tree.AddColumn("First column")
        tree.AddColumn("Second column")

        self.assertEqual(tree.GetColumnCount(), 2)
        tree.RemoveColumn(0)
        self.assertEqual(tree.GetColumnCount(), 1)

        self.assertEqual(tree.GetColumnWidth(0), HTL._DEFAULT_COL_WIDTH)

        tree.AddColumn("Second column")
        tree.SetColumnShown(1, False)
        self.assertTrue(not tree.IsColumnShown(1))

        tree.SetColumnEditable(0, True)
        self.assertTrue(tree.IsColumnEditable(0))

    def test_lib_agw_hypertreelistConstantsExist(self):
        HTL.TR_ALIGN_WINDOWS
        HTL.TR_AUTO_CHECK_CHILD
        HTL.TR_AUTO_CHECK_PARENT
        HTL.TR_AUTO_TOGGLE_CHILD
        HTL.TR_COLUMN_LINES
        HTL.TR_EDIT_LABELS
        HTL.TR_ELLIPSIZE_LONG_ITEMS
        HTL.TR_EXTENDED
        HTL.TR_FULL_ROW_HIGHLIGHT
        HTL.TR_HAS_BUTTONS
        HTL.TR_HAS_VARIABLE_ROW_HEIGHT
        HTL.TR_HIDE_ROOT
        HTL.TR_LINES_AT_ROOT
        HTL.TR_MULTIPLE
        HTL.TR_NO_BUTTONS
        HTL.TR_NO_HEADER
        HTL.TR_NO_LINES
        HTL.TR_ROW_LINES
        HTL.TR_SINGLE
        HTL.TR_TWIST_BUTTONS
        HTL.TR_VIRTUAL
        HTL.TREE_HITTEST_ONITEMCHECKICON
        HTL.TR_FILL_WHOLE_COLUMN_BACKGROUND

    def test_lib_agw_hypertreelistEvents(self):
        HTL.EVT_TREE_ITEM_CHECKED
        HTL.EVT_TREE_ITEM_CHECKING
        HTL.EVT_TREE_ITEM_HYPERLINK

    def test_lib_agw_hypertreelistSetItemColour(self):
        tree = HTL.HyperTreeList(self.frame)
        tree.AddColumn("First column")
        root = tree.AddRoot('root item')
        child = tree.AppendItem(root, 'child item')
        
        self.assertEqual(None, tree.GetItemBackgroundColour(root))
        
        colour = wx.RED
        tree.SetItemBackgroundColour(child, colour)
        self.assertEqual(colour, tree.GetItemBackgroundColour(child))

    def test_lib_agw_hypertreelistSetItemColourOfColumns(self):
        tree = HTL.HyperTreeList(self.frame)
        tree.AddColumn("First column")
        tree.AddColumn("Second column")
        tree.AddColumn("Third column")
        root = tree.AddRoot('root item')
        child = tree.AppendItem(root, 'child item')

        colColour0 = wx.GREEN
        colColour2 = wx.RED
        tree.SetItemBackgroundColour(child, colColour0)
        tree.SetItemBackgroundColour(child, colColour2, column=2)

        self.assertEqual(colColour2, tree.GetItemBackgroundColour(child, column=2))
        self.assertNotEqual(tree.GetItemBackgroundColour(child),
                         tree.GetItemBackgroundColour(child,column=2))
        self.assertEqual(None, tree.GetItemBackgroundColour(child, column=1))

    def test_lib_agw_hypertreelistColourWholeItemColumns(self):

        tree = HTL.HyperTreeList(self.frame, agwStyle=HTL.TR_DEFAULT_STYLE|
                                                      HTL.TR_FILL_WHOLE_COLUMN_BACKGROUND)
        tree.AddColumn("First column")
        tree.AddColumn("Second column")
        root = tree.AddRoot('root item')
            
        tree.SetItemBackgroundColour(root, wx.RED)
        tree.SetItemBackgroundColour(root, wx.GREEN, column=1)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
