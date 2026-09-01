#---------------------------------------------------------------------------
# Name:        wx/__init__.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

# Load the main version string into the package namespace
import wx.__version__
__version__ = wx.__version__.VERSION_STRING

import os


# Select platform backend
__plat__ = '@DEFAULT@'
if 'WX_API' in os.environ:
    __plat__ = os.environ['WX_API']
    if __plat__ not in ['@PLATS@']:
        raise ImportError(f'invalid WX_API {__plat__}')


# Import all items from the core wxPython module so they appear in the wx
# package namespace.
from wx.core import *


# Clean up the package namespace
del core
del wx
