# --------------------------------------------------------------------------- #
# PYBUSYINFO Control wxPython IMPLEMENTATION
# Inspired By And Heavily Based On wxBusyInfo.
#
# Python Code By:
#
# Andrea Gavana, @ 10 December 2009
# Latest Revision: 27 Dec 2012, 21.00 GMT
#
#
# TODO List/Caveats
#
# 1. ?
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@gmail.com
# andrea.gavana@maerskoil.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
# Tags:        phoenix-port, unittest, documented, py3-port
#
# End Of Comments
# --------------------------------------------------------------------------- #

"""
:class:`~wx.lib.agw.pybusyinfo.PyBusyInfo` constructs a busy info window and displays a message in it.


Description
===========

:class:`PyBusyInfo` constructs a busy info window and displays a message in it.

This class makes it easy to tell your user that the program is temporarily busy.
Just create a :class:`PyBusyInfo` object, and within the current scope, a message window
will be shown.

For example::

    busy = PyBusyInfo("Please wait, working...")

    for i in xrange(10000):
        DoACalculation()

    del busy


It works by creating a window in the constructor, and deleting it in the destructor.
You may also want to call :func:`Yield` () to refresh the window periodically (in case
it had been obscured by other windows, for example).


Usage
=====

Usage example::

    import wx
    import wx.lib.agw.pybusyinfo as PBI

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "PyBusyInfo Demo")

            panel = wx.Panel(self)

            b = wx.Button(panel, -1, "Test PyBusyInfo ", (50,50))
            self.Bind(wx.EVT_BUTTON, self.OnButton, b)


        def OnButton(self, event):

            message = "Please wait 5 seconds, working..."
            busy = PBI.PyBusyInfo(message, parent=self, title="Really Busy")

            wx.Yield()

            for indx in xrange(5):
                wx.MilliSleep(1000)

            del busy


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()



Supported Platforms
===================

:class:`PyBusyInfo` has been tested on the following platforms:
  * Windows (Windows XP).


Window Styles
=============

`No particular window styles are available for this class.`


Events Processing
=================

`No custom events are available for this class.`


License And Version
===================

:class:`PyBusyInfo` is distributed under the wxPython license.

Latest Revision: Andrea Gavana @ 27 Dec 2012, 21.00 GMT

Version 0.3

"""

# Version Info
__version__ = "0.3"

import wx

_ = wx.GetTranslation


class PyInfoFrame(wx.Frame):
    """ Base class for :class:`PyBusyInfo`. """

    def __init__(self, parent, message, title, icon):
        """
        Default class constructor.

        :param `parent`: the frame parent;
        :param `message`: the message to display in the :class:`PyBusyInfo`;
        :param `title`: the main :class:`PyBusyInfo` title;
        :param `icon`: an icon to draw as the frame icon, an instance of :class:`wx.Bitmap`.
        """

        wx.Frame.__init__(self, parent, wx.ID_ANY, title, wx.DefaultPosition,
                          wx.DefaultSize, wx.NO_BORDER|wx.FRAME_TOOL_WINDOW|wx.FRAME_SHAPED|wx.STAY_ON_TOP)

        panel = wx.Panel(self)
        panel.SetCursor(wx.HOURGLASS_CURSOR)

        self._message = message
        self._title = title
        self._icon = icon

        dc = wx.ClientDC(self)
        textWidth, textHeight, dummy = dc.GetFullMultiLineTextExtent(self._message)
        sizeText = wx.Size(textWidth, textHeight)

        self.SetClientSize((max(sizeText.x, 340) + 60, max(sizeText.y, 40) + 60))
        # need to size the panel correctly first so that text.Centre() works
        panel.SetSize(self.GetClientSize())

        # Bind the events to draw ourselves
        panel.Bind(wx.EVT_PAINT, self.OnPaint)
        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)

        self.Centre(wx.BOTH)

        # Create a non-rectangular region to set the frame shape
        size = self.GetSize()
        bmp = wx.Bitmap(size.x, size.y)
        dc = wx.BufferedDC(None, bmp)
        dc.SetBackground(wx.BLACK_BRUSH)
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        dc.DrawRoundedRectangle(0, 0, size.x, size.y, 12)
        r = wx.Region(bmp, wx.BLACK)
        # Store the non-rectangular region
        self.reg = r

        if wx.Platform == "__WXGTK__":
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetBusyShape)
        else:
            self.SetBusyShape()

        # Add a custom bitmap at the top (if any)


    def SetBusyShape(self, event=None):
        """
        Sets :class:`PyInfoFrame` shape using the region created from the bitmap.

        :param `event`: a :class:`wx.WindowCreateEvent` event (GTK only, as GTK supports setting
         the window shape only during window creation).
        """

        self.SetShape(self.reg)
        if event:
            # GTK only
            event.Skip()


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`PyInfoFrame`.

        :param `event`: a :class:`PaintEvent` to be processed.
        """

        panel = event.GetEventObject()

        dc = wx.BufferedPaintDC(panel)
        dc.Clear()

        # Fill the background with a gradient shading
        startColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        endColour = wx.WHITE

        rect = panel.GetRect()
        dc.GradientFillLinear(rect, startColour, endColour, wx.SOUTH)

        # Draw the label
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        dc.SetFont(font)

        # Draw the message
        rect2 = wx.Rect(*rect)
        rect2.height += 20
        dc.DrawLabel(self._message, rect2, alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)

        # Draw the top title
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.SetPen(wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT)))
        dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT))

        if self._icon.IsOk():
            iconWidth, iconHeight = self._icon.GetWidth(), self._icon.GetHeight()
            dummy, textHeight = dc.GetTextExtent(self._title)
            textXPos, textYPos = iconWidth + 10, (iconHeight-textHeight)//2
            dc.DrawBitmap(self._icon, 5, 5, True)
        else:
            textXPos, textYPos = 5, 0

        dc.DrawText(self._title, textXPos, textYPos+5)
        dc.DrawLine(5, 25, rect.width-5, 25)

        size = self.GetSize()
        dc.SetPen(wx.Pen(startColour, 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRoundedRectangle(0, 0, size.x, size.y-1, 12)


    def OnErase(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`PyInfoFrame`.

        :param `event`: a :class:`EraseEvent` event to be processed.

        :note: This method is intentionally empty to reduce flicker.
        """

        # This is empty on purpose, to avoid flickering
        pass


