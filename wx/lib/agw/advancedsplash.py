# --------------------------------------------------------------------------- #
# ADVANCEDSPLASH Control wxPython IMPLEMENTATION
# Python Code By:
#
# Andrea Gavana, @ 10 Oct 2005
# Latest Revision: 19 Dec 2012, 21.00 GMT
#
#
# TODO List/Caveats
#
# 1. Actually, Setting The Shape Of AdvancedSplash Is Done Using "SetShape"
#    Function On A Frame. This Works, AFAIK, On This Following Platforms:
#
#    - MSW
#    - UNIX/Linux
#    - MacOS Carbon
#
#    Obviously I May Be Wrong Here. Could Someone Verify That Lines 139-145
#    Work Correctly On Other Platforms Than Mine (MSW XP/2000)?
#    Moreover, Is There A Way To Avoid The Use Of The "SetShape" Method?
#    I Don't Know.
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
:class:`AdvancedSplash` tries to reproduce the behavior of :class:`~adv.SplashScreen`, with
some enhancements.


Description
===========

:class:`AdvancedSplash` tries to reproduce the behavior of :class:`~adv.SplashScreen`, but with
some enhancements (in my opinion).

:class:`AdvancedSplash` starts its construction from a simple frame. Then, depending on
the options passed to it, it sets the frame shape accordingly to the image passed
as input. :class:`AdvancedSplash` behaves somewhat like :class:`~adv.SplashScreen`, and almost
all the methods available in :class:`~adv.SplashScreen` are available also in
this module.


Usage
=====

Sample usage::

    import wx
    import wx.lib.agw.advancedsplash as AS

    app = wx.App(0)

    frame = wx.Frame(None, -1, "AdvancedSplash Test")
    
    imagePath = "my_splash_image.png"
    bitmap = wx.Bitmap(imagePath, wx.BITMAP_TYPE_PNG)
    shadow = wx.WHITE
    
    splash = AS.AdvancedSplash(frame, bitmap=bitmap, timeout=5000,
                               agwStyle=AS.AS_TIMEOUT |
                               AS.AS_CENTER_ON_PARENT |
                               AS.AS_SHADOW_BITMAP,
                               shadowcolour=shadow)

    app.MainLoop()
    

None of the options are strictly required (a part of the `bitmap` parameter).
If you use the defaults you get a very simple :class:`AdvancedSplash`.


Methods and Settings
====================

:class:`AdvancedSplash` is customizable, and in particular you can set:

- Whether you want to mask a colour or not in your input bitmap;
- Where to center the splash screen (on screen, on parent or nowhere);
- Whether it is a "timeout" splashscreen or not;
- The time after which :class:`AdvancedSplash` is destroyed (if it is a timeout splashscreen);
- The (optional) text you wish to display;
- The font, colour and position of the displayed text (optional).


Window Styles
=============

This class supports the following window styles:

======================= =========== ==================================================
Window Styles           Hex Value   Description
======================= =========== ==================================================
``AS_TIMEOUT``                  0x1 :class:`AdvancedSplash` will be destroyed after `timeout` milliseconds.
``AS_NOTIMEOUT``                0x2 :class:`AdvancedSplash` can be destroyed by clicking on it, pressing a key or by explicitly call the `Close()` method.
``AS_CENTER_ON_SCREEN``         0x4 :class:`AdvancedSplash` will be centered on screen.
``AS_CENTER_ON_PARENT``         0x8 :class:`AdvancedSplash` will be centered on parent.
``AS_NO_CENTER``               0x10 :class:`AdvancedSplash` will not be centered.
``AS_SHADOW_BITMAP``           0x20 If the bitmap you pass as input has no transparency, you can choose one colour that will be masked in your bitmap. the final shape of :class:`AdvancedSplash` will be defined only by non-transparent (non-masked) pixels.
======================= =========== ==================================================


Events Processing
=================

`No custom events are available for this class.`


License And Version
===================

:class:`AdvancedSplash` control is distributed under the wxPython license.

Latest revision: Andrea Gavana @ 19 Dec 2012, 21.00 GMT

Version 0.5

