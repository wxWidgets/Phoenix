# -*- coding: utf-8 -*-
import unittest
from unittests import wtc
import wx
import numpy as np

import wx.lib.plot as wxplot

#---------------------------------------------------------------------------

class lib_plot_PlotCanvas_Tests(wtc.WidgetTestCase):

    def test_lib_plot_plotcanvasCtor(self):
        """ Ctor? """
        p = wxplot.PlotCanvas(self.frame)

    def test_lib_plot_plotcanvasBarsLegend(self):
        p = wxplot.PlotCanvas(self.frame, size=(400, 300))
        p.enableLegend = True
        hist = wxplot.PolyHistogram([2, 3, 4], [0, 1, 2, 3], legend='Histogram')
        bars = wxplot.PolyBars([(1, 2), (2, 3)], legend='Bars')
        p.Draw(wxplot.PlotGraphics([hist, bars]))

    def test_lib_plot_plotcanvasAxisSpec(self):
        p = wxplot.PlotCanvas(self.frame, size=(400, 300))
        line = wxplot.PolyLine([(0, 0), (1, 2), (2, 1)])
        for attr in ('xSpec', 'ySpec'):
            for value in ('none', 'min', 'auto', 5, 2.5, (0, 3)):
                setattr(p, attr, value)
                assert getattr(p, attr) == value

            setattr(p, attr, [-1, 4])
            assert getattr(p, attr) == (-1, 4)
            p.Draw(wxplot.PlotGraphics([line]))

            for value in ('bogus', None, (0, 1, 2), [0]):
                with self.assertRaises(TypeError):
                    setattr(p, attr, value)
            assert getattr(p, attr) == (-1, 4)

    def test_lib_plot_pointLabelAfterRedraw(self):
        p = wxplot.PlotCanvas(self.frame, size=(400, 300))
        p.enablePointLabel = True
        drawn = []
        p.pointLabelFunc = lambda dc, mDataDict: drawn.append(mDataDict['pointXY'])
        p.Draw(wxplot.PlotGraphics([wxplot.PolyLine([(0, 0), (1, 1), (2, 0)])]))
        p.UpdatePointLabel({'pointXY': (0, 0)})
        # Redrawing (e.g. while dragging) wipes the label from the buffer, so
        # the next update must not draw the old label again to "erase" it.
        p.Redraw()
        drawn.clear()
        p.UpdatePointLabel({'pointXY': (1, 1)})
        self.assertEqual(drawn, [(1, 1)])

    def test_lib_plot_zoomRubberBand(self):
        p = wxplot.PlotCanvas(self.frame, size=(400, 300))
        p.Draw(wxplot.PlotGraphics([wxplot.PolyLine([(0, 0), (1, 1), (2, 0)])]))
        self.myYield()
        before = p._Buffer.ConvertToImage().GetData()
        p._drawRubberBand((0.5, 0.2), (1.5, 0.8))
        self.assertTrue(p._rubberBand.width > 0 and p._rubberBand.height > 0)
        self.myYield()
        # The box is drawn over the plot on screen, never into the buffer
        self.assertEqual(p._Buffer.ConvertToImage().GetData(), before)
        p._clearRubberBand()
        self.assertIsNone(p._rubberBand)


class RecordingDC:
    """Records the lines a PolyLine draws, as (x1, y1, x2, y2) tuples."""

    def __init__(self, box):
        self.box = box
        self.lines = []

    def SetPen(self, pen):
        pass

    def GetClippingBox(self):
        return (True,) + self.box

    def DrawLineList(self, lines):
        self.lines.extend(tuple(line) for line in np.asarray(lines).tolist())

    def DrawLines(self, points):
        points = [tuple(p) for p in points]
        self.lines.extend(p1 + p2 for p1, p2 in zip(points, points[1:]))


class lib_plot_PolyLine_Tests(wtc.WidgetTestCase):

    def drawLine(self, points, box):
        line = wxplot.PolyLine(points)
        line._pointSize = (1, 1)
        dc = RecordingDC(box)
        line.draw(dc, 1)
        return dc.lines

    def test_lib_plot_polyLineSameColumn(self):
        x = np.repeat(np.arange(20), 50)
        y = np.random.default_rng(0).integers(0, 100, len(x))
        lines = self.drawLine(np.column_stack((x, y)).astype(float), (0, 0, 400, 300))
        self.assertLess(len(lines), 4 * 20)
        for col in range(20):
            ys = y[x == col]
            covered = set()
            for x1, y1, x2, y2 in lines:
                if x1 == x2 == col:
                    covered.update(range(min(y1, y2), max(y1, y2) + 1))
            self.assertEqual(covered, set(range(ys.min(), ys.max() + 1)))
        between = {(x[i], y[i], x[i + 1], y[i + 1]) for i in range(len(x) - 1) if x[i] != x[i + 1]}
        self.assertEqual({line for line in lines if line[0] != line[2]}, between)

    def test_lib_plot_polyLineOutsideClipping(self):
        x = np.arange(-500, 1500)
        y = (50 + 40 * np.sin(x / 10)).astype(int)
        lines = self.drawLine(np.column_stack((x, y)).astype(float), (100, 0, 200, 100))
        visible = {(x[i], y[i], x[i + 1], y[i + 1]) for i in range(len(x) - 1) if 100 <= x[i] < 300}
        self.assertTrue(visible <= set(lines))
        self.assertLess(len(lines), 220)


class lib_plot_Tests(wtc.WidgetTestCase):
    def test_lib_plot_tempstyle_contextmanager(self):
        pass

    def test_lib_plot_tempstyle_decorator(self):
        pass

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
