import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class listctrl_Tests(wtc.WidgetTestCase):

    def test_listctrlCtor(self):
        lc = wx.ListCtrl(self.frame, style=wx.LC_REPORT)


    def test_listctrlDefaultCtor(self):
        lc = wx.ListCtrl()
        lc.Create(self.frame, style=wx.LC_REPORT)


    def test_listctrlEventTypes(self):
        wx.wxEVT_COMMAND_LIST_BEGIN_DRAG
        wx.wxEVT_COMMAND_LIST_BEGIN_RDRAG
        wx.wxEVT_COMMAND_LIST_BEGIN_LABEL_EDIT
        wx.wxEVT_COMMAND_LIST_END_LABEL_EDIT
        wx.wxEVT_COMMAND_LIST_DELETE_ITEM
        wx.wxEVT_COMMAND_LIST_DELETE_ALL_ITEMS
        wx.wxEVT_COMMAND_LIST_ITEM_SELECTED
        wx.wxEVT_COMMAND_LIST_ITEM_DESELECTED
        wx.wxEVT_COMMAND_LIST_KEY_DOWN
        wx.wxEVT_COMMAND_LIST_INSERT_ITEM
        wx.wxEVT_COMMAND_LIST_COL_CLICK
        wx.wxEVT_COMMAND_LIST_ITEM_RIGHT_CLICK
        wx.wxEVT_COMMAND_LIST_ITEM_MIDDLE_CLICK
        wx.wxEVT_COMMAND_LIST_ITEM_ACTIVATED
        wx.wxEVT_COMMAND_LIST_CACHE_HINT
        wx.wxEVT_COMMAND_LIST_COL_RIGHT_CLICK
        wx.wxEVT_COMMAND_LIST_COL_BEGIN_DRAG
        wx.wxEVT_COMMAND_LIST_COL_DRAGGING
        wx.wxEVT_COMMAND_LIST_COL_END_DRAG
        wx.wxEVT_COMMAND_LIST_ITEM_FOCUSED

        wx.EVT_LIST_BEGIN_DRAG
        wx.EVT_LIST_BEGIN_RDRAG
        wx.EVT_LIST_BEGIN_LABEL_EDIT
        wx.EVT_LIST_END_LABEL_EDIT
        wx.EVT_LIST_DELETE_ITEM
        wx.EVT_LIST_DELETE_ALL_ITEMS
        wx.EVT_LIST_ITEM_SELECTED
        wx.EVT_LIST_ITEM_DESELECTED
        wx.EVT_LIST_KEY_DOWN
        wx.EVT_LIST_INSERT_ITEM
        wx.EVT_LIST_COL_CLICK
        wx.EVT_LIST_ITEM_RIGHT_CLICK
        wx.EVT_LIST_ITEM_MIDDLE_CLICK
        wx.EVT_LIST_ITEM_ACTIVATED
        wx.EVT_LIST_CACHE_HINT
        wx.EVT_LIST_COL_RIGHT_CLICK
        wx.EVT_LIST_COL_BEGIN_DRAG
        wx.EVT_LIST_COL_DRAGGING
        wx.EVT_LIST_COL_END_DRAG
        wx.EVT_LIST_ITEM_FOCUSED


    def test_listctrlEvent(self):
        # check creating a ListEvent, and if the properties are working
        evt = wx.ListEvent(wx.wxEVT_COMMAND_LIST_ITEM_SELECTED, 123)

        evt.KeyCode = 111
        assert evt.GetKeyCode() == 111

        evt.Index = 222
        assert evt.GetIndex() == 222

        evt.Column = 3
        assert evt.GetColumn() == 3

        evt.Point = (44, 55)
        assert evt.GetPoint() == (44, 55)

        i = wx.ListItem()
        i.SetId(66)
        evt.Item = i
        assert evt.GetItem().GetId() == 66

        evt.CacheFrom = 77
        assert evt.GetCacheFrom() == 77

        evt.CacheTo = 88
        assert evt.GetCacheTo() == 88


    def test_listctrlConstants(self):
        wx.LC_VRULES
        wx.LC_HRULES

        wx.LC_ICON
        wx.LC_SMALL_ICON
        wx.LC_LIST
        wx.LC_REPORT

        wx.LC_ALIGN_TOP
        wx.LC_ALIGN_LEFT
        wx.LC_AUTOARRANGE
        wx.LC_VIRTUAL
        wx.LC_EDIT_LABELS
        wx.LC_NO_HEADER
        wx.LC_NO_SORT_HEADER
        wx.LC_SINGLE_SEL
        wx.LC_SORT_ASCENDING
        wx.LC_SORT_DESCENDING

        wx.LC_MASK_TYPE
        wx.LC_MASK_ALIGN
        wx.LC_MASK_SORT

        wx.LIST_MASK_STATE
        wx.LIST_MASK_TEXT
        wx.LIST_MASK_IMAGE
        wx.LIST_MASK_DATA
        wx.LIST_SET_ITEM
        wx.LIST_MASK_WIDTH
        wx.LIST_MASK_FORMAT

        wx.LIST_STATE_DONTCARE
        wx.LIST_STATE_DROPHILITED
        wx.LIST_STATE_FOCUSED
        wx.LIST_STATE_SELECTED
        wx.LIST_STATE_CUT

        wx.LIST_HITTEST_ABOVE
        wx.LIST_HITTEST_BELOW
        wx.LIST_HITTEST_NOWHERE
        wx.LIST_HITTEST_ONITEMICON
        wx.LIST_HITTEST_ONITEMLABEL
        wx.LIST_HITTEST_ONITEMSTATEICON
        wx.LIST_HITTEST_TOLEFT
        wx.LIST_HITTEST_TORIGHT
        wx.LIST_HITTEST_ONITEM

        wx.LIST_GETSUBITEMRECT_WHOLEITEM

        wx.LIST_NEXT_ABOVE
        wx.LIST_NEXT_ALL
        wx.LIST_NEXT_BELOW
        wx.LIST_NEXT_LEFT
        wx.LIST_NEXT_RIGHT

        wx.LIST_ALIGN_DEFAULT
        wx.LIST_ALIGN_LEFT
        wx.LIST_ALIGN_TOP
        wx.LIST_ALIGN_SNAP_TO_GRID

        wx.LIST_FORMAT_LEFT
        wx.LIST_FORMAT_RIGHT
        wx.LIST_FORMAT_CENTRE
        wx.LIST_FORMAT_CENTER

        wx.LIST_AUTOSIZE
        wx.LIST_AUTOSIZE_USEHEADER

        wx.LIST_RECT_BOUNDS
        wx.LIST_RECT_ICON
        wx.LIST_RECT_LABEL

        wx.LIST_FIND_UP
        wx.LIST_FIND_DOWN
        wx.LIST_FIND_LEFT
        wx.LIST_FIND_RIGHT


    def _makeListCtrl(self):
        lc = wx.ListCtrl(self.frame, style=wx.LC_REPORT)
        lc.AppendColumn('AAAA')
        lc.AppendColumn('BBBB')
        lc.InsertItem(0, 'item 1A')
        lc.SetItem(0, 1, 'item 1B')
        return lc


    def test_listctrlItemData01(self):
        lc = self._makeListCtrl()
        lc.SetItemData(0, 12345)
        data = lc.GetItemData(0)
        assert data == 12345


    def test_listctrlItemData02(self):
        lc = self._makeListCtrl()
        with self.assertRaises(OverflowError):
            lc.SetItemData(0, wx._core._LLONG_MAX + 100)


    def test_listctrlDeleteAllColumns(self):
        lc = self._makeListCtrl()
        lc.DeleteAllColumns()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
