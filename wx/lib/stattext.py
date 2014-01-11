#----------------------------------------------------------------------
# Name:        wx.lib.stattext
# Purpose:     A generic wxGenStaticText class.  Using this should
#              eliminate some of the platform differences in wxStaticText,
#              such as background colours and mouse sensitivity.
#
# Author:      Robin Dunn
#
# Created:     8-July-2002
# Copyright:   (c) 2002 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port, unittest, documented
#----------------------------------------------------------------------
# 12/12/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 compatability update.
# o Untested.
#

"""
:class:`GenStaticText` is a generic implementation of :class:`StaticText`.


Description
===========

:class:`GenStaticText` is a generic implementation of :class:`StaticText`.

Some of the platforms supported by wxPython (most notably GTK), do not consider
:class:`StaticText` as a separate widget; instead, the label is just drawn on its
parent window. This essentially bars the use of almost all mouse events (such as
detection of mouse motions, mouse clicks and so on).

Moreover, these platforms do not allow the developer to change the widget's background
colour.

Using :class:`GenStaticText` will overcome all the problems described above, as it
is a generic widget and a real window on its own.


Usage
=====

Sample usage::

    import wx
    import wx.lib.stattext as ST

    app = wx.App(0)

    frame = wx.Frame(None, -1, "wx.lib.stattext Test")
    panel = wx.Panel(frame)    

    st1 = ST.GenStaticText(panel, -1, "This is an example of static text", (20, 10))

    st2 = ST.GenStaticText(panel, -1, "Is this yellow?", (20, 70), (120, -1))
    st2.SetBackgroundColour('Yellow')

    ST.GenStaticText(panel, -1, "align center", (160, 70), (120, -1), wx.ALIGN_CENTER)
    ST.GenStaticText(panel, -1, "align right", (300, 70), (120, -1), wx.ALIGN_RIGHT)

    frame.Show()
    app.MainLoop()
    

"""

import wx

BUFFERED = 0   # In unbuffered mode we can let the theme shine through,
               # otherwise we draw the background ourselves.

if wx.Platform == "__WXMAC__":
    try:
        from Carbon.Appearance import kThemeBrushDialogBackgroundActive
    except ImportError:
        kThemeBrushDialogBackgroundActive = 1
        
#----------------------------------------------------------------------

