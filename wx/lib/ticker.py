#----------------------------------------------------------------------
# Name:        wx.lib.ticker
# Purpose:     A news-ticker style scrolling text control
#
# Author:      Chris Mellon
#
# Created:     29-Aug-2004
# Copyright:   (c) 2004 by Chris Mellon
# Licence:     wxWindows license
# Tags:        phoenix-port, unittest, documented, py3-port
#----------------------------------------------------------------------

"""
News-ticker style scrolling text control

    * Can scroll from right to left or left to right.

    * Speed of the ticking is controlled by two parameters:

      - Frames per Second(FPS): How many times per second the ticker updates

      - Pixels per Frame(PPF): How many pixels the text moves each update

Low FPS with high PPF will result in "jumpy" text, lower PPF with higher FPS
is smoother (but blurrier and more CPU intensive) text.
"""

import wx

#----------------------------------------------------------------------

class Ticker(wx.Control):
    def __init__(self,
            parent,
            id=-1,
            text=wx.EmptyString,
            fgcolor = wx.BLACK,
            bgcolor = wx.WHITE,
            start=True,
            ppf=2,
            fps=20,
            direction="rtl",
            pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER,
            name="Ticker"
        ):
        """
        Default class constructor.

        :param wx.Window `parent`: the parent
        :param integer `id`: an identifier for the control: a value of -1 is taken to mean a default
        :param string `text`: text in the ticker
        :param wx.Colour `fgcolor`: text/foreground color
        :param wx.Colour `bgcolor`: background color
        :param boolean `start`: if True, the ticker starts immediately
        :param int `ppf`: pixels per frame
        :param int `fps`: frames per second
        :param `direction`: direction of ticking, 'rtl' or 'ltr'
        :param wx.Point `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform
        :param `name`: the control name

        """
        wx.Control.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        self.timer = wx.Timer(owner=self)
        self._extent = (-1, -1)  #cache value for the GetTextExtent call
        self._offset = 0
        self._fps = fps  #frames per second
        self._ppf = ppf  #pixels per frame
        self.SetDirection(direction)
        self.SetText(text)
        self.SetInitialSize(size)
        self.SetForegroundColour(fgcolor)
        self.SetBackgroundColour(bgcolor)
        self.Bind(wx.EVT_TIMER, self.OnTick)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        if start:
            self.Start()


    def Stop(self):
        """Stop moving the text"""
        self.timer.Stop()


    def Start(self):
        """Starts the text moving"""
        if not self.timer.IsRunning():
            self.timer.Start(1000 / self._fps)


    def IsTicking(self):
        """Is the ticker ticking? ie, is the text moving?"""
        return self.timer.IsRunning()


    def SetFPS(self, fps):
        """
        Adjust the update speed of the ticker.

        :param int `fps`: frames per second.

        """
        self._fps = fps
        self.Stop()
        self.Start()


    def GetFPS(self):
        """
        Get the frames per second speed of the ticker.
        """
        return self._fps


    def SetPPF(self, ppf):
        """
        Set the number of pixels per frame the ticker moves - ie,
        how "jumpy" it is.

        :param int `ppf`: the pixels per frame setting.

        """
        self._ppf = ppf


    def GetPPF(self):
        """Get pixels per frame setting."""
        return self._ppf


    def SetFont(self, font):
        """
        Set the font for the control.

        :param wx.Font `font`: the font to be used.

        """
        self._extent = (-1, -1)
        wx.Control.SetFont(self, font)


    def SetDirection(self, dir):
        """
        Sets the direction of the ticker: right to left (rtl) or
        left to right (ltr).

        :param `dir`: the direction 'rtl' or 'ltr'

        """
        if dir == "ltr" or dir == "rtl":
            if self._offset != 0:
                #Change the offset so it's correct for the new direction
                self._offset = self._extent[0] + self.GetSize()[0] - self._offset
            self._dir = dir
        else:
            raise TypeError


    def GetDirection(self):
        """Get the set direction."""
        return self._dir


    def SetText(self, text):
        """
        Set the ticker text.

        :param string `text`: the ticker text

        """
        self._text = text
        self._extent = (-1, -1)
        if not self._text:
            self.Refresh() #Refresh here to clear away the old text.


    def GetText(self):
        """Get the current ticker text."""
        return self._text


    def UpdateExtent(self, dc):
        """
        Updates the cached text extent if needed.

        :param wx.DC `dc`: the dc to use.

        """
        if not self._text:
            self._extent = (-1, -1)
            return
        if self._extent == (-1, -1):
            self._extent = dc.GetTextExtent(self.GetText())


    def DrawText(self, dc):
        """
        Draws the ticker text at the current offset using the provided DC.

        :param wx.DC `dc`: the dc to use.

        """
        dc.SetTextForeground(self.GetForegroundColour())
        dc.SetFont(self.GetFont())
        self.UpdateExtent(dc)
        if self._dir == "ltr":
            offx = self._offset - self._extent[0]
        else:
            offx = self.GetSize()[0] - self._offset
        offy = (self.GetSize()[1] - self._extent[1]) / 2 #centered vertically
        dc.DrawText(self._text, offx, offy)


    def OnTick(self, evt):
        """
        Handles the ``wx.EVT_TIMER`` event for :class:`Ticker`.

        :param `evt`: a :class:`TimerEvent` event to be processed.

        """
        self._offset += self._ppf
        w1 = self.GetSize()[0]
        w2 = self._extent[0]
        if self._offset >= w1+w2:
            self._offset = 0
        self.Refresh()


    def OnPaint(self, evt):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`Ticker`.

        :param `evt`: a :class:`PaintEvent` event to be processed.

        """
        dc = wx.BufferedPaintDC(self)
        brush = wx.Brush(self.GetBackgroundColour())
        dc.SetBackground(brush)
        dc.Clear()
        self.DrawText(dc)


    def OnErase(self, evt):
        """
        Noop because of double buffering

        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`Ticker`.

        :param `evt`: a :class:`EraseEvent` event to be processed.

        """
        pass


    def AcceptsFocus(self):
        """Non-interactive, so don't accept focus"""
        return False


    def DoGetBestSize(self):
        """
        Width we don't care about, height is either -1, or the character
        height of our text with a little extra padding
        """
        if self._extent == (-1, -1):
            if not self._text:
                h = self.GetCharHeight()
            else:
                h = self.GetTextExtent(self.GetText())[1]
        else:
            h = self._extent[1]
        return (100, h+5)


    def ShouldInheritColours(self):
        """Don't get colours from our parent."""
        return False



#testcase/demo
if __name__ == '__main__':
    app = wx.App()
    f = wx.Frame(None)
    p = wx.Panel(f)
    t = Ticker(p, text="Some sample ticker text")
    #set ticker properties here if you want
    s = wx.BoxSizer(wx.VERTICAL)
    s.Add(t, flag=wx.GROW, proportion=0)
    p.SetSizer(s)
    f.Show()
    app.MainLoop()