# -------------------------------------------------------------------- #
# The actual PyBusyInfo implementation
# -------------------------------------------------------------------- #

class PyBusyInfo(object):
    """
    Constructs a busy info window as child of parent and displays a message in it.
    """

    def __init__(self, message, parent=None, title=_("Busy"), icon=wx.NullBitmap):
        """
        Default class constructor.

        :param `parent`: the :class:`PyBusyInfo` parent;
        :param `message`: the message to display in the :class:`PyBusyInfo`;
        :param `title`: the main :class:`PyBusyInfo` title;
        :param `icon`: an icon to draw as the frame icon, an instance of :class:`wx.Bitmap`.

        :note: If `parent` is not ``None`` you must ensure that it is not closed
         while the busy info is shown.
        """

        self._infoFrame = PyInfoFrame(parent, message, title, icon)

        if parent and parent.HasFlag(wx.STAY_ON_TOP):
            # we must have this flag to be in front of our parent if it has it
            self._infoFrame.SetWindowStyleFlag(wx.STAY_ON_TOP)

        # Added for the screenshot-taking tool
        self.Show()


    def __del__(self):
        """ Overloaded method, for compatibility with wxWidgets. """

        self._infoFrame.Show(False)
        self._infoFrame.Destroy()


    def Show(self, show=True):
        """
        Shows or hides the window.

        You may need to call `Raise` for a top level window if you want to bring it to
        top, although this is not needed if :meth:`PyBusyInfo.Show` is called immediately after the frame creation.

        :param bool `show`: ``True`` to show the :class:`PyBusyInfo` frame, ``False`` to hide it.

        :return: ``True`` if the window has been shown or hidden or ``False`` if nothing was done
         because it already was in the requested state.

        .. note::

           Notice that the default state of newly created top level windows is hidden (to allow
           you to create their contents without flicker) unlike for all the other, not derived from
           :class:`TopLevelWindow`, windows that are by default created in the shown state.


        .. versionadded:: 0.9.5
        """

        retVal = self._infoFrame.Show(show)

        if show:
            self._infoFrame.Refresh()
            self._infoFrame.Update()

        return retVal


    def Update(self):
        """
        Calling this method immediately repaints the invalidated area of the window and all of its
        children recursively (this normally only happens when the flow of control returns to the
        event loop).

        :note: Notice that this function doesn't invalidate any area of the window so nothing happens
         if nothing has been invalidated (i.e. marked as requiring a redraw). Use `Refresh` first if
         you want to immediately redraw the window unconditionally.

        .. versionadded:: 0.9.5
        """

        self._infoFrame.Update()


if __name__ == '__main__':

    import wx

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "PyBusyInfo Demo")

            panel = wx.Panel(self)

            b = wx.Button(panel, -1, "Test PyBusyInfo ", (50,50))
            self.Bind(wx.EVT_BUTTON, self.OnButton, b)


        def OnButton(self, event):

            message = "Please wait 5 seconds, working..."
            busy = PyBusyInfo(message, parent=self, title="Really Busy")

            wx.Yield()

            for indx in range(5):
                wx.MilliSleep(1000)

            del busy


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()

