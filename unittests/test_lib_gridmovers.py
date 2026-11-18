import unittest
from unittests import wtc
import wx
import wx.grid
import wx.lib.gridmovers as gridmovers

#---------------------------------------------------------------------------

class lib_gridmovers_Tests(wtc.WidgetTestCase):

    def makeGrid(self):
        grid = wx.grid.Grid(self.frame)
        grid.CreateGrid(5, 5)
        self.frame.SendSizeEvent()
        self.myYield()
        return grid

    def click(self, mover, labelWin, pos, ctrl=False):
        for evtType, handler in ((wx.wxEVT_LEFT_DOWN, mover.OnPress),
                                 (wx.wxEVT_LEFT_UP, mover.OnRelease)):
            evt = wx.MouseEvent(evtType)
            evt.SetPosition(pos)
            evt.SetControlDown(ctrl)
            evt.SetEventObject(labelWin)
            handler(evt)

    def colLabelPos(self, grid, col):
        rect = grid.CellToRect(0, col)
        return wx.Point(rect.x + rect.width // 2, grid.GetColLabelSize() // 2)

    def rowLabelPos(self, grid, row):
        rect = grid.CellToRect(row, 0)
        return wx.Point(grid.GetRowLabelSize() // 2, rect.y + rect.height // 2)

    def test_lib_gridmoversColClickSelects(self):
        grid = self.makeGrid()
        mover = gridmovers.GridColMover(grid)
        clicks = []
        grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK,
                  lambda evt: (clicks.append((evt.GetRow(), evt.GetCol())), evt.Skip()))
        children = len(grid.GetChildren())
        self.click(mover, grid.GetGridColLabelWindow(), self.colLabelPos(grid, 2))
        self.assertEqual(clicks, [(-1, 2)])
        self.assertEqual(list(grid.GetSelectedCols()), [2])
        # The drag window made for the click is gone again
        self.assertEqual(len(grid.GetChildren()), children)

    def test_lib_gridmoversRowClickHandled(self):
        # A handler that doesn't skip the label click keeps the row unselected
        grid = self.makeGrid()
        mover = gridmovers.GridRowMover(grid)
        clicks = []
        grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK,
                  lambda evt: clicks.append((evt.GetRow(), evt.GetCol())))
        self.click(mover, grid.GetGridRowLabelWindow(), self.rowLabelPos(grid, 3))
        self.assertEqual(clicks, [(3, -1)])
        self.assertEqual(list(grid.GetSelectedRows()), [])

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
