# -*- coding: utf-8 -*-
"""
wx.lib.plot
===========

This is a simple plotting library for the wxPython Phoenix project.

"""
__version__ = "0.0.1"
__updated__ = "2016-07-05"

# For those who still use ``from package import *`` for some reason
__all__ = [
    'PolyLine',
    'PolySpline',
    'PolyMarker',
    'PolyBars',
    'PolyHistogram',
    'BoxPlot',
    'PlotGraphics',
    'PlotCanvas',
    'PlotPrintout',
]

# Expose items so that the old API can still be used.
# Old: import wx.lib.plot as wxplot
# New: from wx.lib.plot import plot as wxplot
from .plot import (
    PolyPoints,
    PolyLine,
    PolySpline,
    PolyMarker,
    PolyBars,
    PolyHistogram,
    BoxPlot,
    PlotGraphics,
    PlotCanvas,
    PlotPrintout,
)
