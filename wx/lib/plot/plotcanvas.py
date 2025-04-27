# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0330, C0103
#   E1101: Module X has no Y member
#   C0330: Wrong continued indentation
#   C0103: Invalid attribute/variable/method name
"""
plotcanvas.py
=============

This is the main window that you will want to import into your application.

"""
__docformat__ = "restructuredtext en"

# Standard Library
import sys
import time as _time

# Third-Party
import wx
import numpy as np

# Package
from .polyobjects import PlotPrintout
from .polyobjects import PolyMarker, PolyLine, PolyBoxPlot
from .utils import DisplaySide
from .utils import set_displayside
from .utils import pendingDeprecation
from .utils import TempStyle
from .utils import scale_and_shift_point


class PlotCanvas(wx.Panel):
    """
    Creates a PlotCanvas object.

    Subclass of a wx.Panel which holds two scrollbars and the actual
    plotting canvas (self.canvas). It allows for simple general plotting
    of data with zoom, labels, and automatic axis scaling.

    This is the main window that you will want to import into your
    application.

    Parameters for ``__init__`` are the same as any :class:`wx.Panel`.
    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name="plotCanvas"):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        sizer = wx.FlexGridSizer(2, 2, 0, 0)
        self.canvas = wx.Window(self, -1)
        self.sb_vert = wx.ScrollBar(self, -1, style=wx.SB_VERTICAL)
        self.sb_vert.SetScrollbar(0, 1000, 1000, 1000)
        self.sb_hor = wx.ScrollBar(self, -1, style=wx.SB_HORIZONTAL)
        self.sb_hor.SetScrollbar(0, 1000, 1000, 1000)

        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.sb_vert, 0, wx.EXPAND)
        sizer.Add(self.sb_hor, 0, wx.EXPAND)
        sizer.Add((0, 0))

        self.sb_vert.Show(False)
        self.sb_hor.Show(False)

        self.SetSizer(sizer)
        sizer.AddGrowableRow(0, 1)
        sizer.AddGrowableCol(0, 1)
        self.Fit()

        self.border = (1, 1)

        self.SetBackgroundColour("white")
        self.SetForegroundColour("black")

        # Create some mouse events for zooming
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.canvas.Bind(wx.EVT_MOTION, self.OnMotion)
        self.canvas.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseDoubleClick)
        self.canvas.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)

        # scrollbar events
        self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnScroll)
        self.Bind(wx.EVT_SCROLL_PAGEUP, self.OnScroll)
        self.Bind(wx.EVT_SCROLL_PAGEDOWN, self.OnScroll)
        self.Bind(wx.EVT_SCROLL_LINEUP, self.OnScroll)
        self.Bind(wx.EVT_SCROLL_LINEDOWN, self.OnScroll)

        # set cursor as cross-hairs
        self.defaultCursor = wx.Cursor(wx.CURSOR_ARROW)
        self.HandCursor = wx.Cursor(wx.CURSOR_SIZING)
        self.GrabHandCursor = wx.Cursor(wx.CURSOR_SIZING)
        self.MagCursor = wx.Cursor(wx.CURSOR_MAGNIFIER)
        self.canvas.SetCursor(self.defaultCursor)

        # Things for printing
        self._print_data = None
        self._pageSetupData = None
        self.printerScale = 1
        self.parent = parent

        # scrollbar variables
        self._sb_ignore = False
        self._sb_show = False
        self._adjustingSB = False
        self._sb_xfullrange = 0
        self._sb_yfullrange = 0
        self._sb_xunit = 0
        self._sb_yunit = 0

        self._screenCoordinates = np.array([0.0, 0.0])

        # Zooming variables
        self._zoomInFactor = 0.5
        self._zoomOutFactor = 2
        self._zoomCorner1 = np.array([0.0, 0.0])  # left mouse down corner
        self._zoomCorner2 = np.array([0.0, 0.0])   # left mouse up corner
        self._zoomEnabled = False
        self._hasDragged = False

        # Drawing Variables
        self.last_draw = None
        self._pointScale = 1
        self._pointShift = 0
        self._xSpec = 'auto'
        self._ySpec = 'auto'

        # Initial Plot Options
        self._dragEnabled = False
        self._logscale = (False, False)
        self._absScale = (False, False)
        self._gridEnabled = (True, True)
        self._legendEnabled = False
        self._titleEnabled = True
        self._xAxisLabelEnabled = True
        self._yAxisLabelEnabled = True
        self._axesLabelsEnabled = True
        self._centerLinesEnabled = False
        self._diagonalsEnabled = False
        self._ticksEnabled = DisplaySide(False, False, False, False)
        self._axesEnabled = DisplaySide(True, True, True, True)
        self._axesValuesEnabled = DisplaySide(True, True, False, False)

        # Fonts
        self._fontCache = {}
        self._fontSizeAxis = 10
        self._fontSizeTitle = 15
        self._fontSizeLegend = 7

        # pointLabels
        self._pointLabelEnabled = False
        self.last_PointLabel = None
        self._pointLabelFunc = None
        self.canvas.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        if sys.platform != "darwin":
            self._logicalFunction = wx.EQUIV  # (NOT src) XOR dst
        else:
            # wx.EQUIV not supported on Mac OS X
            self._logicalFunction = wx.COPY

        self._useScientificNotation = False

        self._antiAliasingEnabled = False
        self._hiResEnabled = False
        self._pointSize = (1.0, 1.0)
        self._fontScale = 1.0

        self.canvas.Bind(wx.EVT_PAINT, self.OnPaint)
        self.canvas.Bind(wx.EVT_SIZE, self.OnSize)
        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)  # sets the initial size based on client size

        # Default Pens
        self._gridPen = wx.Pen(wx.Colour(180, 180, 180, 255),
                               int(self._pointSize[0]),
                               wx.PENSTYLE_DOT)

        self._centerLinePen = wx.Pen(wx.RED,
                                     int(self._pointSize[0]),
                                     wx.PENSTYLE_SHORT_DASH)

        self._axesPen = wx.Pen(wx.BLACK,
                               int(self._pointSize[0]),
                               wx.PENSTYLE_SOLID)

        self._tickPen = wx.Pen(wx.BLACK,
                               int(self._pointSize[0]),
                               wx.PENSTYLE_SOLID)
        self._tickLength = tuple(-x * 2 for x in self._pointSize)

        self._diagonalPen = wx.Pen(wx.BLUE,
                                   int(self._pointSize[0]),
                                   wx.PENSTYLE_DOT_DASH)

    def SetCursor(self, cursor):
        self.canvas.SetCursor(cursor)

    ### Pen Properties
    @property
    def gridPen(self):
        """
        The :class:`wx.Pen` used to draw the grid lines on the plot.

        :getter: Returns the :class:`wx.Pen` used for drawing the grid
                 lines.
        :setter: Sets the :class:`wx.Pen` use for drawging the grid lines.
        :type:   :class:`wx.Pen`
        :raise:  `TypeError` when setting a value that is not a
                 :class:`wx.Pen`.
        """
        return self._gridPen

    @gridPen.setter
    def gridPen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._gridPen = pen

    @property
    def diagonalPen(self):
        """
        The :class:`wx.Pen` used to draw the diagonal lines on the plot.

        :getter: Returns the :class:`wx.Pen` used for drawing the diagonal
                 lines.
        :setter: Sets the :class:`wx.Pen` use for drawging the diagonal lines.
        :type:   :class:`wx.Pen`
        :raise:  `TypeError` when setting a value that is not a
                 :class:`wx.Pen`.
        """
        return self._diagonalPen

    @diagonalPen.setter
    def diagonalPen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._diagonalPen = pen

    @property
    def centerLinePen(self):
        """
        The :class:`wx.Pen` used to draw the center lines on the plot.

        :getter: Returns the :class:`wx.Pen` used for drawing the center
                 lines.
        :setter: Sets the :class:`wx.Pen` use for drawging the center lines.
        :type:   :class:`wx.Pen`
        :raise:  `TypeError` when setting a value that is not a
                 :class:`wx.Pen`.
        """
        return self._centerLinePen

    @centerLinePen.setter
    def centerLinePen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._centerLinePen = pen

    @property
    def axesPen(self):
        """
        The :class:`wx.Pen` used to draw the axes lines on the plot.

        :getter: Returns the :class:`wx.Pen` used for drawing the axes
                 lines.
        :setter: Sets the :class:`wx.Pen` use for drawging the axes lines.
        :type:   :class:`wx.Pen`
        :raise:  `TypeError` when setting a value that is not a
                 :class:`wx.Pen`.
        """
        return self._axesPen

    @axesPen.setter
    def axesPen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._axesPen = pen

    @property
    def tickPen(self):
        """
        The :class:`wx.Pen` used to draw the tick marks on the plot.

        :getter: Returns the :class:`wx.Pen` used for drawing the tick marks.
        :setter: Sets the :class:`wx.Pen` use for drawging the tick marks.
        :type:   :class:`wx.Pen`
        :raise:  `TypeError` when setting a value that is not a
                 :class:`wx.Pen`.
        """
        return self._tickPen

    @tickPen.setter
    def tickPen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._tickPen = pen

    @property
    def tickLength(self):
        """
        The length of the tick marks on an axis.

        :getter: Returns the length of the tick marks.
        :setter: Sets the length of the tick marks.
        :type:   tuple of (xlength, ylength): int or float
        :raise:  `TypeError` when setting a value that is not an int or float.
        """
        return self._tickLength

    @tickLength.setter
    def tickLength(self, length):
        if not isinstance(length, (tuple, list)):
            raise TypeError("`length` must be a 2-tuple of ints or floats")
        self._tickLength = length

    @property
    def tickLengthPrinterScale(self):
        return (3 * self.printerScale * self._tickLength[0],
                3 * self.printerScale * self._tickLength[1])

    # SaveFile
    def SaveFile(self, fileName=''):
        """
        Saves the file to the type specified in the extension. If no file
        name is specified a dialog box is provided.  Returns True if
        successful, otherwise False.

        .bmp  Save a Windows bitmap file.
        .xbm  Save an X bitmap file.
        .xpm  Save an XPM bitmap file.
        .png  Save a Portable Network Graphics file.
        .jpg  Save a Joint Photographic Experts Group file.

        """
        extensions = {
            "bmp": wx.BITMAP_TYPE_BMP,       # Save a Windows bitmap file.
            "xbm": wx.BITMAP_TYPE_XBM,       # Save an X bitmap file.
            "xpm": wx.BITMAP_TYPE_XPM,       # Save an XPM bitmap file.
            "jpg": wx.BITMAP_TYPE_JPEG,      # Save a JPG file.
            "png": wx.BITMAP_TYPE_PNG,       # Save a PNG file.
        }

        fType = fileName[-3:].lower()
        dlg1 = None
        while fType not in extensions:

            msg_txt = ('File name extension\n'  # implicit str concat
                       'must be one of\nbmp, xbm, xpm, png, or jpg')

            if dlg1:               # FileDialog exists: Check for extension
                dlg2 = wx.MessageDialog(self, msg_txt, 'File Name Error',
                                        wx.OK | wx.ICON_ERROR)
                try:
                    dlg2.ShowModal()
                finally:
                    dlg2.Destroy()
            # FileDialog doesn't exist: just check one
            else:
                msg_txt = ("Choose a file with extension bmp, "
                           "gif, xbm, xpm, png, or jpg")
                wildcard_str = ("BMP files (*.bmp)|*.bmp|XBM files (*.xbm)|"
                                "*.xbm|XPM file (*.xpm)|*.xpm|"
                                "PNG files (*.png)|*.png|"
                                "JPG files (*.jpg)|*.jpg")
                dlg1 = wx.FileDialog(self,
                                     msg_txt,
                                     ".",
                                     "",
                                     wildcard_str,
                                     wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                                     )

            if dlg1.ShowModal() == wx.ID_OK:
                fileName = dlg1.GetPath()
                fType = fileName[-3:].lower()
            else:                      # exit without saving
                dlg1.Destroy()
                return False

        if dlg1:
            dlg1.Destroy()

        # Save Bitmap
        res = self._Buffer.SaveFile(fileName, extensions[fType])
        return res

    @property
    def print_data(self):
        if not self._print_data:
            self._print_data = wx.PrintData()
            self._print_data.SetPaperId(wx.PAPER_LETTER)
            self._print_data.SetOrientation(wx.LANDSCAPE)
        return self._print_data

    @property
    def pageSetupData(self):
        if not self._pageSetupData:
            self._pageSetupData = wx.PageSetupDialogData()
            self._pageSetupData.SetMarginBottomRight((25, 25))
            self._pageSetupData.SetMarginTopLeft((25, 25))
            self._pageSetupData.SetPrintData(self.print_data)
        return self._pageSetupData

    def PageSetup(self):
        """Brings up the page setup dialog"""
        data = self.pageSetupData
        data.SetPrintData(self.print_data)
        dlg = wx.PageSetupDialog(self.parent, data)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetPageSetupData()
                # updates page parameters from dialog
                self.pageSetupData.SetMarginBottomRight(
                    data.GetMarginBottomRight())
                self.pageSetupData.SetMarginTopLeft(data.GetMarginTopLeft())
                self.pageSetupData.SetPrintData(data.GetPrintData())
                self._print_data = wx.PrintData(
                    data.GetPrintData())  # updates print_data
        finally:
            dlg.Destroy()

    def Printout(self, paper=None):
        """Print current plot."""
        if paper is not None:
            self.print_data.SetPaperId(paper)
        pdd = wx.PrintDialogData(self.print_data)
        printer = wx.Printer(pdd)
        out = PlotPrintout(self)
        print_ok = printer.Print(self.parent, out)
        if print_ok:
            self._print_data = wx.PrintData(
                printer.GetPrintDialogData().GetPrintData())
        out.Destroy()

    def PrintPreview(self):
        """Print-preview current plot."""
        printout = PlotPrintout(self)
        printout2 = PlotPrintout(self)
        self.preview = wx.PrintPreview(printout, printout2, self.print_data)
        if not self.preview.IsOk():
            wx.MessageDialog(self, "Print Preview failed.\n"
                             "Check that default printer is configured\n",
                             "Print error", wx.OK | wx.CENTRE).ShowModal()
        self.preview.SetZoom(40)
        # search up tree to find frame instance
        frameInst = self
        while not isinstance(frameInst, wx.Frame):
            frameInst = frameInst.GetParent()
        frame = wx.PreviewFrame(self.preview, frameInst, "Preview")
        frame.Initialize()
        frame.SetPosition(self.GetPosition())
        frame.SetSize((600, 550))
        frame.Centre(wx.BOTH)
        frame.Show(True)

    def setLogScale(self, logscale):
        """
        Set the log scale boolean value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.logScale`
           property instead.
        """
        pendingDeprecation("self.logScale property")
        self.logScale = logscale

    def getLogScale(self):
        """
        Set the log scale boolean value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.logScale`
           property instead.
        """
        pendingDeprecation("self.logScale property")
        return self.logScale

    @property
    def logScale(self):
        """
        The logScale value as a 2-tuple of bools:
        ``(x_axis_is_log_scale, y_axis_is_log_scale)``.

        :getter: Returns the value of logScale.
        :setter: Sets the value of logScale.
        :type:   tuple of bools, length 2
        :raise:  `TypeError` when setting an invalid value.
        """
        return self._logscale

    @logScale.setter
    def logScale(self, logscale):
        if type(logscale) != tuple:
            raise TypeError(
                'logscale must be a tuple of bools, e.g. (False, False)'
            )
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            graphics.logScale = logscale
            self.last_draw = (graphics, None, None)
        self.xSpec = 'min'
        self.ySpec = 'min'
        self._logscale = logscale

    @property
    def absScale(self):
        """
        The absScale value as a 2-tuple of bools:
        ``(x_axis_is_abs_scale, y_axis_is_abs_scale)``.

        :getter: Returns the value of absScale.
        :setter: Sets the value of absScale.
        :type:   tuple of bools, length 2
        :raise:  `TypeError` when setting an invalid value.
        """
        return self._absScale

    @absScale.setter
    def absScale(self, absscale):
        if not isinstance(absscale, tuple):
            raise TypeError(
                "absscale must be tuple of bools, e.g. (False, False)"
            )
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            graphics.absScale = absscale
            self.last_draw = (graphics, None, None)
        self.xSpec = 'min'
        self.ySpec = 'min'
        self._absScale = absscale

    def SetFontSizeAxis(self, point=10):
        """
        Set the tick and axis label font size (default is 10 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.fontSizeAxis`
           property
           instead.
        """
        pendingDeprecation("self.fontSizeAxis property")
        self.fontSizeAxis = point

    def GetFontSizeAxis(self):
        """
        Get current tick and axis label font size in points

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.fontSizeAxis`
           property
           instead.
        """
        pendingDeprecation("self.fontSizeAxis property")
        return self.fontSizeAxis

    @property
    def fontSizeAxis(self):
        """
        The current tick and axis label font size in points.

        Default is 10pt font.

        :getter: Returns the value of fontSizeAxis.
        :setter: Sets the value of fontSizeAxis.
        :type:   int or float
        """
        return self._fontSizeAxis

    @fontSizeAxis.setter
    def fontSizeAxis(self, value):
        self._fontSizeAxis = value

    def SetFontSizeTitle(self, point=15):
        """
        Set Title font size (default is 15 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.fontSizeTitle`
           property instead.
        """
        pendingDeprecation("self.fontSizeTitle property")
        self.fontSizeTitle = point

    def GetFontSizeTitle(self):
        """
        Get Title font size (default is 15 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.fontSizeTitle`
           property instead.
        """
        pendingDeprecation("self.fontSizeTitle property")
        return self.fontSizeTitle

    @property
    def fontSizeTitle(self):
        """
        The current Title font size in points.

        Default is 15pt font.

        :getter: Returns the value of fontSizeTitle.
        :setter: Sets the value of fontSizeTitle.
        :type:   int or float
        """
        return self._fontSizeTitle

    @fontSizeTitle.setter
    def fontSizeTitle(self, pointsize):
        self._fontSizeTitle = pointsize

    def SetFontSizeLegend(self, point=7):
        """
        Set legend font size (default is 7 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.fontSizeLegend'
           property instead.
        """
        pendingDeprecation("self.fontSizeLegend property")
        self.fontSizeLegend = point

    def GetFontSizeLegend(self):
        """
        Get legend font size (default is 7 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.fontSizeLegend'
           property instead.
        """
        return self.fontSizeLegend

    @property
    def fontSizeLegend(self):
        """
        The current Legned font size in points.

        Default is 7pt font.

        :getter: Returns the value of fontSizeLegend.
        :setter: Sets the value of fontSizeLegend.
        :type:   int or float
        """
        return self._fontSizeLegend

    @fontSizeLegend.setter
    def fontSizeLegend(self, point):
        self._fontSizeLegend = point

    def SetShowScrollbars(self, value):
        """
        Set the showScrollbars value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.showScrollbars`
           property instead.
        """
        pendingDeprecation("self.showScrollbars property")
        self.showScrollbars = value

    def GetShowScrollbars(self):
        """
        Get the showScrollbars value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.showScrollbars`
           property instead.
        """
        pendingDeprecation("self.showScrollbars property")
        return self.showScrollbars

    @property
    def showScrollbars(self):
        """
        The current showScrollbars value.

        :getter: Returns the value of showScrollbars.
        :setter: Sets the value of showScrollbars.
        :type:   bool
        :raises: `TypeError` if setting a non-boolean value.
        """
        return self._sb_show

    @showScrollbars.setter
    def showScrollbars(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value should be True or False")
        if value == self._sb_show:
            # no change, so don't do anything
            return
        self._sb_show = value
        self.sb_vert.Show(value)
        self.sb_hor.Show(value)

        def _do_update():
            self.Layout()
            if self.last_draw is not None:
                self._adjustScrollbars()
        wx.CallAfter(_do_update)

    def SetUseScientificNotation(self, useScientificNotation):
        """
        Set the useScientificNotation value.

        .. deprecated:: Feb 27, 2016

           Use the
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.useScientificNotation`
           property instead.
        """
        pendingDeprecation("self.useScientificNotation property")
        self.useScientificNotation = useScientificNotation

    def GetUseScientificNotation(self):
        """
        Get the useScientificNotation value.

        .. deprecated:: Feb 27, 2016

           Use the
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.useScientificNotation`
           property instead.
        """
        pendingDeprecation("self.useScientificNotation property")
        return self.useScientificNotation

    @property
    def useScientificNotation(self):
        """
        The current useScientificNotation value.

        :getter: Returns the value of useScientificNotation.
        :setter: Sets the value of useScientificNotation.
        :type:   bool
        :raises: `TypeError` if setting a non-boolean value.
        """
        return self._useScientificNotation

    @useScientificNotation.setter
    def useScientificNotation(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value should be True or False")
        self._useScientificNotation = value

    def SetEnableAntiAliasing(self, enableAntiAliasing):
        """
        Set the enableAntiAliasing value.

        .. deprecated:: Feb 27, 2016

           Use the
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableAntiAliasing`
           property instead.
        """
        pendingDeprecation("self.enableAntiAliasing property")
        self.enableAntiAliasing = enableAntiAliasing

    def GetEnableAntiAliasing(self):
        """
        Get the enableAntiAliasing value.

        .. deprecated:: Feb 27, 2016

           Use the
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableAntiAliasing`
           property instead.
        """
        pendingDeprecation("self.enableAntiAliasing property")
        return self.enableAntiAliasing

    @property
    def enableAntiAliasing(self):
        """
        The current enableAntiAliasing value.

        :getter: Returns the value of enableAntiAliasing.
        :setter: Sets the value of enableAntiAliasing.
        :type:   bool
        :raises: `TypeError` if setting a non-boolean value.
        """
        return self._antiAliasingEnabled

    @enableAntiAliasing.setter
    def enableAntiAliasing(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value should be True or False")
        self._antiAliasingEnabled = value
        self.Redraw()

    def SetEnableHiRes(self, enableHiRes):
        """
        Set the enableHiRes value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableHiRes`
           property instead.
        """
        pendingDeprecation("self.enableHiRes property")
        self.enableHiRes = enableHiRes

    def GetEnableHiRes(self):
        """
        Get the enableHiRes value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableHiRes`
           property instead.
        """
        pendingDeprecation("self.enableHiRes property")
        return self._hiResEnabled

    @property
    def enableHiRes(self):
        """
        The current enableHiRes value.

        :getter: Returns the value of enableHiRes.
        :setter: Sets the value of enableHiRes.
        :type:   bool
        :raises: `TypeError` if setting a non-boolean value.
        """
        return self._hiResEnabled

    @enableHiRes.setter
    def enableHiRes(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value should be True or False")
        self._hiResEnabled = value
        self.Redraw()

    def SetEnableDrag(self, value):
        """
        Set the enableDrag value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableDrag`
           property instead.
        """
        pendingDeprecation("self.enableDrag property")
        self.enableDrag = value

    def GetEnableDrag(self):
        """
        Get the enableDrag value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableDrag`
           property instead.
        """
        pendingDeprecation("self.enableDrag property")
        return self.enableDrag

    @property
    def enableDrag(self):
        """
        The current enableDrag value.

        :getter: Returns the value of enableDrag.
        :setter: Sets the value of enableDrag.
        :type:   bool
        :raises: `TypeError` if setting a non-boolean value.

        .. note::
           This is mutually exclusive with
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableZoom`. Setting
           one will disable the other.

        .. seealso::
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableZoom`
        """
        return self._dragEnabled

    @enableDrag.setter
    def enableDrag(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value must be a bool.")
        if value:
            if self.enableZoom:
                self.enableZoom = False
            self.SetCursor(self.HandCursor)
        else:
            self.SetCursor(self.defaultCursor)
        self._dragEnabled = value

    def SetEnableZoom(self, value):
        """
        Set the enableZoom value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableZoom`
           property instead.
        """
        pendingDeprecation("self.enableZoom property")
        self.enableZoom = value

    def GetEnableZoom(self):
        """
        Get the enableZoom value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableZoom`
           property instead.
        """
        pendingDeprecation("self.enableZoom property")
        return self.enableZoom

    @property
    def enableZoom(self):
        """
        The current enableZoom value.

        :getter: Returns the value of enableZoom.
        :setter: Sets the value of enableZoom.
        :type:   bool
        :raises: `TypeError` if setting a non-boolean value.

        .. note::
           This is mutually exclusive with
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableDrag`. Setting
           one will disable the other.

        .. seealso::
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableDrag`
        """
        return self._zoomEnabled

    @enableZoom.setter
    def enableZoom(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value must be a bool.")
        if value:
            if self.enableDrag:
                self.enableDrag = False
            self.SetCursor(self.MagCursor)
        else:
            self.SetCursor(self.defaultCursor)
        self._zoomEnabled = value

    def SetEnableGrid(self, value):
        """
        Set the enableGrid value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableGrid`
           property instead.
        """
        pendingDeprecation("self.enableGrid property")
        self.enableGrid = value

    def GetEnableGrid(self):
        """
        Get the enableGrid value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableGrid`
           property instead.
        """
        pendingDeprecation("self.enableGrid property")
        return self.enableGrid

    @property
    def enableGrid(self):
        """
        The current enableGrid value.

        :getter: Returns the value of enableGrid.
        :setter: Sets the value of enableGrid.
        :type:   bool or 2-tuple of bools
        :raises: `TypeError` if setting an invalid value.

        If set to a single boolean value, then both X and y grids will be
        enabled (``enableGrid = True``) or disabled (``enableGrid = False``).

        If a 2-tuple of bools, the 1st value is the X (vertical) grid and
        the 2nd value is the Y (horizontal) grid.
        """
        return self._gridEnabled

    @enableGrid.setter
    def enableGrid(self, value):
        if isinstance(value, bool):
            value = (value, value)
        elif isinstance(value, tuple) and len(value) == 2:
            pass
        else:
            err_txt = "Value must be a bool or 2-tuple of bool."
            raise TypeError(err_txt)

        self._gridEnabled = value
        self.Redraw()

    def SetEnableCenterLines(self, value):
        """
        Set the enableCenterLines value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableCenterLines`
           property instead.
        """
        pendingDeprecation("self.enableCenterLines property")
        self.enableCenterLines = value

    def GetEnableCenterLines(self):
        """
        Get the enableCenterLines value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableCenterLines`
           property instead.
        """
        pendingDeprecation("self.enableCenterLines property")
        return self.enableCenterLines

    @property
    def enableCenterLines(self):
        """
        The current enableCenterLines value.

        :getter: Returns the value of enableCenterLines.
        :setter: Sets the value of enableCenterLines.
        :type:   bool or str
        :raises: `TypeError` if setting an invalid value.

        If set to a single boolean value, then both horizontal and vertical
        lines will be enabled or disabled.

        If a string, must be one of ``('Horizontal', 'Vertical')``.
        """
        return self._centerLinesEnabled

    @enableCenterLines.setter
    def enableCenterLines(self, value):
        if value not in [True, False, 'Horizontal', 'Vertical']:
            raise TypeError(
                "Value should be True, False, 'Horizontal' or 'Vertical'")
        self._centerLinesEnabled = value
        self.Redraw()

    def SetEnableDiagonals(self, value):
        """
        Set the enableDiagonals value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableDiagonals`
           property instead.
        """
        pendingDeprecation("self.enableDiagonals property")
        self.enableDiagonals = value

    def GetEnableDiagonals(self):
        """
        Get the enableDiagonals value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableDiagonals`
           property instead.
        """
        pendingDeprecation("self.enableDiagonals property")
        return self.enableDiagonals

    @property
    def enableDiagonals(self):
        """
        The current enableDiagonals value.

        :getter: Returns the value of enableDiagonals.
        :setter: Sets the value of enableDiagonals.
        :type:   bool or str
        :raises: `TypeError` if setting an invalid value.

        If set to a single boolean value, then both diagonal lines will
        be enabled or disabled.

        If a string, must be one of ``('Bottomleft-Topright',
        'Bottomright-Topleft')``.
        """
        return self._diagonalsEnabled

    @enableDiagonals.setter
    def enableDiagonals(self, value):
        # TODO: Rename Bottomleft-TopRight, Bottomright-Topleft
        if value not in [True, False,
                         'Bottomleft-Topright', 'Bottomright-Topleft']:
            raise TypeError(
                "Value should be True, False, 'Bottomleft-Topright' or "
                "'Bottomright-Topleft'"
            )
        self._diagonalsEnabled = value
        self.Redraw()

    def SetEnableLegend(self, value):
        """
        Set the enableLegend value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableLegend`
           property instead.
        """
        pendingDeprecation("self.enableLegend property")
        self.enableLegend = value

    def GetEnableLegend(self):
        """
        Get the enableLegend value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableLegend`
           property instead.
        """
        pendingDeprecation("self.enableLegend property")
        return self.enableLegend

    @property
    def enableLegend(self):
        """
        The current enableLegend value.

        :getter: Returns the value of enableLegend.
        :setter: Sets the value of enableLegend.
        :type:   bool
        :raises: `TypeError` if setting a non-boolean value.
        """
        return self._legendEnabled

    @enableLegend.setter
    def enableLegend(self, value):
        """Set True to enable legend."""
        # XXX: why not `if not isinstance(value, bool):`?
        if value not in [True, False]:
            raise TypeError("Value should be True or False")
        self._legendEnabled = value
        self.Redraw()

    def SetEnableTitle(self, value):
        """
        Set the enableTitle value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableTitle`
           property instead.
        """
        pendingDeprecation("self.enableTitle property")
        self.enableTitle = value

    def GetEnableTitle(self):
        """
        Get the enableTitle value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enableTitle`
           property instead.
        """
        pendingDeprecation("self.enableTitle property")
        return self.enableTitle

    @property
    def enableTitle(self):
        """
        The current enableTitle value.

        :getter: Returns the value of enableTitle.
        :setter: Sets the value of enableTitle.
        :type:   bool
        :raises: `TypeError` if setting a non-boolean value.
        """
        return self._titleEnabled

    @enableTitle.setter
    def enableTitle(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value must be a bool.")
        self._titleEnabled = value
        self.Redraw()

    def SetEnablePointLabel(self, value):
        """
        Set the enablePointLabel value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enablePointLabel`
           property instead.
        """
        pendingDeprecation("self.enablePointLabel property")
        self.enablePointLabel = value

    def GetEnablePointLabel(self):
        """
        Set the enablePointLabel value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enablePointLabel`
           property instead.
        """
        pendingDeprecation("self.enablePointLabel property")
        return self.enablePointLabel

    @property
    def enablePointLabel(self):
        """
        The current enablePointLabel value.

        :getter: Returns the value of enablePointLabel.
        :setter: Sets the value of enablePointLabel.
        :type:   bool
        :raises: `TypeError` if setting a non-boolean value.
        """
        return self._pointLabelEnabled

    @enablePointLabel.setter
    def enablePointLabel(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value must be a bool.")
        self._pointLabelEnabled = value
        self.Redraw()  # will erase existing pointLabel if present
        self.last_PointLabel = None

    @property
    def enableAxes(self):
        """
        The current enableAxes value.

        :getter: Returns the value of enableAxes.
        :setter: Sets the value of enableAxes.
        :type:   bool, 2-tuple of bool, or 4-tuple of bool
        :raises: `TypeError` if setting an invalid value.
        :raises: `ValueError` if the tuple has incorrect length.

        If bool, enable or disable all axis

        If 2-tuple, enable or disable the bottom or left axes: ``(bottom,
        left)``

        If 4-tuple, enable or disable each axis individually: ``(bottom,
        left, top, right)``
        """
        return self._axesEnabled

    @enableAxes.setter
    def enableAxes(self, value):
        self._axesEnabled = set_displayside(value)
        self.Redraw()

    @property
    def enableAxesValues(self):
        """
        The current enableAxesValues value.

        :getter: Returns the value of enableAxesValues.
        :setter: Sets the value of enableAxesValues.
        :type:   bool, 2-tuple of bool, or 4-tuple of bool
        :raises: `TypeError` if setting an invalid value.
        :raises: `ValueError` if the tuple has incorrect length.

        If bool, enable or disable all axis values

        If 2-tuple, enable or disable the bottom or left axes values:
        ``(bottom, left)``

        If 4-tuple, enable or disable each axis value individually:
        ``(bottom, left, top, right)``
        """
        return self._axesValuesEnabled

    @enableAxesValues.setter
    def enableAxesValues(self, value):
        self._axesValuesEnabled = set_displayside(value)
        self.Redraw()

    @property
    def enableTicks(self):
        """
        The current enableTicks value.

        :getter: Returns the value of enableTicks.
        :setter: Sets the value of enableTicks.
        :type:   bool, 2-tuple of bool, or 4-tuple of bool
        :raises: `TypeError` if setting an invalid value.
        :raises: `ValueError` if the tuple has incorrect length.

        If bool, enable or disable all ticks

        If 2-tuple, enable or disable the bottom or left ticks:
        ``(bottom, left)``

        If 4-tuple, enable or disable each tick side individually:
        ``(bottom, left, top, right)``
        """
        return self._ticksEnabled

    @enableTicks.setter
    def enableTicks(self, value):
        self._ticksEnabled = set_displayside(value)
        self.Redraw()

    @property
    def enablePlotTitle(self):
        """
        The current enablePlotTitle value.

        :getter: Returns the value of enablePlotTitle.
        :setter: Sets the value of enablePlotTitle.
        :type:   bool
        :raises: `TypeError` if setting an invalid value.
        """
        return self._titleEnabled

    @enablePlotTitle.setter
    def enablePlotTitle(self, value):
        if not isinstance(value, bool):
            raise TypeError("`value` must be boolean True or False")
        self._titleEnabled = value
        self.Redraw()

    @property
    def enableXAxisLabel(self):
        """
        The current enableXAxisLabel value.

        :getter: Returns the value of enableXAxisLabel.
        :setter: Sets the value of enableXAxisLabel.
        :type:   bool
        :raises: `TypeError` if setting an invalid value.
        """
        return self._xAxisLabelEnabled

    @enableXAxisLabel.setter
    def enableXAxisLabel(self, value):
        if not isinstance(value, bool):
            raise TypeError("`value` must be boolean True or False")
        self._xAxisLabelEnabled = value
        self.Redraw()

    @property
    def enableYAxisLabel(self):
        """
        The current enableYAxisLabel value.

        :getter: Returns the value of enableYAxisLabel.
        :setter: Sets the value of enableYAxisLabel.
        :type:   bool
        :raises: `TypeError` if setting an invalid value.
        """
        return self._yAxisLabelEnabled

    @enableYAxisLabel.setter
    def enableYAxisLabel(self, value):
        if not isinstance(value, bool):
            raise TypeError("`value` must be boolean True or False")
        self._yAxisLabelEnabled = value
        self.Redraw()

    # TODO: this conflicts with enableXAxisLabel and enableYAxisLabel
    @property
    def enableAxesLabels(self):
        """
        The current enableAxesLabels value.

        :getter: Returns the value of enableAxesLabels.
        :setter: Sets the value of enableAxesLabels.
        :type:   bool
        :raises: `TypeError` if setting an invalid value.
        """
        return self._axesLabelsEnabled

    @enableAxesLabels.setter
    def enableAxesLabels(self, value):
        if not isinstance(value, bool):
            raise TypeError("`value` must be boolean True or False")
        self._axesLabelsEnabled = value
        self.Redraw()

    def SetPointLabelFunc(self, func):
        """
        Set the enablePointLabel value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enablePointLabel`
           property instead.
        """
        pendingDeprecation("self.pointLabelFunc property")
        self.pointLabelFunc = func

    def GetPointLabelFunc(self):
        """
        Get the enablePointLabel value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.enablePointLabel`
           property instead.
        """
        pendingDeprecation("self.pointLabelFunc property")
        return self.pointLabelFunc

    @property
    def pointLabelFunc(self):
        """
        The current pointLabelFunc value.

        :getter: Returns the value of pointLabelFunc.
        :setter: Sets the value of pointLabelFunc.
        :type:   function

        TODO: More information is needed.
        Sets the function with custom code for pointLabel drawing
        """
        return self._pointLabelFunc

    @pointLabelFunc.setter
    def pointLabelFunc(self, func):
        self._pointLabelFunc = func

    def Reset(self):
        """Unzoom the plot."""
        self.last_PointLabel = None  # reset pointLabel
        if self.last_draw is not None:
            self._Draw(self.last_draw[0])

    def ScrollRight(self, units):
        """Move view right number of axis units."""
        self.last_PointLabel = None  # reset pointLabel
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            xAxis = (xAxis[0] + units, xAxis[1] + units)
            self._Draw(graphics, xAxis, yAxis)

    def ScrollUp(self, units):
        """Move view up number of axis units."""
        self.last_PointLabel = None  # reset pointLabel
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            yAxis = (yAxis[0] + units, yAxis[1] + units)
            self._Draw(graphics, xAxis, yAxis)

    def GetXY(self, event):
        """Wrapper around _getXY, which handles log scales"""
        x, y = self._getXY(event)
        if self.logScale[0]:
            x = np.power(10, x)
        if self.logScale[1]:
            y = np.power(10, y)
        return x, y

    def _getXY(self, event):
        """Takes a mouse event and returns the XY user axis values."""
        x, y = self.PositionScreenToUser(event.GetPosition())
        return x, y

    def PositionUserToScreen(self, pntXY):
        """Converts User position to Screen Coordinates"""
        userPos = np.array(pntXY)
        x, y = userPos * self._pointScale + self._pointShift
        return x, y

    def PositionScreenToUser(self, pntXY):
        """Converts Screen position to User Coordinates"""
        screenPos = np.array(pntXY)
        x, y = (screenPos - self._pointShift) / self._pointScale
        return x, y

    def SetXSpec(self, spectype='auto'):
        """
        Set the xSpec value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.xSpec`
           property instead.
        """
        pendingDeprecation("self.xSpec property")
        self.xSpec = spectype

    def SetYSpec(self, spectype='auto'):
        """
        Set the ySpec value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.ySpec`
           property instead.
        """
        pendingDeprecation("self.ySpec property")
        self.ySpec = spectype

    def GetXSpec(self):
        """
        Get the xSpec value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.xSpec`
           property instead.
        """
        pendingDeprecation("self.xSpec property")
        return self.xSpec

    def GetYSpec(self):
        """
        Get the ySpec value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.ySpec`
           property instead.
        """
        pendingDeprecation("self.ySpec property")
        return self.ySpec

    @property
    def xSpec(self):
        """
        Defines the X axis type.

        Default is 'auto'.

        :getter: Returns the value of xSpec.
        :setter: Sets the value of xSpec.
        :type:   str, int, or length-2 sequence of floats
        :raises: `TypeError` if setting an invalid value.

        Valid strings:
        + 'none' - shows no axis or tick mark values
        + 'min' - shows min bounding box values
        + 'auto' - rounds axis range to sensible values

        Other valid values:
        + <number> - like 'min', but with <number> tick marks
        + list or tuple: a list of (min, max) values. Must be length 2.

        .. seealso::
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.ySpec`
        """
        return self._xSpec

    @xSpec.setter
    def xSpec(self, value):
        ok_values = ('none', 'min', 'auto')
        if value not in ok_values and not isinstance(value, (int, float)):
            if not isinstance(value, (list, tuple)) and len(value != 2):
                err_str = ("xSpec must be 'none', 'min', 'auto', "
                           "a number, or sequence of numbers (length 2)")
                raise TypeError(err_str)
        self._xSpec = value

    @property
    def ySpec(self):
        """
        Defines the Y axis type.

        Default is 'auto'.

        :getter: Returns the value of xSpec.
        :setter: Sets the value of xSpec.
        :type:   str, int, or length-2 sequence of floats
        :raises: `TypeError` if setting an invalid value.

        Valid strings:
        + 'none' - shows no axis or tick mark values
        + 'min' - shows min bounding box values
        + 'auto' - rounds axis range to sensible values

        Other valid values:
        + <number> - like 'min', but with <number> tick marks
        + list or tuple: a list of (min, max) values. Must be length 2.

        .. seealso::
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.xSpec`
        """
        return self._ySpec

    @ySpec.setter
    def ySpec(self, value):
        ok_values = ('none', 'min', 'auto')
        if value not in ok_values and not isinstance(value, (int, float)):
            if not isinstance(value, (list, tuple)) and len(value != 2):
                err_str = ("ySpec must be 'none', 'min', 'auto', "
                           "a number, or sequence of numbers (length 2)")
                raise TypeError(err_str)
        self._ySpec = value

    def GetXMaxRange(self):
        """
        Get the xMaxRange value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.xMaxRange`
           property instead.
        """
        pendingDeprecation("self.xMaxRange property")
        return self.xMaxRange

    @property
    def xMaxRange(self):
        """
        The plots' maximum X range as a tuple of ``(min, max)``.

        :getter: Returns the value of xMaxRange.

        .. seealso::
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.yMaxRange`
        """
        xAxis = self._getXMaxRange()
        if self.logScale[0]:
            xAxis = np.power(10, xAxis)
        return xAxis

    def _getXMaxRange(self):
        """Returns (minX, maxX) x-axis range for displayed graph"""
        graphics = self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        xAxis = self._axisInterval(self._xSpec, p1[0], p2[0])  # in user units
        return xAxis

    def GetYMaxRange(self):
        """
        Get the yMaxRange value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.yMaxRange`
           property instead.
        """
        pendingDeprecation("self.yMaxRange property")
        return self.yMaxRange

    @property
    def yMaxRange(self):
        """
        The plots' maximum Y range as a tuple of ``(min, max)``.

        :getter: Returns the value of yMaxRange.

        .. seealso::
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.xMaxRange`
        """
        yAxis = self._getYMaxRange()
        if self.logScale[1]:
            yAxis = np.power(10, yAxis)
        return yAxis

    def _getYMaxRange(self):
        """Returns (minY, maxY) y-axis range for displayed graph"""
        graphics = self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        yAxis = self._axisInterval(self._ySpec, p1[1], p2[1])
        return yAxis

    def GetXCurrentRange(self):
        """
        Get the xCurrentRange value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.xCurrentRange`
           property instead.
        """
        pendingDeprecation("self.xCurrentRange property")
        return self.xCurrentRange

    @property
    def xCurrentRange(self):
        """
        The plots' X range of the currently displayed portion as
        a tuple of ``(min, max)``

        :getter: Returns the value of xCurrentRange.

        .. seealso::
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.yCurrentRange`
        """
        xAxis = self._getXCurrentRange()
        if self.logScale[0]:
            xAxis = np.power(10, xAxis)
        return xAxis

    def _getXCurrentRange(self):
        """Returns (minX, maxX) x-axis for currently displayed
        portion of graph"""
        return self.last_draw[1]

    def GetYCurrentRange(self):
        """
        Get the yCurrentRange value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.yCurrentRange`
           property instead.
        """
        pendingDeprecation("self.yCurrentRange property")
        return self.yCurrentRange

    @property
    def yCurrentRange(self):
        """
        The plots' Y range of the currently displayed portion as
        a tuple of ``(min, max)``

        :getter: Returns the value of yCurrentRange.

        .. seealso::
           :attr:`~wx.lib.plot.plotcanvas.PlotCanvas.xCurrentRange`
        """
        yAxis = self._getYCurrentRange()
        if self.logScale[1]:
            yAxis = np.power(10, yAxis)
        return yAxis

    def _getYCurrentRange(self):
        """Returns (minY, maxY) y-axis for currently displayed
        portion of graph"""
        return self.last_draw[2]

    def Draw(self, graphics, xAxis=None, yAxis=None, dc=None):
        """Wrapper around _Draw, which handles log axes"""

        graphics.logScale = self.logScale

        # check Axis is either tuple or none
        err_txt = "xAxis should be None or (minX, maxX). Got type `{}`."
        if type(xAxis) not in [type(None), tuple]:
            raise TypeError(err_txt .format(type(xAxis)))

        err_txt = "yAxis should be None or (minY, maxY). Got type `{}`."
        if type(yAxis) not in [type(None), tuple]:
            raise TypeError(err_txt.format(type(yAxis)))

        # check case for axis = (a,b) where a==b caused by improper zooms
        if xAxis is not None:
            if xAxis[0] == xAxis[1]:
                return
            if self.logScale[0]:
                xAxis = np.log10(xAxis)
        if yAxis is not None:
            if yAxis[0] == yAxis[1]:
                return
            if self.logScale[1]:
                yAxis = np.log10(yAxis)
        self._Draw(graphics, xAxis, yAxis, dc)

    def _Draw(self, graphics, xAxis=None, yAxis=None, dc=None):
        """\
        Draw objects in graphics with specified x and y axis.
        graphics- instance of PlotGraphics with list of PolyXXX objects
        xAxis - tuple with (min, max) axis range to view
        yAxis - same as xAxis
        dc - drawing context - doesn't have to be specified.
        If it's not, the offscreen buffer is used
        """

        if dc is None:
            # sets new dc and clears it
            dc = wx.BufferedDC(wx.ClientDC(self.canvas), self._Buffer)
            bbr = wx.Brush(self.GetBackgroundColour(), wx.BRUSHSTYLE_SOLID)
            dc.SetBackground(bbr)
            dc.SetBackgroundMode(wx.SOLID)
            dc.Clear()
        if self._antiAliasingEnabled:
            if not isinstance(dc, wx.GCDC):
                try:
                    dc = wx.GCDC(dc)
                except Exception:               # XXX: Yucky.
                    pass
                else:
                    if self._hiResEnabled:
                        # high precision: each logical unit is 1/20 of a point
                        dc.SetMapMode(wx.MM_TWIPS)
                    self._pointSize = tuple(
                        1.0 / lscale for lscale in dc.GetLogicalScale())
                    self._setSize()
        elif self._pointSize != (1.0, 1.0):
            self._pointSize = (1.0, 1.0)
            self._setSize()

        if (sys.platform in ("darwin", "win32")
                or not isinstance(dc, wx.GCDC)
                or wx.VERSION >= (2, 9)):
            self._fontScale = sum(self._pointSize) / 2.0
        else:
            # on Linux, we need to correct the font size by a certain
            # factor if wx.GCDC is used, to make text the same size as
            # if wx.GCDC weren't used
            screenppi = map(float, wx.ScreenDC().GetPPI())
            ppi = dc.GetPPI()
            self._fontScale = (
                (screenppi[0] / ppi[0] * self._pointSize[0]
                 + screenppi[1] / ppi[1] * self._pointSize[1])
                / 2.0
            )

        graphics._pointSize = self._pointSize

        dc.SetTextForeground(self.GetForegroundColour())
        dc.SetTextBackground(self.GetBackgroundColour())

        # dc.Clear()

        # set font size for every thing but title and legend
        dc.SetFont(self._getFont(self._fontSizeAxis))

        # sizes axis to axis type, create lower left and upper right
        # corners of plot
        if xAxis is None or yAxis is None:
            # One or both axis not specified in Draw
            p1, p2 = graphics.boundingBox()     # min, max points of graphics
            if xAxis is None:
                xAxis = self._axisInterval(
                    self._xSpec, p1[0], p2[0])  # in user units
            if yAxis is None:
                yAxis = self._axisInterval(self._ySpec, p1[1], p2[1])
            # Adjust bounding box for axis spec
            # lower left corner user scale (xmin,ymin)
            p1[0], p1[1] = xAxis[0], yAxis[0]
            # upper right corner user scale (xmax,ymax)
            p2[0], p2[1] = xAxis[1], yAxis[1]
        else:
            # Both axis specified in Draw
            # lower left corner user scale (xmin,ymin)
            p1 = np.array([xAxis[0], yAxis[0]])
            # upper right corner user scale (xmax,ymax)
            p2 = np.array([xAxis[1], yAxis[1]])

        # saves most recent values
        self.last_draw = (graphics, np.array(xAxis), np.array(yAxis))

        # Get ticks and textExtents for axis if required
        xticks = yticks = None
        xTextExtent = yTextExtent = (0, 0)  # No text for ticks
        if self._xSpec != 'none':
            xticks = self._xticks(xAxis[0], xAxis[1])
            # w h of x axis text last number on axis
            xTextExtent = dc.GetTextExtent(xticks[-1][1])

        if self._ySpec != 'none':
            yticks = self._yticks(yAxis[0], yAxis[1])
            if self.logScale[1]:
                # make sure we have enough room to display SI notation.
                yTextExtent = dc.GetTextExtent('-2e-2')
            else:
                yTextExtentBottom = dc.GetTextExtent(yticks[0][1])
                yTextExtentTop = dc.GetTextExtent(yticks[-1][1])
                yTextExtent = (max(yTextExtentBottom[0], yTextExtentTop[0]),
                               max(yTextExtentBottom[1], yTextExtentTop[1]))

        # TextExtents for Title and Axis Labels
        titleWH, xLabelWH, yLabelWH = self._titleLablesWH(dc, graphics)

        # TextExtents for Legend
        legendBoxWH, legendSymExt, legendTextExt = self._legendWH(
            dc,
            graphics
        )

        # room around graph area
        # use larger of number width or legend width
        rhsW = max(xTextExtent[0], legendBoxWH[0]) + 5 * self._pointSize[0]
        lhsW = yTextExtent[0] + yLabelWH[1] + 3 * self._pointSize[0]
        bottomH = (max(xTextExtent[1], yTextExtent[1] / 2.)
                   + xLabelWH[1] + 2 * self._pointSize[1])
        topH = yTextExtent[1] / 2. + titleWH[1]
        # make plot area smaller by text size
        textSize_scale = np.array([rhsW + lhsW, bottomH + topH])
        # shift plot area by this amount
        textSize_shift = np.array([lhsW, bottomH])

        # Draw the labels (title, axes labels)
        self._drawPlotAreaLabels(dc, graphics, lhsW, rhsW, titleWH,
                                 bottomH, topH, xLabelWH, yLabelWH)

        # drawing legend makers and text
        if self._legendEnabled:
            self._drawLegend(dc,
                             graphics,
                             rhsW,
                             topH,
                             legendBoxWH,
                             legendSymExt,
                             legendTextExt)

        # allow for scaling and shifting plotted points
        scale = ((self.plotbox_size - textSize_scale) / (p2 - p1)
                 * np.array((1, -1)))
        shift = (-p1 * scale + self.plotbox_origin
                 + textSize_shift * np.array((1, -1)))
        # make available for mouse events
        self._pointScale = scale / self._pointSize
        self._pointShift = shift / self._pointSize
        self._drawPlotAreaItems(dc, p1, p2, scale, shift, xticks, yticks)

        graphics.scaleAndShift(scale, shift)
        # thicken up lines and markers if printing
        graphics.printerScale = self.printerScale

        # set clipping area so drawing does not occur outside axis box
        ptx, pty, rectWidth, rectHeight = self._point2ClientCoord(p1, p2)
        # allow graph to overlap axis lines by adding units to w and h
        dc.SetClippingRegion(int(ptx * self._pointSize[0]),
                             int(pty * self._pointSize[1]),
                             int(rectWidth * self._pointSize[0] + 2),
                             int(rectHeight * self._pointSize[1] + 1))
        # Draw the lines and markers
#        start = _time.perf_counter()
        graphics.draw(dc)
#        time_str = "entire graphics drawing took: {} seconds"
#        print(time_str.format(_time.perf_counter() - start))
        # remove the clipping region
        dc.DestroyClippingRegion()

        self._adjustScrollbars()

    def Redraw(self, dc=None):
        """Redraw the existing plot."""
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            self._Draw(graphics, xAxis, yAxis, dc)

    def Clear(self):
        """Erase the window."""
        self.last_PointLabel = None  # reset pointLabel
        dc = wx.BufferedDC(wx.ClientDC(self.canvas), self._Buffer)
        bbr = wx.Brush(self.GetBackgroundColour(), wx.SOLID)
        dc.SetBackground(bbr)
        dc.SetBackgroundMode(wx.SOLID)
        dc.Clear()
        if self._antiAliasingEnabled:
            try:
                dc = wx.GCDC(dc)
            except Exception:
                pass
        dc.SetTextForeground(self.GetForegroundColour())
        dc.SetTextBackground(self.GetBackgroundColour())
        self.last_draw = None

    def Zoom(self, Center, Ratio):
        """
        Zoom on the plot
        Centers on the X,Y coords given in Center
        Zooms by the Ratio = (Xratio, Yratio) given
        """
        self.last_PointLabel = None  # reset maker
        x, y = Center
        if self.last_draw is not None:
            (graphics, xAxis, yAxis) = self.last_draw
            w = (xAxis[1] - xAxis[0]) * Ratio[0]
            h = (yAxis[1] - yAxis[0]) * Ratio[1]
            xAxis = (x - w / 2, x + w / 2)
            yAxis = (y - h / 2, y + h / 2)
            self._Draw(graphics, xAxis, yAxis)

    def GetClosestPoints(self, pntXY, pointScaled=True):
        """
        Returns list with
        [curveNumber, legend, index of closest point,
        pointXY, scaledXY, distance]
        list for each curve.
        Returns [] if no curves are being plotted.

        x, y in user coords
        if pointScaled == True based on screen coords
        if pointScaled == False based on user coords
        """
        if self.last_draw is None:
            # no graph available
            return []
        graphics, xAxis, yAxis = self.last_draw
        l = []
        for curveNum, obj in enumerate(graphics):
            # check there are points in the curve
            if len(obj.points) == 0:
                continue  # go to next obj
            #[curveNum, legend, closest pt index, pointXY, scaledXY, dist]
            cn = ([curveNum] +
                  [obj.getLegend()] + obj.getClosestPoint(pntXY, pointScaled))
            l.append(cn)
        return l

    def GetClosestPoint(self, pntXY, pointScaled=True):
        """
        Returns list with
        [curveNumber, legend, index of closest point,
        pointXY, scaledXY, distance]
        list for only the closest curve.
        Returns [] if no curves are being plotted.

        x, y in user coords
        if pointScaled == True based on screen coords
        if pointScaled == False based on user coords
        """
        # closest points on screen based on screen scaling (pointScaled=True)
        closestPts = self.GetClosestPoints(pntXY, pointScaled)
        if closestPts == []:
            return []  # no graph present
        # find one with least distance
        dists = [c[-1] for c in closestPts]
        mdist = min(dists)  # Min dist
        i = dists.index(mdist)  # index for min dist
        return closestPts[i]  # this is the closest point on closest curve

    def UpdatePointLabel(self, mDataDict):
        """
        Updates the pointLabel point on screen with data contained in
        mDataDict.

        mDataDict will be passed to your function set by
        SetPointLabelFunc.  It can contain anything you
        want to display on the screen at the scaledXY point
        you specify.

        This function can be called from parent window with onClick,
        onMotion events etc.
        """
        if self.last_PointLabel is not None:
            # compare pointXY
            if np.any(
                    mDataDict["pointXY"] != self.last_PointLabel["pointXY"]):
                # closest changed
                self._drawPointLabel(self.last_PointLabel)  # erase old
                self._drawPointLabel(mDataDict)  # plot new
        else:
            # just plot new with no erase
            self._drawPointLabel(mDataDict)  # plot new
        # save for next erase
        self.last_PointLabel = mDataDict

    # event handlers **********************************
    # TODO: some of these event handlers can be modified
    #       Meaning: only bind the event if the item is enabled. Disable
    #       the event when the item is disabled.
    #
    #       Example::
    #
    #           if self._zoomEnabled:
    #               self.Bind(stuff)
    #           else:
    #               self.UnBind(stuff)   # or equivalent
    #
    #           def OnZoom(self, event):
    #               # process zoom event.
    #
    #       What this change would do is remove most of the if statements
    #       within these event handlers.
    def OnMotion(self, event):
        if self._zoomEnabled and event.LeftIsDown():
            if self._hasDragged:
                self._drawRubberBand(
                    self._zoomCorner1, self._zoomCorner2)  # remove old
            else:
                self._hasDragged = True
            self._zoomCorner2[0], self._zoomCorner2[1] = self._getXY(event)
            self._drawRubberBand(
                self._zoomCorner1, self._zoomCorner2)  # add new
        elif self._dragEnabled and event.LeftIsDown():
            coordinates = event.GetPosition()
            newpos, oldpos = map(
                np.array,
                map(self.PositionScreenToUser,
                    [coordinates, self._screenCoordinates]
                    )
            )
            dist = newpos - oldpos
            self._screenCoordinates = coordinates

            if self.last_draw is not None:
                graphics, xAxis, yAxis = self.last_draw
                yAxis -= dist[1]
                xAxis -= dist[0]
                self._Draw(graphics, xAxis, yAxis)

    def OnMouseLeftDown(self, event):
        self._zoomCorner1[0], self._zoomCorner1[1] = self._getXY(event)
        self._screenCoordinates = np.array(event.GetPosition())
        if self._dragEnabled:
            self.SetCursor(self.GrabHandCursor)
            self.canvas.CaptureMouse()

    def OnMouseLeftUp(self, event):
        if self._zoomEnabled:
            if self._hasDragged is True:
                self._drawRubberBand(
                    self._zoomCorner1, self._zoomCorner2)  # remove old
                self._zoomCorner2[0], self._zoomCorner2[1] = self._getXY(event)
                self._hasDragged = False  # reset flag
                minX, minY = np.minimum(self._zoomCorner1, self._zoomCorner2)
                maxX, maxY = np.maximum(self._zoomCorner1, self._zoomCorner2)
                self.last_PointLabel = None  # reset pointLabel
                if self.last_draw is not None:
                    self._Draw(self.last_draw[0],
                               xAxis=(minX, maxX),
                               yAxis=(minY, maxY),
                               dc=None)
            # else: # A box has not been drawn, zoom in on a point
            # this interfered with the double click, so I've disables it.
            #    X,Y = self._getXY(event)
            #    self.Zoom( (X,Y), (self._zoomInFactor,self._zoomInFactor) )
        if self._dragEnabled:
            self.SetCursor(self.HandCursor)
            if self.canvas.HasCapture():
                self.canvas.ReleaseMouse()

    def OnMouseDoubleClick(self, event):
        if self._zoomEnabled:
            # Give a little time for the click to be totally finished
            # before (possibly) removing the scrollbars and trigering
            # size events, etc.
            wx.CallLater(200, self.Reset)

    def OnMouseRightDown(self, event):
        if self._zoomEnabled:
            X, Y = self._getXY(event)
            self.Zoom((X, Y), (self._zoomOutFactor, self._zoomOutFactor))

    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        if self.last_PointLabel is not None:
            self._drawPointLabel(self.last_PointLabel)  # erase old
            self.last_PointLabel = None
        dc = wx.BufferedPaintDC(self.canvas, self._Buffer)
        if self._antiAliasingEnabled:
            try:
                dc = wx.GCDC(dc)
            except Exception:
                pass

    def OnSize(self, event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size = self.canvas.GetClientSize()
        Size.width = max(1, Size.width)
        Size.height = max(1, Size.height)

        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.Bitmap(Size.width, Size.height)
        self._setSize()

        self.last_PointLabel = None  # reset pointLabel

        if self.last_draw is None:
            self.Clear()
        else:
            graphics, xSpec, ySpec = self.last_draw
            self._Draw(graphics, xSpec, ySpec)

    def OnLeave(self, event):
        """Used to erase pointLabel when mouse outside window"""
        if self.last_PointLabel is not None:
            self._drawPointLabel(self.last_PointLabel)  # erase old
            self.last_PointLabel = None

    def OnScroll(self, evt):
        if not self._adjustingSB:
            self._sb_ignore = True
            sbpos = evt.GetPosition()

            if evt.GetOrientation() == wx.VERTICAL:
                fullrange = self.sb_vert.GetRange()
                pagesize = self.sb_vert.GetPageSize()
                sbpos = fullrange - pagesize - sbpos
                dist = (sbpos * self._sb_yunit -
                        (self._getYCurrentRange()[0] - self._sb_yfullrange[0]))
                self.ScrollUp(dist)

            if evt.GetOrientation() == wx.HORIZONTAL:
                dist = (sbpos * self._sb_xunit -
                        (self._getXCurrentRange()[0] - self._sb_xfullrange[0]))
                self.ScrollRight(dist)

    # Private Methods **************************************************
    def _setSize(self, width=None, height=None):
        """DC width and height."""
        if width is None:
            (self.width, self.height) = self.canvas.GetClientSize()
        else:
            self.width, self.height = width, height
        self.width *= self._pointSize[0]  # high precision
        self.height *= self._pointSize[1]  # high precision
        self.plotbox_size = 0.97 * np.array([self.width, self.height])
        xo = 0.5 * (self.width - self.plotbox_size[0])
        yo = self.height - 0.5 * (self.height - self.plotbox_size[1])
        self.plotbox_origin = np.array([xo, yo])

    def _setPrinterScale(self, scale):
        """Used to thicken lines and increase marker size for print out."""
        # line thickness on printer is very thin at 600 dot/in. Markers small
        self.printerScale = scale

    def _printDraw(self, printDC):
        """Used for printing."""
        if self.last_draw is not None:
            graphics, xSpec, ySpec = self.last_draw
            self._Draw(graphics, xSpec, ySpec, printDC)

    def _drawPointLabel(self, mDataDict):
        """Draws and erases pointLabels"""
        width = self._Buffer.GetWidth()
        height = self._Buffer.GetHeight()
        if sys.platform not in ("darwin", "linux"):
            tmp_Buffer = wx.Bitmap(width, height)
            dcs = wx.MemoryDC()
            dcs.SelectObject(tmp_Buffer)
            dcs.Clear()
        else:
            tmp_Buffer = self._Buffer.GetSubBitmap((0, 0, width, height))
            dcs = wx.MemoryDC(self._Buffer)
        self._pointLabelFunc(dcs, mDataDict)  # custom user pointLabel func

        dc = wx.ClientDC(self.canvas)
        dc = wx.BufferedDC(dc, self._Buffer)
        # this will erase if called twice
        dc.Blit(0, 0, width, height, dcs, 0, 0, self._logicalFunction)
        if sys.platform in ("darwin", "linux"):
            self._Buffer = tmp_Buffer

    def _drawLegend(self, dc, graphics, rhsW, topH, legendBoxWH,
                    legendSymExt, legendTextExt):
        """Draws legend symbols and text"""
        # top right hand corner of graph box is ref corner
        trhc = (self.plotbox_origin +
                (self.plotbox_size - [rhsW, topH]) * [1, -1])
        # border space between legend sym and graph box
        legendLHS = .091 * legendBoxWH[0]
        # 1.1 used as space between lines
        lineHeight = max(legendSymExt[1], legendTextExt[1]) * 1.1
        dc.SetFont(self._getFont(self._fontSizeLegend))

        from .polyobjects import PolyLine
        from .polyobjects import PolyMarker
        from .polyobjects import PolyBoxPlot

        for i in range(len(graphics)):
            o = graphics[i]
            s = i * lineHeight
            if isinstance(o, PolyMarker) or isinstance(o, PolyBoxPlot):
                # draw marker with legend
                pnt = (trhc[0] + legendLHS + legendSymExt[0] / 2.,
                       trhc[1] + s + lineHeight / 2.)
                o.draw(dc, self.printerScale, coord=np.array([pnt]))
            elif isinstance(o, PolyLine):
                # draw line with legend
                pnt1 = (trhc[0] + legendLHS, trhc[1] + s + lineHeight / 2.)
                pnt2 = (trhc[0] + legendLHS + legendSymExt[0],
                        trhc[1] + s + lineHeight / 2.)
                o.draw(dc, self.printerScale, coord=np.array([pnt1, pnt2]))
            else:
                raise TypeError(
                    "object is neither PolyMarker or PolyLine instance")
            # draw legend txt
            pnt = ((trhc[0] + legendLHS + legendSymExt[0]
                    + 5 * self._pointSize[0]),
                   trhc[1] + s + lineHeight / 2. - legendTextExt[1] / 2)
            dc.DrawText(o.getLegend(), int(pnt[0]), int(pnt[1]))
        dc.SetFont(self._getFont(self._fontSizeAxis))  # reset

    def _titleLablesWH(self, dc, graphics):
        """Draws Title and labels and returns width and height for each"""
        # TextExtents for Title and Axis Labels
        dc.SetFont(self._getFont(self._fontSizeTitle))
        if self.enablePlotTitle:
            title = graphics.title
            titleWH = dc.GetTextExtent(title)
        else:
            titleWH = (0, 0)
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabel, yLabel = graphics.xLabel, graphics.yLabel
        xLabelWH = dc.GetTextExtent(xLabel)
        yLabelWH = dc.GetTextExtent(yLabel)
        return titleWH, xLabelWH, yLabelWH

    def _legendWH(self, dc, graphics):
        """Returns the size in screen units for legend box"""
        if self._legendEnabled is not True:
            legendBoxWH = symExt = txtExt = (0, 0)
        else:
            # find max symbol size
            symExt = graphics.getSymExtent(self.printerScale)
            # find max legend text extent
            dc.SetFont(self._getFont(self._fontSizeLegend))
            txtList = graphics.getLegendNames()
            txtExt = dc.GetTextExtent(txtList[0])
            for txt in graphics.getLegendNames()[1:]:
                txtExt = np.maximum(txtExt, dc.GetTextExtent(txt))
            maxW = symExt[0] + txtExt[0]
            maxH = max(symExt[1], txtExt[1])
            # padding .1 for lhs of legend box and space between lines
            maxW = maxW * 1.1
            maxH = maxH * 1.1 * len(txtList)
            dc.SetFont(self._getFont(self._fontSizeAxis))
            legendBoxWH = (maxW, maxH)
        return (legendBoxWH, symExt, txtExt)

    def _drawRubberBand(self, corner1, corner2):
        """Draws/erases rect box from corner1 to corner2"""
        ptx, pty, rectWidth, rectHeight = self._point2ClientCoord(
            corner1, corner2)
        # draw rectangle
        dc = wx.ClientDC(self.canvas)
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush(wx.WHITE, wx.BRUSHSTYLE_TRANSPARENT))
        dc.SetLogicalFunction(wx.INVERT)
        dc.DrawRectangle(int(ptx), int(pty), int(rectWidth), int(rectHeight))
        dc.SetLogicalFunction(wx.COPY)

    def _getFont(self, size):
        """Take font size, adjusts if printing and returns wx.Font"""
        s = size * self.printerScale * self._fontScale
        of = self.GetFont()
        # Linux speed up to get font from cache rather than X font server
        key = (int(s), of.GetFamily(), of.GetStyle(), of.GetWeight())
        font = self._fontCache.get(key, None)
        if font:
            return font                 # yeah! cache hit
        else:
            font = wx.Font(
                int(s), of.GetFamily(), of.GetStyle(), of.GetWeight())
            self._fontCache[key] = font
            return font

    def _point2ClientCoord(self, corner1, corner2):
        """Converts user point coords to client screen int
        coords x,y,width,height"""
        c1 = np.array(corner1)
        c2 = np.array(corner2)
        # convert to screen coords
        pt1 = c1 * self._pointScale + self._pointShift
        pt2 = c2 * self._pointScale + self._pointShift
        # make height and width positive
        pul = np.minimum(pt1, pt2)  # Upper left corner
        plr = np.maximum(pt1, pt2)  # Lower right corner
        rectWidth, rectHeight = plr - pul
        ptx, pty = pul
        return ptx, pty, rectWidth, rectHeight

    def _axisInterval(self, spec, lower, upper):
        """Returns sensible axis range for given spec"""
        if spec == 'none' or spec == 'min' or isinstance(spec, (float, int)):
            if lower == upper:
                return lower - 0.5, upper + 0.5
            else:
                return lower, upper
        elif spec == 'auto':
            range = upper - lower
            if range == 0.:
                return lower - 0.5, upper + 0.5
            log = np.log10(range)
            power = np.floor(log)
            fraction = log - power
            if fraction <= 0.05:
                power = power - 1
            grid = 10. ** power
            lower = lower - lower % grid
            mod = upper % grid
            if mod != 0:
                upper = upper - mod + grid
            return lower, upper
#        elif type(spec) == type(()):
        elif isinstance(spec, tuple):
            lower, upper = spec
            if lower <= upper:
                return lower, upper
            else:
                return upper, lower
        else:
            raise ValueError(str(spec) + ': illegal axis specification')

    @TempStyle('pen')
    def _drawGrid(self, dc, p1, p2, scale, shift, xticks, yticks):
        """
        Draws the gridlines

        :param :class:`wx.DC` `dc`: The :class:`wx.DC` to draw on.
        :type `dc`: :class:`wx.DC`
        :param p1: The lower-left hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p1 = (-10, -5)
        :type p1: :class:`np.array`, length 2
        :param p2: The upper-right hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p2 = (10, 5)
        :type p2: :class:`np.array`, length 2
        :param scale: The [X, Y] scaling factor to convert plot coords to
                      DC coords
        :type scale: :class:`np.array`, length 2
        :param shift: The [X, Y] shift values to convert plot coords to
                      DC coords. Must be in plot units, not DC units.
        :type shift: :class:`np.array`, length 2
        :param xticks: The X tick definition
        :type xticks: list of length-2 lists
        :param yticks: The Y tick definition
        :type yticks: list of length-2 lists
        """
        # increases thickness for printing only
        pen = self.gridPen
        penWidth = self.printerScale * pen.GetWidth()
        pen.SetWidth(int(penWidth))
        dc.SetPen(pen)

        x, y, width, height = self._point2ClientCoord(p1, p2)

        if self._xSpec != 'none':
            if self.enableGrid[0]:
                for x, _ in xticks:
                    pt = scale_and_shift_point(x, p1[1], scale, shift)
                    dc.DrawLine(int(pt[0]), int(pt[1]), int(pt[0]), int(pt[1] - height))

        if self._ySpec != 'none':
            if self.enableGrid[1]:
                for y, label in yticks:
                    pt = scale_and_shift_point(p1[0], y, scale, shift)
                    dc.DrawLine(int(pt[0]), int(pt[1]), int(pt[0] + width), int(pt[1]))

    @TempStyle('pen')
    def _drawTicks(self, dc, p1, p2, scale, shift, xticks, yticks):
        """Draw the tick marks

        :param :class:`wx.DC` `dc`: The :class:`wx.DC` to draw on.
        :type `dc`: :class:`wx.DC`
        :param p1: The lower-left hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p1 = (-10, -5)
        :type p1: :class:`np.array`, length 2
        :param p2: The upper-right hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p2 = (10, 5)
        :type p2: :class:`np.array`, length 2
        :param scale: The [X, Y] scaling factor to convert plot coords to
                      DC coords
        :type scale: :class:`np.array`, length 2
        :param shift: The [X, Y] shift values to convert plot coords to
                      DC coords. Must be in plot units, not DC units.
        :type shift: :class:`np.array`, length 2
        :param xticks: The X tick definition
        :type xticks: list of length-2 lists
        :param yticks: The Y tick definition
        :type yticks: list of length-2 lists
        """
        # TODO: add option for ticks to extend outside of graph
        #       - done via negative ticklength values?
        #           + works but the axes values cut off the ticks.
        # increases thickness for printing only
        pen = self.tickPen
        penWidth = self.printerScale * pen.GetWidth()
        pen.SetWidth(int(penWidth))
        dc.SetPen(pen)

        # lengthen lines for printing
        xTickLength = self.tickLengthPrinterScale[0]
        yTickLength = self.tickLengthPrinterScale[1]

        ticks = self.enableTicks
        if self.xSpec != 'none':        # I don't like this :-/
            if ticks.bottom:
                lines = []
                for x, label in xticks:
                    pt = scale_and_shift_point(x, p1[1], scale, shift)
                    lines.append((int(pt[0]), int(pt[1]), int(pt[0]), int(pt[1] - xTickLength)))
                dc.DrawLineList(lines)
            if ticks.top:
                lines = []
                for x, label in xticks:
                    pt = scale_and_shift_point(x, p2[1], scale, shift)
                    lines.append((int(pt[0]), int(pt[1]), int(pt[0]), int(pt[1] + xTickLength)))
                dc.DrawLineList(lines)

        if self.ySpec != 'none':
            if ticks.left:
                lines = []
                for y, label in yticks:
                    pt = scale_and_shift_point(p1[0], y, scale, shift)
                    lines.append((int(pt[0]), int(pt[1]), int(pt[0] + yTickLength), int(pt[1])))
                dc.DrawLineList(lines)
            if ticks.right:
                lines = []
                for y, label in yticks:
                    pt = scale_and_shift_point(p2[0], y, scale, shift)
                    lines.append((int(pt[0]), int(pt[1]), int(pt[0] - yTickLength), int(pt[1])))
                dc.DrawLineList(lines)

    @TempStyle('pen')
    def _drawCenterLines(self, dc, p1, p2, scale, shift):
        """Draws the center lines

        :param :class:`wx.DC` `dc`: The :class:`wx.DC` to draw on.
        :type `dc`: :class:`wx.DC`
        :param p1: The lower-left hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p1 = (-10, -5)
        :type p1: :class:`np.array`, length 2
        :param p2: The upper-right hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p2 = (10, 5)
        :type p2: :class:`np.array`, length 2
        :param scale: The [X, Y] scaling factor to convert plot coords to
                      DC coords
        :type scale: :class:`np.array`, length 2
        :param shift: The [X, Y] shift values to convert plot coords to
                      DC coords. Must be in plot units, not DC units.
        :type shift: :class:`np.array`, length 2
        """
        # increases thickness for printing only
        pen = self.centerLinePen
        penWidth = self.printerScale * pen.GetWidth()
        pen.SetWidth(int(penWidth))
        dc.SetPen(pen)

        if self._centerLinesEnabled in ('Horizontal', True):
            y1 = scale[1] * p1[1] + shift[1]
            y2 = scale[1] * p2[1] + shift[1]
            y = (y1 - y2) / 2.0 + y2
            dc.DrawLine(int(scale[0] * p1[0] + shift[0]),
                        int(y),
                        int(scale[0] * p2[0] + shift[0]),
                        int(y))
        if self._centerLinesEnabled in ('Vertical', True):
            x1 = scale[0] * p1[0] + shift[0]
            x2 = scale[0] * p2[0] + shift[0]
            x = (x1 - x2) / 2.0 + x2
            dc.DrawLine(int(x),
                        int(scale[1] * p1[1] + shift[1]),
                        int(x),
                        int(scale[1] * p2[1] + shift[1]))

    @TempStyle('pen')
    def _drawDiagonals(self, dc, p1, p2, scale, shift):
        """
        Draws the diagonal lines.

        :param :class:`wx.DC` `dc`: The :class:`wx.DC` to draw on.
        :type `dc`: :class:`wx.DC`
        :param p1: The lower-left hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p1 = (-10, -5)
        :type p1: :class:`np.array`, length 2
        :param p2: The upper-right hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p2 = (10, 5)
        :type p2: :class:`np.array`, length 2
        :param scale: The [X, Y] scaling factor to convert plot coords to
                      DC coords
        :type scale: :class:`np.array`, length 2
        :param shift: The [X, Y] shift values to convert plot coords to
                      DC coords. Must be in plot units, not DC units.
        :type shift: :class:`np.array`, length 2
        """
        pen = self.diagonalPen
        penWidth = self.printerScale * pen.GetWidth()
        pen.SetWidth(int(penWidth))
        dc.SetPen(pen)

        if self._diagonalsEnabled in ('Bottomleft-Topright', True):
            dc.DrawLine(int(scale[0] * p1[0] + shift[0]),
                        int(scale[1] * p1[1] + shift[1]),
                        int(scale[0] * p2[0] + shift[0]),
                        int(scale[1] * p2[1] + shift[1]))
        if self._diagonalsEnabled in ('Bottomright-Topleft', True):
            dc.DrawLine(int(scale[0] * p1[0] + shift[0]),
                        int(scale[1] * p2[1] + shift[1]),
                        int(scale[0] * p2[0] + shift[0]),
                        int(scale[1] * p1[1] + shift[1]))

    @TempStyle('pen')
    def _drawAxes(self, dc, p1, p2, scale, shift):
        """
        Draw the frame lines.

        :param :class:`wx.DC` `dc`: The :class:`wx.DC` to draw on.
        :type `dc`: :class:`wx.DC`
        :param p1: The lower-left hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p1 = (-10, -5)
        :type p1: :class:`np.array`, length 2
        :param p2: The upper-right hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p2 = (10, 5)
        :type p2: :class:`np.array`, length 2
        :param scale: The [X, Y] scaling factor to convert plot coords to
                      DC coords
        :type scale: :class:`np.array`, length 2
        :param shift: The [X, Y] shift values to convert plot coords to
                      DC coords. Must be in plot units, not DC units.
        :type shift: :class:`np.array`, length 2
        """
        # increases thickness for printing only
        pen = self.axesPen
        penWidth = self.printerScale * pen.GetWidth()
        pen.SetWidth(int(penWidth))
        dc.SetPen(pen)

        axes = self.enableAxes
        if self.xSpec != 'none':
            if axes.bottom:
                lower, upper = p1[0], p2[0]
                a1 = scale_and_shift_point(lower, p1[1], scale, shift)
                a2 = scale_and_shift_point(upper, p1[1], scale, shift)
                dc.DrawLine(int(a1[0]), int(a1[1]), int(a2[0]), int(a2[1]))
            if axes.top:
                lower, upper = p1[0], p2[0]
                a1 = scale_and_shift_point(lower, p2[1], scale, shift)
                a2 = scale_and_shift_point(upper, p2[1], scale, shift)
                dc.DrawLine(int(a1[0]), int(a1[1]), int(a2[0]), int(a2[1]))

        if self.ySpec != 'none':
            if axes.left:
                lower, upper = p1[1], p2[1]
                a1 = scale_and_shift_point(p1[0], lower, scale, shift)
                a2 = scale_and_shift_point(p1[0], upper, scale, shift)
                dc.DrawLine(int(a1[0]), int(a1[1]), int(a2[0]), int(a2[1]))
            if axes.right:
                lower, upper = p1[1], p2[1]
                a1 = scale_and_shift_point(p2[0], lower, scale, shift)
                a2 = scale_and_shift_point(p2[0], upper, scale, shift)
                dc.DrawLine(int(a1[0]), int(a1[1]), int(a2[0]), int(a2[1]))

    @TempStyle('pen')
    def _drawAxesValues(self, dc, p1, p2, scale, shift, xticks, yticks):
        """
        Draws the axes values: numbers representing each major grid or tick.

        :param :class:`wx.DC` `dc`: The :class:`wx.DC` to draw on.
        :type `dc`: :class:`wx.DC`
        :param p1: The lower-left hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p1 = (-10, -5)
        :type p1: :class:`np.array`, length 2
        :param p2: The upper-right hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p2 = (10, 5)
        :type p2: :class:`np.array`, length 2
        :param scale: The [X, Y] scaling factor to convert plot coords to
                      DC coords
        :type scale: :class:`np.array`, length 2
        :param shift: The [X, Y] shift values to convert plot coords to
                      DC coords. Must be in plot units, not DC units.
        :type shift: :class:`np.array`, length 2
        :param xticks: The X tick definition
        :type xticks: list of length-2 lists
        :param yticks: The Y tick definition
        :type yticks: list of length-2 lists
        """
        # get the tick lengths so that labels don't overlap
        xTickLength = self.tickLengthPrinterScale[0]
        yTickLength = self.tickLengthPrinterScale[1]
        # only care about negative (out of plot area) tick lengths.
        xTickLength = xTickLength if xTickLength < 0 else 0
        yTickLength = yTickLength if yTickLength < 0 else 0

        # TODO: More code duplication? Same as _drawGrid and _drawTicks?
        # TODO: update the bounding boxes when adding right and top values
        axes = self.enableAxesValues
        if self.xSpec != 'none':
            if axes.bottom:
                labels = [tick[1] for tick in xticks]
                coords = []
                for x, label in xticks:
                    w = dc.GetTextExtent(label)[0]
                    pt = scale_and_shift_point(x, p1[1], scale, shift)
                    coords.append(
                        (int(pt[0] - w/2),
                         int(pt[1] + 2 * self._pointSize[1] - xTickLength))
                    )
                dc.DrawTextList(labels, coords)

            if axes.top:
                labels = [tick[1] for tick in xticks]
                coords = []
                for x, label in xticks:
                    w, h = dc.GetTextExtent(label)
                    pt = scale_and_shift_point(x, p2[1], scale, shift)
                    coords.append(
                        (int(pt[0] - w/2),
                         int(pt[1] - 2 * self._pointSize[1] - h - xTickLength))
                    )
                dc.DrawTextList(labels, coords)

        if self.ySpec != 'none':
            if axes.left:
                h = dc.GetCharHeight()
                labels = [tick[1] for tick in yticks]
                coords = []
                for y, label in yticks:
                    w = dc.GetTextExtent(label)[0]
                    pt = scale_and_shift_point(p1[0], y, scale, shift)
                    coords.append(
                        (int(pt[0] - w - 3 * self._pointSize[0] + yTickLength),
                         int(pt[1] - 0.5 * h))
                    )
                dc.DrawTextList(labels, coords)

            if axes.right:
                h = dc.GetCharHeight()
                labels = [tick[1] for tick in yticks]
                coords = []
                for y, label in yticks:
                    w = dc.GetTextExtent(label)[0]
                    pt = scale_and_shift_point(p2[0], y, scale, shift)
                    coords.append(
                        (int(pt[0] + 3 * self._pointSize[0] + yTickLength),
                         int(pt[1] - 0.5 * h))
                    )
                dc.DrawTextList(labels, coords)

    @TempStyle('pen')
    def _drawPlotAreaItems(self, dc, p1, p2, scale, shift, xticks, yticks):
        """
        Draws each frame element

        :param :class:`wx.DC` `dc`: The :class:`wx.DC` to draw on.
        :type `dc`: :class:`wx.DC`
        :param p1: The lower-left hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p1 = (-10, -5)
        :type p1: :class:`np.array`, length 2
        :param p2: The upper-right hand corner of the plot in plot coords. So,
                   if the plot ranges from x=-10 to 10 and y=-5 to 5, then
                   p2 = (10, 5)
        :type p2: :class:`np.array`, length 2
        :param scale: The [X, Y] scaling factor to convert plot coords to
                      DC coords
        :type scale: :class:`np.array`, length 2
        :param shift: The [X, Y] shift values to convert plot coords to
                      DC coords. Must be in plot units, not DC units.
        :type shift: :class:`np.array`, length 2
        :param xticks: The X tick definition
        :type xticks: list of length-2 lists
        :param yticks: The Y tick definition
        :type yticks: list of length-2 lists
        """
        if self._gridEnabled:
            self._drawGrid(dc, p1, p2, scale, shift, xticks, yticks)

        if self._ticksEnabled:
            self._drawTicks(dc, p1, p2, scale, shift, xticks, yticks)

        if self._centerLinesEnabled:
            self._drawCenterLines(dc, p1, p2, scale, shift)

        if self._diagonalsEnabled:
            self._drawDiagonals(dc, p1, p2, scale, shift)

        if self._axesEnabled:
            self._drawAxes(dc, p1, p2, scale, shift)

        if self._axesValuesEnabled:
            self._drawAxesValues(dc, p1, p2, scale, shift, xticks, yticks)

    @TempStyle('pen')
    def _drawPlotTitle(self, dc, graphics, lhsW, rhsW, titleWH):
        """
        Draws the plot title
        """
        dc.SetFont(self._getFont(self._fontSizeTitle))
        titlePos = (
            self.plotbox_origin[0] + lhsW
            + (self.plotbox_size[0] - lhsW - rhsW) / 2. - titleWH[0] / 2.,
            self.plotbox_origin[1] - self.plotbox_size[1]
        )
        dc.DrawText(graphics.title, int(titlePos[0]), int(titlePos[1]))

    def _drawAxesLabels(self, dc, graphics, lhsW, rhsW, bottomH, topH,
                        xLabelWH, yLabelWH):
        """
        Draws the axes labels
        """
        # get the tick lengths so that labels don't overlap
        xTickLength = self.tickLengthPrinterScale[0]
        yTickLength = self.tickLengthPrinterScale[1]
        # only care about negative (out of plot area) tick lengths.
        xTickLength = xTickLength if xTickLength < 0 else 0
        yTickLength = yTickLength if yTickLength < 0 else 0

        # TODO: axes values get big when this is turned off
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabelPos = (
            self.plotbox_origin[0] + lhsW
            + (self.plotbox_size[0] - lhsW - rhsW) / 2. - xLabelWH[0] / 2.,
            self.plotbox_origin[1] - xLabelWH[1] - yTickLength
        )
        dc.DrawText(graphics.xLabel, int(xLabelPos[0]), int(xLabelPos[1]))
        yLabelPos = (
            self.plotbox_origin[0] - 3 * self._pointSize[0] + xTickLength,
            self.plotbox_origin[1] - bottomH
            - (self.plotbox_size[1] - bottomH - topH) / 2. + yLabelWH[0] / 2.
        )
        if graphics.yLabel:  # bug fix for Linux
            dc.DrawRotatedText(
                graphics.yLabel, int(yLabelPos[0]), int(yLabelPos[1]), 90)

    @TempStyle('pen')
    def _drawPlotAreaLabels(self, dc, graphics, lhsW, rhsW, titleWH,
                            bottomH, topH, xLabelWH, yLabelWH):
        """
        Draw the plot area labels.
        """
        if self._titleEnabled:
            self._drawPlotTitle(dc, graphics, lhsW, rhsW, titleWH)

        if self._axesLabelsEnabled:
            self._drawAxesLabels(dc, graphics, lhsW, rhsW,
                                 bottomH, topH, xLabelWH, yLabelWH)

    def _xticks(self, *args):
        if self._logscale[0]:
            return self._logticks(*args)
        else:
            attr = {'numticks': self._xSpec}
            return self._ticks(*args, **attr)

    def _yticks(self, *args):
        if self._logscale[1]:
            return self._logticks(*args)
        else:
            attr = {'numticks': self._ySpec}
            return self._ticks(*args, **attr)

    def _logticks(self, lower, upper):
        #lower,upper = map(np.log10,[lower,upper])
        # print('logticks',lower,upper)
        ticks = []
        mag = np.power(10, np.floor(lower))
        if upper - lower > 6:
            t = np.power(10, np.ceil(lower))
            base = np.power(10, np.floor((upper - lower) / 6))

            def inc(t):
                return t * base - t
        else:
            t = np.ceil(np.power(10, lower) / mag) * mag

            def inc(t):
                return 10 ** int(np.floor(np.log10(t) + 1e-16))
        majortick = int(np.log10(mag))
        while t <= pow(10, upper):
            if majortick != int(np.floor(np.log10(t) + 1e-16)):
                majortick = int(np.floor(np.log10(t) + 1e-16))
                ticklabel = '1e%d' % majortick
            else:
                if upper - lower < 2:
                    minortick = int(t / pow(10, majortick) + .5)
                    ticklabel = '%de%d' % (minortick, majortick)
                else:
                    ticklabel = ''
            ticks.append((np.log10(t), ticklabel))
            t += inc(t)
        if len(ticks) == 0:
            ticks = [(0, '')]
        return ticks

    def _ticks(self, lower, upper, numticks=None):
        if isinstance(numticks, (float, int)):
            ideal = (upper - lower) / float(numticks)
        else:
            ideal = (upper - lower) / 7.
        log = np.log10(ideal)
        power = np.floor(log)
        if isinstance(numticks, (float, int)):
            grid = ideal
        else:
            fraction = log - power
            factor = 1.
            error = fraction
            for f, lf in self._multiples:
                e = np.fabs(fraction - lf)
                if e < error:
                    error = e
                    factor = f
            grid = factor * 10. ** power
        if self._useScientificNotation and (power > 4 or power < -4):
            format = '%+7.1e'
        elif power >= 0:
            digits = max(1, int(power))
            format = '%' + repr(digits) + '.0f'
        else:
            digits = -int(power)
            format = '%' + repr(digits + 2) + '.' + repr(digits) + 'f'
        ticks = []
        t = -grid * np.floor(-lower / grid)
        while t <= upper:
            if t == -0:
                t = 0
            ticks.append((t, format % (t,)))
            t = t + grid
        return ticks

    _multiples = [(2., np.log10(2.)), (5., np.log10(5.))]


    def _adjustScrollbars(self):
        if self._sb_ignore:
            self._sb_ignore = False
            return

        if not self.showScrollbars:
            return

        self._adjustingSB = True
        needScrollbars = False

        # horizontal scrollbar
        r_current = self._getXCurrentRange()
        r_max = list(self._getXMaxRange())
        sbfullrange = float(self.sb_hor.GetRange())

        r_max[0] = min(r_max[0], r_current[0])
        r_max[1] = max(r_max[1], r_current[1])

        self._sb_xfullrange = r_max

        unit = (r_max[1] - r_max[0]) / float(self.sb_hor.GetRange())
        pos = int((r_current[0] - r_max[0]) / unit)

        if pos >= 0:
            pagesize = int((r_current[1] - r_current[0]) / unit)

            self.sb_hor.SetScrollbar(pos, pagesize, int(sbfullrange), pagesize)
            self._sb_xunit = unit
            needScrollbars = needScrollbars or (pagesize != sbfullrange)
        else:
            self.sb_hor.SetScrollbar(0, 1000, 1000, 1000)

        # vertical scrollbar
        r_current = self._getYCurrentRange()
        r_max = list(self._getYMaxRange())
        sbfullrange = float(self.sb_vert.GetRange())

        r_max[0] = min(r_max[0], r_current[0])
        r_max[1] = max(r_max[1], r_current[1])

        self._sb_yfullrange = r_max

        unit = (r_max[1] - r_max[0]) / sbfullrange
        pos = int((r_current[0] - r_max[0]) / unit)

        if pos >= 0:
            pagesize = int((r_current[1] - r_current[0]) / unit)
            pos = (sbfullrange - 1 - pos - pagesize)
            self.sb_vert.SetScrollbar(int(pos), pagesize, int(sbfullrange), pagesize)
            self._sb_yunit = unit
            needScrollbars = needScrollbars or (pagesize != sbfullrange)
        else:
            self.sb_vert.SetScrollbar(0, 1000, 1000, 1000)

        self.sb_hor.Show(needScrollbars)
        self.sb_vert.Show(needScrollbars)
        self._adjustingSB = False
