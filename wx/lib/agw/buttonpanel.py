# --------------------------------------------------------------------------- #
# BUTTONPANEL Widget wxPython IMPLEMENTATION
#
# Original C++ Code From Eran. You Can Find It At:
#
# http://wxforum.shadonet.com/viewtopic.php?t=6619
#
# License: wxWidgets license
#
#
# Python Code By:
#
# Andrea Gavana, @ 02 Oct 2006
# Latest Revision: 27 Dec 2012, 21.00 GMT
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
A custom panel class with gradient background shading with the possibility to
add buttons and controls still respecting the gradient background.


Description
===========

With :class:`ButtonPanel` class you have a panel with gradient colouring
on it and with the possibility to place some buttons on it. Using a
standard panel with normal :class:`Button` leads to an ugly result: the
buttons are placed correctly on the panel - but with grey area around
them. Gradient colouring is kept behind the images - this was achieved
due to the PNG format and the transparency of the bitmaps.

The image are functioning like a buttons and can be caught in your
code using the usual::

  self.Bind(wx.EVT_BUTTON, self.OnButton)

method.

The control is generic, and support theming (well, I tested it under
Windows with the three defauls themes: grey, blue, silver and the
classic look).


Usage
=====

:class:`ButtonPanel` supports 4 alignments: left, right, top, bottom, which have a
different meaning and behavior with respect to :class:`ToolBar`. The easiest
thing is to try the demo to understand, but I'll try to explain how it works.

**CASE 1**: :class:`ButtonPanel` has a main caption text.

- Left alignment means :class:`ButtonPanel` is horizontal, with the text aligned to the
  left. When you shrink the demo frame, if there is not enough room for all
  the controls to be shown, the controls closest to the text are hidden;

- Right alignment means :class:`ButtonPanel` is horizontal, with the text aligned to the
  right. Item layout as above;

- Top alignment means :class:`ButtonPanel` is vertical, with the text aligned to the top.
  Item layout as above;

- Bottom alignment means :class:`ButtonPanel` is vertical, with the text aligned to the
  bottom. Item layout as above.


**CASE 2**: :class:`ButtonPanel` has **no** main caption text.

- In this case, left and right alignment are the same (as top and bottom are the same),
  but the layout strategy changes: now if there is not enough room for all the controls
  to be shown, the last added items are hidden ("last" means on the far right for an
  horizontal :class:`ButtonPanel` and far bottom for a vertical :class:`ButtonPanel`).


Usage example::

    import wx
    import wx.lib.agw.buttonpanel as BP

    class MyFrame(wx.Frame):

        def __init__(self, parent, id=-1, title="ButtonPanel", pos=wx.DefaultPosition,
                     size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):

            wx.Frame.__init__(self, parent, id, title, pos, size, style)

            mainPanel = wx.Panel(self, -1)
            self.logtext = wx.TextCtrl(mainPanel, -1, "", style=wx.TE_MULTILINE)

            vSizer = wx.BoxSizer(wx.VERTICAL)
            mainPanel.SetSizer(vSizer)

            titleBar = BP.ButtonPanel(mainPanel, -1, "A Simple Test & Demo")

            btn1 = BP.ButtonInfo(titleBar, wx.ID_ANY, wx.Bitmap("png4.png", wx.BITMAP_TYPE_PNG))
            titleBar.AddButton(btn1)
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn1)

            btn2 = BP.ButtonInfo(titleBar, wx.ID_ANY, wx.Bitmap("png3.png", wx.BITMAP_TYPE_PNG))
            titleBar.AddButton(btn2)
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn2)

            btn3 = BP.ButtonInfo(titleBar, wx.ID_ANY, wx.Bitmap("png2.png", wx.BITMAP_TYPE_PNG))
            titleBar.AddButton(btn3)
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn3)

            btn4 = BP.ButtonInfo(titleBar, wx.ID_ANY, wx.Bitmap("png1.png", wx.BITMAP_TYPE_PNG))
            titleBar.AddButton(btn4)
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn4)

            vSizer.Add(titleBar, 0, wx.EXPAND)
            vSizer.Add((20, 20))
            vSizer.Add(self.logtext, 1, wx.EXPAND | wx.ALL, 5)

            titleBar.DoLayout()
            vSizer.Layout()


        def OnButton(self, event):
            ''' Handler for the ``wx.EVT_BUTTON`` event. '''

            obj = event.GetEventObject()

            # This will print the button label
            print(obj.GetText())


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()



Window Styles
=============

This class supports the following window styles:

==================== =========== ==================================================
Window Styles        Hex Value   Description
==================== =========== ==================================================
``BP_DEFAULT_STYLE``         0x1 :class:`ButtonPanel` has a plain solid background.
``BP_USE_GRADIENT``          0x2 :class:`ButtonPanel` has a gradient shading background.
==================== =========== ==================================================


Events Processing
=================

This class processes the following events:

================= ==================================================
Event Name        Description
================= ==================================================
``wx.EVT_BUTTON`` Process a `wxEVT_COMMAND_BUTTON_CLICKED` event, when a button is clicked.
================= ==================================================


License And Version
===================

:class:`ButtonPanel` is distributed under the wxPython license.

Latest Revision: Andrea Gavana @ 27 Dec 2012, 21.00 GMT

Version 0.7.

