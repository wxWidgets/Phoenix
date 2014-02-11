#---------------------------------------------------------------------------
# Name:        expando.py
# Purpose:     A multi-line text control that expands and collapses as more
#              or less lines are needed to display its content.
#
# Author:      Robin Dunn
#
# Created:     18-Sept-2006
# Copyright:   (c) 2006 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port, unittest, documented
#
#---------------------------------------------------------------------------

"""
This module contains the :class:`ExpandoTextCtrl`, which is a multi-line
text control that will expand its height on the fly to be able to show
all the lines of the content of the control.


Description
===========

The :class:`ExpandoTextCtrl` is a multi-line :class:`TextCtrl` that will
adjust its height on the fly as needed to accomodate the number of
lines needed to display the current content of the control.  It is
assumed that the width of the control will be a fixed value and
that only the height will be adjusted automatically.  If the
control is used in a sizer then the width should be set as part of
the initial or min size of the control.

When the control resizes itself it will attempt to also make
necessary adjustments in the sizer hierarchy it is a member of (if
any) but if that is not suffiecient then the programmer can catch
the EVT_ETC_LAYOUT_NEEDED event in the container and make any
other layout adjustments that may be needed.


Usage
=====

Sample usage::

    import wx
    from wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED

    class MyFrame(wx.Frame):

        def __init__(self):
        
            wx.Frame.__init__(self, None, title="Test ExpandoTextCtrl")
            self.pnl = p = wx.Panel(self)
            self.eom = ExpandoTextCtrl(p, size=(250,-1),
                                       value="This control will expand as you type")
            self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, self.eom)

            # create some buttons and sizers to use in testing some
            # features and also the layout
            vBtnSizer = wx.BoxSizer(wx.VERTICAL)

            btn = wx.Button(p, -1, "Write Text")
            self.Bind(wx.EVT_BUTTON, self.OnWriteText, btn)
            vBtnSizer.Add(btn, 0, wx.ALL|wx.EXPAND, 5)

            btn = wx.Button(p, -1, "Append Text")
            self.Bind(wx.EVT_BUTTON, self.OnAppendText, btn)
            vBtnSizer.Add(btn, 0, wx.ALL|wx.EXPAND, 5)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            col1 = wx.BoxSizer(wx.VERTICAL)
            col1.Add(self.eom, 0, wx.ALL, 10)
            sizer.Add(col1)
            sizer.Add(vBtnSizer)
            p.SetSizer(sizer)

            # Put the panel in a sizer for the frame so we can use self.Fit()
            frameSizer = wx.BoxSizer()
            frameSizer.Add(p, 1, wx.EXPAND)
            self.SetSizer(frameSizer)
            
            self.Fit()


        def OnRefit(self, evt):
            # The Expando control will redo the layout of the
            # sizer it belongs to, but sometimes this may not be
            # enough, so it will send us this event so we can do any
            # other layout adjustments needed.  In this case we'll
            # just resize the frame to fit the new needs of the sizer.
            self.Fit()

            
        def OnWriteText(self, evt):
            self.eom.WriteText("This is a test...  Only a test.  If this had "
                               "been a real emergency you would have seen the "
                               "quick brown fox jump over the lazy dog.")
        
        def OnAppendText(self, evt):
            self.eom.AppendText("Appended text.")

    app = wx.App(0)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()

"""

import wx
import wx.lib.newevent


# This event class and binder object can be used to catch
# notifications that the ExpandoTextCtrl has resized itself and
# that layout adjustments may need to be made.
wxEVT_ETC_LAYOUT_NEEDED = wx.NewEventType()
EVT_ETC_LAYOUT_NEEDED = wx.PyEventBinder(wxEVT_ETC_LAYOUT_NEEDED, 1)


#---------------------------------------------------------------------------

