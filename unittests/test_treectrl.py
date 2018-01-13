import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class treectrl_Tests(wtc.WidgetTestCase):

    def test_treectrlCtor(self):
        t = wx.TreeCtrl(self.frame)

    def test_treectrlDefaultCtor(self):
        t = wx.TreeCtrl()
        t.Create(self.frame)


    def test_treectrlTreeItemId01(self):
        tree = wx.TreeCtrl(self.frame)
        root = tree.AddRoot('root item')
        self.assertTrue(isinstance(root, wx.TreeItemId))
        self.assertTrue(root.IsOk())

        r = tree.GetRootItem()
        self.assertTrue(r is not root)
        self.assertTrue(r == root)

        child = tree.AppendItem(root, 'child item')
        self.assertTrue(child is not root)
        self.assertTrue(child != root)


    def test_treectrlTreeItemId02(self):
        # Can a TreeItemId be a dictionary key?
        tree = wx.TreeCtrl(self.frame)
        root = tree.AddRoot('root item')
        r = tree.GetRootItem()
        child = tree.AppendItem(root, 'child item')

        d = dict()
        d[root] = 'root'
        d[child] = 'child'
        assert d[root] == 'root'
        assert d[r] == 'root'


    def test_treectrlTreeItemId03(self):
        # Compare with None
        tree = wx.TreeCtrl(self.frame)
        root = tree.AddRoot('root item')
        self.assertTrue(root != None)
        self.assertFalse(root == None)


    def test_treectrlTreeItemData(self):
        value = 'Some Python Object'
        tree = wx.TreeCtrl(self.frame)
        root = tree.AddRoot('root item', data=value)
        v = tree.GetItemData(root)
        self.assertTrue(v == value)
        tree.SetItemData(root, None)
        self.assertTrue(tree.GetItemData(root) is None)


    def test_treectrlTreeItemPyData(self):
        # ensure that the "Py" versions raise deprecation warnings
        value = 'Some Python Object'
        tree = wx.TreeCtrl(self.frame)
        root = tree.AddRoot('root item')
        tree.SetItemData(root, value)

        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaises(wx.wxPyDeprecationWarning):
                tree.SetItemPyData(root, value)

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaises(wx.wxPyDeprecationWarning):
                tree.GetItemPyData(root)


    def test_treectrlGetSelections(self):
        tree = wx.TreeCtrl(self.frame, style=wx.TR_MULTIPLE)
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
        self.assertTrue(isinstance(sel[0], wx.TreeItemId))



    def test_treectrlGetFirstNext(self):
        tree = wx.TreeCtrl(self.frame)
        root = tree.AddRoot('root item')
        c1 = tree.AppendItem(root, 'c1')
        c2 = tree.AppendItem(root, 'c2')
        c3 = tree.AppendItem(root, 'c3')
        c4 = tree.AppendItem(root, 'c4')

        children = []
        item, cookie = tree.GetFirstChild(root)
        while item:
            children.append(item)
            item, cookie = tree.GetNextChild(root, cookie)

        self.assertEqual(len(children), 4)
        self.assertEqual(children[0], c1)
        self.assertEqual(children[1], c2)
        self.assertEqual(children[2], c3)
        self.assertEqual(children[3], c4)



    def test_treectrlConstantsExist(self):
        wx.TR_NO_BUTTONS
        wx.TR_HAS_BUTTONS
        wx.TR_NO_LINES
        wx.TR_LINES_AT_ROOT
        wx.TR_SINGLE
        wx.TR_MULTIPLE
        wx.TR_HAS_VARIABLE_ROW_HEIGHT
        wx.TR_EDIT_LABELS
        wx.TR_HIDE_ROOT
        wx.TR_ROW_LINES
        wx.TR_FULL_ROW_HIGHLIGHT
        wx.TR_DEFAULT_STYLE
        wx.TR_TWIST_BUTTONS
        wx.TreeItemIcon_Normal
        wx.TreeItemIcon_Selected
        wx.TreeItemIcon_Expanded
        wx.TreeItemIcon_SelectedExpanded
        wx.TREE_ITEMSTATE_NONE
        wx.TREE_ITEMSTATE_NEXT
        wx.TREE_ITEMSTATE_PREV
        wx.TREE_HITTEST_ABOVE
        wx.TREE_HITTEST_BELOW
        wx.TREE_HITTEST_NOWHERE
        wx.TREE_HITTEST_ONITEMBUTTON
        wx.TREE_HITTEST_ONITEMICON
        wx.TREE_HITTEST_ONITEMINDENT
        wx.TREE_HITTEST_ONITEMLABEL
        wx.TREE_HITTEST_ONITEMRIGHT
        wx.TREE_HITTEST_ONITEMSTATEICON
        wx.TREE_HITTEST_TOLEFT
        wx.TREE_HITTEST_TORIGHT
        wx.TREE_HITTEST_ONITEMUPPERPART
        wx.TREE_HITTEST_ONITEMLOWERPART
        wx.TREE_HITTEST_ONITEM


    def test_treeEventsExist(self):
        wx.wxEVT_COMMAND_TREE_BEGIN_DRAG
        wx.wxEVT_COMMAND_TREE_BEGIN_RDRAG
        wx.wxEVT_COMMAND_TREE_BEGIN_LABEL_EDIT
        wx.wxEVT_COMMAND_TREE_END_LABEL_EDIT
        wx.wxEVT_COMMAND_TREE_DELETE_ITEM
        wx.wxEVT_COMMAND_TREE_GET_INFO
        wx.wxEVT_COMMAND_TREE_SET_INFO
        wx.wxEVT_COMMAND_TREE_ITEM_EXPANDED
        wx.wxEVT_COMMAND_TREE_ITEM_EXPANDING
        wx.wxEVT_COMMAND_TREE_ITEM_COLLAPSED
        wx.wxEVT_COMMAND_TREE_ITEM_COLLAPSING
        wx.wxEVT_COMMAND_TREE_SEL_CHANGED
        wx.wxEVT_COMMAND_TREE_SEL_CHANGING
        wx.wxEVT_COMMAND_TREE_KEY_DOWN
        wx.wxEVT_COMMAND_TREE_ITEM_ACTIVATED
        wx.wxEVT_COMMAND_TREE_ITEM_RIGHT_CLICK
        wx.wxEVT_COMMAND_TREE_ITEM_MIDDLE_CLICK
        wx.wxEVT_COMMAND_TREE_END_DRAG
        wx.wxEVT_COMMAND_TREE_STATE_IMAGE_CLICK
        wx.wxEVT_COMMAND_TREE_ITEM_GETTOOLTIP
        wx.wxEVT_COMMAND_TREE_ITEM_MENU

        wx.EVT_TREE_BEGIN_DRAG
        wx.EVT_TREE_BEGIN_RDRAG
        wx.EVT_TREE_BEGIN_LABEL_EDIT
        wx.EVT_TREE_END_LABEL_EDIT
        wx.EVT_TREE_DELETE_ITEM
        wx.EVT_TREE_GET_INFO
        wx.EVT_TREE_SET_INFO
        wx.EVT_TREE_ITEM_EXPANDED
        wx.EVT_TREE_ITEM_EXPANDING
        wx.EVT_TREE_ITEM_COLLAPSED
        wx.EVT_TREE_ITEM_COLLAPSING
        wx.EVT_TREE_SEL_CHANGED
        wx.EVT_TREE_SEL_CHANGING
        wx.EVT_TREE_KEY_DOWN
        wx.EVT_TREE_ITEM_ACTIVATED
        wx.EVT_TREE_ITEM_RIGHT_CLICK
        wx.EVT_TREE_ITEM_MIDDLE_CLICK
        wx.EVT_TREE_END_DRAG
        wx.EVT_TREE_STATE_IMAGE_CLICK
        wx.EVT_TREE_ITEM_GETTOOLTIP
        wx.EVT_TREE_ITEM_MENU

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
