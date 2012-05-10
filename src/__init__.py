#---------------------------------------------------------------------------
# Name:        wx/__init__.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

# Load the main version string into the package namespace
import __version__
__version__ = __version__.VERSION_STRING


# Import all items from the core wxPython modules so they appear in the wx
# package namespace.
from core import *

