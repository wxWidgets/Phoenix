import collections
import unittest
from unittests import wtc
import wx
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr

#---------------------------------------------------------------------------

class Grid(wx.grid.Grid, glr.GridWithLabelRenderersMixin):
    """A grid that notes which paint handler is running"""
    def __init__(self, *args, **kw):
        wx.grid.Grid.__init__(self, *args, **kw)
        glr.GridWithLabelRenderersMixin.__init__(self)
        self.painting = None

    def _noting(name):
        def handler(self, evt):
            self.painting = name
            try:
                getattr(glr.GridWithLabelRenderersMixin, '_onPaint' + name)(self, evt)
            finally:
                self.painting = None
        return handler

    _onPaintRowLabels = _noting('RowLabels')
    _onPaintColLabels = _noting('ColLabels')
    _onPaintFrozenRowLabels = _noting('FrozenRowLabels')
    _onPaintFrozenColLabels = _noting('FrozenColLabels')


class RecordingRenderer(glr.GridLabelRenderer):
    """Records which labels were drawn by which paint handler"""
    def __init__(self):
        self.drawn = collections.defaultdict(collections.Counter)

    def Draw(self, grid, dc, rect, rowOrCol):
        self.drawn[grid.painting][rowOrCol] += 1

#---------------------------------------------------------------------------

class GridWithLabelRenderersMixin_Tests(wtc.WidgetTestCase):

    def makeGrid(self):
        g = Grid(self.frame)
        g.CreateGrid(6, 6)
        self.frame.SendSizeEvent()
        self.myYield()
        return g

    def freezeTo(self, grid, rows, cols):
        assert grid.FreezeTo(rows, cols)
        self.frame.SendSizeEvent()
        self.myYield()

    def repaint(self, window, renderer, handler):
        """
        Repaint the window in a main loop, as it is not painted in the
        loop made by myYield. Return what the paint handler drew.
        """
        renderer.drawn.clear()
        window.Refresh()
        wx.CallLater(200, self.app.ExitMainLoop)
        self.app.MainLoop()
        return renderer.drawn[handler]

    def test_scrolledColLabelsUseRenderer(self):
        g = self.makeGrid()
        r = RecordingRenderer()
        g.SetDefaultColLabelRenderer(r)
        drawn = self.repaint(g.GetGridColLabelWindow(), r, 'ColLabels')
        assert {0, 1} <= set(drawn)

    def test_frozenColLabelsUseRenderer(self):
        g = self.makeGrid()
        r = RecordingRenderer()
        g.SetDefaultColLabelRenderer(r)
        self.freezeTo(g, 0, 2)
        drawn = self.repaint(g.GetFrozenColLabelWindow(), r, 'FrozenColLabels')
        assert set(drawn) == {0, 1}, dict(drawn)

    def test_frozenRowLabelsUseRenderer(self):
        g = self.makeGrid()
        r = RecordingRenderer()
        g.SetDefaultRowLabelRenderer(r)
        self.freezeTo(g, 2, 0)
        drawn = self.repaint(g.GetFrozenRowLabelWindow(), r, 'FrozenRowLabels')
        assert set(drawn) == {0, 1}, dict(drawn)

    def isBoundOnce(self, window, handler):
        # Unbind returns whether the handler was bound
        return window.Unbind(wx.EVT_PAINT, handler=handler) and \
               not window.Unbind(wx.EVT_PAINT, handler=handler)

    def test_freezeAgainBindsOnce(self):
        g = self.makeGrid()
        for cols in (2, 3, 2):
            self.freezeTo(g, 0, cols)
        assert self.isBoundOnce(g.GetFrozenColLabelWindow(), g._onPaintFrozenColLabels)

    def test_unfreezeAndFreeze(self):
        g = self.makeGrid()
        for rows, cols in ((1, 2), (0, 0), (0, 1)):
            self.freezeTo(g, rows, cols)
        assert g.GetFrozenRowLabelWindow() is None
        assert self.isBoundOnce(g.GetFrozenColLabelWindow(), g._onPaintFrozenColLabels)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
