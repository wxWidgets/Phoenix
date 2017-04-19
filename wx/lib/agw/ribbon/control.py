# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         control.py
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
`RibbonControl` serves as a base class for all controls which share the ribbon
charactertics of having a ribbon art provider, and (optionally) non-continous
resizing.


Description
===========

Despite what the name may imply, it is not the top-level control for creating a
ribbon interface - that is :class:`~wx.lib.agw.ribbon.bar.RibbonBar`. Ribbon controls often have a region which
is "transparent", and shows the contents of the ribbon page or panel behind it.

If implementing a new ribbon control, then it may be useful to realise that this
effect is done by the art provider when painting the background of the control,
and hence in the paint handler for the new control, you should call a draw background
method on the art provider (:meth:`RibbonMSWArtProvider.DrawButtonBarBackground() <lib.agw.ribbon.art_msw.RibbonMSWArtProvider.DrawButtonBarBackground>` and
:meth:`RibbonMSWArtProvider.DrawToolBarBackground() <lib.agw.ribbon.art_msw.RibbonMSWArtProvider.DrawToolBarBackground>` typically just redraw what is behind the
rectangle being painted) if you want transparent regions.

"""

import wx

class RibbonControl(wx.Control):
    """ Base class for all the Ribbon stuff. """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 validator=wx.DefaultValidator, name="RibbonControl"):
        """
        Default class constructor.

        :param wx.Window `parent`: pointer to a parent window;
        :param integer `id`: window identifier. If ``wx.ID_ANY``, will automatically create
         an identifier;
        :param `pos`: window position. ``wx.DefaultPosition`` indicates that wxPython
         should generate a default position for the window;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: window size. ``wx.DefaultSize`` indicates that wxPython should
         generate a default size for the window. If no suitable size can be found, the
         window will be sized to 20x20 pixels so that the window is visible but obviously
         not correctly sized;
        :type `size`: tuple or :class:`wx.Point`
        :param integer `style`: the window style;
        :param wx.Validator `validator`: window validator;
        :param string `name`: window name.
        """

        wx.Control.__init__(self, parent, id, pos, size, style, validator, name)
        self._art = None

        if isinstance(parent, RibbonControl):
            self._art = parent.GetArtProvider()


    def SetArtProvider(self, art):
        """
        Set the art provider to be used.

        In many cases, setting the art provider will also set the art provider on all
        child windows which extend :class:`RibbonControl`. In most cases, controls will not
        take ownership of the given pointer, with the notable exception being
        :meth:`RibbonBar.SetArtProvider() <lib.agw.ribbon.bar.RibbonBar.SetArtProvider>`.

        :param `art`: an art provider.
        """

        self._art = art


    def GetArtProvider(self):
        """
        Get the art provider to be used.

        Note that until an art provider has been set in some way, this function may
        return ``None``.
        """

        return self._art


    def IsSizingContinuous(self):
        """
        Returns ``True`` if this window can take any size (greater than its minimum size),
        ``False`` if it can only take certain sizes.

        :see: :meth:`~RibbonControl.GetNextSmallerSize`, :meth:`~RibbonControl.GetNextLargerSize`
        """

        return True


    def DoGetNextSmallerSize(self, direction, size):
        """
        Implementation of :meth:`~RibbonControl.GetNextSmallerSize`.

        Controls which have non-continuous sizing must override this virtual function
        rather than :meth:`~RibbonControl.GetNextSmallerSize`.

        :param integer `direction`: the direction(s) in which the size should increase;
        :param wx.Size `size`: the size for which a larger size should be found.
        """

        # Dummy implementation for code which doesn't check for IsSizingContinuous() == true
        minimum = self.GetMinSize()

        if direction & wx.HORIZONTAL and size.x > minimum.x:
            size.x -= 1
        if direction & wx.VERTICAL and size.y > minimum.y:
            size.y -= 1

        return size


    def DoGetNextLargerSize(self, direction, size):
        """
        Implementation of :meth:`~RibbonControl.GetNextLargerSize`.

        Controls which have non-continuous sizing must override this virtual function
        rather than :meth:`~RibbonControl.GetNextLargerSize`.

        :param integer `direction`: the direction(s) in which the size should increase;
        :param wx.Size `size`: the size for which a larger size should be found.
        """

        # Dummy implementation for code which doesn't check for IsSizingContinuous() == true
        if direction & wx.HORIZONTAL:
            size.x += 1
        if direction & wx.VERTICAL:
            size.y += 1

        return size


    def GetNextSmallerSize(self, direction, relative_to=None):
        """
        If sizing is not continuous, then return a suitable size for the control which
        is smaller than the given size.

        :param integer `direction`: The direction(s) in which the size should reduce;
        :param wx.Size `relative_to`: The size for which a smaller size should be found.

        :returns: if there is no smaller size, otherwise a suitable size which is smaller
         in the given direction(s), and the same as in the other direction (if any).

        :see: :meth:`~RibbonControl.IsSizingContinuous`, :meth:`~RibbonControl.DoGetNextSmallerSize`
        """

        if relative_to is not None:
            return self.DoGetNextSmallerSize(direction, relative_to)

        return self.DoGetNextSmallerSize(direction, self.GetSize())


    def GetNextLargerSize(self, direction, relative_to=None):
        """
        If sizing is not continuous, then return a suitable size for the control which
        is larger then the given size.

        :param integer `direction`: The direction(s) in which the size should reduce;
        :param wx.Size `relative_to`: The size for which a smaller size should be found.

        :returns: if there is no larger size, otherwise a suitable size which is larger
         in the given direction(s), and the same as in the other direction (if any).

        :see: :meth:`~RibbonControl.IsSizingContinuous`, :meth:`~RibbonControl.DoGetNextLargerSize`
        """

        if relative_to is not None:
            return self.DoGetNextLargerSize(direction, relative_to)

        return self.DoGetNextLargerSize(direction, self.GetSize())


    def Realize(self):
        """
        Perform initial size and layout calculations after children have been added,
        and/or realize children.
        """

        pass


    def Realise(self):
        """
        Alias for :meth:`~RibbonControl.Realize`.
        """

        pass



