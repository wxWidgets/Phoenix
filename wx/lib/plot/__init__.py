# -*- coding: utf-8 -*-
# pylint: disable=C0413
#   C0413: Import should be placed at the top of the module
"""
A simple plotting library for the wxPython Phoenix project.

"""
__version__ = "0.0.1"
__updated__ = "2016-07-05"
__docformat__ = "restructuredtext en"

# For those who still use ``from package import *`` for some reason
__all__ = [
    'PolyLine',
    'PolySpline',
    'PolyMarker',
    'PolyBars',
    'PolyHistogram',
    'BoxPlot',
    'PolyBoxPlot',
    'PlotGraphics',
    'PlotCanvas',
    'PlotPrintout',
]

# Expose items so that the old API can still be used.
# Old: import wx.lib.plot as wxplot
# New: from wx.lib import plot as wxplot
from .plotcanvas import PlotCanvas

from .polyobjects import PolyPoints
from .polyobjects import PolyLine
from .polyobjects import PolySpline
from .polyobjects import PolyMarker
from .polyobjects import PolyBars
from .polyobjects import PolyHistogram
from .polyobjects import PolyBoxPlot
from .polyobjects import PlotGraphics
from .polyobjects import PlotPrintout

from .utils import TempStyle
from .utils import pendingDeprecation

# For backwards compat.
BoxPlot = PolyBoxPlot
