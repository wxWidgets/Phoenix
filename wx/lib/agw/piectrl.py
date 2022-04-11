# --------------------------------------------------------------------------- #
# PIECTRL Control wxPython IMPLEMENTATION
# Python Code By:
#
# Andrea Gavana, @ 31 Oct 2005
# Latest Revision: 16 Jul 2012, 15.00 GMT
#
#
# TODO List/Caveats
#
# 1. Maybe Integrate The Very Nice PyOpenGL Implementation Of A PieChart Coded
#    By Will McGugan?
#
# 2. Not Tested On Other Platforms, Only On Windows 2000/XP, With Python 2.4.1
#    And wxPython 2.6.1.0
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
:class:`~wx.lib.agw.piectrl.PieCtrl` and :class:`~wx.lib.agw.piectrl.ProgressPie` are simple classes that reproduce the behavior of a pie
chart.


Description
===========

:class:`PieCtrl` and :class:`ProgressPie` are simple classes that reproduce the behavior of a pie
chart. They use only pure wxPython classes/methods, without external dependencies.
:class:`PieCtrl` is somewhat a "static" control, that you may create in order to display
a simple pie chart on a :class:`Panel` or similar. :class:`ProgressPie` tries to emulate the
behavior of :class:`ProgressDialog`, but using a pie chart instead of a gauge.


Usage
=====

Usage example::

    import wx
    import wx.lib.agw.piectrl as PC

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "PieCtrl Demo")

            panel = wx.Panel(self)

            # create a simple PieCtrl with 3 sectors
            mypie = PC.PieCtrl(panel, -1, wx.DefaultPosition, wx.Size(180,270))

            part = PC.PiePart()

            part.SetLabel("Label 1")
            part.SetValue(300)
            part.SetColour(wx.Colour(200, 50, 50))
            mypie._series.append(part)

            part = PC.PiePart()

            part.SetLabel("Label 2")
            part.SetValue(200)
            part.SetColour(wx.Colour(50, 200, 50))
            mypie._series.append(part)

            part = PC.PiePart()

            part.SetLabel("helloworld label 3")
            part.SetValue(50)
            part.SetColour(wx.Colour(50, 50, 200))
            mypie._series.append(part)

            # create a ProgressPie
            progress_pie = PC.ProgressPie(panel, 100, 50, -1, wx.DefaultPosition,
                                          wx.Size(180, 200), wx.SIMPLE_BORDER)

            progress_pie.SetBackColour(wx.Colour(150, 200, 255))
            progress_pie.SetFilledColour(wx.RED)
            progress_pie.SetUnfilledColour(wx.WHITE)
            progress_pie.SetHeight(20)

            main_sizer = wx.BoxSizer(wx.HORIZONTAL)

            main_sizer.Add(mypie, 1, wx.EXPAND | wx.ALL, 5)
            main_sizer.Add(progress_pie, 1, wx.EXPAND | wx.ALL, 5)

            panel.SetSizer(main_sizer)
            main_sizer.Layout()


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()



Methods and Settings
====================

With :class:`PieCtrl` you can:

- Create a :class:`PieCtrl` with different sectors;
- Set the sector values, colours and labels;
- Assign a legend to the :class:`PieCtrl`;
- Use an image as the :class:`PieCtrl` background;
- Change the vertical rotation (perspective) of the :class:`PieCtrl`;
- Show/hide the segment edges.


Window Styles
=============

`No particular window styles are available for this class.`


Events Processing
=================

`No custom events are available for this class.`


License And Version
===================

:class:`PieCtrl` is distributed under the wxPython license.

Latest revision: Andrea Gavana @ 16 Jul 2012, 15.00 GMT

Version 0.3

