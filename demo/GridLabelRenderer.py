#!/usr/bin/env python

import wx
import wx.grid as grid
import wx.lib.mixins.gridlabelrenderer as glr

#----------------------------------------------------------------------

class MyGrid(grid.Grid, glr.GridWithLabelRenderersMixin):
    def __init__(self, *args, **kw):
        grid.Grid.__init__(self, *args, **kw)
        glr.GridWithLabelRenderersMixin.__init__(self)


class MyRowLabelRenderer(glr.GridLabelRenderer):
    def __init__(self, bgcolor):
        self._bgcolor = bgcolor

    def Draw(self, grid, dc, rect, row):
        dc.SetBrush(wx.Brush(self._bgcolor))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(rect)
        hAlign, vAlign = grid.GetRowLabelAlignment()
        text = grid.GetRowLabelValue(row)
        self.DrawBorder(grid, dc, rect)
        self.DrawText(grid, dc, rect, text, hAlign, vAlign)


class MyColLabelRenderer(glr.GridLabelRenderer):
    def __init__(self, bgcolor):
        self._bgcolor = bgcolor

    def Draw(self, grid, dc, rect, col):
        dc.SetBrush(wx.Brush(self._bgcolor))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(rect)
        hAlign, vAlign = grid.GetColLabelAlignment()
        text = grid.GetColLabelValue(col)
        self.DrawBorder(grid, dc, rect)
        self.DrawText(grid, dc, rect, text, hAlign, vAlign)


class MyCornerLabelRenderer(glr.GridLabelRenderer):
    def __init__(self):
        import images
        self._bmp = images.Smiles.GetBitmap()

    def Draw(self, grid, dc, rect, rc):
        x = rect.left + (rect.width - self._bmp.GetWidth()) // 2
        y = rect.top + (rect.height - self._bmp.GetHeight()) // 2
        dc.DrawBitmap(self._bmp, x, y, True)



class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        ROWS = 27
        COLS = 15

        g = MyGrid(self, size=(100,100))
        g.CreateGrid(ROWS, COLS)

        g.SetCornerLabelRenderer(MyCornerLabelRenderer())

        for row in range(0, ROWS, 3):
            g.SetRowLabelRenderer(row+0, MyRowLabelRenderer('#ffe0e0'))
            g.SetRowLabelRenderer(row+1, MyRowLabelRenderer('#e0ffe0'))
            g.SetRowLabelRenderer(row+2, MyRowLabelRenderer('#e0e0ff'))

        for col in range(0, COLS, 3):
            g.SetColLabelRenderer(col+0, MyColLabelRenderer('#e0ffe0'))
            g.SetColLabelRenderer(col+1, MyColLabelRenderer('#e0e0ff'))
            g.SetColLabelRenderer(col+2, MyColLabelRenderer('#ffe0e0'))

        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(g, 1, wx.EXPAND)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>GridLabelRenderer</h2>

The <tt>wx.lib.mixins.gridlabelrenderer</tt> module provides a mixin
class for wx.grid.Grid that enables it to have plugin renderers that
work like the normal cell renderers do.  If desired you can specify a
different renderer for each row or col label, and even for the little
corner label in the upper left corner of the grid.  When each of those
labels needs to be drawn the mixin calls the render's Draw method with
the dc and rectangle, allowing your renderer class to do just about
anything that it wants.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

