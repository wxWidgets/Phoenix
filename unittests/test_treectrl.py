import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class treectrl_Tests(wtc.WidgetTestCase):

    def test_treectrlCtor(self):
        t = wx.TreeCtrl(self.frame)
        
    def test_treectrlDefaultCtor(self):
        t = wx.TreeCtrl()
        t.Create(self.frame)
        
    
    def test_treectrlTreeItemId(self):
        tree = wx.TreeCtrl(self.frame)
        root = tree.AddRoot('root item')
        self.assertTrue( isinstance(root, wx.TreeItemId) )
        self.assertTrue( root.IsOk() )

        r = tree.GetRootItem()
        self.assertTrue( r is not root )
        self.assertTrue( r == root )
        
        child = tree.AppendItem(root, 'child item')
        self.assertTrue( child is not root )
        self.assertTrue( child != root )


    def test_treectrlTreeItemData(self):
        value = 'Some Python Object'
        tree = wx.TreeCtrl(self.frame)
        data = wx.TreeItemData(value)
        root = tree.AddRoot('root item', data=data)
        d = tree.GetItemData(root)
        self.assertTrue(d.GetData() == value)
        self.assertTrue(d.Data == value)
        self.assertTrue(d.Id == root)
        tree.SetItemData(root, None)
        self.assertTrue(tree.GetItemData(root) is None)
        
        
    def test_treectrlTreeItemPyData(self):
        value = 'Some Python Object'
        tree = wx.TreeCtrl(self.frame)
        root = tree.AddRoot('root item')
        tree.SetItemPyData(root, value)
        self.assertTrue(tree.GetItemPyData(root) == value)
        self.assertTrue(tree.GetItemData(root).GetData() == value)
        tree.SetItemPyData(root, None)
        self.assertTrue(tree.GetItemPyData(root) is None)
        
        

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