class GenStaticText(wx.Control):
    """ :class:`GenStaticText` is a generic implementation of :class:`StaticText`. """
    labelDelta = 1

    def __init__(self, parent, ID=-1, label="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0,
                 name="genstattext"):
        """
        Default class constructor.

        :param `parent`: parent window, must not be ``None``;
        :param integer `ID`: window identifier. A value of -1 indicates a default value;
        :param string `label`: the static text label (i.e., its text label);
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param integer `style`: the underlying :class:`Control` style;
        :param string `name`: the widget name.

        :type parent: :class:`Window`
        :type pos: tuple or :class:`Point`
        :type size: tuple or :class:`Size`
        """

        wx.Control.__init__(self, parent, ID, pos, size, style|wx.NO_BORDER,
                             wx.DefaultValidator, name)

        wx.Control.SetLabel(self, label) # don't check wx.ST_NO_AUTORESIZE yet
        self.InheritAttributes()
        self.SetInitialSize(size)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        if BUFFERED:
            self.defBackClr = self.GetBackgroundColour()
            self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        else:
            self.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
            


    def SetLabel(self, label):
        """
        Sets the static text label and updates the control's size to exactly
        fit the label unless the control has wx.ST_NO_AUTORESIZE flag.

        :param string `label`: the static text label (i.e., its text label).
        """
        
        wx.Control.SetLabel(self, label)
        style = self.GetWindowStyleFlag()
        self.InvalidateBestSize()
        if not style & wx.ST_NO_AUTORESIZE:
            self.SetSize(self.GetBestSize())
        self.Refresh()


    def SetFont(self, font):
        """
        Sets the static text font and updates the control's size to exactly
        fit the label unless the control has wx.ST_NO_AUTORESIZE flag.

        :param Font `font`: a valid font instance, which will be the new font used
         to display the text.
        """
        
        wx.Control.SetFont(self, font)
        style = self.GetWindowStyleFlag()
        self.InvalidateBestSize()
        if not style & wx.ST_NO_AUTORESIZE:
            self.SetSize(self.GetBestSize())
        self.Refresh()


    def DoGetBestSize(self):
        """
        Overridden base class virtual.  Determines the best size of
        the control based on the label size and the current font.

        .. note:: Overridden from :class:`Control`.
        """
        
        label = self.GetLabel()
        font = self.GetFont()
        if not font:
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        dc = wx.ClientDC(self)
        dc.SetFont(font)
        
        maxWidth = totalHeight = 0
        for line in label.split('\n'):
            if line == '':
                w, h = dc.GetTextExtent('W')  # empty lines have height too
            else:
                w, h = dc.GetTextExtent(line)
            totalHeight += h
            maxWidth = max(maxWidth, w)
        best = wx.Size(maxWidth, totalHeight)
        self.CacheBestSize(best)
        return best


    def Enable(self, enable=True):
        """
        Enable or disable the widget for user input. 

        :param bool `enable`: If ``True``, enables the window for input. If ``False``, disables the window.

        :returns: ``True`` if the window has been enabled or disabled, ``False`` if nothing was
         done, i.e. if the window had already been in the specified state.

        .. note:: Note that when a parent window is disabled, all of its children are disabled as
           well and they are reenabled again when the parent is.

        .. note:: Overridden from :class:`Control`.
        """

        retVal = wx.Control.Enable(self, enable)
        self.Refresh()

        return retVal
    

    def Disable(self):
        """
        Disables the control.

        :returns: ``True`` if the window has been disabled, ``False`` if it had been
         already disabled before the call to this function.
         
        .. note:: This is functionally equivalent of calling :meth:`~Control.Enable` with a ``False`` flag.

        .. note:: Overridden from :class:`Control`.
        """

        retVal = wx.Control.Disable(self)
        self.Refresh()

        return retVal


    def AcceptsFocus(self):
        """
        Can this window be given focus by mouse click?

        .. note:: Overridden from :class:`Control`.
        """

        return False


    def GetDefaultAttributes(self):
        """
        Overridden base class virtual.  By default we should use
        the same font/colour attributes as the native :class:`StaticText`.

        .. note:: Overridden from :class:`Control`.
        """
        
        return wx.StaticText.GetClassDefaultAttributes()


    def ShouldInheritColours(self):
        """
        Overridden base class virtual.  If the parent has non-default
        colours then we want this control to inherit them.

        .. note:: Overridden from :class:`Control`.
        """

        return True

    
    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` for :class:`GenStaticText`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """
        
        if BUFFERED:
            dc = wx.BufferedPaintDC(self)
        else:
            dc = wx.PaintDC(self)
        width, height = self.GetClientSize()
        if not width or not height:
            return

        if BUFFERED:
            clr = self.GetBackgroundColour()
            if wx.Platform == "__WXMAC__" and clr == self.defBackClr:
                # if colour is still the default then use the theme's  background on Mac
                themeColour = wx.MacThemeColour(kThemeBrushDialogBackgroundActive)
                backBrush = wx.Brush(themeColour)
            else:
                backBrush = wx.Brush(clr, wx.BRUSHSTYLE_SOLID)
            dc.SetBackground(backBrush)
            dc.Clear()

        if self.IsEnabled():
            dc.SetTextForeground(self.GetForegroundColour())
        else:
            dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
            
        dc.SetFont(self.GetFont())
        label = self.GetLabel()
        style = self.GetWindowStyleFlag()
        x = y = 0
        for line in label.split('\n'):
            if line == '':
                w, h = self.GetTextExtent('W')  # empty lines have height too
            else:
                w, h = self.GetTextExtent(line)
            if style & wx.ALIGN_RIGHT:
                x = width - w
            if style & wx.ALIGN_CENTER:
                x = (width - w)/2
            dc.DrawText(line, x, y)
            y += h


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`GenStaticText`.

        :param `event`: a :class:`EraseEvent` event to be processed.

        .. note:: This is intentionally empty to reduce flicker.
        """

        pass


#----------------------------------------------------------------------