class ExpandoTextCtrl(wx.TextCtrl):
    """
    The ExpandoTextCtrl is a multi-line wx.TextCtrl that will
    adjust its height on the fly as needed to accomodate the number of
    lines needed to display the current content of the control.  It is
    assumed that the width of the control will be a fixed value and
    that only the height will be adjusted automatically.  If the
    control is used in a sizer then the width should be set as part of
    the initial or min size of the control.

    When the control resizes itself it will attempt to also make
    necessary adjustments in the sizer hierarchy it is a member of (if
    any) but if that is not suffiecient then the programmer can catch
    the EVT_ETC_LAYOUT_NEEDED event in the container and make any
    other layout adjustments that may be needed.
    """
    
    _defaultHeight = -1
    _leading = 1   # TODO: find a way to calculate this, it may vary by platform
    
    def __init__(self, parent, id=-1, value="",
                 pos=wx.DefaultPosition,  size=wx.DefaultSize,
                 style=0, validator=wx.DefaultValidator, name="expando"):
        """
        Default class constructor.

        :param `parent`: parent window, must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param string `value`: the control text label;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param integer `style`: the underlying :class:`Control` style;
        :param Validator `validator`: the window validator;
        :param string `name`: the widget name.

        :type parent: :class:`Window`
        :type pos: tuple or :class:`Point`
        :type size: tuple or :class:`Size`
        """

        # find the default height of a single line control
        self.defaultHeight = self._getDefaultHeight(parent)
        # make sure we default to that height if none was given
        w, h = size
        if h == -1:
            h = self.defaultHeight
        # always use the multi-line style
        style = style | wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_RICH2
        # init the base class
        wx.TextCtrl.__init__(self, parent, id, value, pos, (w, h),
                             style, validator, name)
        # save some basic metrics
        self.extraHeight = self.defaultHeight - self.GetCharHeight()
        self.numLines = 1
        self.maxHeight = -1
        if value:
            wx.CallAfter(self._adjustCtrl)
                        
        self.Bind(wx.EVT_TEXT, self.OnTextChanged)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def SetMaxHeight(self, h):
        """
        Sets the maximum height that the control will expand to on its
        own, and adjusts it down if needed.

        :param integer `h`: the maximum control height, in pixels.
        """

        self.maxHeight = h
        if h != -1 and self.GetSize().height > h:
            self.SetSize((-1, h))


    def GetMaxHeight(self):
        """
        Returns the maximum height that the control will expand to on its own.

        :rtype: int
        """
        
        return self.maxHeight


    def SetFont(self, font):
        """
        Sets the font for the :class:`ExpandoTextCtrl`.

        :param Font font: font to associate with the :class:`ExpandoTextCtrl`, pass
         ``NullFont`` to reset to the default font.

        :rtype: bool
        :returns: ``True`` if the font was really changed, ``False`` if it was already
         set to this font and nothing was done.
        """
        
        retVal = wx.TextCtrl.SetFont(self, font)
        self.numLines = -1
        self._adjustCtrl()

        return retVal
        

    def WriteText(self, text):
        """
        Writes the text into the text control at the current insertion position.

        :param string `text`: text to write to the text control.

        .. note::

           Newlines in the text string are the only control characters allowed, and they
           will cause appropriate line breaks. See :meth:`AppendText` for more convenient
           ways of writing to the window. After the write operation, the insertion point
           will be at the end of the inserted text, so subsequent write operations will
           be appended. To append text after the user may have interacted with the control,
           call :meth:`TextCtrl.SetInsertionPointEnd` before writing.
           
        """
        
        # work around a bug of a lack of a EVT_TEXT when calling
        # WriteText on wxMac
        wx.TextCtrl.WriteText(self, text)
        self._adjustCtrl()


    def AppendText(self, text):
        """
        Appends the text to the end of the text control.

        :param string `text`: text to write to the text control.

        .. seealso:: :meth:`WriteText`
        """
        
        # Instead of using wx.TextCtrl.AppendText append and set the
        # insertion point ourselves.  This works around a bug on wxMSW
        # where it scrolls the old text out of view, and since there
        # is no scrollbar there is no way to get back to it.
        self.SetValue(self.GetValue() + text)
        self.SetInsertionPointEnd()


    def OnTextChanged(self, evt):
        """
        Handles the ``wx.EVT_TEXT`` event for :class:`ExpandoTextCtrl`.

        :param `event`: a :class:`CommandEvent` event to be processed.
        """

        # check if any adjustments are needed on every text update
        self._adjustCtrl()
        evt.Skip()
        

    def OnSize(self, evt):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`ExpandoTextCtrl`.

        :param `event`: a :class:`SizeEvent` event to be processed.
        """

        # The number of lines needed can change when the ctrl is resized too.
        self._adjustCtrl()
        evt.Skip()


    def _adjustCtrl(self):
        # if the current number of lines is different than before
        # then recalculate the size needed and readjust
        numLines = self.GetNumberOfLines()
        if numLines != self.numLines:
            self.numLines = numLines
            charHeight = self.GetCharHeight()
            height = numLines * (charHeight+self._leading) + self.extraHeight
            if not (self.maxHeight != -1 and height > self.maxHeight):
                # The size is changing...  if the control is not in a
                # sizer then we just want to change the size and
                # that's it, the programmer will need to deal with
                # potential layout issues.  If it is being managed by
                # a sizer then we'll change the min size setting and
                # then try to do a layout.  In either case we'll also
                # send an event so the parent can handle any special
                # layout issues that it wants to deal with.
                if self.GetContainingSizer() is not None:
                    mw, mh = self.GetMinSize()
                    self.SetMinSize((mw, height))
                    if self.GetParent().GetSizer() is not None:
                        self.GetParent().Layout()
                    else:
                        self.GetContainingSizer().Layout()
                else:
                    self.SetSize((-1, height))
                # send notification that layout may be needed
                evt = wx.CommandEvent(wxEVT_ETC_LAYOUT_NEEDED, self.GetId())
                evt.SetEventObject(self)
                evt.height = height
                evt.numLines = numLines
                self.GetEventHandler().ProcessEvent(evt)
                

    def _getDefaultHeight(self, parent):
        # checked for cached value
        if self.__class__._defaultHeight != -1:
            return self.__class__._defaultHeight
        # otherwise make a single line textctrl and find out its default height
        tc = wx.TextCtrl(parent)
        sz = tc.GetSize()
        tc.Destroy()
        self.__class__._defaultHeight = sz.height
        return sz.height


    if 'wxGTK' in wx.PlatformInfo or 'wxOSX-cocoa' in wx.PlatformInfo: 
        # GetNumberOfLines in some ports doesn't count wrapped lines, so we
        # need to implement our own.
        def GetNumberOfLines(self):
            text = self.GetValue()
            width = self.GetClientSize().width
            dc = wx.ClientDC(self)
            dc.SetFont(self.GetFont())
            count = 0 
            for line in text.split('\n'):
                count += 1
                w, h = dc.GetTextExtent(line)
                if w > width - self._getExtra():
                    # the width of the text is wider than the control,
                    # calc how many lines it will be wrapped to
                    count += self._wrapLine(line, dc, width)
                    
            if not count:
                count = 1
            return count

        def _getExtra(self):
            if 'wxOSX-cocoa' in wx.PlatformInfo:
                return wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
            else:
                return 0
            
        def _wrapLine(self, line, dc, width):
            # Estimate where the control will wrap the lines and
            # return the count of extra lines needed.
            pte = dc.GetPartialTextExtents(line)  
            width -= wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
            if not pte or width < pte[0]:
                return 1
            idx = 0
            start = 0
            count = 0
            spc = -1
            while idx < len(pte):
                if line[idx] == ' ':
                    spc = idx
                if pte[idx] - start > width:
                    # we've reached the max width, add a new line
                    count += 1
                    # did we see a space? if so restart the count at that pos
                    if spc != -1:
                        idx = spc + 1
                        spc = -1
                    try:
                        start = pte[idx]
                    except IndexError:
                        start = pte[-1]
                else:
                    idx += 1
            return count

#---------------------------------------------------------------------------
