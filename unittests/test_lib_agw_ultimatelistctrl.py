import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.lib.agw.ultimatelistctrl as ULC

#---------------------------------------------------------------------------

class VirtualList(ULC.UltimateListCtrl):

    def OnGetItemText(self, item, col):
        return 'Item %d' % item

    def OnGetItemTextColour(self, item, col):
        return None

    def OnGetItemToolTip(self, item, col):
        return None


class lib_agw_ultimatelistctrl_Tests(wtc.WidgetTestCase):

    def test_lib_agw_ultimatelistctrlCtorReport(self):
        ulc = ULC.UltimateListCtrl(self.frame, agwStyle=wx.LC_REPORT)

    def test_lib_agw_ultimatelistctrlCtorIcon(self):
        ulc = ULC.UltimateListCtrl(self.frame, agwStyle=wx.LC_ICON)

    def test_lib_agw_ultimatelistctrlCtorList(self):
        ulc = ULC.UltimateListCtrl(self.frame, agwStyle=wx.LC_LIST)

    def test_lib_agw_ultimatelistctrlCtorVirtual(self):
        ulc = ULC.UltimateListCtrl(self.frame, agwStyle=wx.LC_REPORT|wx.LC_VIRTUAL)

    def test_lib_agw_ultimatelistctrlPaintFarDown(self):
        # With Cairo, nothing was drawn past y = 2**23, about 335000 rows down
        ulc = VirtualList(self.frame, size=(300, 200), agwStyle=wx.LC_REPORT | wx.LC_VIRTUAL)
        ulc.InsertColumn(0, 'First', width=200)
        ulc.SetItemCount(1000000)
        # On MSW, the main window isn't sized until the size event is handled
        ulc.SendSizeEvent()
        main = ulc._mainWin
        main.RecalculatePositions(True)
        main.Scroll(0, main.GetLineY(999990) // ULC.SCROLL_UNIT_Y)
        main.ResetVisibleLinesRange()
        self.assertEqual(main.GetVisibleLinesRange()[1], 999999)

        w, h = main.GetClientSize()
        bmp = wx.Bitmap(w, h)
        dc = wx.MemoryDC(bmp)
        with mock.patch.object(wx, 'BufferedPaintDC', lambda win: dc), \
             mock.patch.object(main, 'IsExposed', return_value=True):
            main.OnPaint(None)
        dc.SelectObject(wx.NullBitmap)

        # The text is the only dark thing drawn
        self.assertLess(min(bmp.ConvertToImage().GetData()), 100)

    def test_lib_agw_thumbnailctrlStyles(self):
        ULC.ULC_VRULES
        ULC.ULC_HRULES
        ULC.ULC_ICON
        ULC.ULC_SMALL_ICON
        ULC.ULC_LIST
        ULC.ULC_REPORT
        ULC.ULC_ALIGN_TOP
        ULC.ULC_ALIGN_LEFT
        ULC.ULC_AUTOARRANGE
        ULC.ULC_VIRTUAL
        ULC.ULC_EDIT_LABELS
        ULC.ULC_NO_HEADER
        ULC.ULC_NO_SORT_HEADER
        ULC.ULC_SINGLE_SEL
        ULC.ULC_SORT_ASCENDING
        ULC.ULC_SORT_DESCENDING
        ULC.ULC_TILE
        ULC.ULC_NO_HIGHLIGHT
        ULC.ULC_STICKY_HIGHLIGHT
        ULC.ULC_STICKY_NOSELEVENT
        ULC.ULC_SEND_LEFTCLICK
        ULC.ULC_HAS_VARIABLE_ROW_HEIGHT
        ULC.ULC_AUTO_CHECK_CHILD
        ULC.ULC_AUTO_TOGGLE_CHILD
        ULC.ULC_AUTO_CHECK_PARENT
        ULC.ULC_SHOW_TOOLTIPS
        ULC.ULC_HOT_TRACKING
        ULC.ULC_BORDER_SELECT
        ULC.ULC_TRACK_SELECT
        ULC.ULC_HEADER_IN_ALL_VIEWS
        ULC.ULC_NO_FULL_ROW_SELECT
        ULC.ULC_FOOTER
        ULC.ULC_USER_ROW_HEIGHT

    def test_lib_agw_ultimatelistctrlEvents(self):
        wx.EVT_LIST_BEGIN_DRAG
        wx.EVT_LIST_BEGIN_RDRAG
        wx.EVT_LIST_BEGIN_LABEL_EDIT
        wx.EVT_LIST_END_LABEL_EDIT
        wx.EVT_LIST_DELETE_ITEM
        wx.EVT_LIST_DELETE_ALL_ITEMS
        wx.EVT_LIST_KEY_DOWN
        wx.EVT_LIST_INSERT_ITEM
        wx.EVT_LIST_COL_CLICK
        wx.EVT_LIST_COL_RIGHT_CLICK
        wx.EVT_LIST_COL_BEGIN_DRAG
        wx.EVT_LIST_COL_END_DRAG
        wx.EVT_LIST_COL_DRAGGING
        wx.EVT_LIST_ITEM_SELECTED
        wx.EVT_LIST_ITEM_DESELECTED
        wx.EVT_LIST_ITEM_RIGHT_CLICK
        wx.EVT_LIST_ITEM_MIDDLE_CLICK
        wx.EVT_LIST_ITEM_ACTIVATED
        wx.EVT_LIST_ITEM_FOCUSED
        wx.EVT_LIST_CACHE_HINT
        # in doc but does not exist???
        #wx.EVT_LIST_ITEM_CHECKING
        #wx.EVT_LIST_ITEM_CHECKED
        #wx.EVT_LIST_COL_CHECKING
        #wx.EVT_LIST_COL_CHECKED
        #wx.EVT_LIST_FOOTER_CHECKING
        #wx.EVT_LIST_FOOTER_CHECKED
        #wx.EVT_LIST_ITEM_HYPERLINK
        #wx.EVT_LIST_FOOTER_CLICK
        #wx.EVT_LIST_FOOTER_RIGHT_CLICK
        #wx.EVT_LIST_ITEM_LEFT_CLICK
        #wx.EVT_LIST_END_DRAG

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