"""


#----------------------------------------------------------------------
# Beginning Of PIECTRL wxPython Code
#----------------------------------------------------------------------


import wx

from math import pi, sin, cos

#----------------------------------------------------------------------
# Class PieCtrlLegend
# This Class Handles The Legend For The Classic PieCtrl.
#----------------------------------------------------------------------

class PieCtrlLegend(wx.Window):
    """
    This class displays a legend window for the classic :class:`PieCtrl`.
    """

    def __init__(self, parent, title, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """
        Default class constructor.

        :param `parent`: the :class:`PieCtrlLegend` parent;
        :param `title`: the legend title;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the window style (unused).
        """

        wx.Window.__init__(self, parent, id, pos, size, style)

        self._title = title
        self._istransparent = False
        self._horborder = 5
        self._verborder = 5
        self._titlecolour = wx.Colour(0, 0, 127)
        self._labelcolour = wx.BLACK
        self._labelfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self._backcolour = wx.YELLOW
        self._backgroundDC = wx.MemoryDC()
        self._parent = parent

        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def SetTransparent(self, value=False):
        """
        Toggles the legend transparency (visibility).

        :param `value`: ``True`` to set the legend as transparent, ``False`` otherwise.
        """

        self._istransparent = value
        self.Refresh()


    def RecreateBackground(self, parentdc):
        """
        Recreates the legend background.

        :param `parentdc`: an instance of :class:`wx.DC`.
        """

        w, h = self.GetSize()
        self._background = wx.Bitmap(w, h)
        self._backgroundDC.SelectObject(self._background)

        if self.IsTransparent():

            self._backgroundDC.Blit(0, 0, w, h, parentdc, self.GetPosition().x,
                                    self.GetPosition().y)

        else:

            self._backgroundDC.SetBackground(wx.Brush(self._backcolour))
            self._backgroundDC.Clear()

        self.Refresh()


    def SetHorizontalBorder(self, value):
        """
        Sets the legend's horizontal border.

        :param `value`: the horizontal border thickness, in pixels.
        """

        self._horborder = value
        self.Refresh()


    def GetHorizontalBorder(self):
        """ Returns the legend's horizontal border, in pixels. """

        return self._horborder


    def SetVerticalBorder(self, value):
        """
        Sets the legend's vertical border.

        :param `value`: the horizontal border thickness, in pixels.
        """

        self._verborder = value
        self.Refresh()


    def GetVerticalBorder(self):
        """ Returns the legend's vertical border, in pixels. """

        return self._verborder


    def SetLabelColour(self, colour):
        """
        Sets the legend label colour.

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._labelcolour = colour
        self.Refresh()


    def GetLabelColour(self):
        """ Returns the legend label colour. """

        return self._labelcolour


    def SetLabelFont(self, font):
        """
        Sets the legend label font.

        :param `font`: a valid :class:`wx.Font` object.
        """

        self._labelfont = font
        self.Refresh()


    def GetLabelFont(self):
        """ Returns the legend label font. """

        return self._labelfont


    def SetBackColour(self, colour):
        """
        Sets the legend background colour.

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._backcolour = colour
        self.Refresh()


    def GetBackColour(self):
        """ Returns the legend background colour. """

        return self._backcolour


    def IsTransparent(self):
        """ Returns whether the legend background is transparent or not. """

        return self._istransparent


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`PieCtrlLegend`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        pdc = wx.PaintDC(self)

        w, h = self.GetSize()
        bmp = wx.Bitmap(w, h)
        mdc = wx.MemoryDC()
        mdc.SelectObject(bmp)

        if self.IsTransparent():

            parentdc = wx.ClientDC(self.GetParent())
            mdc.Blit(0, 0, w, h, self._backgroundDC, 0, 0)

        else:

            mdc.SetBackground(wx.Brush(self._backcolour))
            mdc.Clear()

        dy = self._verborder
        mdc.SetFont(self._labelfont)
        mdc.SetTextForeground(self._labelcolour)
        maxwidth = 0

        # local opts
        wxBrush = wx.Brush
        _parent_series = self._parent._series
        _horborder = self._horborder
        mdc_GetTextExtent = mdc.GetTextExtent
        mdc_SetBrush = mdc.SetBrush
        mdc_DrawCircle = mdc.DrawCircle
        mdc_DrawText = mdc.DrawText

        for ii in range(len(_parent_series)):

            tw, th = mdc_GetTextExtent(_parent_series[ii].GetLabel())
            mdc_SetBrush(wxBrush(_parent_series[ii].GetColour()))
            mdc_DrawCircle(_horborder+5, dy+th//2, 5)
            mdc_DrawText(_parent_series[ii].GetLabel(), _horborder+15, dy)
            dy = dy + th + 3
            maxwidth = max(maxwidth, int(2*_horborder+tw+15))

        dy = dy + self._verborder
        if w != maxwidth or h != dy:
            self.SetSize((maxwidth, dy))

        pdc.Blit(0, 0, w, h, mdc, 0, 0)


#----------------------------------------------------------------------
# Class PiePart
# This Class Handles The Legend Segments Properties, Such As Value,
# Colour And Label.
#----------------------------------------------------------------------

class PiePart(object):
    """
    This class handles the legend segments properties, such as value,
    colour and label.
    """

    def __init__(self, value=0, colour=wx.BLACK, label=""):
        """
        Default class constructor.

        :param `value`: the pie part value;
        :param `colour`: the pie part colour;
        :param `label`: the pie part text label.
        """

        self._value = value
        self._colour = colour
        self._label = label


    def SetValue(self, value):
        """
        Sets the segment absolute value.

        :param `value`: a floating point number representing the :class:`PiePart` value.
        """

        self._value = value


    def GetValue(self):
        """ Returns the segment absolute value. """

        return self._value


    def SetColour(self, colour):
        """
        Sets the segment colour.

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._colour = colour


    def GetColour(self):
        """ Returns the segment colour. """

        return self._colour


    def SetLabel(self, label):
        """
        Sets the segment label.

        :param `label`: the pie part text label.
        """

        self._label = label


    def GetLabel(self):
        """ Returns the segment label. """

        return self._label


#----------------------------------------------------------------------
# Class PieCtrl
# This Is The Main PieCtrl Implementation, Used Also By ProgressPie.
#----------------------------------------------------------------------

class PieCtrl(wx.Window):
    """
    :class:`PieCtrl` is somewhat a "static" control, that you may create in order to display
    a simple pie chart on a :class:`Panel` or similar.
    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name="PieCtrl"):
        """
        Default class constructor.

        :param `parent`: the :class:`PieCtrl` parent. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the window style (unused);
        :param `name`: the window name.
        """

        wx.Window.__init__(self, parent, id, pos, size, style, name)

        self._angle = pi/12.0
        self._rotationangle = 0
        self._height = 10
        self._background = wx.NullBitmap
        self._canvasbitmap = wx.Bitmap(1, 1)
        self._canvasDC = wx.MemoryDC()
        self._backcolour = wx.WHITE
        self._showedges = True
        self._series = []

        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.RecreateCanvas()
        self._legend = PieCtrlLegend(self, "PieCtrl", -1, wx.Point(10,10), wx.Size(100,75))


    def SetBackground(self, bmp):
        """
        Sets the :class:`PieCtrl` background image.

        :param `bmp`: a valid :class:`wx.Bitmap` object.
        """

        self._background = bmp
        self.Refresh()


    def GetBackground(self):
        """ Returns the :class:`PieCtrl` background image. """

        return self._background


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`PieCtrl`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        self.RecreateCanvas()
        self.Refresh()
        event.Skip()


    def RecreateCanvas(self):
        """ Recreates the :class:`PieCtrl` container (canvas). """

        self._canvasbitmap = wx.Bitmap(max(1, self.GetSize().GetWidth()),
                                       max(1, self.GetSize().GetHeight()))
        self._canvasDC.SelectObject(self._canvasbitmap)


    def GetPartAngles(self):
        """ Returns the angles associated to all segments. """

        angles = []
        total = 0.0

        _series = self._series  # local opt

        for ii in range(len(_series)):
            total = total + _series[ii].GetValue()

        current = 0.0
        angles.append(current)

        for ii in range(len(_series)):

            current = current + _series[ii].GetValue()
            angles.append(360.0*current/total)

        return angles


    def SetAngle(self, angle):
        """
        Sets the orientation angle for :class:`PieCtrl`.

        :param `angle`: the orientation angle for :class:`PieCtrl`, in radians.
        """
        if angle < 0:
            angle = 0
        if angle > pi/2:
            angle = pi/2

        self._angle = angle
        self.Refresh()


    def GetAngle(self):
        """ Returns the orientation angle for :class:`PieCtrl`, in radians. """

        return self._angle


    def SetRotationAngle(self, angle):
        """
        Sets the angle at which the first sector starts.

        :param `angle`: the first sector angle, in radians.
        """

        if angle < 0:
            angle = 0
        if angle > 2*pi:
            angle = 2*pi

        self._rotationangle = angle
        self.Refresh()


    def GetRotationAngle(self):
        """ Returns the angle at which the first sector starts, in radians. """

        return self._rotationangle


    def SetShowEdges(self, value=True):
        """
        Sets whether the :class:`PieCtrl` edges are visible or not.

        :param `value`: ``True`` to show the edges, ``False`` to hide them.
        """

        self._showedges = value
        self.Refresh()


    def GetShowEdges(self):
        """ Returns whether the :class:`PieCtrl` edges are visible or not. """

        return self._showedges


    def SetBackColour(self, colour):
        """
        Sets the :class:`PieCtrl` background colour.

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._backcolour = colour
        self.Refresh()


    def GetBackColour(self):
        """ Returns the :class:`PieCtrl` background colour. """

        return self._backcolour


    def SetHeight(self, value):
        """
        Sets the height (in pixels) of the :class:`PieCtrl`.

        :param `value`: the new height of the widget, in pixels.
        """

        self._height = value


    def GetHeight(self):
        """ Returns the height (in pixels) of the :class:`PieCtrl`. """

        return self._height


    def GetLegend(self):
        """ Returns the :class:`PieCtrl` legend. """

        return self._legend


    def DrawParts(self, dc, cx, cy, w, h):
        """
        Draws the :class:`PieCtrl` external edges.

        :param `dc`: an instance of :class:`wx.DC`;
        :param `cx`: the part `x` coordinate;
        :param `cy`: the part `y` coordinate;
        :param `w`: the control's width;
        :param `h`: the control's height.
        """

        # local opts
        _angle = self._angle
        _rotationangle = self._rotationangle
        wxPen = wx.Pen
        wxBrush = wx.Brush
        dc_SetPen = dc.SetPen
        dc_SetBrush = dc.SetBrush
        dc_DrawEllipticArc = dc.DrawEllipticArc

        angles = self.GetPartAngles()
        oldpen = dc.GetPen()

        if self._showedges:
            dc_SetPen(wx.BLACK_PEN)

        for ii in range(len(angles)):
            if ii > 0:
                if not self._showedges:
                    dc_SetPen(wxPen(self._series[ii-1].GetColour()))

                dc_SetBrush(wxBrush(self._series[ii-1].GetColour()))

                if angles[ii-1] != angles[ii]:
                    height = int(h*sin(_angle))
                    if height > 0:
                        dc_DrawEllipticArc(0, int((1-sin(_angle))*(h//2)+cy),
                                        w, height,
                                        angles[ii-1]+_rotationangle/pi*180,
                                        angles[ii]+_rotationangle/pi*180)

        if len(self._series) == 1:
            height = int(h*sin(_angle))
            if height > 0:
                dc_SetBrush(wxBrush(self._series[0].GetColour()))
                dc_DrawEllipticArc(0, int((1-sin(_angle))*(h//2)+cy),
                                w, height, 0, 360)

        dc_SetPen(oldpen)


    def Draw(self, dc):
        """
        Draws all the sectors of :class:`PieCtrl`.

        :param `dc`: an instance of :class:`wx.DC`.
        """

        w, h = self.GetSize()

        # local opts
        _angle = self._angle
        _rotationangle = self._rotationangle
        _height = self._height
        _canvasDC = self._canvasDC
        wxBrush = wx.Brush
        wxPen = wx.Pen
        wxColour = wx.Colour
        _canvasDC_SetBrush = _canvasDC.SetBrush
        _canvasDC_SetPen = _canvasDC.SetPen
        _canvasDC_GetPen = _canvasDC.GetPen
        _canvasDC_DrawPolygon = _canvasDC.DrawPolygon
        tau = pi * 2

        _canvasDC.SetBackground(wx.WHITE_BRUSH)
        _canvasDC.Clear()

        if self._background != wx.NullBitmap:
            ## for ii in range(0, w, self._background.GetWidth()):
            ##     for jj in range(0, h, self._background.GetHeight()):
            ##         _canvasDC.DrawBitmap(self._background, ii, jj)
            _background = self._background
            bw, bh = _background.GetSize()
            _canvasDC_DrawBitmap = _canvasDC.DrawBitmap
            [_canvasDC_DrawBitmap(_background, ii, jj)
                for jj in range(0, h, bh)
                    for ii in range(0, w, bw)]
        else:
            _canvasDC.SetBackground(wxBrush(self._backcolour))
            _canvasDC.Clear()

        if len(self._series) > 0:
            _series = self._series  # local opt

            if _angle <= pi/2:
                self.DrawParts(_canvasDC, 0, int(_height*cos(_angle)), w, h)
            else:
                self.DrawParts(_canvasDC, 0, 0, w, h)

            points = [[0, 0]]*4
            triangle = [[0, 0]]*3
            _canvasDC_SetPen(wx.BLACK_PEN)
            angles = self.GetPartAngles()
            angleindex = 0
            c = _series[angleindex].GetColour()
            _canvasDC_SetBrush(wxBrush(wxColour(c.red, c.green, c.blue)))
            changeangle = False
            x = 0.0

            while x <= tau:

                changeangle = False

                if angleindex < len(angles):

                    if x/pi*180.0 >= angles[angleindex+1]:

                        changeangle = True
                        x = angles[angleindex+1]*pi/180.0

                points[0] = points[1]
                px = int(w/2.0*(1+cos(x+_rotationangle)))
                py = int(h/2.0-sin(_angle)*h/2.0*sin(x+_rotationangle)-1)
                points[1] = [px, py]
                triangle[0] = [w // 2, h // 2]
                triangle[1] = points[0]
                triangle[2] = points[1]

                if x > 0:

                    _canvasDC_SetBrush(wxBrush(_series[angleindex].GetColour()))
                    oldPen = _canvasDC_GetPen()
                    _canvasDC_SetPen(wxPen(_series[angleindex].GetColour()))
                    _canvasDC_DrawPolygon(triangle)
                    _canvasDC_SetPen(oldPen)

                if changeangle:

                    angleindex = angleindex + 1

                x = x + 0.05

            points[0] = points[1]
            px = int(w/2.0 * (1+cos(tau+_rotationangle)))
            py = int(h/2.0-sin(_angle)*h/2.0*sin(tau+_rotationangle)-1)
            points[1] = [px, py]
            triangle[0] = [w // 2, h // 2]
            triangle[1] = points[0]
            triangle[2] = points[1]

            _canvasDC_SetBrush(wxBrush(_series[angleindex].GetColour()))
            oldPen = _canvasDC_GetPen()
            _canvasDC_SetPen(wxPen(_series[angleindex].GetColour()))
            _canvasDC_DrawPolygon(triangle)

            _canvasDC_SetPen(oldPen)
            angleindex = 0

            x = 0.0

            while x <= tau:

                changeangle = False
                if angleindex < len(angles):

                    if x/pi*180 >= angles[angleindex+1]:

                        changeangle = True
                        x = angles[angleindex+1]*pi/180

                points[0] = points[1]
                points[3] = points[2]
                px = int(w/2.0 * (1+cos(x+_rotationangle)))
                py = int(h/2.0-sin(_angle)*h/2.0*sin(x+_rotationangle)-1)
                points[1] = [px, py]
                points[2] = [px, int(py+_height*cos(_angle))]

                if w > 0:
                    c = _series[angleindex].GetColour()
                    v = 1.0-float(px)/w
                    curColour = wxColour(int(c.red*v), int(c.green*v), int(c.blue*v))

                    if not self._showedges:
                        _canvasDC_SetPen(wxPen(curColour))

                    _canvasDC_SetBrush(wxBrush(curColour))

                if sin(x+_rotationangle) < 0 and sin(x-0.05+_rotationangle) <= 0 and x > 0:
                    _canvasDC_DrawPolygon(points)

                if changeangle:

                    angleindex = angleindex + 1

                x = x + 0.05

            points[0] = points[1]
            points[3] = points[2]
            px = int(w/2.0 * (1+cos(tau+_rotationangle)))
            py = int(h/2.0-sin(_angle)*h/2.0*sin(tau+_rotationangle)-1)
            points[1] = [px, py]
            points[2] = [px, int(py+_height*cos(_angle))]

            if w > 0:
                c = _series[angleindex].GetColour()
                v = 1.0-float(px)/w
                curColour = wxColour(int(c.red*v), int(c.green*v), int(c.blue*v))

                if not self._showedges:
                    _canvasDC_SetPen(wxPen(curColour))

                _canvasDC_SetBrush(wxBrush(curColour))

            if sin(x+_rotationangle) < 0 and sin(x-0.05+_rotationangle) <= 0:
                _canvasDC_DrawPolygon(points)

            if _angle <= pi/2:
                self.DrawParts(_canvasDC, 0, 0, w, h)
            else:
                self.DrawParts(_canvasDC, 0, int(_height*cos(_angle)), w, h)

        dc.Blit(0, 0, w, h, _canvasDC, 0, 0)
        self._legend.RecreateBackground(_canvasDC)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`PieCtrl`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        pdc = wx.PaintDC(self)
        self.Draw(pdc)


#----------------------------------------------------------------------
# Class ProgressPie
# This Is The Main ProgressPie Implementation. Is Is A Subclassing Of
# PieCtrl, With 2 Sectors.
#----------------------------------------------------------------------

class ProgressPie(PieCtrl):
    """
    :class:`ProgressPie` tries to emulate the behavior of :class:`ProgressDialog`, but
    using a pie chart instead of a gauge.
    """

    def __init__(self, parent, maxvalue, value, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        """
        Default class constructor.

        :param `parent`: the :class:`PieCtrl` parent. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the window style (unused);
        :param `name`: the window name.
        """

        PieCtrl.__init__(self, parent, id, pos, size, style)

        self._maxvalue = maxvalue
        self._value = value
        self.GetLegend().Hide()

        self._filledcolour = wx.Colour(0, 0, 127)
        self._unfilledcolour = wx.WHITE
        part = PiePart()
        part.SetColour(self._filledcolour)
        a = min(float(value), maxvalue)
        part.SetValue(max(a, 0.0))
        self._series.append(part)
        part = PiePart()
        part.SetColour(self._unfilledcolour)
        part.SetValue(max(0.0, maxvalue-part.GetValue()))
        self._series.append(part)


    def SetValue(self, value):
        """
        Sets the :class:`ProgressPie` value.

        :param `value`: a floating point number representing the new value.
        """

        self._value = min(value, self._maxvalue)
        self._series[0].SetValue(max(self._value, 0.0))
        self._series[1].SetValue(max(self._maxvalue-self._value, 0.0))
        self.Refresh()


    def GetValue(self):
        """ Returns the :class:`ProgressPie` value. """

        return self._value


    def SetMaxValue(self, value):
        """
        Sets the :class:`ProgressPie` maximum value.

        :param `value`: a floating point number representing the maximum value.
        """

        self._maxvalue = value
        self._value = min(self._value, self._maxvalue)
        self._series[0].SetValue(max(self._value, 0.0))
        self._series[1].SetValue(max(self._maxvalue-self._value, 0.0))
        self.Refresh()


    def GetMaxValue(self):
        """ Returns the :class:`ProgressPie`  maximum value. """

        return self._maxvalue


    def SetFilledColour(self, colour):
        """
        Sets the colour that progressively fills the :class:`ProgressPie` .

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._filledcolour = colour
        self._series[0].SetColour(self._filledcolour)
        self.Refresh()


    def SetUnfilledColour(self, colour):
        """
        Sets the colour that is filled.

        :param `colour`: a valid :class:`wx.Colour` object.
        """

        self._unfilledcolour= colour
        self._series[1].SetColour(self._unfilledcolour)
        self.Refresh()


    def GetFilledColour(self):
        """ Returns the colour that progressively fills the :class:`ProgressPie`. """

        return self._filledcolour


    def GetUnfilledColour(self):
        """ Returns the colour that is filled. """

        return self._unfilledcolour



