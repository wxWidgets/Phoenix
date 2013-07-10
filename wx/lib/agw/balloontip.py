# --------------------------------------------------------------------------- #
# BALLOONTIP wxPython IMPLEMENTATION
# Python Code By:
#
# Andrea Gavana, @ 29 May 2005
# Latest Revision: 16 Jul 2012, 15.00 GMT
#
#
# TODO List/Caveats
#
# 1. With wx.ListBox (And Probably Other Controls), The BalloonTip Sometimes
#    Flashes (It Is Created And Suddenly Destroyed). I Don't Know What Is
#    Happening. Probably I Don't Handle Correctly The wx.EVT_ENTER_WINDOW
#    wx.EVT_LEAVE_WINDOW?
#
# 2. wx.RadioBox Seems Not To Receive The wx.EVT_ENTER_WINDOW Event
#
# 3. wx.SpinCtrl (And Probably Other Controls), When Put In A Sizer, Does Not
#    Return The Correct Size/Position. Probably Is Something I Am Missing.
#
# 4. Other Issues?
#
#
# FIXED Problems
#
# 1. Now BalloonTip Control Works Also For TaskBarIcon (Thanks To Everyone
#    For The Suggetions I Read In The wxPython Mailing List)
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
# Tags:        phoenix-port, unittest, documented
#
# End Of Comments
# --------------------------------------------------------------------------- #

"""
:class:`BalloonTip` is a class that allows you to display tooltips in a balloon style
window.


Description
===========

:class:`BalloonTip` is a class that allows you to display tooltips in a balloon style
window (actually a frame), similarly to the windows XP balloon help. There is
also an arrow that points to the center of the control designed as a "target"
for the :class:`BalloonTip`.

What it can do:

- Set the balloon shape as a rectangle or a rounded rectangle;
- Set an icon to the top-left of the :class:`BalloonTip` frame;
- Set a title at the top of the :class:`BalloonTip` frame;
- Automatic "best" placement of :class:`BalloonTip` frame depending on the target
  control/window position;
- Runtime customization of title/tip fonts and foreground colours;
- Runtime change of :class:`BalloonTip` frame shape;
- Set the balloon background colour;
- Possibility to set the delay after which the :class:`BalloonTip` is displayed;
- Possibility to set the delay after which the :class:`BalloonTip` is destroyed;
- Three different behaviors for the :class:`BalloonTip` window (regardless the delay
  destruction time set):
  
  a) Destroy by leave: the :class:`BalloonTip` is destroyed when the mouse leaves the
     target control/window;
  b) Destroy by click: the :class:`BalloonTip` is destroyed when you click on any area
     of the target control/window;
  c) Destroy by button: the :class:`BalloonTip` is destroyed when you click on the
     top-right close button;
- Possibility to enable/disable globally the :class:`BalloonTip` on you application;
- Set the :class:`BalloonTip` also for the taskbar icon.


Usage
=====

Usage example::

    import wx
    import wx.lib.agw.balloontip as BT

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "BalloonTip Demo")        

            panel = wx.Panel(self)
            
            # Let's suppose that in your application you have a wx.TextCtrl defined as:
            mytextctrl = wx.TextCtrl(panel, -1, "I am a textctrl", pos=(100, 100))

            # You can define your BalloonTip as follows:
            tipballoon = BT.BalloonTip(topicon=None, toptitle="textctrl",
                                       message="this is a textctrl",
                                       shape=BT.BT_ROUNDED,
                                       tipstyle=BT.BT_LEAVE)

            # Set the BalloonTip target
            tipballoon.SetTarget(mytextctrl)
            # Set the BalloonTip background colour
            tipballoon.SetBalloonColour(wx.WHITE)
            # Set the font for the balloon title
            tipballoon.SetTitleFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
            # Set the colour for the balloon title
            tipballoon.SetTitleColour(wx.BLACK)
            # Leave the message font as default
            tipballoon.SetMessageFont()
            # Set the message (tip) foreground colour
            tipballoon.SetMessageColour(wx.LIGHT_GREY)
            # Set the start delay for the BalloonTip
            tipballoon.SetStartDelay(1000)
            # Set the time after which the BalloonTip is destroyed
            tipballoon.SetEndDelay(3000)

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()


Window Styles
=============

This class supports the following window styles:

================ =========== ==================================================
Window Styles    Hex Value   Description
================ =========== ==================================================
``BT_ROUNDED``           0x1 :class:`BalloonTip` will have a rounded rectangular shape.
``BT_RECTANGLE``         0x2 :class:`BalloonTip` will have a rectangular shape.
``BT_LEAVE``             0x3 :class:`BalloonTip` will be destroyed when the user moves the mouse outside the target window.
``BT_CLICK``             0x4 :class:`BalloonTip` will be destroyed when the user click on :class:`BalloonTip`.
``BT_BUTTON``            0x5 :class:`BalloonTip` will be destroyed when the user click on the close button.
================ =========== ==================================================


Events Processing
=================

`No custom events are available for this class.`


License And Version
===================

BalloonTip is distributed under the wxPython license.

Latest revision: Andrea Gavana @ 16 Jul 2012, 15.00 GMT

Version 0.3

"""


