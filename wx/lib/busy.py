#---------------------------------------------------------------------------
#  File:         busy.py
#  Description:  A class like wx.BusyInfo but which doesn't take up so much
#                space by default and which has a nicer look.
#
#  Date:         11-Sept-2012
#  Author:       Robin Dunn
#  Tags:         phoenix-port, unittest, documented
#---------------------------------------------------------------------------

"""
A class like :class:`wx.BusyInfo` but which doesn't take up so much space by default
and which has a nicer look.
"""

import wx
from wx.lib.stattext import GenStaticText as StaticText

#---------------------------------------------------------------------------


class BusyInfo(object):
    """
    This class is just like :class:`wx.BusyInfo`, except that its default
    size is smaller, (unless the size of the message requires a larger window
    size) and the background and foreground colors of the message box can be
    set.

    Creating an instace of the class will create and show a window with the
    given message, and when the instance is deleted then that window will be
    closed. This class also implements the context manager magic methods, so
    it can be used with Python's `with` statement, like this::

        with BusyInfo('Please wait...'):
            doSomethingThatNeedsWaiting()

    """

    def __init__(self, msg, parent=None, bgColour=None, fgColour=None):
        """
        Create a new :class:`BusyInfo`.

        :param string `msg`:     a string to be displayed in the BusyInfo window.
        :param wx.Window `parent`:  an optional window to be used as the parent of
            the `:class:`BusyInfo`.  If given then the ``BusyInfo`` will be centered
            over that window, otherwise it will be centered on the screen.
        :param wx.Colour `bgColour`: colour to be used for the background
            of the :class:`BusyInfo`
        :param wx.Colour `fgColour`: colour to be used for the foreground (text)
            of the :class:`BusyInfo`
        """
        self.frame = _InfoFrame(parent, msg, bgColour, fgColour)
        self.frame.Show()
        self.frame.Refresh()
        self.frame.Update()

    def __del__(self):
        self.Close()

    def Close(self):
        """
        Hide and close the busy info box.
        """
        if self.frame:
            self.frame.Hide()
            self.frame.Close()
            self.frame = None


    # Magic methods for using this class as a Context Manager
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Close()
        return False


#---------------------------------------------------------------------------

class _InfoFrame(wx.Frame):
    def __init__(self, parent, msg, bgColour=None, fgColour=None):
        wx.Frame.__init__(self, parent, style=wx.BORDER_SIMPLE|wx.FRAME_TOOL_WINDOW|wx.STAY_ON_TOP)

        bgColour = bgColour if bgColour is not None else wx.Colour(253, 255, 225)
        fgColour = fgColour if fgColour is not None else wx.BLACK

        panel = wx.Panel(self)
        text = StaticText(panel, -1, msg)

        for win in [panel, text]:
            win.SetCursor(wx.HOURGLASS_CURSOR)
            win.SetBackgroundColour(bgColour)
            win.SetForegroundColour(fgColour)

        size = text.GetBestSize()
        self.SetClientSize((size.width + 60, size.height + 40))
        panel.SetSize(self.GetClientSize())
        text.Center()
        self.Center()


#---------------------------------------------------------------------------


if __name__ == '__main__':

    def test1(frm):
        with BusyInfo("short message...", frm):
            wx.Sleep(2)
        wx.CallLater(1000, test2, frm)

    def test2(frm):
        with BusyInfo("This is my longer short message.  Please be patient...", frm):
            wx.Sleep(2)
            wx.CallLater(1000, test3, frm)

    def test3(frm):
        busy = BusyInfo("Without using the context manager...", frm)
        wx.Sleep(2)
        del busy
        wx.CallLater(1000, test4, frm)

    def test4(frm):
        with BusyInfo("Without using the parent window..."):
            wx.Sleep(2)
        wx.CallLater(1000, test5, frm)

    def test5(frm):

        message = """A long message with line breaks:
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit
esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est
laborum."""
        with BusyInfo(message, frm):
            wx.Sleep(2)


    app = wx.App(False)
    frm = wx.Frame(None, title="BusyInfoTest")
    wx.CallLater(1000, test1, frm)
    frm.Show()
    app.MainLoop()