"""


import wx

# Some constants to tune the BPArt class
BP_BACKGROUND_COLOUR = 0
""" Background brush colour when no gradient shading exists. """
BP_GRADIENT_COLOUR_FROM = 1
""" Starting gradient colour, used only when ``BP_USE_GRADIENT`` style is applied. """
BP_GRADIENT_COLOUR_TO = 2
""" Ending gradient colour, used only when ``BP_USE_GRADIENT`` style is applied. """
BP_BORDER_COLOUR = 3
""" Pen colour to paint the border of :class:`ButtonPanel`. """
BP_TEXT_COLOUR = 4
""" Main :class:`ButtonPanel` caption colour. """
BP_BUTTONTEXT_COLOUR = 5
""" Text colour for buttons with text. """
BP_BUTTONTEXT_INACTIVE_COLOUR = 6
""" Text colour for inactive buttons with text. """
BP_SELECTION_BRUSH_COLOUR = 7
""" Brush colour to be used when hovering or selecting a button. """
BP_SELECTION_PEN_COLOUR = 8
""" Pen colour to be used when hovering or selecting a button. """
BP_SEPARATOR_COLOUR = 9
""" Pen colour used to paint the separators. """
BP_TEXT_FONT = 10
""" Font of the :class:`ButtonPanel` main caption. """
BP_BUTTONTEXT_FONT = 11
""" Text font for the buttons with text. """

BP_BUTTONTEXT_ALIGN_BOTTOM = 12
""" Flag that indicates the image and text in buttons is stacked. """
BP_BUTTONTEXT_ALIGN_RIGHT = 13
""" Flag that indicates the text is shown alongside the image in buttons with text. """

BP_SEPARATOR_SIZE = 14
""" Separator size. NB: This is not the line width, but the sum of the space before and after the separator line plus the width of the line. """
BP_MARGINS_SIZE = 15
""" Size of the left/right margins in :class:`ButtonPanel` (top/bottom for vertically aligned :class:`ButtonPanel`)."""
BP_BORDER_SIZE = 16
""" Size of the border. """
BP_PADDING_SIZE = 17
""" Inter-tool separator size. """

# Caption Gradient Type
BP_GRADIENT_NONE = 0
""" No gradient shading should be used to paint the background. """
BP_GRADIENT_VERTICAL = 1
""" Vertical gradient shading should be used to paint the background. """
BP_GRADIENT_HORIZONTAL = 2
""" Horizontal gradient shading should be used to paint the background. """

# Flags for HitTest() method
BP_HT_BUTTON = 200
""" This flag indicates that the user has hit a button inside :class:`ButtonPanel`. """
BP_HT_NONE = 201
""" This flag indicates that no buttons were hit inside :class:`ButtonPanel`. """

# Alignment of buttons in the panel
BP_ALIGN_RIGHT = 1
""" Aligns the buttons to the right (for an horizontal :class:`ButtonPanel`). """
BP_ALIGN_LEFT = 2
""" Aligns the buttons to the left (for an horizontal :class:`ButtonPanel`). """
BP_ALIGN_TOP = 4
""" Aligns the buttons at the top (for a vertical :class:`ButtonPanel`). """
BP_ALIGN_BOTTOM = 8
""" Aligns the buttons at the bottom (for a vertical :class:`ButtonPanel`). """

# ButtonPanel styles
BP_DEFAULT_STYLE = 1
""" :class:`ButtonPanel` has a plain solid background. """
BP_USE_GRADIENT = 2
""" :class:`ButtonPanel` has a gradient shading background. """

# Delay used to cancel the longHelp in the statusbar field
_DELAY = 3000


# Check for the new method in 2.7 (not present in 2.6.3.3)
if wx.VERSION_STRING < "2.7":
    wx.Rect.Contains = lambda self, point: wx.Rect.Inside(self, point)


def BrightenColour(colour, factor):
    """
    Brighten the input colour by a factor.

    :param `colour`: a valid :class:`wx.Colour` instance;
    :param integer `factor`: the factor by which the input colour should be brightened.

    :return: An instance of :class:`wx.Colour`, a brightened version of the input `colour`.
    """

    val = colour.Red()*factor
    if val > 255:
        red = 255
    else:
        red = val

    val = colour.Green()*factor
    if val > 255:
        green = 255
    else:
        green = val

    val = colour.Blue()*factor
    if val > 255:
        blue = 255
    else:
        blue = val

    return wx.Colour(int(red), int(green), int(blue))


# ----------------------------------------------------------------------------

def MakeDisabledBitmap(original):
    """
    Creates a disabled-looking bitmap starting from the input one.

    :param `original`: an instance of :class:`wx.Bitmap` to be greyed-out.

    :return: A greyed-out representation of the input bitmap, an instance of :class:`wx.Bitmap`.
    """

    img = original.ConvertToImage()
    return wx.Bitmap(img.ConvertToGreyscale())


# ---------------------------------------------------------------------------- #
# Class BPArt
# Handles all the drawings for buttons, separators and text and allows the
# programmer to set colours, sizes and gradient shadings for ButtonPanel
# ---------------------------------------------------------------------------- #

class BPArt(object):
    """
    :class:`BPArt` is an art provider class which does all of the drawing for :class:`ButtonPanel`.
    This allows the library caller to customize the :class:`BPArt` or to completely replace
    all drawing with custom BPArts.
    """

    def __init__(self, parentStyle):
        """
        Default class constructor.

        :param integer `parentStyle`: the window style for :class:`ButtonPanel`.
        """

        base_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)

        self._background_brush = wx.Brush(base_colour, wx.BRUSHSTYLE_SOLID)
        self._gradient_colour_to = wx.WHITE
        self._gradient_colour_from = wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)

        if parentStyle & BP_USE_GRADIENT:
            self._border_pen = wx.Pen(wx.WHITE, 3)
            self._caption_text_colour = wx.WHITE
            self._buttontext_colour = wx.Colour(70, 143, 255)
            self._separator_pen = wx.Pen(BrightenColour(self._gradient_colour_from, 1.4))
            self._gradient_type = BP_GRADIENT_VERTICAL
        else:
            self._border_pen = wx.Pen(BrightenColour(base_colour, 0.9), 3)
            self._caption_text_colour = wx.BLACK
            self._buttontext_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT)
            self._separator_pen = wx.Pen(BrightenColour(base_colour, 0.9))
            self._gradient_type = BP_GRADIENT_NONE

        self._buttontext_inactive_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self._selection_brush = wx.Brush(wx.Colour(225, 225, 255))
        self._selection_pen = wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))

        sysfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self._caption_font = wx.Font(sysfont.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                                     False, sysfont.GetFaceName())
        self._buttontext_font = wx.Font(sysfont.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                                        False, sysfont.GetFaceName())

        self._separator_size = 7
        self._margins_size = wx.Size(6, 6)
        self._caption_border_size = 3
        self._padding_size = wx.Size(6, 6)


    def GetMetric(self, id):
        """
        Returns the option value for the specified size `id`.

        :param integer `id`: the identification bit for the size value. This can be one of the
         following bits:

         ============================== ======= =====================================
         Size Id                         Value  Description
         ============================== ======= =====================================
         ``BP_SEPARATOR_SIZE``               14 Separator size. Note: This is not the line width, but the sum of the space before and after the separator line plus the width of the line
         ``BP_MARGINS_SIZE``                 15 Size of the left/right margins in :class:`ButtonPanel` (top/bottom for vertically aligned :class:`ButtonPanel`)
         ``BP_BORDER_SIZE``                  16 Size of the border
         ``BP_PADDING_SIZE``                 17 Inter-tool separator size
         ============================== ======= =====================================

        :return: An integer representing the option value for the input `id`.

        :raise: `Exception` if the `id` is not recognized.
        """

        if id == BP_SEPARATOR_SIZE:
            return self._separator_size
        elif id == BP_MARGINS_SIZE:
            return self._margins_size
        elif id == BP_BORDER_SIZE:
            return self._caption_border_size
        elif id == BP_PADDING_SIZE:
            return self._padding_size
        else:
            raise Exception("\nERROR: Invalid Metric Ordinal. ")


    def SetMetric(self, id, new_val):
        """
        Sets the option value for the specified size `id`.

        :param integer `id`: the identification bit for the size value;
        :param integer `new_val`: the new value for the size.

        :raise: `Exception` if the `id` is not recognized.

        :see: :meth:`~BPArt.GetMetric` for a list of meaningful size ids.
        """

        if id == BP_SEPARATOR_SIZE:
            self._separator_size = new_val
        elif id == BP_MARGINS_SIZE:
            self._margins_size = new_val
        elif id == BP_BORDER_SIZE:
            self._caption_border_size = new_val
            self._border_pen.SetWidth(new_val)
        elif id == BP_PADDING_SIZE:
            self._padding_size = new_val
        else:
            raise Exception("\nERROR: Invalid Metric Ordinal. ")


    def GetColour(self, id):
        """
        Returns the option value for the specified colour `id`.

        :param integer `id`: the identification bit for the colour value. This can be one of the
         following bits:

         ================================== ======= =====================================
         Colour Id                           Value  Description
         ================================== ======= =====================================
         ``BP_BACKGROUND_COLOUR``                 0 Background brush colour when no gradient shading exists
         ``BP_GRADIENT_COLOUR_FROM``              1 Starting gradient colour, used only when ``BP_USE_GRADIENT`` style is applied
         ``BP_GRADIENT_COLOUR_TO``                2 Ending gradient colour, used only when ``BP_USE_GRADIENT`` style is applied
         ``BP_BORDER_COLOUR``                     3 Pen colour to paint the border of :class:`ButtonPanel`
         ``BP_TEXT_COLOUR``                       4 Main :class:`ButtonPanel` caption colour
         ``BP_BUTTONTEXT_COLOUR``                 5 Text colour for buttons with text
         ``BP_BUTTONTEXT_INACTIVE_COLOUR``        6 Text colour for inactive buttons with text
         ``BP_SELECTION_BRUSH_COLOUR``            7 Brush colour to be used when hovering or selecting a button
         ``BP_SELECTION_PEN_COLOUR``              8 Pen colour to be used when hovering or selecting a button
         ``BP_SEPARATOR_COLOUR``                  9 Pen colour used to paint the separators
         ================================== ======= =====================================

        :return: An instance of :class:`wx.Colour` for the input `id`.

        :raise: `Exception` if the `id` is not recognized.
        """

        if id == BP_BACKGROUND_COLOUR:
            return self._background_brush.GetColour()
        elif id == BP_GRADIENT_COLOUR_FROM:
            return self._gradient_colour_from
        elif id == BP_GRADIENT_COLOUR_TO:
            return self._gradient_colour_to
        elif id == BP_BORDER_COLOUR:
            return self._border_pen.GetColour()
        elif id == BP_TEXT_COLOUR:
            return self._caption_text_colour
        elif id == BP_BUTTONTEXT_COLOUR:
            return self._buttontext_colour
        elif id == BP_BUTTONTEXT_INACTIVE_COLOUR:
            return self._buttontext_inactive_colour
        elif id == BP_SELECTION_BRUSH_COLOUR:
            return self._selection_brush.GetColour()
        elif id == BP_SELECTION_PEN_COLOUR:
            return self._selection_pen.GetColour()
        elif id == BP_SEPARATOR_COLOUR:
            return self._separator_pen.GetColour()
        else:
            raise Exception("\nERROR: Invalid Colour Ordinal. ")


    def SetColour(self, id, colour):
        """
        Sets the option value for the specified colour `id`.

        :param integer `id`: the identification bit for the colour value;
        :param `colour`: the new value for the colour (a valid :class:`wx.Colour` instance).

        :raise: `Exception` if the `id` is not recognized.

        :see: :meth:`~BPArt.GetColour` for a list of meaningful colour ids.
        """

        if id == BP_BACKGROUND_COLOUR:
            self._background_brush.SetColour(colour)
        elif id == BP_GRADIENT_COLOUR_FROM:
            self._gradient_colour_from = colour
        elif id == BP_GRADIENT_COLOUR_TO:
            self._gradient_colour_to = colour
        elif id == BP_BORDER_COLOUR:
            self._border_pen.SetColour(colour)
        elif id == BP_TEXT_COLOUR:
            self._caption_text_colour = colour
        elif id == BP_BUTTONTEXT_COLOUR:
            self._buttontext_colour = colour
        elif id == BP_BUTTONTEXT_INACTIVE_COLOUR:
            self._buttontext_inactive_colour = colour
        elif id == BP_SELECTION_BRUSH_COLOUR:
            self._selection_brush.SetColour(colour)
        elif id == BP_SELECTION_PEN_COLOUR:
            self._selection_pen.SetColour(colour)
        elif id == BP_SEPARATOR_COLOUR:
            self._separator_pen.SetColour(colour)
        else:
            raise Exception("\nERROR: Invalid Colour Ordinal. ")


    GetColor = GetColour
    SetColor = SetColour


    def GetFont(self, id):
        """
        Returns the option value for the specified font `id`.

        :param integer `id`: the identification bit for the font value. This can be one of the
         following bits:

         ============================== ======= =====================================
         Size Id                         Value  Description
         ============================== ======= =====================================
         ``BP_TEXT_FONT``                    10 Font of the :class:`ButtonPanel` main caption
         ``BP_BUTTONTEXT_FONT``              11 Text font for the buttons with text
         ============================== ======= =====================================

        :return: An instance of :class:`wx.Font` for the input `id`.

        :raise: `Exception` if the `id` is not recognized.
        """

        if id == BP_TEXT_FONT:
            return self._caption_font
        elif id == BP_BUTTONTEXT_FONT:
            return self._buttontext_font

        return wx.NoneFont


    def SetFont(self, id, font):
        """
        Sets the option value for the specified font `id`.

        :param integer `id`: the identification bit for the font value;
        :param `colour`: the new value for the font (a valid :class:`wx.Font` instance).

        :raise: `Exception` if the `id` is not recognized.

        :see: :meth:`~BPArt.GetFont` for a list of meaningful font ids.
        """

        if id == BP_TEXT_FONT:
            self._caption_font = font
        elif id == BP_BUTTONTEXT_FONT:
            self._buttontext_font = font


    def SetGradientType(self, gradient):
        """
        Sets the gradient type for :class:`BPArt` drawings.

        :param integer `gradient`: can be one of the following bits:

         ============================ ======= ============================
         Gradient Type                 Value  Description
         ============================ ======= ============================
         ``BP_GRADIENT_NONE``               0 No gradient shading should be used to paint the background
         ``BP_GRADIENT_VERTICAL``           1 Vertical gradient shading should be used to paint the background
         ``BP_GRADIENT_HORIZONTAL``         2 Horizontal gradient shading should be used to paint the background
         ============================ ======= ============================

        """

        self._gradient_type = gradient


    def GetGradientType(self):
        """
        Returns the gradient type for :class:`BPArt` drawings.

        :return: An integer representing the gradient type.

        :see: :meth:`~BPArt.SetGradientType` for a list of possible gradient types.
        """

        return self._gradient_type


    def DrawSeparator(self, dc, rect, isVertical):
        """
        Draws a separator in :class:`ButtonPanel`.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the separator client rectangle;
        :param bool `isVertical`: ``True`` if :class:`ButtonPanel` is in vertical orientation,
         ``False`` otherwise.
        """

        dc.SetPen(self._separator_pen)

        if isVertical:
            ystart = yend = rect.y + rect.height//2
            xstart = int(rect.x + 1.5*self._caption_border_size)
            xend = int(rect.x + rect.width - 1.5*self._caption_border_size)
            dc.DrawLine(xstart, ystart, xend, yend)
        else:
            xstart = xend = rect.x + rect.width//2
            ystart = int(rect.y + 1.5*self._caption_border_size)
            yend = int(rect.y + rect.height - 1.5*self._caption_border_size)
            dc.DrawLine(xstart, ystart, xend, yend)


    def DrawCaption(self, dc, rect, captionText):
        """
        Draws the main caption text in :class:`ButtonPanel`.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the main caption text rectangle;
        :param string `captionText`: the caption text string.
        """

        textColour = self._caption_text_colour
        textFont = self._caption_font
        padding = self._padding_size

        dc.SetTextForeground(textColour)
        dc.SetFont(textFont)

        dc.DrawText(captionText, rect.x + padding.x, rect.y+padding.y)


    def DrawButton(self, dc, rect, buttonBitmap, isVertical, buttonStatus,
                   isToggled, textAlignment, text=""):
        """
        Draws a button in :class:`ButtonPanel`, together with its text (if any).

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the button client rectangle;
        :param wx.Bitmap `buttonBitmap`: the bitmap associated with the button;
        :param bool `isVertical`: ``True`` if :class:`ButtonPanel` is in vertical orientation,
         ``False`` otherwise;
        :param string `buttonStatus`: one of "Normal", "Toggled", "Pressed", "Disabled" or "Hover";
        :param bool `isToggled`: whether the button is toggled or not;
        :param integer `textAlignment`: the text alignment inside the button;
        :param string `text`: the button label.
        """

        bmpxsize, bmpysize = buttonBitmap.GetWidth(), buttonBitmap.GetHeight()
        dx = dy = focus = 0

        borderw = self._caption_border_size
        padding = self._padding_size

        buttonFont = self._buttontext_font
        dc.SetFont(buttonFont)

        if isVertical:

            rect = wx.Rect(borderw, rect.y, rect.width-2*borderw, rect.height)

            if text != "":

                textW, textH = dc.GetTextExtent(text)

                if textAlignment == BP_BUTTONTEXT_ALIGN_RIGHT:
                    fullExtent = bmpxsize + padding.x//2 + textW
                    bmpypos = rect.y + (rect.height - bmpysize)//2
                    bmpxpos = rect.x + (rect.width - fullExtent)//2
                    textxpos = bmpxpos + padding.x//2 + bmpxsize
                    textypos = bmpypos + (bmpysize - textH)//2
                else:
                    bmpxpos = rect.x + (rect.width - bmpxsize)//2
                    bmpypos = rect.y + padding.y
                    textxpos = rect.x + (rect.width - textW)//2
                    textypos = bmpypos + bmpysize + padding.y//2
            else:
                bmpxpos = rect.x + (rect.width - bmpxsize)//2
                bmpypos = rect.y + (rect.height - bmpysize)//2


        else:

            rect = wx.Rect(rect.x, borderw, rect.width, rect.height-2*borderw)

            if text != "":

                textW, textH = dc.GetTextExtent(text)

                if textAlignment == BP_BUTTONTEXT_ALIGN_RIGHT:
                    fullExtent = bmpxsize + padding.x//2 + textW
                    bmpypos = rect.y + (rect.height - bmpysize)//2
                    bmpxpos = rect.x + (rect.width - fullExtent)//2
                    textxpos = bmpxpos + padding.x//2 + bmpxsize
                    textypos = bmpypos + (bmpysize - textH)//2
                else:
                    fullExtent = bmpysize + padding.y//2 + textH
                    bmpxpos = rect.x + (rect.width - bmpxsize)//2
                    bmpypos = rect.y + (rect.height - fullExtent)//2
                    textxpos = rect.x + (rect.width - textW)//2
                    textypos = bmpypos + bmpysize + padding.y//2
            else:
                bmpxpos = rect.x + (rect.width - bmpxsize)//2
                bmpypos = rect.y + (rect.height - bmpysize)//2

        # Draw a button
        # [ Padding | Text | .. Buttons .. | Padding ]

        if buttonStatus in ["Pressed", "Toggled", "Hover"]:
            dc.SetBrush(self._selection_brush)
            dc.SetPen(self._selection_pen)
            dc.DrawRoundedRectangle(rect, 4)

        if buttonStatus == "Pressed" or isToggled:
            dx = dy = 1

        if buttonBitmap:
            dc.DrawBitmap(buttonBitmap, bmpxpos+dx, bmpypos+dy, True)

        if text != "":
            isEnabled = buttonStatus != "Disabled"
            self.DrawLabel(dc, text, isEnabled, textxpos+dx, textypos+dy)


    def DrawLabel(self, dc, text, isEnabled, xpos, ypos):
        """
        Draws the label for a button.

        :param `dc`: an instance of :class:`wx.DC`;
        :param string `text`: the button label;
        :param bool `isEnabled`: ``True`` if the button is enabled, ``False`` otherwise;
        :param integer `xpos`: the text `x` position inside the button;
        :param integer `ypos`: the text `y` position inside the button.
        """

        if not isEnabled:
            dc.SetTextForeground(self._buttontext_inactive_colour)
        else:
            dc.SetTextForeground(self._buttontext_colour)

        dc.DrawText(text, xpos, ypos)


    def DrawButtonPanel(self, dc, rect, style):
        """
        Paint the :class:`ButtonPanel`'s background.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the :class:`ButtonPanel` client rectangle;
        :param integer `style`: the :class:`ButtonPanel` window style.
        """

        if style & BP_USE_GRADIENT:
            # Draw gradient colour in the backgroud of the panel
            self.FillGradientColour(dc, rect)

        # Draw a rectangle around the panel
        backBrush = (style & BP_USE_GRADIENT and [wx.TRANSPARENT_BRUSH] or \
                     [self._background_brush])[0]

        dc.SetBrush(backBrush)
        dc.SetPen(self._border_pen)
        dc.DrawRectangle(rect)


    def FillGradientColour(self, dc, rect):
        """
        Gradient fill from colour 1 to colour 2 with top to bottom or left to right.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the :class:`ButtonPanel` client rectangle.
        """

        if rect.height < 1 or rect.width < 1:
            return

        isVertical = self._gradient_type == BP_GRADIENT_VERTICAL
        size = (isVertical and [rect.height] or [rect.width])[0]
        start = (isVertical and [rect.y] or [rect.x])[0]

        # calculate gradient coefficients

        col2 = self._gradient_colour_from
        col1 = self._gradient_colour_to

        rf, gf, bf = 0, 0, 0
        rstep = float((col2.Red() - col1.Red()))/float(size)
        gstep = float((col2.Green() - col1.Green()))/float(size)
        bstep = float((col2.Blue() - col1.Blue()))/float(size)

        for coord in range(start, start + size):

            currCol = wx.Colour(col1.Red() + int(rf), col1.Green() + int(gf), col1.Blue() + int(bf))
            dc.SetBrush(wx.Brush(currCol, wx.BRUSHSTYLE_SOLID))
            dc.SetPen(wx.Pen(currCol))
            if isVertical:
                dc.DrawLine(rect.x, coord, rect.x + rect.width, coord)
            else:
                dc.DrawLine(coord, rect.y, coord, rect.y + rect.height)

            rf += rstep
            gf += gstep
            bf += bstep


class StatusBarTimer(wx.Timer):
    """ Timer used for deleting :class:`StatusBar` long help after ``_DELAY`` seconds."""

    def __init__(self, owner):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param `owner`: an instance of :class:`ButtonPanel`.
        """

        wx.Timer.__init__(self)
        self._owner = owner


    def Notify(self):
        """ The timer has expired. """

        self._owner.OnStatusBarTimer()