import wx
import time

import wx.adv
from wx.lib.buttons import GenButton

# Define The Values For The BalloonTip Frame Shape
BT_ROUNDED = 1
""" :class:`BalloonTip` will have a rounded rectangular shape. """
BT_RECTANGLE = 2
""" :class:`BalloonTip` will have a rectangular shape. """

# Define The Value For The BalloonTip Destruction Behavior
BT_LEAVE = 3
""" :class:`BalloonTip` will be destroyed when the user moves the mouse outside the target window. """
BT_CLICK = 4
""" :class:`BalloonTip` will be destroyed when the user click on :class:`BalloonTip`. """
BT_BUTTON = 5
""" :class:`BalloonTip` will be destroyed when the user click on the close button. """


# ---------------------------------------------------------------
# Class BalloonFrame
# ---------------------------------------------------------------
# This Class Is Called By The Main BalloonTip Class, And It Is
# Responsible For The Frame Creation/Positioning On Screen
# Depending On Target Control/Window, The Frame Can Position
# Itself To NW (Default), NE, SW, SE. The Switch On Positioning
# Is Done By Calculating The Absolute Position Of The Target
# Control/Window Plus/Minus The BalloonTip Size. The Pointing
# Arrow Is Positioned Accordingly.
# ---------------------------------------------------------------