if __name__ == '__main__':

    import wx

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "PieCtrl Demo")

            panel = wx.Panel(self)

            # create a simple PieCtrl with 3 sectors
            mypie = PieCtrl(panel, -1, wx.DefaultPosition, wx.Size(180,270))

            part = PiePart()

            part.SetLabel("Label 1")
            part.SetValue(300)
            part.SetColour(wx.Colour(200, 50, 50))
            mypie._series.append(part)

            part = PiePart()

            part.SetLabel("Label 2")
            part.SetValue(200)
            part.SetColour(wx.Colour(50, 200, 50))
            mypie._series.append(part)

            part = PiePart()

            part.SetLabel("helloworld label 3")
            part.SetValue(50)
            part.SetColour(wx.Colour(50, 50, 200))
            mypie._series.append(part)

            # create a ProgressPie
            progress_pie = ProgressPie(panel, 100, 50, -1, wx.DefaultPosition,
                                       wx.Size(180, 200), wx.SIMPLE_BORDER)

            progress_pie.SetBackColour(wx.Colour(150, 200, 255))
            progress_pie.SetFilledColour(wx.RED)
            progress_pie.SetUnfilledColour(wx.WHITE)
            progress_pie.SetHeight(20)

            main_sizer = wx.BoxSizer(wx.HORIZONTAL)

            main_sizer.Add(mypie, 1, wx.EXPAND | wx.ALL, 5)
            main_sizer.Add(progress_pie, 1, wx.EXPAND | wx.ALL, 5)

            panel.SetSizer(main_sizer)
            main_sizer.Layout()


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()
