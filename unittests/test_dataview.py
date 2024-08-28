import unittest
from unittests import wtc
import wx
import wx.dataview as dv
import os
import sys

pngFile = os.path.join(os.path.dirname(__file__), 'smile.png')

#---------------------------------------------------------------------------


class dataview_Tests(wtc.WidgetTestCase):

    def test_dataviewItem1(self):
        dvi = dv.DataViewItem()
        self.assertFalse(dvi)

    def test_dataviewItem2(self):
        dvi = dv.DataViewItem(12345)
        self.assertTrue(dvi)

    def test_dataviewItem3(self):
        dvi1 = dv.DataViewItem(111)
        dvi2 = dv.DataViewItem(222)
        self.assertTrue(dvi1 != dvi2)
        self.assertFalse(dvi1 == dvi2)

    def test_dataviewItem4(self):
        dvi1 = dv.DataViewItem(111)
        dvi2 = dv.DataViewItem(111)
        self.assertTrue(dvi1 == dvi2)
        self.assertFalse(dvi1 != dvi2)

    def test_dataviewItem5(self):
        self.assertFalse(dv.NullDataViewItem)


    def test_dataviewItem6(self):
        dvi1 = dv.DataViewItem(111)
        dvi2 = dv.DataViewItem(222)
        self.assertTrue(int(dvi1.GetID()) == 111)
        self.assertTrue(int(dvi2.ID) == 222)

    def test_dataviewItem7(self):
        n = sys.maxsize
        dvi = dv.DataViewItem(n)
        self.assertTrue(dvi)
        self.assertTrue(int(dvi.GetID()) == n)


    def test_dataviewItem8(self):
        dvi = dv.DataViewItem(111)
        assert (None == dvi) == False
        assert (None != dvi) == True


    #-------------------------------------------------------
    def test_dataviewItemAttr1(self):
        a = dv.DataViewItemAttr()
        self.assertTrue(a.IsDefault())
        self.assertFalse(a.HasColour())
        self.assertFalse(a.HasFont())
        self.assertFalse(a.HasBackgroundColour())


    def test_dataviewItemAttr2(self):
        a = dv.DataViewItemAttr()
        a.Colour = wx.BLACK
        a.BackgroundColour = wx.WHITE
        a.Bold = True
        a.Italic = True
        self.assertFalse(a.IsDefault())
        self.assertTrue(a.HasColour())
        self.assertTrue(a.HasBackgroundColour())
        self.assertTrue(a.GetBold())
        self.assertTrue(a.GetItalic())


    #-------------------------------------------------------
    def test_dataviewIconText1(self):
        dit = dv.DataViewIconText()
        icon = wx.Icon(pngFile)
        dit.SetIcon(icon)
        dit.SetText('Smile!')


    def test_dataviewIconText2(self):
        icon = wx.Icon(pngFile)
        dit = dv.DataViewIconText('Smile!', wx.BitmapBundle(icon))
        dit.Icon
        dit.Text

    #-------------------------------------------------------
    def test_dataviewCheckIconText1(self):
        dcit = dv.DataViewCheckIconText()
        icon = wx.Icon(pngFile)
        dcit.SetIcon(icon)
        dcit.SetText('Smile!')

    def test_dataviewCheckIconText2(self):
        icon = wx.Icon(pngFile)
        dcit = dv.DataViewCheckIconText('Smile!', wx.BitmapBundle(icon), wx.CHK_CHECKED)
        dcit.Icon
        dcit.Text
        dcit.CheckedState

    def test_dataviewCheckIconText3(self):
        icon = wx.Icon(pngFile)
        dcit = dv.DataViewCheckIconText('Smile!', wx.BitmapBundle(icon))
        state = dcit.GetCheckedState()
        assert state == wx.CHK_UNDETERMINED

        dcit.SetCheckedState(wx.CHK_CHECKED)
        state = dcit.GetCheckedState()
        assert state == wx.CHK_CHECKED



    #-------------------------------------------------------
    def test_dataviewModelNotifier1(self):
        with self.assertRaises(TypeError):
            n = dv.DataViewModelNotifier()


    def test_dataviewModelNotifier2(self):
        class MyNotifier(dv.DataViewModelNotifier):
            def Cleared(self): return True

            def ItemAdded(self, parent, item): return True
            def ItemChanged(self, item): return True
            def ItemDeleted(self, parent, item): return True
            def ItemsAdded(self, parent, items): return True
            def ItemsChanged(self, items): return True
            def ItemsDeleted(self, parent, items): return True

            def Resort(self): pass
            def ValueChanged(self, item, col): return True

        n = MyNotifier()


    #-------------------------------------------------------
    def test_dataviewRenderer01(self):
        with self.assertRaises(TypeError):
            r = dv.DataViewRenderer()


    def test_dataviewRenderer02(self):
        # This one can't be subclassed (that's what dv.DataViewCustomRenderer
        # is for) so make sure it raises an exception too.
        with self.assertRaises(TypeError):
            class MyRenderer(dv.DataViewRenderer):
                def GetValue(self):  return "value"
                def SetValue(self, value): return True

            r = MyRenderer()


    def test_dataviewRenderer03(self):
        r = dv.DataViewTextRenderer()

    def test_dataviewRenderer04(self):
        r = dv.DataViewIconTextRenderer()

    def test_dataviewRenderer05(self):
        r = dv.DataViewProgressRenderer()

    def test_dataviewRenderer06(self):
        r = dv.DataViewSpinRenderer(0, 100)

    def test_dataviewRenderer07(self):
        r = dv.DataViewToggleRenderer()

    def test_dataviewRenderer08(self):
        r = dv.DataViewDateRenderer()

    def test_dataviewRenderer09(self):
        r = dv.DataViewBitmapRenderer()


    def test_dataviewRenderer10(self):
        with self.assertRaises(TypeError):
            r = dv.DataViewCustomRenderer()

    def test_dataviewRenderer11(self):
        class MyCustomRenderer(dv.DataViewCustomRenderer):
            def GetValue(self):  return "value"
            def SetValue(self, value): return True
            def GetSize(self): return wx.Size(100, 25)
            def Render(self, cell, dc, state): return True

        r = MyCustomRenderer()

    def test_dataviewRenderer12(self):
        r = dv.DataViewChoiceRenderer("one two three".split())

    def test_dataviewRenderer13(self):
        r = dv.DataViewCheckIconTextRenderer()


    #-------------------------------------------------------
    def test_dataviewColumn(self):
        r = dv.DataViewIconTextRenderer()
        # create
        c = dv.DataViewColumn('title', r, 0)
        # test that properties exist
        c.Title
        c.Bitmap
        c.Width
        c.MinWidth
        c.Alignment
        c.Flags
        c.SortOrder

        self.myYield()

    #-------------------------------------------------------
    def test_dataviewModel1(self):
        with self.assertRaises(TypeError):
            m = dv.DataViewModel()


    def test_dataviewModel2(self):
        class MyModel(dv.DataViewModel):
            def GetChildren(self, item, children): return 0
            def GetColumnCount(self): return 0
            def GetColumnType(self, col): return 'string'
            def GetParent(self, item): return dv.NullDataViewItem
            def GetValue(self, item, col): return 'value'
            def IsContainer(self, item) : return False
            def SetValue(self, value, item, col): return True

        m = MyModel()

    #-------------------------------------------------------
    def test_dataviewIndexListModel1(self):
        with self.assertRaises(TypeError):
            m = dv.DataViewIndexListModel()

    def test_dataviewIndexListModel2(self):
        class MyModel(dv.DataViewIndexListModel):
            def GetCount(self): return 0
            def GetRow(self, item): return 0
            def GetValueByRow(self, row, col): return 'value'
            def SetValueByRow(self, value, row, col): return True

        m = MyModel()


    def test_dataviewVirtualListModel1(self):
        with self.assertRaises(TypeError):
            m = dv.DataViewVirtualListModel()

    def test_dataviewVirtualModel2(self):
        class MyModel(dv.DataViewVirtualListModel):
            def GetCount(self): return 0
            def GetRow(self, item): return 0
            def GetValueByRow(self, row, col): return 'value'
            def SetValueByRow(self, value, row, col): return True

        m = MyModel()


    #-------------------------------------------------------
    def test_dataviewCtrl1(self):

        class MyModel(dv.DataViewIndexListModel):
            def GetCount(self):
                return 50

            def GetColumnCount(self):
                return 10

            def GetValueByRow(self, row, col):
                return 'value(%d, %d)' % (row, col)

            def SetValueByRow(self, value, row, col):
                return True

            def GetColumnType(self, col):
                return 'string'



        dvc = dv.DataViewCtrl(self.frame, style=dv.DV_ROW_LINES|dv.DV_VERT_RULES|dv.DV_MULTIPLE)
        model = MyModel()
        count1 = model.GetRefCount()
        dvc.AssociateModel(model)
        count2 = model.GetRefCount()

        # The reference count should still be 1 because the model was
        # DecRef'ed when it's ownership transferred to C++ in the
        # AssociateModel call
        self.assertEqual(count2, 1)
        self.assertTrue(count2 == count1)

        # Now try associating it with another view and check counts again
        dvc2 = dv.DataViewCtrl(self.frame, style=dv.DV_ROW_LINES|dv.DV_VERT_RULES|dv.DV_MULTIPLE)
        dvc2.AssociateModel(model)
        self.assertEqual(model.GetRefCount(), 2)

        # Destroying the 2nd view should drop the refcount again
        dvc2.Destroy()
        self.assertEqual(model.GetRefCount(), 1)

        # And since ownership has been transferred, deleting this reference
        # to the model should not cause any problems.
        del model

        dvc.AppendTextColumn("one",   1, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvc.AppendTextColumn("two",   2, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvc.AppendTextColumn("three", 3, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvc.AppendTextColumn("four",  4, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvc.AppendTextColumn("five",  5, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)

        self.frame.SendSizeEvent()
        dvc.Refresh()
        self.myYield()



    #-------------------------------------------------------
    def test_dataviewListCtrl1(self):
        dlc = dv.DataViewListCtrl()
        dlc.Create(self.frame)
        self.doListCtrlTest(dlc)


    def test_dataviewListCtrl2(self):
        dlc = dv.DataViewListCtrl(self.frame)
        self.doListCtrlTest(dlc)

    def doListCtrlTest(self, dlc):
        assert isinstance(dlc, dv.DataViewListCtrl)
        for label in "one two three four".split():
            dlc.AppendTextColumn(label)
        col = dv.DataViewColumn('five', dv.DataViewBitmapRenderer(), 4)
        dlc.AppendColumn(col)

        bmp = wx.Bitmap(pngFile)
        for n in range(50):
            rowdata = ['%s-%02d' % (s, n) for s in "one two three four".split()]
            rowdata.append(bmp)
            dlc.AppendItem(rowdata)

        self.frame.SendSizeEvent()
        dlc.Refresh()
        self.myYield()


    def test_dataviewHitTest(self):
        dlc = dv.DataViewListCtrl(self.frame)
        self.doListCtrlTest(dlc)
        item, col = dlc.HitTest((10,50))
        self.assertTrue(isinstance(item, dv.DataViewItem))
        self.assertTrue(isinstance(col, dv.DataViewColumn) or col is None)

    #-------------------------------------------------------
    # DataViewTreeCtrl


    def test_dataviewTreeCtrl1(self):
        dtc = dv.DataViewTreeCtrl()
        dtc.Create(self.frame)
        self.doTreeCtrlTest(dtc)


    def test_dataviewTreeCtrl2(self):
        dtc = dv.DataViewTreeCtrl(self.frame)
        self.doTreeCtrlTest(dtc)


    def doTreeCtrlTest(self, dvtc):
        isz = (16,16)
        il = wx.ImageList(*isz)
        fldridx     = il.Add(wx.ArtProvider.GetIcon(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetIcon(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx     = il.Add(wx.ArtProvider.GetIcon(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        dvtc.SetImageList(il)

        self.root = dvtc.AppendContainer(dv.NullDataViewItem,
                                         "The Root Item",
                                         fldridx, fldropenidx)
        for x in range(15):
            child = dvtc.AppendContainer(self.root, "Item %d" % x,
                                         fldridx, fldropenidx)
            for y in range(5):
                last = dvtc.AppendContainer(
                    child, "item %d-%s" % (x, chr(ord("a")+y)),
                    fldridx, fldropenidx)
                for z in range(5):
                    item = dvtc.AppendItem(
                        last, "item %d-%s-%d" % (x, chr(ord("a")+y), z),
                        fileidx)
                    dvtc.ExpandAncestors(item)

        self.frame.SendSizeEvent()
        dvtc.Refresh()
        self.myYield()


    #-------------------------------------------------------
    def test_dataviewConst(self):
        dv.DVC_DEFAULT_RENDERER_SIZE
        dv.DVC_DEFAULT_WIDTH
        dv.DVC_TOGGLE_DEFAULT_WIDTH
        dv.DVC_DEFAULT_MINWIDTH
        dv.DVR_DEFAULT_ALIGNMENT

        dv.DATAVIEW_CELL_INERT
        dv.DATAVIEW_CELL_ACTIVATABLE
        dv.DATAVIEW_CELL_EDITABLE
        dv.DATAVIEW_CELL_SELECTED
        dv.DATAVIEW_CELL_PRELIT
        dv.DATAVIEW_CELL_INSENSITIVE
        dv.DATAVIEW_CELL_FOCUSED

        dv.DATAVIEW_COL_RESIZABLE
        dv.DATAVIEW_COL_SORTABLE
        dv.DATAVIEW_COL_REORDERABLE
        dv.DATAVIEW_COL_HIDDEN

        dv.DV_SINGLE
        dv.DV_MULTIPLE
        dv.DV_NO_HEADER
        dv.DV_HORIZ_RULES
        dv.DV_VERT_RULES
        dv.DV_ROW_LINES
        dv.DV_VARIABLE_LINE_HEIGHT


    def test_dataviewEvt1(self):
        evt = dv.DataViewEvent()

        evt.GetItem
        evt.SetItem
        evt.GetColumn
        evt.SetColumn
        evt.GetModel
        evt.SetModel
        evt.GetValue
        evt.SetValue
        evt.IsEditCancelled
        evt.SetDataViewColumn
        evt.GetDataViewColumn
        evt.GetPosition
        evt.SetPosition
        evt.GetCacheFrom
        evt.GetCacheTo
        evt.SetCache
        evt.SetDataObject
        evt.GetDataObject
        evt.SetDataFormat
        evt.GetDataFormat
        evt.SetDataSize
        evt.GetDataSize
        evt.SetDataBuffer
        evt.GetDataBuffer
        evt.SetDragFlags
        evt.GetDragFlags
        evt.SetDropEffect
        evt.GetDropEffect


    def test_dataviewEvt2(self):
        dv.wxEVT_COMMAND_DATAVIEW_SELECTION_CHANGED;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_ACTIVATED;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSED;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDED;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSING;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDING;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_START_EDITING;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_STARTED;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_DONE;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_VALUE_CHANGED;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_CONTEXT_MENU;
        dv.wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_CLICK;
        dv.wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK;
        dv.wxEVT_COMMAND_DATAVIEW_COLUMN_SORTED;
        dv.wxEVT_COMMAND_DATAVIEW_COLUMN_REORDERED;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_BEGIN_DRAG;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_DROP_POSSIBLE;
        dv.wxEVT_COMMAND_DATAVIEW_ITEM_DROP;
        dv.wxEVT_COMMAND_DATAVIEW_CACHE_HINT;

        dv.EVT_DATAVIEW_SELECTION_CHANGED
        dv.EVT_DATAVIEW_ITEM_ACTIVATED
        dv.EVT_DATAVIEW_ITEM_COLLAPSED
        dv.EVT_DATAVIEW_ITEM_EXPANDED
        dv.EVT_DATAVIEW_ITEM_COLLAPSING
        dv.EVT_DATAVIEW_ITEM_EXPANDING
        dv.EVT_DATAVIEW_ITEM_START_EDITING
        dv.EVT_DATAVIEW_ITEM_EDITING_STARTED
        dv.EVT_DATAVIEW_ITEM_EDITING_DONE
        dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED
        dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU
        dv.EVT_DATAVIEW_COLUMN_HEADER_CLICK
        dv.EVT_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK
        dv.EVT_DATAVIEW_COLUMN_SORTED
        dv.EVT_DATAVIEW_COLUMN_REORDERED
        dv.EVT_DATAVIEW_ITEM_BEGIN_DRAG
        dv.EVT_DATAVIEW_ITEM_DROP_POSSIBLE
        dv.EVT_DATAVIEW_ITEM_DROP
        dv.EVT_DATAVIEW_CACHE_HINT




#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
