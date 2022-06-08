import unittest
from unittests import wtc
import wx
import wx.grid


#---------------------------------------------------------------------------



class grid_Tests(wtc.WidgetTestCase):

    # NOTE: Most of these tests simply check that the class exists and can be
    # instantiated. It would be nice to add more here, but in the meantime it
    # will probably be easier to test features and interoperability between
    # the classes in a non-unitest situation. See Phoenix/samples/grid

    def test_grid00(self):
        wx.grid.GRID_AUTOSIZE
        wx.grid.GRID_DRAW_ROWS_HEADER
        wx.grid.GRID_DRAW_COLS_HEADER
        wx.grid.GRID_DRAW_CELL_LINES
        wx.grid.GRID_DRAW_BOX_RECT
        wx.grid.GRID_DRAW_SELECTION
        wx.grid.GRID_DRAW_DEFAULT


    def test_grid01(self):
        c1 = wx.grid.GridCellCoords()
        c2 = wx.grid.GridCellCoords(5,10)


    def test_grid02(self):
        r = wx.grid.GridCellAutoWrapStringRenderer()

    def test_grid03(self):
        r = wx.grid.GridCellBoolRenderer()

    def test_grid04(self):
        r = wx.grid.GridCellDateTimeRenderer()

    def test_grid05(self):
        r = wx.grid.GridCellEnumRenderer()

    def test_grid06(self):
        r = wx.grid.GridCellFloatRenderer()

    def test_grid07(self):
        r = wx.grid.GridCellNumberRenderer()

    def test_grid08(self):
        r = wx.grid.GridCellStringRenderer()

    def test_grid09(self):
        class MyRenderer(wx.grid.GridCellRenderer):
            def Clone(self):
                return MyRenderer()

            def Draw(self, grid, attr, dc, rect, row, col, isSelected):
                pass

            def GetBestSize(self, grid, attr, dc, row, col):
                return (80,20)

        r = MyRenderer()



    def test_grid10(self):
        e = wx.grid.GridCellAutoWrapStringEditor()

    def test_grid11(self):
        e = wx.grid.GridCellBoolEditor()

    def test_grid12(self):
        e = wx.grid.GridCellChoiceEditor('one two three'.split())

    def test_grid13(self):
        e = wx.grid.GridCellEnumEditor()

    def test_grid14(self):
        e = wx.grid.GridCellTextEditor()

    def test_grid15(self):
        e = wx.grid.GridCellFloatEditor()

    def test_grid16(self):
        e = wx.grid.GridCellNumberEditor()

    def test_grid17(self):
        class MyEditor(wx.grid.GridCellEditor):
            def Clone(self): return MyEditor()
            def BeginEdit(self, row, col, grid): pass
            def Create(self, parent, id, evtHandler): pass
            def EndEdit(self, row, col, grid, oldval): return None
            def ApplyEdit(self, row, col, grid): pass
            def Reset(self): pass
            def GetValue(self): return ""

        e = MyEditor()
        return e

    def test_grid17a(self):
        e = self.test_grid17()
        e.GetControl
        e.SetControl


    def test_grid18(self):
        a = wx.grid.GridCellAttr()
        a.DecRef()

    def test_grid18a(self):
        # test that some GCA methods which were missing are now present
        a = wx.grid.GridCellAttr()
        b = wx.grid.GridCellAttr()
        a.MergeWith(b)

        a.SetFont(wx.NORMAL_FONT)
        a.SetOverflow(True)
        a.SetSize(3,4)
        a.SetKind(wx.grid.GridCellAttr.Cell)

        a.HasReadWriteMode()
        a.HasOverflowMode()
        a.HasSize()

        a.GetSize()
        a.GetOverflow()
        a.GetKind()

        a.DecRef()


    def test_grid19(self):
        wx.grid.GridCellAttr.Any
        wx.grid.GridCellAttr.Cell
        wx.grid.GridCellAttr.Row
        wx.grid.GridCellAttr.Col
        wx.grid.GridCellAttr.Default
        wx.grid.GridCellAttr.Merged


    def test_grid20(self):
        class MyRenderer(wx.grid.GridCornerHeaderRenderer):
            def DrawBorder(self, grid, dc, rect):
                pass
        r = MyRenderer()

    def test_grid21(self):
        class MyRenderer(wx.grid.GridHeaderLabelsRenderer):
            def DrawBorder(self, grid, dc, rect):
                pass
            def DrawLabel(self, grid, dc, value, rect, horizAlign, vertAlign, textOrientation):
                pass
        r = MyRenderer()

    def test_grid22(self):
        class MyRenderer(wx.grid.GridRowHeaderRenderer):
            def DrawBorder(self, grid, dc, rect):
                pass
            def DrawLabel(self, grid, dc, value, rect, horizAlign, vertAlign, textOrientation):
                pass
        r = MyRenderer()

    def test_grid23(self):
        class MyRenderer(wx.grid.GridColumnHeaderRenderer):
            def DrawBorder(self, grid, dc, rect):
                pass
            def DrawLabel(self, grid, dc, value, rect, horizAlign, vertAlign, textOrientation):
                pass
        r = MyRenderer()

    def test_grid24(self):
        r = wx.grid.GridRowHeaderRendererDefault()

    def test_grid25(self):
        r = wx.grid.GridColumnHeaderRendererDefault()

    def test_grid26(self):
        r = wx.grid.GridCornerHeaderRendererDefault()



    def test_grid27(self):
        p = wx.grid.GridCellAttrProvider()

    def test_grid28(self):
        class MyTable(wx.grid.GridTableBase):
            def GetNumberRows(self): return 1
            def GetNumberCols(self): return 1
            def GetValue(self, row, col): return ""
            def SetValue(self, row, col, value): pass
        t = MyTable()


    def test_grid29(self):
        t = wx.grid.GridStringTable()

    def test_grid30(self):
        m = wx.grid.GridTableMessage()

    def test_grid31(self):
        m = wx.grid.GridSizesInfo()



    def test_grid32(self):
        g = wx.grid.Grid(self.frame)
        g.CreateGrid(10,5)



    def test_grid33(self):
        g = wx.grid.Grid(self.frame)
        g.CreateGrid(10,5)
        ul = wx.grid.GridUpdateLocker(g)
        g.SetCellValue(1,2, 'hello')
        g.SetCellValue((2,2), 'world')
        del ul

    def test_grid34(self):
        g = wx.grid.Grid(self.frame)
        g.CreateGrid(10,5)
        with wx.grid.GridUpdateLocker(g):
            g.SetCellValue(1,2, 'hello')
            g.SetCellValue((2,2), 'world')


    def test_grid35(self):
        e = wx.grid.GridEvent()

    def test_grid36(self):
        e = wx.grid.GridSizeEvent()

    def test_grid37(self):
        e = wx.grid.GridRangeSelectEvent()

    def test_grid38(self):
        e = wx.grid.GridEditorCreatedEvent()

    def test_grid39(self):
        wx.grid.wxEVT_GRID_CELL_LEFT_CLICK
        wx.grid.wxEVT_GRID_CELL_RIGHT_CLICK
        wx.grid.wxEVT_GRID_CELL_LEFT_DCLICK
        wx.grid.wxEVT_GRID_CELL_RIGHT_DCLICK
        wx.grid.wxEVT_GRID_LABEL_LEFT_CLICK
        wx.grid.wxEVT_GRID_LABEL_RIGHT_CLICK
        wx.grid.wxEVT_GRID_LABEL_LEFT_DCLICK
        wx.grid.wxEVT_GRID_LABEL_RIGHT_DCLICK
        wx.grid.wxEVT_GRID_ROW_SIZE
        wx.grid.wxEVT_GRID_COL_SIZE
        wx.grid.wxEVT_GRID_COL_AUTO_SIZE
        wx.grid.wxEVT_GRID_RANGE_SELECT
        wx.grid.wxEVT_GRID_RANGE_SELECTING
        wx.grid.wxEVT_GRID_RANGE_SELECTED
        wx.grid.wxEVT_GRID_CELL_CHANGING
        wx.grid.wxEVT_GRID_CELL_CHANGED
        wx.grid.wxEVT_GRID_SELECT_CELL
        wx.grid.wxEVT_GRID_EDITOR_SHOWN
        wx.grid.wxEVT_GRID_EDITOR_HIDDEN
        wx.grid.wxEVT_GRID_EDITOR_CREATED
        wx.grid.wxEVT_GRID_CELL_BEGIN_DRAG
        wx.grid.wxEVT_GRID_ROW_MOVE
        wx.grid.wxEVT_GRID_COL_MOVE
        wx.grid.wxEVT_GRID_COL_SORT
        wx.grid.wxEVT_GRID_TABBING

    def test_grid40(self):
        wx.grid.EVT_GRID_CELL_LEFT_CLICK
        wx.grid.EVT_GRID_CELL_RIGHT_CLICK
        wx.grid.EVT_GRID_CELL_LEFT_DCLICK
        wx.grid.EVT_GRID_CELL_RIGHT_DCLICK
        wx.grid.EVT_GRID_LABEL_LEFT_CLICK
        wx.grid.EVT_GRID_LABEL_RIGHT_CLICK
        wx.grid.EVT_GRID_LABEL_LEFT_DCLICK
        wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK
        wx.grid.EVT_GRID_ROW_SIZE
        wx.grid.EVT_GRID_COL_SIZE
        wx.grid.EVT_GRID_COL_AUTO_SIZE
        wx.grid.EVT_GRID_RANGE_SELECT
        wx.grid.EVT_GRID_RANGE_SELECTING
        wx.grid.EVT_GRID_RANGE_SELECTED
        wx.grid.EVT_GRID_CELL_CHANGING
        wx.grid.EVT_GRID_CELL_CHANGED
        wx.grid.EVT_GRID_SELECT_CELL
        wx.grid.EVT_GRID_EDITOR_SHOWN
        wx.grid.EVT_GRID_EDITOR_HIDDEN
        wx.grid.EVT_GRID_EDITOR_CREATED
        wx.grid.EVT_GRID_CELL_BEGIN_DRAG
        wx.grid.EVT_GRID_ROW_MOVE
        wx.grid.EVT_GRID_COL_MOVE
        wx.grid.EVT_GRID_COL_SORT
        wx.grid.EVT_GRID_TABBING

        wx.grid.EVT_GRID_CMD_CELL_LEFT_CLICK
        wx.grid.EVT_GRID_CMD_CELL_RIGHT_CLICK
        wx.grid.EVT_GRID_CMD_CELL_LEFT_DCLICK
        wx.grid.EVT_GRID_CMD_CELL_RIGHT_DCLICK
        wx.grid.EVT_GRID_CMD_LABEL_LEFT_CLICK
        wx.grid.EVT_GRID_CMD_LABEL_RIGHT_CLICK
        wx.grid.EVT_GRID_CMD_LABEL_LEFT_DCLICK
        wx.grid.EVT_GRID_CMD_LABEL_RIGHT_DCLICK
        wx.grid.EVT_GRID_CMD_ROW_SIZE
        wx.grid.EVT_GRID_CMD_COL_SIZE
        wx.grid.EVT_GRID_CMD_RANGE_SELECT
        wx.grid.EVT_GRID_CMD_CELL_CHANGING
        wx.grid.EVT_GRID_CMD_CELL_CHANGED
        wx.grid.EVT_GRID_CMD_SELECT_CELL
        wx.grid.EVT_GRID_CMD_EDITOR_SHOWN
        wx.grid.EVT_GRID_CMD_EDITOR_HIDDEN
        wx.grid.EVT_GRID_CMD_EDITOR_CREATED
        wx.grid.EVT_GRID_CMD_CELL_BEGIN_DRAG
        wx.grid.EVT_GRID_CMD_COL_MOVE
        wx.grid.EVT_GRID_CMD_COL_SORT
        wx.grid.EVT_GRID_CMD_TABBING


    def test_grid41(self):
        wx.grid.Grid.SetCellHighlightPenWidth  # Does it exist


    def test_grid43(self):
        # new names
        wx.grid.Grid.SelectCells
        wx.grid.Grid.SelectRows
        wx.grid.Grid.SelectColumns
        wx.grid.Grid.SelectRowsOrColumns


    def test_GetIM(self):
        # Test the immutable version returned by GetIM
        obj = wx.grid.GridCellCoords(1,2)
        im = obj.GetIM()
        assert isinstance(im, tuple)
        assert im.Row == obj.Row
        assert im.Col == obj.Col
        obj2 = wx.grid.GridCellCoords(im)
        assert obj == obj2


    def test_grid44(self):
        g = wx.grid.Grid(self.frame)
        g.CreateGrid(10,10)
        g.SelectBlock((1,1), (5,5))

        tl = g.GetSelectionBlockTopLeft()
        br = g.GetSelectionBlockBottomRight()

        assert tl[0].Get() == (1,1)
        assert br[0].Get() == (5,5)


    def test_grid45(self):
        # See issue #297
        g = wx.grid.Grid(self.frame)
        g.CreateGrid(10,10)
        g.SelectBlock((1,1), (5,5))

        tl = g.GetSelectionBlockTopLeft()[0]
        br = g.GetSelectionBlockBottomRight()[0]

        assert tl.Get() == (1,1)
        assert br.Get() == (5,5)

    def test_grid46(self):
        g = wx.grid.Grid(self.frame)
        g.CreateGrid(10,10)
        g.SelectBlock((1,1), (5,5))
        g.SelectBlock((6,5), (7,9), addToSelected=True)

        blocks = g.GetSelectedBlocks()
        assert isinstance(blocks, wx.grid.GridBlocks)

        count = 0
        for block in blocks:
            count += 1
            assert isinstance(block, wx.grid.GridBlockCoords)

        assert count == 2

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
