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


class lib_plot_Tests(wtc.WidgetTestCase):
    def test_lib_plot_tempstyle_contextmanager(self):
        pass

    def test_lib_plot_tempstyle_decorator(self):
        pass

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
