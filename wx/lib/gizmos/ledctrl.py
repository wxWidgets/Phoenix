#----------------------------------------------------------------------
# Name:        wx.lib.gizmos.ledctrl
# Purpose:
#
# Author:      Robin Dunn
#
# Created:     26-Oct-2017
# Copyright:   (c) 2018 by Total Control Software
# Licence:     wxWindows license
# Tags:
#----------------------------------------------------------------------
"""
Widget to display a series of digits, spaces, dashes or colons in a segmented style.
"""

import wx

LED_ALIGN_LEFT   = 0x01
LED_ALIGN_RIGHT  = 0x02
LED_ALIGN_CENTER = 0x04
LED_ALIGN_MASK   = 0x07

LED_DRAW_FADED = 0x08


class LEDNumberCtrl(wx.Control):
    """
    The LEDNumberCtrl can be used to display a series of digits, (plus spaces,
    colons or dashes,) using a style reminiscent of old-timey segmented
    digital displays.
    """

    # constants used internally
    class const:
        LINE1 = 1
        LINE2 = 2
        LINE3 = 4
        LINE4 = 8
        LINE5 = 16
        LINE6 = 32
        LINE7 = 64
        DECIMALSIGN = 128
        COLON = 256

        DIGITS = {
            '0': LINE1 | LINE2 | LINE3 | LINE4 | LINE5 | LINE6,
            '1': LINE2 | LINE3,
            '2': LINE1 | LINE2 | LINE4 | LINE5 | LINE7,
            '3': LINE1 | LINE2 | LINE3 | LINE4 | LINE7,
            '4': LINE2 | LINE3 | LINE6 | LINE7,
            '5': LINE1 | LINE3 | LINE4 | LINE6 | LINE7,
            '6': LINE1 | LINE3 | LINE4 | LINE5 | LINE6 | LINE7,
            '7': LINE1 | LINE2 | LINE3,
            '8': LINE1 | LINE2 | LINE3 | LINE4 | LINE5 | LINE6 | LINE7,
            '9': LINE1 | LINE2 | LINE3 | LINE6 | LINE7,
            '-': LINE7,
            ':': COLON,
        }
        DIGITALL = 0xFFFF



    def __init__(self, *args, **kw):
        """
        Create a new LEDNumberCtrl.

        Both the normal constructor style with all parameters, or wxWidgets
        2-phase style default constructor is supported. If the default
        constructor is used then the Create method will need to be called
        later before the widget can actually be used.
        """
        if not args and not kw:
            self._init_default()
        else:
            self._init_full(*args, **kw)

    def _init_default(self):
        super(LEDNumberCtrl, self).__init__()
        self._init()

    def _init_full(self, parent, id=wx.ID_ANY,
                   pos=wx.DefaultPosition, size=wx.DefaultSize,
                   style=LED_ALIGN_LEFT|LED_DRAW_FADED, name='ledctrl'):
        super(LEDNumberCtrl, self).__init__(parent, id, pos, size, style, name=name)
        self._init()
        self._post_create()


    def Create(self, parent, id=wx.ID_ANY,
               pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=LED_ALIGN_LEFT|LED_DRAW_FADED, name='ledctrl'):
        super(LEDNumberCtrl, self).Create(parent, id, pos, size, style, name=name)
        return self._post_create()


    def _init(self):
        # set default attributes
        self.m_alignment = LED_ALIGN_LEFT
        self.m_lineMargin = -1
        self.m_digitMargin = -1
        self.m_lineLength = -1
        self.m_lineWidth = -1
        self.m_drawFaded = False
        self.m_leftStartPos = -1
        self.m_value = ''


    def _post_create(self):
        self.SetBackgroundColour(wx.BLACK)
        self.SetForegroundColour(wx.GREEN)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # flags
        style = self.GetWindowStyle()
        if style & LED_DRAW_FADED:
            self.SetDrawFaded(True)
        if style  & LED_ALIGN_MASK:
            self.SetAlignment(style & LED_ALIGN_MASK)

        # event bindings
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        return True


    def GetAlignment(self):
        return self.m_alignment


    def GetDrawFaded(self):
        return self.m_drawFaded


    def GetValue(self):
        return self.m_value


    def SetAlignment(self, alignment, redraw=True):
        """
        Set how the digits will be aligned within the widget.

        Supported values are ``LED_ALIGN_LEFT``, ``LED_ALIGN_RIGHT``,
        and ``LED_ALIGN_CENTER``.
        """
        if alignment != self.m_alignment:
            self.m_alignment = alignment
            self._recalcInternals(self.GetClientSize())

            if redraw:
                self.Refresh(False)


    def SetDrawFaded(self, drawFaded, redraw=True):
        """
        Set whether unlit segments will still be draw with a faded version of
        the foreground colour.
        """
        if drawFaded != self.m_drawFaded:
            self.m_drawFaded = drawFaded

            if redraw:
                self.Refresh(False)


    def SetValue(self, value, redraw=True):
        """
        Set the string value to be displayed.
        """
        if value != self.m_value:
            for ch in value:
                assert ch in '0123456789-.: ', "LEDNumberCtrl can only display numeric string values."

            self.m_value = value
            self._recalcInternals(self.GetClientSize())

            if redraw:
                self.Refresh(False)


    Alignment = property(GetAlignment, SetAlignment)
    DrawFaded = property(GetDrawFaded, SetDrawFaded)
    Value = property(GetValue, SetValue)


    def OnSize(self, evt):
        self._recalcInternals(evt.GetSize())
        evt.Skip()


    def OnPaint(self, evt):
        c = self.const
        dc = wx.AutoBufferedPaintDC(self)

        # Draw the background
        dc.SetBrush(wx.Brush(self.GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(wx.Rect((0, 0), self.GetClientSize()))

        # Iterate the digits and draw each
        offset = 0
        for i, ch in enumerate(self.m_value):
            i -= offset
            # Draw faded lines if wanted.
            if self.m_drawFaded and ch != '.':
                self._drawDigit(dc, c.DIGITALL, i);

            if ch == '.':
                # draw the decimal point in the previous segment
                self._drawDigit(dc, c.DECIMALSIGN, i-1)
                offset += 1
            elif ch == ' ':
                # skip spaces
                continue
            else:
                self._drawDigit(dc, c.DIGITS[ch], i)


    def _recalcInternals(self, size):
        height = size.Height

        if (height * 0.075) < 1:
            self.m_lineMargin = 1
        else:
            self.m_lineMargin = int(height * 0.075)

        if (height * 0.275) < 1:
            self.m_lineLength = 1
        else:
            self.m_lineLength = int(height * 0.275)

        self.m_lineWidth = self.m_lineMargin
        self.m_digitMargin = self.m_lineMargin * 4

        # Count the number of characters in the string; '.' characters are not
        # included because they do not take up space in the display
        count = 0;
        for ch in self.m_value:
            if ch != '.':
                count += 1

        valueWidth = (self.m_lineLength + self.m_digitMargin) * count
        clientWidth = size.Width

        if self.m_alignment == LED_ALIGN_LEFT:
            self.m_leftStartPos = self.m_lineMargin
        elif self.m_alignment == LED_ALIGN_RIGHT:
            self.m_leftStartPos = clientWidth - valueWidth - self.m_lineMargin
        elif self.m_alignment == LED_ALIGN_CENTER:
            self.m_leftStartPos = int((clientWidth - valueWidth) / 2)
        else:
            raise AssertionError("Unknown alignment value for LEDNumberCtrl.")


    def _drawDigit(self, dc, digit, column):
        lineColor = self.GetForegroundColour()
        c = self.const

        if digit == c.DIGITALL:
            R = int(lineColor.Red() / 8)
            G = int(lineColor.Green() / 8)
            B = int(lineColor.Blue() / 8)
            lineColor.Set(R, G, B)

        XPos = self.m_leftStartPos + column * (self.m_lineLength + self.m_digitMargin)

        # Create a pen and draw the lines.
        dc.SetPen(wx.Pen(lineColor, self.m_lineWidth))

        if digit & c.LINE1:
            dc.DrawLine(XPos + self.m_lineMargin * 2, self.m_lineMargin,
                        XPos + self.m_lineLength + self.m_lineMargin * 2, self.m_lineMargin)

        if digit & c.LINE2:
            dc.DrawLine(XPos + self.m_lineLength + self.m_lineMargin * 3, self.m_lineMargin * 2,
                        XPos + self.m_lineLength + self.m_lineMargin * 3, self.m_lineLength + (self.m_lineMargin * 2))

        if digit & c.LINE3:
            dc.DrawLine(XPos + self.m_lineLength + self.m_lineMargin * 3, self.m_lineLength + (self.m_lineMargin * 4),
                        XPos + self.m_lineLength + self.m_lineMargin * 3, self.m_lineLength * 2 + (self.m_lineMargin * 4))

        if digit & c.LINE4:
            dc.DrawLine(XPos + self.m_lineMargin * 2, self.m_lineLength * 2 + (self.m_lineMargin * 5),
                        XPos + self.m_lineLength + self.m_lineMargin * 2, self.m_lineLength * 2 + (self.m_lineMargin * 5))

        if digit & c.LINE5:
            dc.DrawLine(XPos + self.m_lineMargin, self.m_lineLength + (self.m_lineMargin * 4),
                        XPos + self.m_lineMargin, self.m_lineLength * 2 + (self.m_lineMargin * 4))

        if digit & c.LINE6:
            dc.DrawLine(XPos + self.m_lineMargin, self.m_lineMargin * 2,
                        XPos + self.m_lineMargin, self.m_lineLength + (self.m_lineMargin * 2))

        if digit & c.LINE7:
            dc.DrawLine(XPos + self.m_lineMargin * 2, self.m_lineLength + (self.m_lineMargin * 3),
                        XPos + self.m_lineMargin * 2 + self.m_lineLength, self.m_lineLength + (self.m_lineMargin * 3))

        if digit & c.DECIMALSIGN:
            dc.DrawLine(XPos + self.m_lineLength + self.m_lineMargin * 4, self.m_lineLength * 2 + (self.m_lineMargin * 5),
                        XPos + self.m_lineLength + self.m_lineMargin * 4, self.m_lineLength * 2 + (self.m_lineMargin * 5))

        if digit & c.COLON:
            dc.SetBrush(wx.Brush(lineColor))
            centerX = XPos + (self.m_lineLength + self.m_digitMargin) / 2
            radius = self.m_lineWidth / 2
            dc.DrawCircle(centerX, (self.m_lineLength + (self.m_lineMargin * 3)) / 2, radius)
            dc.DrawCircle(centerX, (self.m_lineLength * 2 + (self.m_lineMargin * 5)) * 3 / 4, radius)
