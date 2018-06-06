#---------------------------------------------------------------------------
# Name:        wx/gizmos.py
# Author:      Robin Dunn
#
# Created:     27-Oct-2017
# Copyright:   (c) 2017-2018 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

# This is just a compatibility shim to make the gizmos classes usable from
# the wx.gizmos module, like in Classic.  They're actually in the wx.lib.gizmos
# package now.
#
# This module is deprecated and could be removed some time in the future. Please
# switch your imports to wx.lib.gizmos

from wx.lib.gizmos import *

