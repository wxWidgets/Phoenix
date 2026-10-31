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


class lib_plot_Tests(wtc.WidgetTestCase):
    def test_lib_plot_tempstyle_contextmanager(self):
        pass

    def test_lib_plot_tempstyle_decorator(self):
        pass

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
