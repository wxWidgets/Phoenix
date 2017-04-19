#----------------------------------------------------------------------------
# Name:         scrolledpanel.py
# Author:       Will Sadkin
# Created:      03/21/2003
# Copyright:    (c) 2003 by Will Sadkin
# License:      wxWindows license
# Tags:         phoenix-port
#----------------------------------------------------------------------------
# 12/11/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 compatibility update.
#
# 12/21/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o wxScrolledPanel -> ScrolledPanel
#
# 21 Dec 2012 - Andrea Gavana (andrea.gavana@gmail.com)
#
# Tags:        phoenix-port, unittest, documented
#

"""
:class:`~lib.scrolledpanel.ScrolledPanel` extends :class:`ScrolledWindow`, adding all
the necessary bits to set up scroll handling for you.

Description
===========

:class:`ScrolledPanel` fills a "hole" in the implementation of
:class:`ScrolledWindow`, providing automatic scrollbar and scrolling
behavior and the tab traversal management that :class:`ScrolledWindow`
lacks.  This code was based on the original demo code showing how
to do this, but is now available for general use as a proper class
(and the demo is now converted to just use it.)

It is assumed that the :class:`ScrolledPanel` will have a sizer, as it is
used to calculate the minimal virtual size of the panel and etc.

Usage
=====

Usage example::


    text = '''
    ScrolledPanel extends wx.ScrolledWindow, adding all
    the necessary bits to set up scroll handling for you.

    Here are three fixed size examples of its use. The
    demo panel for this sample is also using it -- the
    wx.StaticLine below is intentionally made too long so a scrollbar will be
    activated.'''

    import wx
    import wx.lib.scrolledpanel as scrolled

    class TestPanel(scrolled.ScrolledPanel):

        def __init__(self, parent):

            scrolled.ScrolledPanel.__init__(self, parent, -1)

            vbox = wx.BoxSizer(wx.VERTICAL)

            desc = wx.StaticText(self, -1, text)

            desc.SetForegroundColour("Blue")
            vbox.Add(desc, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            vbox.Add(wx.StaticLine(self, -1, size=(1024, -1)), 0, wx.ALL, 5)
            vbox.Add((20, 20))

            self.SetSizer(vbox)
            self.SetupScrolling()


    app = wx.App(0)
    frame = wx.Frame(None, wx.ID_ANY)
    fa = TestPanel(frame)
    frame.Show()
    app.MainLoop()

"""

import wx
import math

class ScrolledPanel(wx.ScrolledWindow):
    """
    :class:`ScrolledPanel` fills a "hole" in the implementation of
    :class:`ScrolledWindow`, providing automatic scrollbar and scrolling
    behavior and the tab traversal management that :class:`ScrolledWindow` lacks.
    """

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL,
                 name="scrolledpanel"):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `style`: the underlying :class:`wx.ScrolledWindow` style;
        :param string `name`: the scrolled panel name.
        """

        wx.ScrolledWindow.__init__(self, parent, id,
                                     pos=pos, size=size,
                                     style=style, name=name)
        self.scrollIntoView = True
        self.SetInitialSize(size)
        self.Bind(wx.EVT_CHILD_FOCUS, self.OnChildFocus)


    def SetupScrolling(self, scroll_x=True, scroll_y=True, rate_x=20, rate_y=20,
                       scrollToTop=True, scrollIntoView=True):
        """
        This function sets up the event handling necessary to handle
        scrolling properly. It should be called within the `__init__`
        function of any class that is derived from :class:`ScrolledPanel`,
        once the controls on the panel have been constructed and
        thus the size of the scrolling area can be determined.

        :param bool `scroll_x`: ``True`` to allow horizontal scrolling, ``False`` otherwise;
        :param bool `scroll_y`: ``True`` to allow vertical scrolling, ``False`` otherwise;
        :param int `rate_x`: the horizontal scroll increment;
        :param int `rate_y`: the vertical scroll increment;
        :param bool `scrollToTop`: ``True`` to scroll all way to the top, ``False`` otherwise;
        :param bool `scrollIntoView`: ``True`` to scroll a focused child into view, ``False`` otherwise.
        """

        self.scrollIntoView = scrollIntoView

        # The following is all that is needed to integrate the sizer and the scrolled window
        if not scroll_x: rate_x = 0
        if not scroll_y: rate_y = 0

        # Round up the virtual size to be a multiple of the scroll rate
        sizer = self.GetSizer()
        if sizer:
            w, h = sizer.GetMinSize()
            if rate_x:
                w += rate_x - (w % rate_x)
            if rate_y:
                h += rate_y - (h % rate_y)
            self.SetVirtualSize( (w, h) )
        self.SetScrollRate(rate_x, rate_y)
        wx.CallAfter(self._SetupAfter, scrollToTop) # scroll back to top after initial events


    def _SetupAfter(self, scrollToTop):
        self.SetVirtualSize(self.GetBestVirtualSize())
        if scrollToTop:
            self.Scroll(0,0)


    def OnChildFocus(self, evt):
        """
        If the child window that gets the focus is not fully visible,
        this handler will try to scroll enough to see it.

        :param `evt`: a :class:`ChildFocusEvent` event to be processed.
        """

        child = evt.GetWindow()
        if self.scrollIntoView:
            self.ScrollChildIntoView(child)
            evt.Skip()


    def ScrollChildIntoView(self, child):
        """
        Scroll the panel so that the specified child window is in view.

        :param wx.Window `child`: any :class:`wx.Window` - derived control.

        .. note:: This method looks redundant if `evt.Skip()` is
           called as well - the base :class:`ScrolledWindow` widget now seems
           to be doing the same thing anyway.

        """

        sppu_x, sppu_y = self.GetScrollPixelsPerUnit()
        vs_x, vs_y   = self.GetViewStart()
        cr = child.GetRect()
        clntsz = self.GetClientSize()
        new_vs_x, new_vs_y = -1, -1

        # is it before the left edge?
        if cr.x < 0 and sppu_x > 0:
            new_vs_x = vs_x + (cr.x / sppu_x)

        # is it above the top?
        if cr.y < 0 and sppu_y > 0:
            new_vs_y = vs_y + (cr.y / sppu_y)

        # For the right and bottom edges, scroll enough to show the
        # whole control if possible, but if not just scroll such that
        # the top/left edges are still visible

        # is it past the right edge ?
        if cr.right > clntsz.width and sppu_x > 0:
            diff = math.ceil(1.0 * (cr.right - clntsz.width + 1) / sppu_x)
            if cr.x - diff * sppu_x > 0:
                new_vs_x = vs_x + diff
            else:
                new_vs_x = vs_x + (cr.x / sppu_x)

        # is it below the bottom ?
        if cr.bottom > clntsz.height and sppu_y > 0:
            diff = math.ceil(1.0 * (cr.bottom - clntsz.height + 1) / sppu_y)
            if cr.y - diff * sppu_y > 0:
                new_vs_y = vs_y + diff
            else:
                new_vs_y = vs_y + (cr.y / sppu_y)

        # if we need to adjust
        if new_vs_x != -1 or new_vs_y != -1:
            #print("%s: (%s, %s)" % (self.GetName(), new_vs_x, new_vs_y))
            self.Scroll(new_vs_x, new_vs_y)
