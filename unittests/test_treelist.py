import imp_unittest, unittest
import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class treelist_Tests(wtc.WidgetTestCase):


    def test_treelist1(self):
        wx.adv.TL_SINGLE       
        wx.adv.TL_MULTIPLE     
        wx.adv.TL_CHECKBOX     
        wx.adv.TL_3STATE       
        wx.adv.TL_USER_3STATE  
        wx.adv.TL_DEFAULT_STYLE 
        wx.adv.TL_STYLE_MASK    
                  
        wx.adv.EVT_TREELIST_SELECTION_CHANGED 
        wx.adv.EVT_TREELIST_ITEM_EXPANDING 
        wx.adv.EVT_TREELIST_ITEM_EXPANDED
        wx.adv.EVT_TREELIST_ITEM_CHECKED 
        wx.adv.EVT_TREELIST_ITEM_ACTIVATED
        wx.adv.EVT_TREELIST_ITEM_CONTEXT_MENU
        wx.adv.EVT_TREELIST_COLUMN_SORTED 
        wx.adv.wxEVT_COMMAND_TREELIST_SELECTION_CHANGED
        wx.adv.wxEVT_COMMAND_TREELIST_ITEM_EXPANDING 
        wx.adv.wxEVT_COMMAND_TREELIST_ITEM_EXPANDED 
        wx.adv.wxEVT_COMMAND_TREELIST_ITEM_CHECKED 
        wx.adv.wxEVT_COMMAND_TREELIST_ITEM_ACTIVATED 
        wx.adv.wxEVT_COMMAND_TREELIST_ITEM_CONTEXT_MENU
        wx.adv.wxEVT_COMMAND_TREELIST_COLUMN_SORTED   


    def _populateTree(self, tlc):
        assert isinstance(tlc, wx.adv.TreeListCtrl)
        tlc.AppendColumn('Column 1')
        tlc.AppendColumn('Column 2', align=wx.ALIGN_RIGHT)
        
        # use the hidden root as the parent of the visible root
        root = tlc.AppendItem(tlc.GetRootItem(), 'My Root') 
        tlc.SetItemText(root, 1, 'root col 2')
        
        for x in range(3):
            item = tlc.AppendItem(root, 'item %d' % (x+1))
            tlc.SetItemText(item, 1, 'item col 2')
            
        return root
    
    

    def test_treelist2(self):
        tlc = wx.adv.TreeListCtrl(self.frame)
        root = self._populateTree(tlc)

        s = tlc.GetSelections()
        self.assertTrue(isinstance(s, list))
        self.assertEqual(s, [])

        tlc.Select(root)        
        self.assertEqual(tlc.GetItemText(root), tlc.GetItemText(tlc.GetSelection()))
        
        s = tlc.GetSelections()
        self.assertTrue(isinstance(s, list))
        self.assertEqual(len(s), 1)
        self.assertTrue(isinstance(s[0], wx.adv.TreeListItem))
        
        
    def test_treelist3(self):
        tlc = wx.adv.TreeListCtrl(self.frame, style=wx.adv.TL_MULTIPLE)
        root = self._populateTree(tlc)

        tlc.Select(root)        
        tlc.Select(tlc.GetFirstChild(root))
        s = tlc.GetSelections()
        self.assertTrue(isinstance(s, list))
        self.assertEqual(len(s), 2)
        
                
    def test_treelist4(self):
        tlc = wx.adv.TreeListCtrl(self.frame, style=wx.adv.TL_MULTIPLE)
        root = self._populateTree(tlc)
        
        # test if embedded DataViewCtrl is returned as the correct type
        dvc = tlc.GetChildren()[0]
        self.assertTrue(hasattr(dvc, 'IsTopLevel'))
        self.assertEqual(dvc.__class__.__module__, 'wx._dataview')
        
        
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