"""


#----------------------------------------------------------------------
# Beginning Of ADVANCEDSPLASH wxPython Code
#----------------------------------------------------------------------

import wx

# These Are Used To Declare If The AdvancedSplash Should Be Destroyed After The
# Timeout Or Not
                        
AS_TIMEOUT = 1
""" :class:`AdvancedSplash` will be destroyed after `timeout` milliseconds. """
AS_NOTIMEOUT = 2
""" :class:`AdvancedSplash` can be destroyed by clicking on it, pressing a key or by explicitly call the `Close()` method. """

# These Flags Are Used To Position AdvancedSplash Correctly On Screen
AS_CENTER_ON_SCREEN = 4
""" :class:`AdvancedSplash` will be centered on screen. """
AS_CENTER_ON_PARENT = 8
""" :class:`AdvancedSplash` will be centered on parent. """
AS_NO_CENTER = 16
""" :class:`AdvancedSplash` will not be centered. """

# This Option Allow To Mask A Colour In The Input Bitmap
AS_SHADOW_BITMAP = 32
""" If the bitmap you pass as input has no transparency, you can choose one colour that will be masked in your bitmap. the final shape of :class:`AdvancedSplash` will be defined only by non-transparent (non-masked) pixels. """

#----------------------------------------------------------------------
# ADVANCEDSPLASH Class
# This Is The Main Class Implementation. See __init__() Method For
# Details.
#----------------------------------------------------------------------

class AdvancedSplash(wx.Frame):
    """
    :class:`AdvancedSplash` tries to reproduce the behavior of :class:`~adv.SplashScreen`, with
    some enhancements.

    This is the main class implementation.    
    """
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.STAY_ON_TOP,
                 bitmap=None, timeout=5000,
                 agwStyle=AS_TIMEOUT | AS_CENTER_ON_SCREEN,
                 shadowcolour=wx.NullColour):
        """
        Default class constructor.

        :param `parent`: parent window;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param integer `style`: the underlying :class:`Frame` style;
        :param `bitmap`: this must be a valid bitmap, that you may construct using
         whatever image file format supported by wxPython. If the file you load
         already supports mask/transparency (like png), the transparent areas
         will not be drawn on screen, and the :class:`AdvancedSplash` frame will have
         the shape defined only by *non-transparent* pixels.
         If you use other file formats that does not supports transparency, you
         can obtain the same effect as above by masking a specific colour in
         your :class:`Bitmap`.
        :param integer `timeout`: if you construct :class:`AdvancedSplash` using the style ``AS_TIMEOUT``,
         :class:`AdvancedSplash` will be destroyed after `timeout` milliseconds;
        :param integer `agwStyle`: this value specifies the :class:`AdvancedSplash` styles:
        
         ======================= =========== ==================================================
         Window Styles           Hex Value   Description
         ======================= =========== ==================================================
         ``AS_TIMEOUT``                  0x1 :class:`AdvancedSplash` will be destroyed after `timeout` milliseconds.
         ``AS_NOTIMEOUT``                0x2 :class:`AdvancedSplash` can be destroyed by clicking on it, pressing a key or by explicitly call the `Close()` method.
         ``AS_CENTER_ON_SCREEN``         0x4 :class:`AdvancedSplash` will be centered on screen.
         ``AS_CENTER_ON_PARENT``         0x8 :class:`AdvancedSplash` will be centered on parent.
         ``AS_NO_CENTER``               0x10 :class:`AdvancedSplash` will not be centered.
         ``AS_SHADOW_BITMAP``           0x20 If the bitmap you pass as input has no transparency, you can choose one colour that will be masked in your bitmap. the final shape of :class:`AdvancedSplash` will be defined only by non-transparent (non-masked) pixels.
         ======================= =========== ==================================================

        :param `shadowcolour`: if you construct :class:`AdvancedSplash` using the style
         ``AS_SHADOW_BITMAP``, here you can specify the colour that will be masked on
         your input bitmap. This has to be a valid wxPython colour.

        :type parent: :class:`Window`
        :type pos: tuple or :class:`Point`
        :type size: tuple or :class:`Size`
        :type bitmap: :class:`Bitmap`
        :type shadowcolour: :class:`Colour`

        :raise: `Exception` in the following cases:

         - The ``AS_TIMEOUT`` style is set but `timeout` is not a positive integer;
         - The ``AS_SHADOW_BITMAP`` style is set but `shadowcolour` is not a valid wxPython colour;
         - The :class:`AdvancedSplash` bitmap is an invalid :class:`Bitmap`.
         
        """

        wx.Frame.__init__(self, parent, id, "", pos, size, style)

        # Some Error Checking
        if agwStyle & AS_TIMEOUT and timeout <= 0:
            raise Exception('\nERROR: Style "AS_TIMEOUT" Used With Invalid "timeout" Parameter Value (' \
                            + str(timeout) + ')')

        if agwStyle & AS_SHADOW_BITMAP and not shadowcolour.IsOk():
            raise Exception('\nERROR: Style "AS_SHADOW_BITMAP" Used With Invalid "shadowcolour" Parameter')

        if not bitmap or not bitmap.IsOk():
            raise Exception("\nERROR: Bitmap Passed To AdvancedSplash Is Invalid.")

        if agwStyle & AS_SHADOW_BITMAP:
            # Our Bitmap Is Masked Accordingly To User Input
            self.bmp = self.ShadowBitmap(bitmap, shadowcolour)
        else:
            self.bmp = bitmap

        self._agwStyle = agwStyle

        # Setting Initial Properties
        self.SetText()
        self.SetTextFont()
        self.SetTextPosition()
        self.SetTextColour()

        # Calculate The Shape Of AdvancedSplash Using The Input-Modified Bitmap
        self.reg = wx.Region(self.bmp)

        # Don't Know If It Works On Other Platforms!!
        # Tested Only In Windows XP/2000

        if wx.Platform == "__WXGTK__":
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetSplashShape)
        else:
            self.SetSplashShape()

        w = self.bmp.GetWidth() + 1
        h = self.bmp.GetHeight() + 1

        # Set The AdvancedSplash Size To The Bitmap Size
        self.SetClientSize((w, h))

        if agwStyle & AS_CENTER_ON_SCREEN:
            self.CenterOnScreen()
        elif agwStyle & AS_CENTER_ON_PARENT:
            self.CenterOnParent()

        if agwStyle & AS_TIMEOUT:
            # Starts The Timer. Once Expired, AdvancedSplash Is Destroyed
            self._splashtimer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.OnNotify)
            self._splashtimer.Start(timeout)

        # Catch Some Mouse Events, To Behave Like wx.SplashScreen
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvents)
        self.Bind(wx.EVT_CHAR, self.OnCharEvents)

        self.Show()
        if wx.Platform == "__WXMAC__":
            wx.SafeYield(self, True)


    def SetSplashShape(self, event=None):
        """
        Sets :class:`AdvancedSplash` shape using the region created from the bitmap.

        :param `event`: a :class:`WindowCreateEvent` event (GTK only, as GTK supports setting
         the window shape only during window creation).
        """

        self.SetShape(self.reg)

        if event is not None:
            event.Skip()


    def ShadowBitmap(self, bmp, shadowcolour):
        """
        Applies a mask on the bitmap accordingly to user input.

        :param `bmp`: the bitmap to which we want to apply the mask colour `shadowcolour`;
        :param `shadowcolour`: the mask colour for our bitmap.
        :type bmp: :class:`Bitmap`
        :type shadowcolour: :class:`Colour`

        :return: A masked version of the input bitmap, an instance of :class:`Bitmap`.        
        """

        mask = wx.Mask(bmp, shadowcolour)
        bmp.SetMask(mask)

        return bmp


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`AdvancedSplash`.

        :param `event`: a :class:`PaintEvent` to be processed.
        """

        dc = wx.PaintDC(self)

        # Here We Redraw The Bitmap Over The Frame
        dc.DrawBitmap(self.bmp, 0, 0, True)

        # We Draw The Text Anyway, Wheter It Is Empty ("") Or Not
        textcolour = self.GetTextColour()
        textfont = self.GetTextFont()
        textpos = self.GetTextPosition()
        text = self.GetText()

        dc.SetFont(textfont[0])
        dc.SetTextForeground(textcolour)
        dc.DrawText(text, textpos[0], textpos[1])


    def OnNotify(self, event):
        """
        Handles the timer expiration, and calls the `Close()` method.

        :param `event`: a :class:`wx.TimerEvent` to be processed.
        """

        self.Close()


    def OnMouseEvents(self, event):
        """
        Handles the ``wx.EVT_MOUSE_EVENTS`` events for :class:`AdvancedSplash`.

        :param `event`: a :class:`MouseEvent` to be processed.
        
        :note: This reproduces the behavior of :class:`~adv.SplashScreen`.
        """

        if event.LeftDown() or event.RightDown():
            self.Close()

        event.Skip()


    def OnCharEvents(self, event):
        """
        Handles the ``wx.EVT_CHAR`` event for :class:`AdvancedSplash`.

        :param `event`: a :class:`KeyEvent` to be processed.
        
        :note: This reproduces the behavior of :class:`~adv.SplashScreen`.
        """

        self.Close()


    def OnCloseWindow(self, event):
        """
        Handles the ``wx.EVT_CLOSE`` event for :class:`AdvancedSplash`.

        :param `event`: a :class:`CloseEvent` to be processed.
        
        :note: This reproduces the behavior of :class:`~adv.SplashScreen`.
        """

        if hasattr(self, "_splashtimer"):
            self._splashtimer.Stop()
            del self._splashtimer

        self.Destroy()


    def SetText(self, text=None):
        """
        Sets the text to be displayed on :class:`AdvancedSplash`.

        :param `text`: the text we want to display on top of the bitmap. If `text` is
         set to ``None``, nothing will be drawn on top of the bitmap.
        :type text: string or ``None``
        """

        if text is None:
            text = ""

        self._text = text

        self.Refresh()
        self.Update()


    def GetText(self):
        """
        Returns the text displayed on :class:`AdvancedSplash`.

        :return: A string representing the text drawn on top of the :class:`AdvancedSplash` bitmap.
        """

        return self._text


    def SetTextFont(self, font=None):
        """
        Sets the font for the text in :class:`AdvancedSplash`.

        :param `font`: the font to use while drawing the text on top of our bitmap. If `font`
         is ``None``, a simple generic font is generated.
        :type font: :class:`Font` or ``None``         
        """

        if font is None:
            self._textfont = wx.Font(1, wx.SWISS, wx.NORMAL, wx.BOLD, False)
            self._textsize = 10.0
            self._textfont.SetPointSize(self._textsize)
        else:
            self._textfont = font
            self._textsize = font.GetPointSize()
            self._textfont.SetPointSize(self._textsize)

        self.Refresh()
        self.Update()


    def GetTextFont(self):
        """
        Gets the font for the text in :class:`AdvancedSplash`.

        :return: An instance of :class:`Font` to draw the text and a :class:`Size` object containing
         the text width an height, in pixels.
        """

        return self._textfont, self._textsize


    def SetTextColour(self, colour=None):
        """
        Sets the colour for the text in :class:`AdvancedSplash`.

        :param `colour`: the text colour to use while drawing the text on top of our
         bitmap. If `colour` is ``None``, then ``wx.BLACK`` is used.
        :type colour: :class:`Colour` or ``None``
        """

        if colour is None:
            colour = wx.BLACK

        self._textcolour = colour
        self.Refresh()
        self.Update()


    def GetTextColour(self):
        """
        Gets the colour for the text in :class:`AdvancedSplash`.

        :return: An instance of :class:`Colour`.
        """

        return self._textcolour


    def SetTextPosition(self, position=None):
        """
        Sets the text position inside :class:`AdvancedSplash` frame.

        :param `position`: the text position inside our bitmap. If `position` is ``None``,
         the text will be placed at the top-left corner.
        :type position: tuple or ``None``
        """

        if position is None:
            position = (0, 0)

        self._textpos = position
        self.Refresh()
        self.Update()


    def GetTextPosition(self):
        """
        Returns the text position inside :class:`AdvancedSplash` frame.

        :return: A tuple containing the text `x` and `y` position inside the :class:`AdvancedSplash` frame.
        """

        return self._textpos


    def GetSplashStyle(self):
        """
        Returns a list of strings and a list of integers containing the styles.

        :return: Two Python lists containing the style name and style values for :class:`AdvancedSplash`.
        """

        stringstyle = []
        integerstyle = []

        if self._agwStyle & AS_TIMEOUT:
            stringstyle.append("AS_TIMEOUT")
            integerstyle.append(AS_TIMEOUT)

        if self._agwStyle & AS_NOTIMEOUT:
            stringstyle.append("AS_NOTIMEOUT")
            integerstyle.append(AS_NOTIMEOUT)

        if self._agwStyle & AS_CENTER_ON_SCREEN:
            stringstyle.append("AS_CENTER_ON_SCREEN")
            integerstyle.append(AS_CENTER_ON_SCREEN)

        if self._agwStyle & AS_CENTER_ON_PARENT:
            stringstyle.append("AS_CENTER_ON_PARENT")
            integerstyle.append(AS_CENTER_ON_PARENT)

        if self._agwStyle & AS_NO_CENTER:
            stringstyle.append("AS_NO_CENTER")
            integerstyle.append(AS_NO_CENTER)

        if self._agwStyle & AS_SHADOW_BITMAP:
            stringstyle.append("AS_SHADOW_BITMAP")
            integerstyle.append(AS_SHADOW_BITMAP)

        return stringstyle, integerstyle


if __name__ == '__main__':

    import wx

    app = wx.App(0)

    bitmap = wx.Bitmap(100, 100)    
    splash = AdvancedSplash(None, bitmap=bitmap, timeout=5000)

    app.MainLoop()