class Control(wx.EvtHandler):
    """
    This class represents a base class for all pseudo controls used in
    :class:`ButtonPanel`.
    """

    def __init__(self, parent, size=wx.Size(-1, -1), id=wx.ID_ANY):
        """
        Default class constructor.

        :param wx.Window `parent`: the control parent object. Must not be ``None``;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `id`: window identifier. A value of -1 indicates a default value.
        """

        wx.EvtHandler.__init__(self)

        self._parent = parent

        if id == wx.ID_ANY:
            self._id = wx.NewIdRef()
        else:
            self._id = id

        self._size = size
        self._isshown = True
        self._focus = False


    def Show(self, show=True):
        """
        Shows or hide the control.

        :param bool `show`: If ``True`` displays the window. Otherwise, it hides it.
        """

        self._isshown = show


    def Hide(self):
        """
        Hides the control.

        :note: This is functionally equivalent of calling :meth:`~Control.Show` with a ``False`` input.
        """

        self.Show(False)


    def IsShown(self):
        """ Returns ``True`` if the window is shown, ``False`` if it has been hidden. """

        return self._isshown


    def GetId(self):
        """
        Returns the identifier of the window.

        :return: An integer representing the identifier of the window.

        :note: Each window has an integer identifier. If the application has not provided
         one (or the default ``wx.ID_ANY``) an unique identifier with a negative value will
         be generated.
        """

        return self._id


    def GetBestSize(self):
        """
        This functions returns the best acceptable minimal size for the window. For
        example, for a static control, it will be the minimal size such that the control
        label is not truncated. For windows containing subwindows (typically :class:`Panel`),
        the size returned by this function will be the same as the size the window would
        have had after calling `Fit()`.

        :return: An instance of :class:`wx.Size`.
        """

        return self._size


    def Disable(self):
        """
        Disables the control.

        :returns: ``True`` if the window has been disabled, ``False`` if it had been
         already disabled before the call to this function.

        :note: This is functionally equivalent of calling :meth:`~Control.Enable` with a ``False`` flag.
        """

        return self.Enable(False)


    def Enable(self, enable=True):
        """
        Enable or disable the window for user input.

        :param bool `enable`: If ``True``, enables the window for input. If ``False``, disables the window.

        :returns: ``True`` if the window has been enabled or disabled, ``False`` if nothing was
         done, i.e. if the window had already been in the specified state.

        :note: Note that when a parent window is disabled, all of its children are disabled as
         well and they are reenabled again when the parent is.
        """

        self.disabled = not enable
        return True


    def SetFocus(self, focus=True):
        """
        Sets or kills the focus on the control.

        :param bool `focus`: whether the control can receive keyboard inputs or not.
        """

        self._focus = focus


    def HasFocus(self):
        """
        Returns whether the control has the focus or not.

        :return: ``True`` if the control has the focus, ``False`` otherwise.
        """

        return self._focus


    def OnMouseEvent(self, x, y, event):
        """
        Handles the ``wx.EVT_MOUSE_EVENTS`` events for the control.

        :param integer `x`: the mouse `x` position;
        :param integer `y`: the mouse `y` position;
        :param `event`: the :class:`MouseEvent` event to be processed.
        """

        pass


    def Draw(self, rect):
        """
        Handles the drawing of the control.

        :param wx.Rect `rect`: the control client rectangle.
        """

        pass


