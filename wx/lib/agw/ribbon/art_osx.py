# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         art_msw.py
# Purpose:
#
# Author:       Andrea Gavana <andrea.gavana@gmail.com>
#
# Created:
# Version:
# Date:        
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, documented, py3-port
#----------------------------------------------------------------------------
"""
`art_osx` is responsible for drawing all the components of the ribbon
interface using an AUI-compatible appearance on Mac, because as of now there is no
customized version of the ribbon art provider to provide a more or less native look
on the Mac platform.


Description
===========

This allows a ribbon bar to have a pluggable look-and-feel, while retaining the same
underlying behaviour. As a single art provider is used for all ribbon components, a
ribbon bar usually has a consistent (though unique) appearance.

By default, a :class:`~lib.agw.ribbon.bar.RibbonBar` uses an instance of a class called
:class:`~lib.agw.ribbon.art_default.RibbonDefaultArtProvider`,
which resolves to :class:`~lib.agw.ribbon.art_aui.RibbonAUIArtProvider`,
:class:`~lib.agw.ribbon.art_msw.RibbonMSWArtProvider`, or
:class:`~lib.agw.ribbon.art_osx.RibbonOSXArtProvider` - whichever is most appropriate
to the current platform. These art providers are all
slightly configurable with regard to colours and fonts, but for larger modifications,
you can derive from one of these classes, or write a completely new art provider class.

Call :meth:`RibbonBar.SetArtProvider() <lib.agw.ribbon.bar.RibbonBar.SetArtProvider>` to change the art provider being used.


See Also
========

:class:`~lib.agw.ribbon.bar.RibbonBar`
"""

import wx
from .art_aui import RibbonAUIArtProvider

class RibbonOSXArtProvider(RibbonAUIArtProvider):

    pass