class BalloonFrame(wx.Frame):
    """
    This class is called by the main :class:`BalloonTip` class, and it is
    responsible for the frame creation/positioning on screen
    depending on target control/window, the frame can position
    itself to NW (default), NE, SW, SE. The switch on positioning
    is done by calculating the absolute position of the target
    control/window plus/minus the balloontip size. The pointing
    arrow is positioned accordingly.
    """
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, classparent=None):
        """
        Default class constructor.

        Used internally. Do not call directly this class in your application!
        """

        wx.Frame.__init__(self, None, -1, "BalloonTip", pos, size,
                          style=wx.FRAME_SHAPED |
                          wx.SIMPLE_BORDER |
                          wx.FRAME_NO_TASKBAR |
                          wx.STAY_ON_TOP)

        self._parent = classparent
        self._toptitle = self._parent._toptitle
        self._topicon = self._parent._topicon
        self._message = self._parent._message
        self._shape = self._parent._shape
        self._tipstyle = self._parent._tipstyle

        self._ballooncolour = self._parent._ballooncolour
        self._balloonmsgcolour = self._parent._balloonmsgcolour
        self._balloonmsgfont = self._parent._balloonmsgfont

        if self._toptitle != "":
            self._balloontitlecolour = self._parent._balloontitlecolour
            self._balloontitlefont = self._parent._balloontitlefont

        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.panel = panel

        subsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer.Add((0,20), 0, wx.EXPAND)

        if self._topicon is not None:
            stb = wx.StaticBitmap(panel, -1, self._topicon)
            hsizer.Add(stb, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
            self._balloonbmp = stb

        if self._toptitle != "":
            stt = wx.StaticText(panel, -1, self._toptitle)
            stt.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
            if self._topicon is None:
                hsizer.Add((10,0), 0, wx.EXPAND)

            hsizer.Add(stt, 1, wx.EXPAND | wx.TOP, 10)

            self._balloontitle = stt
            self._balloontitle.SetForegroundColour(self._balloontitlecolour)
            self._balloontitle.SetFont(self._balloontitlefont)

        if self._tipstyle == BT_BUTTON:
            self._closebutton = GenButton(panel, -1, "X", style=wx.NO_BORDER)
            self._closebutton.SetMinSize((16,16))
            self._closebutton.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
            self._closebutton.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterButton)
            self._closebutton.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveButton)
            self._closebutton.SetUseFocusIndicator(False)
            if self._toptitle != "":
                hsizer.Add(self._closebutton, 0, wx.TOP | wx.RIGHT, 5)
            else:
                hsizer.Add((10,0), 1, wx.EXPAND)
                hsizer.Add(self._closebutton, 0, wx.ALIGN_RIGHT | wx.TOP
                           | wx.RIGHT, 5)

        if self._topicon is not None or self._toptitle != "" \
           or self._tipstyle == BT_BUTTON:

            subsizer.Add(hsizer, 0, wx.EXPAND | wx.BOTTOM, 5)

        self._firstline = line = wx.StaticLine(panel, -1, style=wx.LI_HORIZONTAL)

        if self._topicon is not None or self._toptitle != "" \
           or self._tipstyle == BT_BUTTON:
            subsizer.Add(self._firstline, 0, wx.EXPAND | wx.LEFT | wx.RIGHT
                         | wx.BOTTOM, 10)
        else:
            subsizer.Add(self._firstline, 0, wx.EXPAND | wx.LEFT | wx.RIGHT
                         | wx.BOTTOM | wx.TOP, 10)

        mainstt = wx.StaticText(panel, -1, self._message)

        self._balloonmsg = mainstt
        self._balloonmsg.SetForegroundColour(self._balloonmsgcolour)
        self._balloonmsg.SetFont(self._balloonmsgfont)

        subsizer.Add(self._balloonmsg, 1, wx.EXPAND | wx.LEFT | wx.RIGHT |
                     wx.BOTTOM, 10)
        self._secondline = wx.StaticLine(panel, -1, style=wx.LI_HORIZONTAL)
        subsizer.Add(self._secondline, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        subsizer.Add((0,0),1)
        panel.SetSizer(subsizer)

        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizerAndFit(sizer)
        sizer.Layout()

        if self._tipstyle == BT_CLICK:
            if self._toptitle != "":
                self._balloontitle.Bind(wx.EVT_LEFT_DOWN, self.OnClose)

            if self._topicon is not None:
                self._balloonbmp.Bind(wx.EVT_LEFT_DOWN, self.OnClose)

            self._balloonmsg.Bind(wx.EVT_LEFT_DOWN, self.OnClose)
            self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnClose)

        elif self._tipstyle == BT_BUTTON:
            self._closebutton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.panel.SetBackgroundColour(self._ballooncolour)

        if wx.Platform == "__WXGTK__":
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetBalloonShape)
        else:
            self.SetBalloonShape()

        self.Show(True)


    def SetBalloonShape(self, event=None):
        """
        Sets the balloon shape.

        :param `event`: on wxGTK, a :class:`WindowCreateEvent` event to process.
        """

        size = self.GetSize()
        pos = self.GetPosition()

        dc = wx.MemoryDC(wx.Bitmap(1,1))
        textlabel = self._balloonmsg.GetLabel()
        textfont = self._balloonmsg.GetFont()
        textextent = dc.GetFullTextExtent(textlabel, textfont)

        boxheight = size.y - textextent[1]*len(textlabel.split("\n"))
        boxwidth = size.x

        position = wx.GetMousePosition()

        xpos = position[0]
        ypos = position[1]

        if xpos > 20 and ypos > 20:

            # This Is NW Positioning
            positioning = "NW"
            xpos = position[0] - boxwidth + 20
            ypos = position[1] - boxheight - 20

        elif xpos <= 20 and ypos <= 20:

            # This Is SE Positioning
            positioning = "SE"
            xpos = position[0] - 20
            ypos = position[1]

        elif xpos > 20 and ypos <= 20:

            # This Is SW Positioning
            positioning = "SW"
            xpos = position[0] - boxwidth + 20
            ypos = position[1]

        else:

            # This Is NE Positioning
            positioning = "NE"
            xpos = position[0]
            ypos = position[1] - boxheight + 20

        bmp = wx.Bitmap(size.x,size.y)
        dc = wx.BufferedDC(None, bmp)
        dc.SetBackground(wx.Brush(wx.Colour(0,0,0)))
        dc.Clear()
        dc.SetPen(wx.Pen(wx.Colour(0,0,0), 1, wx.PENSTYLE_TRANSPARENT))

        if self._shape == BT_ROUNDED:
            dc.DrawRoundedRectangle(0, 20, boxwidth, boxheight-20, 12)

        elif self._shape == BT_RECTANGLE:
            dc.DrawRectangle(0, 20, boxwidth, boxheight-20)

        if positioning == "NW":
            dc.DrawPolygon(((boxwidth-40, boxheight), (boxwidth-20, boxheight+20),
                            (boxwidth-20, boxheight)))
        elif positioning == "SE":
            dc.DrawPolygon(((20, 20), (20, 0), (40, 20)))

        elif positioning == "SW":
            dc.DrawPolygon(((boxwidth-40, 20), (boxwidth-20, 0), (boxwidth-20, 20)))

        else:
            dc.DrawPolygon(((20, boxheight), (20, boxheight+20), (40, boxheight)))

        r = wx.Region(bmp, wx.Colour(0, 0, 0))
        self.hasShape = self.SetShape(r)

        if self._tipstyle == BT_BUTTON:
            colour = self.panel.GetBackgroundColour()
            self._closebutton.SetBackgroundColour(colour)

        self.SetPosition((xpos, ypos))


    def OnEnterButton(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` for the :class:`BalloonTip` button.

        When the :class:`BalloonTip` is created with the `tipstyle` = ``BT_BUTTON``, this event
        provide some kind of 3D effect when the mouse enters the button area.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        button = event.GetEventObject()
        colour = button.GetBackgroundColour()
        red = colour.Red()
        green = colour.Green()
        blue = colour.Blue()

        if red < 30:
            red = red + 30
        if green < 30:
            green = green + 30
        if blue < 30:
            blue = blue + 30

        colour = wx.Colour(red-30, green-30, blue-30)
        button.SetBackgroundColour(colour)
        button.SetForegroundColour(wx.WHITE)
        button.Refresh()
        event.Skip()


    def OnLeaveButton(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` for the :class:`BalloonTip` button.

        When the :class:`BalloonTip` is created with the `tipstyle` = ``BT_BUTTON``, this event
        provide some kind of 3D effect when the mouse enters the button area.

        :param `event`: a :class:`MouseEvent` event to be processed.        
        """

        button = event.GetEventObject()
        colour = self.panel.GetBackgroundColour()
        button.SetBackgroundColour(colour)
        button.SetForegroundColour(wx.BLACK)
        button.Refresh()
        event.Skip()


    def OnClose(self, event):
        """
        Handles the ``wx.EVT_CLOSE`` event for :class:`BalloonTip`.

        :param `event`: a :class:`CloseEvent` event to be processed.
        """

        if isinstance(self._parent._widget, wx.adv.TaskBarIcon):
            self._parent.taskbarcreation = 0
            self._parent.taskbartime.Stop()
            del self._parent.taskbartime
            del self._parent.BalloonFrame

        self.Destroy()


# ---------------------------------------------------------------
# Class BalloonTip
# ---------------------------------------------------------------
# This Is The Main BalloonTip Implementation
# ---------------------------------------------------------------

class BalloonTip(object):
    """
    :class:`BalloonTip` is a class that allows you to display tooltips in a balloon style
    window.

    This is the main class implementation.
    """    
    def __init__(self, topicon=None, toptitle="",
                 message="", shape=BT_ROUNDED, tipstyle=BT_LEAVE):
        """
        Default class constructor.

        :param `topicon`: an icon that will be displayed on the top-left part of the
         :class:`BalloonTip` frame. If set to ``None``, no icon will be displayed;
        :type `topicon`: :class:`Bitmap` or ``None``
        :param string `toptitle`: a title that will be displayed on the top part of the
         :class:`BalloonTip` frame. If set to an empty string, no title will be displayed;
        :param string `message`: the tip message that will be displayed. It can not be set to
         an empty string;
        :param integer `shape`: the :class:`BalloonTip` shape. It can be one of the following:

         ======================= ========= ====================================
         Shape Flag              Hex Value  Description
         ======================= ========= ====================================
         ``BT_ROUNDED``           0x1      :class:`BalloonTip` will have a rounded rectangular shape.
         ``BT_RECTANGLE``         0x2      :class:`BalloonTip` will have a rectangular shape.
         ======================= ========= ====================================
         
        :param integer `tipstyle`: the :class:`BalloonTip` destruction behavior. It can be one of:

         ======================= ========= ====================================
         Tip Flag                Hex Value  Description
         ======================= ========= ====================================
         ``BT_LEAVE``                  0x3 :class:`BalloonTip` will be destroyed when the user moves the mouse outside the target window.
         ``BT_CLICK``                  0x4 :class:`BalloonTip` will be destroyed when the user click on :class:`BalloonTip`.
         ``BT_BUTTON``                 0x5 :class:`BalloonTip` will be destroyed when the user click on the close button.
         ======================= ========= ====================================

        :raise: `Exception` in the following cases:

         - The `message` parameter is an empty string;
         - The `shape` parameter has an invalid value (i.e., it's not one of ``BT_ROUNDED``, ``BT_RECTANGLE``);
         - The `tipstyle` parameter has an invalid value (i.e., it's not one of ``BT_LEAVE``, ``BT_CLICK``, ``BT_BUTTON``).

        """

        self._shape = shape
        self._topicon = topicon
        self._toptitle = toptitle
        self._message = message
        self._tipstyle = tipstyle

        app = wx.GetApp()
        self._runningapp = app
        self._runningapp.__tooltipenabled__ = True

        if self._message == "":
            raise Exception("\nERROR: You Should At Least Set The Message For The BalloonTip")

        if self._shape not in [BT_ROUNDED, BT_RECTANGLE]:
            raise Exception('\nERROR: BalloonTip Shape Should Be One Of "BT_ROUNDED", "BT_RECTANGLE"')

        if self._tipstyle not in [BT_LEAVE, BT_CLICK, BT_BUTTON]:
            raise Exception('\nERROR: BalloonTip TipStyle Should Be One Of "BT_LEAVE", '\
                            '"BT_CLICK", "BT_BUTTON"')

        self.SetStartDelay()
        self.SetEndDelay()
        self.SetBalloonColour()

        if toptitle != "":
            self.SetTitleFont()
            self.SetTitleColour()

        if topicon is not None:
            self.SetBalloonIcon(topicon)

        self.SetMessageFont()
        self.SetMessageColour()


    def SetTarget(self, widget):
        """
        Sets the target control/window for the :class:`BalloonTip`.

        :param `widget`: any subclass of :class:`Window`.
        """

        self._widget = widget

        if isinstance(widget, wx.adv.TaskBarIcon):
            self._widget.Bind(wx.adv.EVT_TASKBAR_MOVE, self.OnTaskBarMove)
            self._widget.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
            self.taskbarcreation = 0
        else:
            self._widget.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
            self._widget.Bind(wx.EVT_LEAVE_WINDOW, self.OnWidgetLeave)
            self._widget.Bind(wx.EVT_MOTION, self.OnWidgetMotion)
            self._widget.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)


    def GetTarget(self):
        """
        Returns the target window for the :class:`BalloonTip`.

        :return: An instance of :class:`Window`.

        :raise: `Exception` if the :meth:`~BalloonTip.SetTarget` method has not previously called.        
        """

        if not hasattr(self, "_widget"):
            raise Exception("\nERROR: BalloonTip Target Has Not Been Set")

        return self._widget


    def SetStartDelay(self, delay=1):
        """
        Sets the delay time after which the :class:`BalloonTip` is created.

        :param integer `delay`: the number of milliseconds after which :class:`BalloonTip` is created.

        :raise: `Exception` if `delay` is less than ``1`` milliseconds.
        """

        if delay < 1:
            raise Exception("\nERROR: Delay Time For BalloonTip Creation Should Be Greater Than 1 ms")

        self._startdelaytime = float(delay)


    def GetStartDelay(self):
        """
        Returns the delay time after which the :class:`BalloonTip` is created.

        :return: the delay time, in milliseconds.
        """

        return self._startdelaytime


    def SetEndDelay(self, delay=1e6):
        """
        Sets the delay time after which the BalloonTip is destroyed.

        :param integer `delay`: the number of milliseconds after which :class:`BalloonTip` is destroyed.

        :raise: `Exception` if `delay` is less than ``1`` milliseconds.
        """

        if delay < 1:
            raise Exception("\nERROR: Delay Time For BalloonTip Destruction Should Be Greater Than 1 ms")

        self._enddelaytime = float(delay)


    def GetEndDelay(self):
        """
        Returns the delay time after which the :class:`BalloonTip` is destroyed.

        :return: the delay time, in milliseconds.
        """

        return self._enddelaytime


    def OnWidgetEnter(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` for the target control/window and
        starts the :class:`BalloonTip` timer for creation.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if hasattr(self, "BalloonFrame"):
            if self.BalloonFrame:
                return

        if not self._runningapp.__tooltipenabled__:
            return

        self.showtime = wx.Timer(self._widget)
        self._widget.Bind(wx.EVT_TIMER, self.NotifyTimer, self.showtime)
        self.showtime.Start(self._startdelaytime)

        event.Skip()


    def OnWidgetLeave(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` for the target control/window.
        
        :param `event`: a :class:`MouseEvent` event to be processed.

        :note: If the BalloonTip `tipstyle` is set to ``BT_LEAVE``, the :class:`BalloonTip` is destroyed.
        """

        if hasattr(self, "showtime"):
            if self.showtime:
                self.showtime.Stop()
                del self.showtime

        if hasattr(self, "BalloonFrame"):
            if self.BalloonFrame:
                if self._tipstyle == BT_LEAVE:
                    endtime = time.time()
                    if endtime - self.starttime > 0.1:
                        try:
                            self.BalloonFrame.Destroy()
                        except:
                            pass
                else:
                    event.Skip()
            else:
                event.Skip()
        else:
            event.Skip()


    def OnTaskBarMove(self, event):
        """
        Handles the mouse motion inside the taskbar icon area.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not hasattr(self, "BalloonFrame"):
            if self.taskbarcreation == 0:
                self.mousepos = wx.GetMousePosition()
                self.currentmousepos = self.mousepos
                self.taskbartime = wx.Timer(self._widget)
                self._widget.Bind(wx.EVT_TIMER, self.TaskBarTimer, self.taskbartime)
                self.taskbartime.Start(100)
                self.showtime = wx.Timer(self._widget)
                self._widget.Bind(wx.EVT_TIMER, self.NotifyTimer, self.showtime)
                self.showtime.Start(self._startdelaytime)

            if self.taskbarcreation == 0:
                self.taskbarcreation = 1

            return

        event.Skip()


    def OnWidgetMotion(self, event):
        """
        Handle the mouse motion inside the target.

        This prevents the annoying behavior of :class:`BalloonTip` to display when the
        user does something else inside the window. The :class:`BalloonTip` window is
        displayed only when the mouse does *not* move for the start delay time.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if hasattr(self, "BalloonFrame"):
            if self.BalloonFrame:
                return

        if hasattr(self, "showtime"):
            if self.showtime:
                self.showtime.Start(self._startdelaytime)

        event.Skip()


    def NotifyTimer(self, event):
        """
        The creation timer has expired. Creates the :class:`BalloonTip` frame.

        :param `event`: a :class:`wx.TimerEvent` to be processed.
        """

        self.BalloonFrame = BalloonFrame(self._widget, classparent=self)
        self.BalloonFrame.Show(True)
        self.starttime = time.time()

        if hasattr(self, "showtime"):
            self.showtime.Stop()
            del self.showtime

        self.destroytime = wx.Timer(self._widget)
        self._widget.Bind(wx.EVT_TIMER, self.NotifyTimer, self.destroytime)
        self.destroytime.Start(self._enddelaytime)


    def TaskBarTimer(self, event):
        """
        This timer check periodically the mouse position.

        If the current mouse position is sufficiently far from the coordinates
        it had when entered the taskbar icon and the :class:`BalloonTip` style is
        ``BT_LEAVE``, the :class:`BalloonTip` frame is destroyed.

        :param `event`: a :class:`wx.TimerEvent` to be processed.
        """

        self.currentmousepos = wx.GetMousePosition()
        mousepos = self.mousepos

        if abs(self.currentmousepos[0] - mousepos[0]) > 30 or \
           abs(self.currentmousepos[1] - mousepos[1]) > 30:
            if hasattr(self, "BalloonFrame"):
                if self._tipstyle == BT_LEAVE:
                    try:
                        self.BalloonFrame.Destroy()
                        self.taskbartime.Stop()
                        del self.taskbartime
                        del self.BalloonFrame
                        self.taskbarcreation = 0
                    except:
                        pass


    def DestroyTimer(self, event):
        """
        The destruction timer has expired. Destroys the :class:`BalloonTip` frame.

        :param `event`: a :class:`wx.TimerEvent` to be processed.
        """

        self.destroytime.Stop()
        del self.destroytime

        try:
            self.BalloonFrame.Destroy()
        except:
            pass


    def SetBalloonShape(self, shape=BT_ROUNDED):
        """
        Sets the :class:`BalloonTip` frame shape.

        :param integer `shape`: should be one of ``BT_ROUNDED`` or ``BT_RECTANGLE``.

        :raise: `Exception` if the `shape` parameter is not a valid value
         (i.e., it's not one of ``BT_ROUNDED``, ``BT_RECTANGLE``);        
        """

        if shape not in [BT_ROUNDED, BT_RECTANGLE]:
            raise Exception('\nERROR: BalloonTip Shape Should Be One Of "BT_ROUNDED", "BT_RECTANGLE"')

        self._shape = shape


    def GetBalloonShape(self):
        """
        Returns the :class:`BalloonTip` frame shape.

        :return: An integer, one of ``BT_ROUNDED``, ``BT_RECTANGLE``.
        """

        return self._shape


    def SetBalloonIcon(self, icon):
        """
        Sets the :class:`BalloonTip` top-left icon.

        :param `icon`: an instance of :class:`Bitmap`.

        :raise: `Exception` if the `icon` bitmap is not a valid :class:`Bitmap`.
        """

        if icon.IsOk():
            self._topicon = icon
        else:
            raise Exception("\nERROR: Invalid Image Passed To BalloonTip")


    def GetBalloonIcon(self):
        """
        Returns the :class:`BalloonTip` top-left icon.

        :return: An instance of :class:`Bitmap`.
        """

        return self._topicon


    def SetBalloonTitle(self, title=""):
        """
        Sets the :class:`BalloonTip` top title.

        :param string `title`: a string to use as a :class:`BalloonTip` title.
        """

        self._toptitle = title


    def GetBalloonTitle(self):
        """
        Returns the :class:`BalloonTip` top title.

        :return: A string containing the top title.
        """

        return self._toptitle


    def SetBalloonMessage(self, message):
        """
        Sets the :class:`BalloonTip` tip message. 

        :param string `message`: a string identifying the main message body of :class:`BalloonTip`.

        :raise: `Exception` if the message is an empty string.

        :note: The :class:`BalloonTip` message should never be empty.        
        """

        if len(message.strip()) < 1:
            raise Exception("\nERROR: BalloonTip Message Can Not Be Empty")

        self._message = message


    def GetBalloonMessage(self):
        """
        Returns the :class:`BalloonTip` tip message.

        :return: A string containing the main message.
        """

        return self._message


    def SetBalloonTipStyle(self, tipstyle=BT_LEAVE):
        """
        Sets the :class:`BalloonTip` `tipstyle` parameter.

        :param integer `tipstyle`: one of the following bit set:

         ============== ========== =====================================
         Tip Style      Hex Value  Description
         ============== ========== =====================================
         ``BT_LEAVE``          0x3 :class:`BalloonTip` will be destroyed when the user moves the mouse outside the target window.
         ``BT_CLICK``          0x4 :class:`BalloonTip` will be destroyed when the user click on :class:`BalloonTip`.
         ``BT_BUTTON``         0x5 :class:`BalloonTip` will be destroyed when the user click on the close button.
         ============== ========== =====================================

        :raise: `Exception` if the `tipstyle` parameter has an invalid value
         (i.e., it's not one of ``BT_LEAVE``, ``BT_CLICK``, ``BT_BUTTON``).
        """

        if tipstyle not in [BT_LEAVE, BT_CLICK, BT_BUTTON]:
            raise Exception('\nERROR: BalloonTip TipStyle Should Be One Of "BT_LEAVE", '\
                            '"BT_CLICK", "BT_BUTTON"')

        self._tipstyle = tipstyle


    def GetBalloonTipStyle(self):
        """
        Returns the :class:`BalloonTip` `tipstyle` parameter.

        :return: An integer representing the style.
        
        :see: :meth:`~BalloonTip.SetBalloonTipStyle`
        """

        return self._tipstyle


    def SetBalloonColour(self, colour=None):
        """
        Sets the :class:`BalloonTip` background colour.

        :param `colour`: a valid :class:`Colour` instance.
        """

        if colour is None:
            colour = wx.Colour(255, 250, 205)

        self._ballooncolour = colour


    def GetBalloonColour(self):
        """
        Returns the :class:`BalloonTip` background colour.

        :return: An instance of :class:`Colour`.
        """

        return self._ballooncolour


    def SetTitleFont(self, font=None):
        """
        Sets the font for the top title.

        :param `font`: a valid :class:`Font` instance.
        """

        if font is None:
            font = wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)

        self._balloontitlefont = font


    def GetTitleFont(self):
        """
        Returns the font for the top title.

        :return: An instance of :class:`Font`.
        """

        return self._balloontitlefont


    def SetMessageFont(self, font=None):
        """
        Sets the font for the tip message.

        :param `font`: a valid :class:`Font` instance.
        """

        if font is None:
            font = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)

        self._balloonmsgfont = font


    def GetMessageFont(self):
        """
        Returns the font for the tip message.

        :return: An instance of :class:`Font`.
        """

        return self._balloonmsgfont


    def SetTitleColour(self, colour=None):
        """
        Sets the colour for the top title.

        :param `colour`: a valid :class:`Colour` instance.
        """

        if colour is None:
            colour = wx.BLACK

        self._balloontitlecolour = colour


    def GetTitleColour(self):
        """
        Returns the colour for the top title.

        :return: An instance of :class:`Colour`.
        """

        return self._balloontitlecolour


    def SetMessageColour(self, colour=None):
        """
        Sets the colour for the tip message.

        :param `colour`: a valid :class:`Colour` instance.
        """

        if colour is None:
            colour = wx.BLACK

        self._balloonmsgcolour = colour


    def GetMessageColour(self):
        """
        Returns the colour for the tip message.

        :return: An instance of :class:`Colour`.
        """

        return self._balloonmsgcolour


    def OnDestroy(self, event):
        """
        Handles the target destruction, specifically handling the ``wx.EVT_WINDOW_DESTROY``
        event.

        :param `event`: a :class:`WindowDestroyEvent` event to be processed.        
        """
        
        if hasattr(self, "BalloonFrame"):
            if self.BalloonFrame:
                try:
                    if isinstance(self._widget, wx.adv.TaskBarIcon):
                        self._widget.Unbind(wx.adv.EVT_TASKBAR_MOVE)
                        self.taskbartime.Stop()
                        del self.taskbartime
                    else:
                        self._widget.Unbind(wx.EVT_MOTION)
                        self._widget.Unbind(wx.EVT_LEAVE_WINDOW)
                        self._widget.Unbind(wx.EVT_ENTER_WINDOW)

                    self.BalloonFrame.Destroy()

                except:
                    pass

                del self.BalloonFrame


    def EnableTip(self, enable=True):
        """
        Enable/disable globally the :class:`BalloonTip`.

        :param bool `enable`: ``True`` to enable :class:`BalloonTip`, ``False`` otherwise.
        """

        self._runningapp.__tooltipenabled__ = enable


if __name__ == '__main__':

    import wx

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "BalloonTip Demo")        

            panel = wx.Panel(self)
            
            # Let's suppose that in your application you have a wx.TextCtrl defined as:
            mytextctrl = wx.TextCtrl(panel, -1, "I am a textctrl", pos=(100, 100))

            # You can define your BalloonTip as follows:
            tipballoon = BalloonTip(topicon=None, toptitle="textctrl",
                                    message="this is a textctrl",
                                    shape=BT_ROUNDED,
                                    tipstyle=BT_LEAVE)

            # Set the BalloonTip target
            tipballoon.SetTarget(mytextctrl)
            # Set the BalloonTip background colour
            tipballoon.SetBalloonColour(wx.WHITE)
            # Set the font for the balloon title
            tipballoon.SetTitleFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
            # Set the colour for the balloon title
            tipballoon.SetTitleColour(wx.BLACK)
            # Leave the message font as default
            tipballoon.SetMessageFont()
            # Set the message (tip) foreground colour
            tipballoon.SetMessageColour(wx.LIGHT_GREY)
            # Set the start delay for the BalloonTip
            tipballoon.SetStartDelay(1000)
            # Set the time after which the BalloonTip is destroyed
            tipballoon.SetEndDelay(3000)

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()