class Sizer(object):
    """
    This is a mix-in class to add pseudo support to :class:`wx.Sizer`. Just create
    a new class that derives from this class and :class:`wx.Sizer` and intercepts
    any methods that add to the wx sizer.
    """

    def __init__(self):
        """
        Default class constructor.
        For internal use: do not call it in your code!
        """

        self.children = [] # list of child Pseudo Controls

    # Sizer doesn't use the x1,y1,x2,y2 so allow it to
    # be called with or without the coordinates
    def Draw(self, dc, x1=0, y1=0, x2=0, y2=0):
        """ Draws all the children of the sizer. """

        for item in self.children:
            # use sizer coordinates rather than
            # what is passed in
            c = item.GetUserData()
            c.Draw(dc, item.GetRect())


    def GetBestSize(self):
        """
        This functions returns the best acceptable minimal size for the sizer object.

        :return: An instance of :class:`wx.Size`.
        """

        # this should be handled by the wx.Sizer based class
        return self.GetMinSize()


# Pseudo BoxSizer
class BoxSizer(Sizer, wx.BoxSizer):
    """ Pseudo-class that imitates :class:`BoxSizer`. """

    def __init__(self, orient=wx.HORIZONTAL):
        """
        Constructor for :class:`BoxSizer`.

        :param integer `orient`: may be one of ``wx.VERTICAL`` or ``wx.HORIZONTAL`` for creating
         either a column sizer or a row sizer.
        """

        wx.BoxSizer.__init__(self, orient)
        Sizer.__init__(self)

    #-------------------------------------------
    # sizer overrides (only called from Python)
    #-------------------------------------------
    # no support for user data if it's a pseudocontrol
    # since that is already used
    def Add(self, item, proportion=0, flag=0, border=0, userData=None):
        """
        Appends a child item to the sizer.

        :param `item`: the item to be added to :class:`BoxSizer`. Can be an instance of :class:`wx.Window`,
         :class:`wx.Sizer` or a spacer;
        :param integer `proportion`: this parameter is used in :class:`BoxSizer` to indicate if a child of
         a sizer can change its size in the main orientation of the :class:`BoxSizer` - where 0
         stands for not changeable and a value of more than zero is interpreted relative
         to the value of other children of the same :class:`BoxSizer`. For example, you might have
         a horizontal :class:`BoxSizer` with three children, two of which are supposed to change their
         size with the sizer. Then the two stretchable windows would get a value of 1 each to
         make them grow and shrink equally with the sizer's horizontal dimension.
        :param integer `flag`: this parameter can be used to set a number of flags which can be combined using the binary OR operator ``|``.
         Two main behaviours are defined using these flags. One is the border around a window: the border parameter determines the border
         width whereas the flags given here determine which side(s) of the item that the border will be added. The other flags determine
         how the sizer item behaves when the space allotted to the sizer changes, and is somewhat dependent on the specific kind of sizer used:

         +-----------------------------------------------------------------------+------------------------------------------------------------------------------+
         | Sizer Flag                                                            | Description                                                                  |
         +=======================================================================+==============================================================================+
         | | ``wx.TOP``                                                          | These flags are used to specify which side(s) of the sizer                   |
         | | ``wx.BOTTOM``                                                       | item the border width will apply to.                                         |
         | | ``wx.LEFT``                                                         |                                                                              |
         | | ``wx.RIGHT``                                                        |                                                                              |
         | | ``wx.ALL``                                                          |                                                                              |
         +-----------------------------------------------------------------------+------------------------------------------------------------------------------+
         | ``wx.EXPAND``                                                         | The item will be expanded to fill the space assigned to                      |
         |                                                                       | the item.                                                                    |
         +-----------------------------------------------------------------------+------------------------------------------------------------------------------+
         | ``wx.SHAPED``                                                         | The item will be expanded as much as possible while also                     |
         |                                                                       | maintaining its aspect ratio                                                 |
         +-----------------------------------------------------------------------+------------------------------------------------------------------------------+
         | ``wx.FIXED_MINSIZE``                                                  | Normally :class:`wx.Sizer` will use                                          |
         |                                                                       | :meth:`wx.Window.GetEffectiveMinSize` to                                     |
         |                                                                       | determine what the minimal size of window items should be, and will use that |
         |                                                                       | size to calculate the layout. This allows layouts to adjust when an item     |
         |                                                                       | changes and its best size becomes different. If you would rather have a      |
         |                                                                       | window item stay the size it started with then use ``wx.FIXED_MINSIZE``.     |
         +-----------------------------------------------------------------------+------------------------------------------------------------------------------+
         | ``wx.RESERVE_SPACE_EVEN_IF_HIDDEN``                                   | Normally `Sizers` don't allocate space for hidden windows or other items.    |
         |                                                                       | This flag overrides this behavior so that sufficient space is allocated for  |
         |                                                                       | the window even if it isn't visible. This makes it possible to dynamically   |
         |                                                                       | show and hide controls without resizing parent dialog, for example. This     |
         |                                                                       | function is new since wxWidgets version 2.8.8                                |
         +-----------------------------------------------------------------------+------------------------------------------------------------------------------+
         | | ``wx.ALIGN_CENTER`` **or** ``wx.ALIGN_CENTRE``                      | The ``wx.ALIGN*`` flags allow you to specify the alignment of the item       |
         | | ``wx.ALIGN_LEFT``                                                   | within the space allotted to it by the sizer, adjusted for the border if     |
         | | ``wx.ALIGN_RIGHT``                                                  | any.                                                                         |
         | | ``wx.ALIGN_TOP``                                                    |                                                                              |
         | | ``wx.ALIGN_BOTTOM``                                                 |                                                                              |
         | | ``wx.ALIGN_CENTER_VERTICAL`` **or** ``wx.ALIGN_CENTRE_VERTICAL``    |                                                                              |
         | | ``wx.ALIGN_CENTER_HORIZONTAL`` **or** ``wx.ALIGN_CENTRE_HORIZONTAL``|                                                                              |
         +-----------------------------------------------------------------------+------------------------------------------------------------------------------+

        :param integer `border`: determines the border width, if the flag parameter is set
         to include any border flag.
        :param object `userData`: Allows an extra object to be attached to the sizer item,
         for use in derived classes when sizing information is more complex than the
         proportion and flag will allow for.

        :note: there is no support for `userData` parameter if `item` is a pseudocontrol,
         since that is already used.
        """

        # check to see if it's a pseudo object or sizer
        if isinstance(item, Sizer):
            szitem = wx.BoxSizer.Add(self, item, proportion, flag, border, item)
            self.children.append(szitem)
        elif isinstance(item, Control): # Control should be what ever class your controls come from
            sz = item.GetBestSize()
            # add a spacer to track this object
            szitem = wx.BoxSizer.Add(self, sz, proportion, flag, border, item)
            self.children.append(szitem)
        else:
            wx.BoxSizer.Add(self, item, proportion, flag, border, userData)


    def Prepend(self, item, proportion=0, flag=0, border=0, userData=None):
        """
        Prepends a child item to the sizer.

        :see: :meth:`BoxSizer.Add` method for an explanation of the input parameters.
        """

        # check to see if it's a pseudo object or sizer
        if isinstance(item, Sizer):
            szitem = wx.BoxSizer.Prepend(self, item, proportion, flag, border, item)
            self.children.append(szitem)
        elif isinstance(item, Control): # Control should be what ever class your controls come from
            sz = item.GetBestSize()
            # add a spacer to track this object
            szitem = wx.BoxSizer.Prepend(self, sz, proportion, flag, border, item)
            self.children.insert(0,szitem)
        else:
            wx.BoxSizer.Prepend(self, item, proportion, flag, border, userData)


    def Insert(self, before, item, proportion=0, flag=0, border=0, userData=None, realIndex=None):
        """
        Inserts a child item into the sizer.

        :see: :meth:`BoxSizer.Add` method for an explanation of the input parameters.
        """

        # check to see if it's a pseudo object or sizer
        if isinstance(item, Sizer):
            szitem = wx.BoxSizer.Insert(self, before, item, proportion, flag, border, item)
            self.children.append(szitem)
        elif isinstance(item, Control): # Control should be what ever class your controls come from
            sz = item.GetBestSize()
            # add a spacer to track this object
            szitem = wx.BoxSizer.Insert(self, before, sz, proportion, flag, border, item)
            if realIndex is not None:
                self.children.insert(realIndex,szitem)
            else:
                self.children.insert(before,szitem)

        else:
            wx.BoxSizer.Insert(self, before, item, proportion, flag, border, userData)


    def Remove(self, indx, pop=-1):
        """
        Removes an item from the sizer and destroys it.

        This method does not cause any layout or resizing to take place, call
        :meth:`BoxSizer.Layout() <BoxSizer.Layout>` to update the layout on screen after removing a child from
        the sizer.

        :param integer `indx`: the zero-based index of an item to remove;
        :param bool `pop`: whether to remove the sizer item from the list of children.
        """

        if pop >= 0:
            self.children.pop(pop)

        wx.BoxSizer.Remove(self, indx)


    def Layout(self):
        """
        Call this to force layout of the children anew, e.g. after having added a
        child to or removed a child (window, other sizer or space) from the sizer
        while keeping the current dimension.
        """

        for ii, child in enumerate(self.GetChildren()):
            item = child.GetUserData()
            if item and child.IsShown():
                self.SetItemMinSize(ii, *item.GetBestSize())

        wx.BoxSizer.Layout(self)


    def Show(self, item, show=True):
        """
        Shows or hides the sizer item.

        :param `item`: the sizer item we want to show/hide;
        :param bool `show`: ``True`` to show the item, ``False`` to hide it.
        """

        child = self.GetChildren()[item]
        if child and child.GetUserData():
            child.GetUserData().Show(show)

        wx.BoxSizer.Show(self, item, show)


