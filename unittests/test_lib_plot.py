# -*- coding: utf-8 -*-
import unittest
from unittests import wtc
import wx

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


class lib_plot_Tests(wtc.WidgetTestCase):
    def test_lib_plot_tempstyle_contextmanager(self):
        pass

    def test_lib_plot_tempstyle_decorator(self):
        pass

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
