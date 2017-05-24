#---------------------------------------------------------------------------
# Name:        wx/__init__.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

# Load the main version string into the package namespace
import wx.__version__
__version__ = wx.__version__.VERSION_STRING

# Ensure the sip module has been installed.  It should be there because of the
# dependency set in setup.py, but just in case it isn't this will result in a
# nice ImportError instead of a crash when wx.core tries to use it.
import sip

# Ensure it's a real module and not a namespace module due to just happening
# to have a 'sip' folder on the sys.path (such as in our source tree...)
assert hasattr(sip, '__file__'), "It appears that the sip module is not installed."


# Import all items from the core wxPython module so they appear in the wx
# package namespace.
from wx.core import *


# Clean up the package namespace
del core
del wx
del sip