# ---------------------------------------------------------------------------- #
# Class Separator
# This class holds all the information to size and draw a separator inside
# ButtonPanel
# ---------------------------------------------------------------------------- #

class Separator(Control):
    """
    This class holds all the information to size and draw a separator inside
    :class:`ButtonPanel`.
    """

    def __init__(self, parent):
        """
        Default class constructor.

        :param `parent`: the separator parent object, an instance of :class:`ButtonPanel`.
        """

        self._isshown = True
        self._parent = parent
        Control.__init__(self, parent)


    def GetBestSize(self):
        """
        Returns the separator best size.

        :return: An instance of :class:`wx.Size`.
        """

        # 10 is completely arbitrary, but it works anyhow
        if self._parent.IsVertical():
            return wx.Size(10, self._parent._art.GetMetric(BP_SEPARATOR_SIZE))
        else:
            return wx.Size(self._parent._art.GetMetric(BP_SEPARATOR_SIZE), 10)


    def Draw(self, dc, rect):
        """
        Draws the separator. Actually the drawing is done in :class:`BPArt`.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the separator client rectangle.
        """

        if not self.IsShown():
            return

        isVertical = self._parent.IsVertical()
        self._parent._art.DrawSeparator(dc, rect, isVertical)


# ---------------------------------------------------------------------------- #
# Class ButtonPanelText
# This class is used to hold data about the main caption in ButtonPanel
# ---------------------------------------------------------------------------- #

class ButtonPanelText(Control):
    """ This class is used to hold data about the main caption in :class:`ButtonPanel`. """

    def __init__(self, parent, text=""):
        """
        Default class constructor.

        :param `parent`: the text parent object, an instance of :class:`ButtonPanel`;
        :param string `text`: the actual main caption string.
        """

        self._text = text
        self._isshown = True
        self._parent = parent

        Control.__init__(self, parent)


    def GetText(self):
        """
        Returns the caption text.

        :return: A string representing the caption text.
        """

        return self._text


    def SetText(self, text=""):
        """
        Sets the caption text.

        :param string `text`: the main caption string.
        """

        self._text = text


    def CreateDC(self):
        """ Convenience function to create a :class:`wx.DC`. """

        dc = wx.ClientDC(self._parent)
        textFont = self._parent._art.GetFont(BP_TEXT_FONT)
        dc.SetFont(textFont)

        return dc


    def GetBestSize(self):
        """
        Returns the best size for the main caption in :class:`ButtonPanel`.

        :return: An instance of :class:`wx.Size`.
        """

        if self._text == "":
            return wx.Size(0, 0)

        dc = self.CreateDC()
        rect = self._parent.GetClientRect()

        tw, th = dc.GetTextExtent(self._text)
        padding = self._parent._art.GetMetric(BP_PADDING_SIZE)
        self._size = wx.Size(tw+2*padding.x, th+2*padding.y)

        return self._size


    def Draw(self, dc, rect):
        """
        Draws the main caption. Actually the drawing is done in :class:`BPArt`.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the main caption text client rectangle.
        """

        if not self.IsShown():
            return

        captionText = self.GetText()
        self._parent._art.DrawCaption(dc, rect, captionText)


# -- ButtonInfo class implementation ----------------------------------------
# This class holds information about every button that is added to
# ButtonPanel.  It is an auxiliary class that you should use
# every time you add a button.

class ButtonInfo(Control):
    """
    This class holds information about every button that is added to
    :class:`ButtonPanel`. It is an auxiliary class that you should use
    every time you add a button.
    """
    def __init__(self, parent, id=wx.ID_ANY, bmp=wx.NullBitmap,
                 status="Normal", text="", kind=wx.ITEM_NORMAL,
                 shortHelp="", longHelp=""):
        """
        Default class constructor.

        :param `parent`: the parent window (:class:`ButtonPanel`);
        :param integer `id`: the button id;
        :param wx.Bitmap `bmp`: the associated bitmap;
        :param string `status`: button status ("Pressed", "Hover", "Normal", "Toggled", "Disabled");
        :param string `text`: text to be displayed either below of to the right of the button;
        :param integer `kind`: button kind, may be ``wx.ITEM_NORMAL`` for standard buttons or
         ``wx.ITEM_CHECK`` for toggle buttons;
        :param string `shortHelp`: a short help to be shown in the button tooltip;
        :param string `longHelp`: this string is shown in the statusbar (if any) of the parent
         frame when the mouse pointer is inside the button.
        """

        if id == wx.ID_ANY:
            id = wx.NewIdRef()

        self._status = status
        self._rect = wx.Rect()
        self._text = text
        self._kind = kind
        self._toggle = False
        self._textAlignment = BP_BUTTONTEXT_ALIGN_BOTTOM
        self._shortHelp = shortHelp
        self._longHelp = longHelp

        if bmp and bmp.IsOk():
            disabledbmp = MakeDisabledBitmap(bmp)
        else:
            disabledbmp = wx.NullBitmap

        self._bitmaps = {"Normal": bmp, "Toggled": None, "Disabled": disabledbmp,
                         "Hover": None, "Pressed": None}

        Control.__init__(self, parent, id=id)


    def GetBestSize(self):
        """
        Returns the best size for the button.

        :return: An instance of :class:`wx.Size`.
        """

        xsize = self.GetBitmap().GetWidth()
        ysize = self.GetBitmap().GetHeight()

        if self.HasText():
            # We have text in the button
            dc = wx.ClientDC(self._parent)
            normalFont = self._parent._art.GetFont(BP_BUTTONTEXT_FONT)
            dc.SetFont(normalFont)
            tw, th = dc.GetTextExtent(self.GetText())

            if self.GetTextAlignment() == BP_BUTTONTEXT_ALIGN_BOTTOM:
                xsize = max(xsize, tw)
                ysize = ysize + th
            else:
                xsize = xsize + tw
                ysize = max(ysize, th)

        border = self._parent._art.GetMetric(BP_BORDER_SIZE)
        padding = self._parent._art.GetMetric(BP_PADDING_SIZE)

        if self._parent.IsVertical():
            xsize = xsize + 2*border
        else:
            ysize = ysize + 2*border

        self._size = wx.Size(xsize+2*padding.x, ysize+2*padding.y)

        return self._size


    def Draw(self, dc, rect):
        """
        Draws the button on :class:`ButtonPanel`. Actually the drawing is done in :class:`BPArt`.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the main caption text client rectangle.
        """

        if not self.IsShown():
            return

        buttonBitmap = self.GetBitmap()
        isVertical = self._parent.IsVertical()
        text = self.GetText()
        buttonStatus = self.GetStatus()
        isToggled = self.GetToggled()
        textAlignment = self.GetTextAlignment()

        self._parent._art.DrawButton(dc, rect, buttonBitmap, isVertical,
                                     buttonStatus, isToggled, textAlignment, text)

        self.SetRect(rect)


    def CheckRefresh(self, status):
        """
        Checks whether a :class:`ButtonPanel` repaint is needed or not. This is a convenience function.

        :param bool `status`: the status of a newly added :class:`ButtonInfo` or a change in the
         :class:`ButtonInfo` status.
        """

        if status == self._status:
            self._parent.RefreshRect(self.GetRect())


    def SetBitmap(self, bmp, status="Normal"):
        """
        Sets the bitmap associated with this instance of :class:`ButtonInfo`.

        :param `bmp`: a valid :class:`wx.Bitmap` object;
        :param string `status`: the :class:`ButtonInfo` status ("Pressed", "Hover", "Normal",
         "Toggled", "Disabled").
        """

        self._bitmaps[status] = bmp
        self.CheckRefresh(status)


    def GetBitmap(self, status=None):
        """
        Returns the bitmap associated with this instance of :class:`ButtonInfo`.

        :param string `status`: the :class:`ButtonInfo` status ("Pressed", "Hover", "Normal",
         "Toggled", "Disabled").

        :return: An instance of :class:`wx.Bitmap`.
        """

        if status is None:
            status = self._status

        if not self.IsEnabled():
            status = "Disabled"

        if self._bitmaps[status] is None:
            if self.GetToggled():
                if self._bitmaps["Toggled"] is not None:
                    return self._bitmaps["Toggled"]
            return self._bitmaps["Normal"]

        return self._bitmaps[status]


    def GetRect(self):
        """
        Returns the :class:`ButtonInfo` client rectangle.

        :return: An instance of :class:`wx.Rect`.
        """

        return self._rect


    def GetStatus(self):
        """
        Returns the :class:`ButtonInfo` status.

        :return: A string containing the :class:`ButtonInfo` status (one of "Pressed", "Hover", "Normal",
         "Toggled", "Disabled").
        """

        return self._status


    def GetId(self):
        """
        Returns the :class:`ButtonInfo` id.

        :return: An integer representing the button id.
        """

        return self._id


    def SetRect(self, rect):
        """
        Sets the :class:`ButtonInfo` client rectangle.

        :param `rect`: an instance of :class:`wx.Rect`.
        """

        self._rect = rect


    def SetStatus(self, status):
        """
        Sets the :class:`ButtonInfo` status.

        :param string `status`: one of "Pressed", "Hover", "Normal", "Toggled", "Disabled".
        """

        if status == self._status:
            return

        if self.GetToggled() and status == "Normal":
            status = "Toggled"

        self._status = status
        self._parent.RefreshRect(self.GetRect())


    def GetTextAlignment(self):
        """
        Returns the text alignment in the button (bottom or right).

        :return: An integer representing the :class:`ButtonInfo` text alignment.
        """

        return self._textAlignment


    def SetTextAlignment(self, alignment):
        """
        Sets the text alignment in the button (bottom or right).

        :param integer `alignment`: the text alignment in this :class:`ButtonInfo` instance.
        """

        if alignment == self._textAlignment:
            return

        self._textAlignment = alignment


    def GetToggled(self):
        """
        Returns whether a ``wx.ITEM_CHECK`` button is toggled or not.

        :return: ``True`` if the button is toggled, ``False`` otherwise.
        """

        if self._kind == wx.ITEM_NORMAL:
            return False

        return self._toggle


    def SetToggled(self, toggle=True):
        """
        Sets a ``wx.ITEM_CHECK`` button toggled/not toggled.

        :param bool `toggle`: ``True`` to toggle the button, ``False`` otherwise.
        """

        if self._kind == wx.ITEM_NORMAL:
            return

        self._toggle = toggle


    def SetId(self, id):
        """
        Sets the :class:`ButtonInfo` identifier.

        :param integer `id`: the identifier of the window.
        """

        self._id = id


    def AddStatus(self, name="Custom", bmp=wx.NullBitmap):
        """
        Add a programmer-defined status in addition to the 5 default status:

        - Normal;
        - Disabled;
        - Hover;
        - Pressed;
        - Toggled.

        :param string `name`: the new status name;
        :param wx.Bitmap `bmp`: the bitmap associated with the new status.
        """

        self._bitmaps.update({name: bmp})


    def Enable(self, enable=True):
        """
        Enables/disables this instance of :class:`ButtonInfo`.

        :param bool `enable`: ``True`` to enable the button, ``False`` otherwise.
        """

        if enable:
            self._status = "Normal"
        else:
            self._status = "Disabled"


    def IsEnabled(self):
        """
        Returns ``True`` if this instance of :class:`ButtonInfo` is enabled for input,
        ``False`` otherwise.
        """

        return self._status != "Disabled"


    def SetText(self, text=""):
        """
        Sets the button label text.

        :param string `text`: the button label string.
        """

        self._text = text


    def GetText(self):
        """
        Returns the text associated to the button.

        :return: A string containing the :class:`ButtonInfo` text.
        """

        return self._text


    def HasText(self):
        """
        Returns whether the button has text or not.

        :return: ``True`` if this :class:`ButtonInfo` instance has a label, ``False`` otherwise.
        """

        return self._text != ""


    def SetKind(self, kind=wx.ITEM_NORMAL):
        """
        Sets the button type (standard or toggle).

        :param integer `kind`: one of ``wx.ITEM_NORMAL``, ``wx.ITEM_CHECK``.
        """

        self._kind = kind


    def GetKind(self):
        """
        Returns the button type (standard or toggle).

        :return: An integer representing the button type, one of ``wx.ITEM_NORMAL``, ``wx.ITEM_CHECK``.
        """

        return self._kind


    def SetShortHelp(self, help=""):
        """
        Sets the help string to be shown in a tooltip.

        :param string `help`: the string for the short help.
        """

        self._shortHelp = help


    def GetShortHelp(self):
        """
        Returns the help string shown in a tooltip.

        :return: A string containing the :class:`ButtonInfo` short help string.
        """

        return self._shortHelp


    def SetLongHelp(self, help=""):
        """
        Sets the help string to be shown in the statusbar.

        :param string `help`: the string for the long help.
        """

        self._longHelp = help


    def GetLongHelp(self):
        """
        Returns the help string shown in the statusbar.

        :return: A string containing the :class:`ButtonInfo` long help string.
        """

        return self._longHelp


    Bitmap = property(GetBitmap, SetBitmap)
    Id     = property(GetId, SetId)
    Rect   = property(GetRect, SetRect)
    Status = property(GetStatus, SetStatus)


# -- ButtonPanel class implementation ----------------------------------
# This is the main class.

class ButtonPanel(wx.Panel):
    """
    A custom panel class with gradient background shading with the possibility to
    add buttons and controls still respecting the gradient background.
    """

    def __init__(self, parent, id=wx.ID_ANY, text="", agwStyle=BP_DEFAULT_STYLE,
                 alignment=BP_ALIGN_LEFT, name="buttonPanel"):
        """
        Default class constructor.

        :param wx.Window `parent`: the parent window. Must not be ``None``;
        :param integer `id`: window identifier. If ``wx.ID_ANY``, will automatically create an identifier;
        :param string `text`: the main caption text for :class:`ButtonPanel`;
        :param integer `agwStyle`: the AGW-specific window style (one of ``BP_DEFAULT_STYLE``, ``BP_USE_GRADIENT``);
        :param integer `alignment`: alignment of buttons (left or right);
        :param string `name`: window class name.
        """

        wx.Panel.__init__(self, parent, id, wx.DefaultPosition, wx.DefaultSize,
                          wx.NO_BORDER, name=name)

        self._vButtons = []
        self._vSeparators = []

        self._agwStyle = agwStyle
        self._alignment = alignment
        self._statusTimer = None
        self._useHelp = True
        self._freezeCount = 0
        self._currentButton = -1
        self._haveTip = False

        self._art = BPArt(agwStyle)

        self._controlCreated = False

        direction = (self.IsVertical() and [wx.VERTICAL] or [wx.HORIZONTAL])[0]
        self._mainsizer = BoxSizer(direction)
        self.SetSizer(self._mainsizer)

        margins = self._art.GetMetric(BP_MARGINS_SIZE)

        # First spacer to create some room before the first text/button/control
        self._mainsizer.Add((margins.x, margins.y), 0)

        # Last spacer to create some room before the last text/button/control
        self._mainsizer.Add((margins.x, margins.y), 0)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnterWindow)

        self.SetBarText(text)
        self.LayoutItems()


    def SetBarText(self, text):
        """
        Sets the main caption text.

        :param string `text`: the main caption text label. An empty string erases the
         main caption text.
         """

        self.Freeze()

        text = text.strip()

        if self._controlCreated:
            self.RemoveText()

        self._text = ButtonPanelText(self, text)
        lenChildren = len(self._mainsizer.GetChildren())

        if text == "":
            # Even if we have no text, we insert it an empty spacer anyway
            # it is easier to handle if you have to recreate the sizer after.
            if self.IsStandard():
                self._mainsizer.Insert(1, self._text, 0, wx.ALIGN_CENTER,
                                       userData=self._text, realIndex=0)
            else:
                self._mainsizer.Insert(lenChildren-1, self._text, 0, wx.ALIGN_CENTER,
                                       userData=self._text, realIndex=lenChildren)

            return

        # We have text, so insert the text and an expandable spacer
        # alongside it. "Standard" ButtonPanel are left or top aligned.
        if self.IsStandard():
            self._mainsizer.Insert(1, self._text, 0, wx.ALIGN_CENTER,
                                    userData=self._text, realIndex=0)
            self._mainsizer.Insert(2, (0, 0), 1, wx.EXPAND)

        else:
            self._mainsizer.Insert(lenChildren-1, self._text, 0, wx.ALIGN_CENTER,
                                   userData=self._text, realIndex=lenChildren)
            self._mainsizer.Insert(lenChildren-1, (0, 0), 1, wx.EXPAND)


    def RemoveText(self):
        """ Removes the main caption text. """

        lenChildren = len(self._mainsizer.GetChildren())
        lenCustom = len(self._vButtons) + len(self._vSeparators) + 1

        if self.IsStandard():
            # Detach the text
            self._mainsizer.Remove(1, 0)
            if self.HasBarText():
                # Detach the expandable spacer
                self._mainsizer.Remove(1, -1)
        else:
            # Detach the text
            self._mainsizer.Remove(lenChildren-2, lenCustom-1)
            if self.HasBarText():
                # Detach the expandable spacer
                self._mainsizer.Remove(lenChildren-3, -1)


    def GetBarText(self):
        """
        Returns the main caption text.

        :return: A string representing the caption text.
        """

        return self._text.GetText()


    def HasBarText(self):
        """
        Returns whether :class:`ButtonPanel` has a main caption text or not.

        :return: ``True`` if :class:`ButtonPanel` has a main caption text, ``False`` otherwise.
        """

        return hasattr(self, "_text") and self._text.GetText() != ""


    def AddButton(self, btnInfo):
        """
        Adds a button to :class:`ButtonPanel`.

        :param `btnInfo`: an instance of :class:`ButtonInfo`.

        :note: Remember to pass a :class:`ButtonInfo` instance to this method, and not a
         standard :class:`Button` or a :class:`ToolBar` tool.
        """

        lenChildren = len(self._mainsizer.GetChildren())
        self._mainsizer.Insert(lenChildren-1, btnInfo, 0, wx.ALIGN_CENTER|wx.EXPAND, userData=btnInfo)

        self._vButtons.append(btnInfo)


    def AddSpacer(self, size=(0, 0), proportion=1, flag=wx.EXPAND):
        """
        Adds a spacer (stretchable or fixed-size) to :class:`ButtonPanel`.

        :param tuple `size`: the spacer size as a tuple;
        :param integer `proportion`: the spacer proportion (0 for fixed-size, 1 or more for a
         stretchable one);
        :param integer `flag`: one of the :class:`BoxSizer` flags.
        """

        lenChildren = len(self._mainsizer.GetChildren())
        self._mainsizer.Insert(lenChildren-1, size, proportion, flag)


    def AddControl(self, control, proportion=0, flag=wx.ALIGN_CENTER|wx.ALL, border=None):
        """
        Adds a wxPython control to :class:`ButtonPanel`.

        :param `control`: an instance of :class:`wx.Window`;
        :param integer `proportion`: the control proportion (0 for fixed-size, 1 or more for a
         stretchable one);
        :param integer `flag`: one of the :class:`BoxSizer` flags;
        :param integer `border`: the control border width (in pixels), if the `flag` parameter
         is set to include any border flag.
        """

        lenChildren = len(self._mainsizer.GetChildren())

        if border is None:
            border = self._art.GetMetric(BP_PADDING_SIZE)
            border = max(border.x, border.y)

        self._mainsizer.Insert(lenChildren-1, control, proportion, flag, border)


    def AddSeparator(self):
        """ Adds a separator line to :class:`ButtonPanel`. """

        lenChildren = len(self._mainsizer.GetChildren())
        separator = Separator(self)

        self._mainsizer.Insert(lenChildren-1, separator, 0, wx.EXPAND)
        self._vSeparators.append(separator)


    def RemoveAllButtons(self):
        """
        Remove all the buttons from :class:`ButtonPanel`.

        :note: This function is for internal use only. If you are interested in
         manipulating a :class:`ButtonPanel` in real time (ie. removing things on it)
         have a look at the :meth:`~ButtonPanel.Clear` method.
        """

        self._vButtons = []


    def RemoveAllSeparators(self):
        """
        Remove all the separators from :class:`ButtonPanel`.

        :note: This function is for internal use only. If you are interested in
         manipulating a :class:`ButtonPanel` in real time (ie. removing things on it)
         have a look at the :meth:`~ButtonPanel.Clear` method.
        """

        self._vSeparators = []


    def Clear(self):
        """
        Clears the :class:`ButtonPanel`.

        Can be used to reset the :class:`ButtonPanel` if you'd like have a new set of
        buttons on the panel.
        """

        if self.HasBarText():
            bartext = self.GetBarText()
        else:
            bartext = None

        self.Freeze()

        self._currentButton = -1
        self._mainsizer.Clear()
        self.ReCreateSizer(bartext)


    def GetAlignment(self):
        """
        Returns the buttons alignment.

        :return: An integer specifying the buttons alignment.

        :see: :meth:`~ButtonPanel.SetAlignment` for a set of valid alignment bits.
        """

        return self._alignment


    def SetAlignment(self, alignment):
        """
        Sets the buttons alignment.

        :param integer `alignment`: can be one of the following bits:

         ====================== ======= ==========================
         Alignment Flag          Value  Description
         ====================== ======= ==========================
         ``BP_ALIGN_RIGHT``           1 Buttons are aligned on the right
         ``BP_ALIGN_LEFT``            2 Buttons are aligned on the left
         ``BP_ALIGN_TOP``             4 Buttons are aligned at the top
         ``BP_ALIGN_BOTTOM``          8 Buttons are aligned at the bottom
         ====================== ======= ==========================
        """

        if alignment == self._alignment:
            return

        self.Freeze()

        text = self.GetBarText()

        # Remove the text in any case
        self.RemoveText()

        # Remove the first and last spacers
        self._mainsizer.Remove(0, -1)
        self._mainsizer.Remove(len(self._mainsizer.GetChildren())-1, -1)

        self._alignment = alignment

        # Recreate the sizer accordingly to the new alignment
        self.ReCreateSizer(text)


    def IsVertical(self):
        """
        Returns whether :class:`ButtonPanel` is vertically aligned or not.

        :return: ``True`` if :class:`ButtonPanel` is vertically aligned, ``False`` otherwise.
        """

        return self._alignment not in [BP_ALIGN_RIGHT, BP_ALIGN_LEFT]


    def IsStandard(self):
        """
        Returns whether :class:`ButtonPanel` is aligned "Standard" (left/top) or not.

        :return: ``True`` if :class:`ButtonPanel` is aligned "standard", ``False`` otherwise.
        """

        return self._alignment in [BP_ALIGN_LEFT, BP_ALIGN_TOP]


    def DoLayout(self):
        """
        Do the Layout for :class:`ButtonPanel`.

        :note: Call this method every time you make a modification to the layout
         or to the customizable sizes of the pseudo controls.
        """

        margins = self._art.GetMetric(BP_MARGINS_SIZE)
        lenChildren = len(self._mainsizer.GetChildren())

        self._mainsizer.SetItemMinSize(0, (margins.x, margins.y))
        self._mainsizer.SetItemMinSize(lenChildren-1, (margins.x, margins.y))

        self._controlCreated = True
        self.LayoutItems()

        # *VERY* WEIRD: the sizer seems not to respond to any layout until I
        # change the ButtonPanel size and restore it back
        size = self.GetSize()
        self.SetSize((size.x+1, size.y+1))
        self.SetSize((size.x, size.y))

        if self.IsFrozen():
            self.Thaw()


    def ReCreateSizer(self, text=None):
        """
        Recreates the :class:`ButtonPanel` sizer accordingly to the alignment specified.

        :param string `text`: the text to display as main caption. If `text` is set to ``None``,
         the main caption will not be displayed.
        """

        children = self._mainsizer.GetChildren()
        self.RemoveAllButtons()
        self.RemoveAllSeparators()

        # Create a new sizer depending on the alignment chosen
        direction = (self.IsVertical() and [wx.VERTICAL] or [wx.HORIZONTAL])[0]
        self._mainsizer = BoxSizer(direction)

        margins = self._art.GetMetric(BP_MARGINS_SIZE)
        # First spacer to create some room before the first text/button/control
        self._mainsizer.Add((margins.x, margins.y), 0)

        # Last spacer to create some room before the last text/button/control
        self._mainsizer.Add((margins.x, margins.y), 0)

        # This is needed otherwise SetBarText goes mad
        self._controlCreated = False

        for child in children:
            userData = child.GetUserData()
            if userData:
                if isinstance(userData, ButtonInfo):
                    # It is a ButtonInfo, can't be anything else
                    self.AddButton(child.GetUserData())
                elif isinstance(userData, Separator):
                    self.AddSeparator()

            else:
                if child.IsSpacer():
                    # This is a spacer, expandable or not
                    self.AddSpacer(child.GetSize(), child.GetProportion(),
                                   child.GetFlag())
                else:
                    # This is a wxPython control
                    self.AddControl(child.GetWindow(), child.GetProportion(),
                                    child.GetFlag(), child.GetBorder())

        self.SetSizer(self._mainsizer)

        if text is not None:
            self.SetBarText(text)

        self.DoLayout()

        self.Thaw()


    def DoGetBestSize(self):
        """
        Gets the size which best suits :class:`ButtonPanel`: for a control, it would be
        the minimal size which doesn't truncate the control, for a panel - the
        same size as it would have after a call to `Fit()`.

        :return: An instance of :class:`wx.Size`.

        :note: Overridden from :class:`Panel`.
        """

        w = h = btnWidth = btnHeight = 0
        isVertical = self.IsVertical()

        padding = self._art.GetMetric(BP_PADDING_SIZE)
        border = self._art.GetMetric(BP_BORDER_SIZE)
        margins = self._art.GetMetric(BP_MARGINS_SIZE)
        separator_size = self._art.GetMetric(BP_SEPARATOR_SIZE)

        # Add the space required for the main caption
        if self.HasBarText():
            w, h = self._text.GetBestSize()
            if isVertical:
                h += padding.y
            else:
                w += padding.x
        else:
            w = h = border

        # Add the button's sizes
        for btn in self._vButtons:

            bw, bh = btn.GetBestSize()
            btnWidth = max(btnWidth, bw)
            btnHeight = max(btnHeight, bh)

            if isVertical:
                w = max(w, btnWidth)
                h += bh
            else:
                h = max(h, btnHeight)
                w += bw

        # Add the control's sizes
        for control in self.GetControls():
            cw, ch = control.GetSize()
            if isVertical:
                h += ch
                w = max(w, cw)
            else:
                w += cw
                h = max(h, ch)

        # Add the separator's sizes and the 2 SizerItems at the beginning
        # and at the end
        if self.IsVertical():
            h += 2*margins.y + len(self._vSeparators)*separator_size
        else:
            w += 2*margins.x + len(self._vSeparators)*separator_size

        return wx.Size(w, h)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`ButtonPanel`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.BufferedPaintDC(self)
        rect = self.GetClientRect()

        self._art.DrawButtonPanel(dc, rect, self._agwStyle)
        self._mainsizer.Draw(dc)


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`ButtonPanel`.

        :param `event`: a :class:`EraseEvent` event to be processed.

        :note: This is intentionally empty to reduce flicker.
        """

        pass


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`ButtonPanel`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.

        .. todo::

           Improve the chain of methods :meth:`~ButtonPanel.OnSize` ==> :meth:`~ButtonPanel.DoLayout` ==> :meth:`~ButtonPanel.LayoutItems`
           to avoid multiple calls to :meth:`~ButtonPanel.LayoutItems`.
        """

        # NOTE: It seems like LayoutItems number of calls can be optimized in some way.
        # Currently every DoLayout (or every parent Layout()) calls about 3 times
        # the LayoutItems method. Any idea on how to improve it?
        self.LayoutItems()
        self.Refresh()

        event.Skip()


    def LayoutItems(self):
        """
        Layout the items using a different algorithms depending on the existance
        of the main caption.
        """

        nonspacers, allchildren = self.GetNonFlexibleChildren()

        if self.HasBarText():
            self.FlexibleLayout(nonspacers, allchildren)
        else:
            self.SizeLayout(nonspacers, allchildren)

        self._mainsizer.Layout()


    def SizeLayout(self, nonspacers, children):
        """
        Layout the items when no main caption exists.

        :param list `nonspacers`: a list of items which are not spacers;
        :param list `children`: a list of all the children of :class:`ButtonPanel`.
        """

        size = self.GetSize()
        isVertical = self.IsVertical()

        corner = 0
        indx1 = len(nonspacers)

        for item in nonspacers:
            corner += self.GetItemSize(item, isVertical)
            if corner > size[isVertical]:
                indx1 = nonspacers.index(item)
                break

        # Leave out the last spacer, it has to be there always
        for ii in range(len(nonspacers)-1):
            indx = children.index(nonspacers[ii])
            self._mainsizer.Show(indx, ii < indx1)


    def GetItemSize(self, item, isVertical):
        """
        Returns the size of an item in the main :class:`ButtonPanel` sizer.

        :param `item`: an instance of :class:`ButtonInfo`;
        :param bool `isVertical`: ``True`` if :class:`ButtonPanel` is in vertical orientation,
         ``False`` otherwise.

        :return: An instance of :class:`wx.Size`.
        """

        if item.GetUserData():
            return item.GetUserData().GetBestSize()[isVertical]
        else:
            return item.GetSize()[isVertical]


    def FlexibleLayout(self, nonspacers, allchildren):
        """
        Layout the items when the main caption exists.

        :param list `nonspacers`: a list of items which are not spacers;
        :param list `allchildren`: a list of all the children of :class:`ButtonPanel`.
        """

        if len(nonspacers) < 2:
            return

        isVertical = self.IsVertical()
        isStandard = self.IsStandard()

        size = self.GetSize()[isVertical]
        padding = self._art.GetMetric(BP_PADDING_SIZE)

        fixed = (isStandard and [nonspacers[1]] or [nonspacers[-2]])[0]

        if isStandard:
            nonspacers.reverse()
            leftendx = fixed.GetSize()[isVertical] + padding.x
        else:
            rightstartx = size - fixed.GetSize()[isVertical]
            size = 0

        count = lennonspacers = len(nonspacers)

        for item in nonspacers:
            if isStandard:
                size -= self.GetItemSize(item, isVertical)
                if size < leftendx:
                    break
            else:
                size += self.GetItemSize(item, isVertical)
                if size > rightstartx:
                    break

            count = count - 1

        nonspacers.reverse()

        for jj in range(2, lennonspacers):
            indx = allchildren.index(nonspacers[jj])
            self._mainsizer.Show(indx, jj >= count)


    def GetNonFlexibleChildren(self):
        """
        Returns all the :class:`ButtonPanel` main sizer's children that are not
        flexible spacers.

        :return: A list of items inside :class:`ButtonPanel` that are not flexible spacers.
        """

        children1 = []
        children2 = list(self._mainsizer.GetChildren())

        for child in children2:
            if child.IsSpacer():
                if child.GetUserData() or child.GetProportion() == 0:
                    children1.append(child)
            else:
                children1.append(child)

        return children1, children2


    def GetControls(self):
        """
        Returns the wxPython controls that belongs to :class:`ButtonPanel`.

        :return: A list of items inside :class:`ButtonPanel` that are wxPython controls.
        """

        children2 = self._mainsizer.GetChildren()
        children1 = [child for child in children2 if not child.IsSpacer()]

        return children1


    def SetStyle(self, agwStyle):
        """
        Sets the :class:`ButtonPanel` window style.

        :param integer `agwStyle`: one of the following bits:

         ==================== =========== ==================================================
         Window Styles        Hex Value   Description
         ==================== =========== ==================================================
         ``BP_DEFAULT_STYLE``         0x1 :class:`ButtonPanel` has a plain solid background.
         ``BP_USE_GRADIENT``          0x2 :class:`ButtonPanel` has a gradient shading background.
         ==================== =========== ==================================================

        """

        if agwStyle == self._agwStyle:
            return

        self._agwStyle = agwStyle
        self.Refresh()


    def GetStyle(self):
        """
        Returns the :class:`ButtonPanel` window style.

        :see: :meth:`~ButtonPanel.SetStyle` for a list of valid window styles.
        """

        return self._agwStyle


    def OnMouseMove(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`ButtonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        # Check to see if we are hovering a button
        tabId, flags = self.HitTest(event.GetPosition())

        if flags != BP_HT_BUTTON:
            self.RemoveHelp()
            self.RepaintOldSelection()
            self._currentButton = -1
            return

        btn = self._vButtons[tabId]

        if not btn.IsEnabled():
            self.RemoveHelp()
            self.RepaintOldSelection()
            return

        if tabId != self._currentButton:
            self.RepaintOldSelection()

        if btn.GetRect().Contains(event.GetPosition()):
            if btn.GetStatus() != "Pressed":
                btn.SetStatus("Hover")
        else:
            btn.SetStatus("Normal")

        if tabId != self._currentButton:
            self.RemoveHelp()
            self.DoGiveHelp(btn)

        self._currentButton = tabId

        event.Skip()


    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`ButtonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        tabId, hit = self.HitTest(event.GetPosition())

        if hit == BP_HT_BUTTON:
            btn = self._vButtons[tabId]
            if btn.IsEnabled():
                btn.SetStatus("Pressed")
                self._currentButton = tabId


    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`ButtonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        tabId, flags = self.HitTest(event.GetPosition())

        if flags != BP_HT_BUTTON:
            return

        hit = self._vButtons[tabId]

        if hit.GetStatus() == "Disabled":
            return

        for btn in self._vButtons:
            if btn != hit:
                btn.SetFocus(False)

        if hit.GetStatus() == "Pressed":
            hit.SetToggled(not hit.GetToggled())

            # Update the button status to be hovered
            hit.SetStatus("Hover")
            hit.SetFocus()
            self._currentButton = tabId

            # Fire a button click event
            btnEvent = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, hit.GetId())
            btnEvent.SetEventObject(hit)
            self.GetEventHandler().ProcessEvent(btnEvent)


    def OnMouseLeave(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`ButtonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        # Reset all buttons statuses
        for btn in self._vButtons:
            if not btn.IsEnabled():
                continue
            btn.SetStatus("Normal")

        self.RemoveHelp()

        event.Skip()


    def OnMouseEnterWindow(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` event for :class:`ButtonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        tabId, flags = self.HitTest(event.GetPosition())

        if flags == BP_HT_BUTTON:

            hit = self._vButtons[tabId]

            if hit.GetStatus() == "Disabled":
                event.Skip()
                return

            self.DoGiveHelp(hit)
            self._currentButton = tabId

        event.Skip()


    def DoGiveHelp(self, hit):
        """
        Shows tooltips and long help strings in :class:`StatusBar`.

        :param `hit`: an instance of :class:`ButtonInfo` where the mouse is hovering.
        """

        if not self.GetUseHelp():
            return

        shortHelp = hit.GetShortHelp()
        if shortHelp:
            self.SetToolTip(shortHelp)
            self._haveTip = True

        longHelp = hit.GetLongHelp()
        if not longHelp:
            return

        topLevel = wx.GetTopLevelParent(self)

        if isinstance(topLevel, wx.Frame) and topLevel.GetStatusBar():
            statusBar = topLevel.GetStatusBar()

            if self._statusTimer and self._statusTimer.IsRunning():
                self._statusTimer.Stop()
                statusBar.PopStatusText(0)

            statusBar.PushStatusText(longHelp, 0)
            self._statusTimer = StatusBarTimer(self)
            self._statusTimer.Start(_DELAY, wx.TIMER_ONE_SHOT)


    def RemoveHelp(self):
        """ Removes the tooltips and statusbar help (if any) for a button. """

        if not self.GetUseHelp():
            return

        if self._haveTip:
            self.SetToolTip("")
            self._haveTip = False

        if self._statusTimer and self._statusTimer.IsRunning():
            topLevel = wx.GetTopLevelParent(self)
            statusBar = topLevel.GetStatusBar()
            self._statusTimer.Stop()
            statusBar.PopStatusText(0)
            self._statusTimer = None


    def RepaintOldSelection(self):
        """ Repaints the old selected/hovered button. """

        current = self._currentButton

        if current == -1:
            return

        btn = self._vButtons[current]
        if not btn.IsEnabled():
            return

        btn.SetStatus("Normal")


    def OnStatusBarTimer(self):
        """ Handles the timer expiring to delete the long help string in :class:`StatusBar`. """

        topLevel = wx.GetTopLevelParent(self)
        statusBar = topLevel.GetStatusBar()
        statusBar.PopStatusText(0)


    def SetUseHelp(self, useHelp=True):
        """
        Sets whether or not short and long help strings should be displayed as tooltips
        and :class:`StatusBar` items respectively.

        :param bool `useHelp`: ``True`` to display short and long help strings as tooltips
         and :class:`StatusBar` items respectively, ``False`` otherwise.
        """

        self._useHelp = useHelp


    def GetUseHelp(self):
        """
        Returns whether or not short and long help strings should be displayed as tooltips
        and :class:`StatusBar` items respectively.

        :return: ``True`` if the short and long help strings should be displayed as tooltips
         and :class:`StatusBar` items respectively, ``False`` otherwise.
        """

        return self._useHelp


    def HitTest(self, pt):
        """
        HitTest method for :class:`ButtonPanel`.

        :param `pt`: the mouse position, an instance of :class:`wx.Point`.

        :returns: an instance of :class:`ButtonInfo` and the hit flag ``BP_HT_BUTTON`` if a button
         client rectangle contains the input point `pt`, or ``wx.NOT_FOUND`` and ``BP_HT_NONE``.
        """

        for ii in range(len(self._vButtons)):
            if not self._vButtons[ii].IsEnabled():
                continue
            if self._vButtons[ii].GetRect().Contains(pt):
                return ii, BP_HT_BUTTON

        return wx.NOT_FOUND, BP_HT_NONE


    def GetBPArt(self):
        """ Returns the associated :class:`BPArt` art provider. """

        return self._art


    def SetBPArt(self, art):
        """
        Sets a new :class:`BPArt` art provider to :class:`ButtonPanel`.

        :param `art`: an instance of :class:`BPArt`.
        """

        self._art = art
        self.Refresh()


    if wx.VERSION < (2,7,1,1):
        def Freeze(self):
            """
            Freezes the window or, in other words, prevents any updates from taking place
            on screen, the window is not redrawn at all. :meth:`~ButtonPanel.Thaw` must be called to reenable
            window redrawing. Calls to these two functions may be nested.

            :note: This method is useful for visual appearance optimization.
            """

            self._freezeCount = self._freezeCount + 1
            wx.Panel.Freeze(self)


        def Thaw(self):
            """
            Reenables window updating after a previous call to :meth:`~ButtonPanel.Freeze`. To really thaw the
            control, it must be called exactly the same number of times as :meth:`~ButtonPanel.Freeze`.
            """

            if self._freezeCount == 0:
                raise Exception("\nERROR: Thawing Unfrozen ButtonPanel?")

            self._freezeCount = self._freezeCount - 1
            wx.Panel.Thaw(self)


        def IsFrozen(self):
            """ Returns ``True`` if the window is currently frozen by a call to :meth:`~ButtonPanel.Freeze`. """

            return self._freezeCount != 0


if __name__ == '__main__':

    import wx

    class MyFrame(wx.Frame):

        def __init__(self, parent, id=-1, title='ButtonPanel', pos=wx.DefaultPosition,
                     size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):

            wx.Frame.__init__(self, parent, id, title, pos, size, style)

            mainPanel = wx.Panel(self, -1)
            self.logtext = wx.TextCtrl(mainPanel, -1, '', style=wx.TE_MULTILINE)

            vSizer = wx.BoxSizer(wx.VERTICAL)
            mainPanel.SetSizer(vSizer)

            titleBar = ButtonPanel(mainPanel, -1, 'A Simple Test & Demo')

            btn1 = ButtonInfo(titleBar, wx.ID_ANY,
                              wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (32, 32)),
                              text='Button 1')
            titleBar.AddButton(btn1)
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn1)

            btn2 = ButtonInfo(titleBar, wx.ID_ANY,
                              wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (32, 32)),
                              text='Button 2')
            titleBar.AddButton(btn2)
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn2)

            btn3 = ButtonInfo(titleBar, wx.ID_ANY,
                              wx.ArtProvider.GetBitmap(wx.ART_WARNING, wx.ART_OTHER, (32, 32)),
                              text='Button 3')

            titleBar.AddButton(btn3)
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn3)

            vSizer.Add(titleBar, 0, wx.EXPAND)
            vSizer.Add((20, 20))
            vSizer.Add(self.logtext, 1, wx.EXPAND|wx.ALL, 5)

            titleBar.DoLayout()
            vSizer.Layout()


        def OnButton(self, event):
            ''' Handler for the ``wx.EVT_BUTTON`` event. '''

            obj = event.GetEventObject()

            # This will print the button label
            print((obj.GetText()))


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()
