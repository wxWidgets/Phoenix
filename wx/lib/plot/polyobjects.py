# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0330, C0103
#   E1101: Module X has no Y member
#   C0330: Wrong continued indentation
#   C0103: Invalid attribute/variable/method name
"""
polyobjects.py
==============

This contains all of the PolyXXX objects used by :mod:`wx.lib.plot`.

"""
__docformat__ = "restructuredtext en"

# Standard Library
import time as _time
import wx
import warnings
from collections import namedtuple

# Third-Party
try:
    import numpy as np
except:
    msg = """
    This module requires the NumPy module, which could not be
    imported.  It probably is not installed (it's not part of the
    standard Python distribution). See the Numeric Python site
    (http://numpy.scipy.org) for information on downloading source or
    binaries."""
    raise ImportError("NumPy not found.\n" + msg)

# Package
from .utils import pendingDeprecation
from .utils import TempStyle
from .utils import pairwise


# XXX: Comment out this line to disable deprecation warnings
warnings.simplefilter('default')


class PolyPoints(object):
    """
    Base Class for lines and markers.

    :param points: The points to plot
    :type points: list of ``(x, y)`` pairs
    :param attr: Additional attributes
    :type attr: dict

    .. warning::
       All methods are private.
    """

    def __init__(self, points, attr):
        self._points = np.array(points).astype(np.float64)
        self._logscale = (False, False)
        self._absScale = (False, False)
        self._symlogscale = (False, False)
        self._pointSize = (1.0, 1.0)
        self.currentScale = (1, 1)
        self.currentShift = (0, 0)
        self.scaled = self.points
        self.attributes = {}
        self.attributes.update(self._attributes)
        for name, value in attr.items():
            if name not in self._attributes.keys():
                err_txt = "Style attribute incorrect. Should be one of {}"
                raise KeyError(err_txt.format(self._attributes.keys()))
            self.attributes[name] = value

    @property
    def logScale(self):
        """
        A tuple of ``(x_axis_is_log10, y_axis_is_log10)`` booleans. If a value
        is ``True``, then that axis is plotted on a logarithmic base 10 scale.

        :getter: Returns the current value of logScale
        :setter: Sets the value of logScale
        :type: tuple of bool, length 2
        :raises ValueError: when setting an invalid value
        """
        return self._logscale

    @logScale.setter
    def logScale(self, logscale):
        if not isinstance(logscale, tuple) or len(logscale) != 2:
            raise ValueError("`logscale` must be a 2-tuple of bools")
        self._logscale = logscale

    def setLogScale(self, logscale):
        """
        Set to change the axes to plot Log10(values)

        Value must be a tuple of booleans (x_axis_bool, y_axis_bool)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.polyobjects.PolyPoints.logScale`
           property instead.
        """
        pendingDeprecation("self.logScale property")
        self._logscale = logscale

    @property
    def symLogScale(self):
        """
        .. warning::

           Not yet implemented.

        A tuple of ``(x_axis_is_SymLog10, y_axis_is_SymLog10)`` booleans.
        If a value is ``True``, then that axis is plotted on a symmetric
        logarithmic base 10 scale.

        A Symmetric Log10 scale means that values can be positive and
        negative. Any values less than
        :attr:`~wx.lig.plot.PolyPoints.symLogThresh` will be plotted on
        a linear scale to avoid the plot going to infinity near 0.

        :getter: Returns the current value of symLogScale
        :setter: Sets the value of symLogScale
        :type: tuple of bool, length 2
        :raises ValueError: when setting an invalid value

        .. notes::

           This is a simplified example of how SymLog works::

             if x >= thresh:
                 x = Log10(x)
             elif x =< thresh:
                 x = -Log10(Abs(x))
             else:
                 x = x

        .. seealso::

           + :attr:`~wx.lib.plot.PolyPoints.symLogThresh`
           + See http://matplotlib.org/examples/pylab_examples/symlog_demo.html
             for an example.
        """
        return self._symlogscale

    # TODO: Implement symmetric log scale
    @symLogScale.setter
    def symLogScale(self, symlogscale, thresh):
        raise NotImplementedError("Symmetric Log Scale not yet implemented")

        if not isinstance(symlogscale, tuple) or len(symlogscale) != 2:
            raise ValueError("`symlogscale` must be a 2-tuple of bools")
        self._symlogscale = symlogscale

    @property
    def symLogThresh(self):
        """
        .. warning::

           Not yet implemented.

        A tuple of ``(x_thresh, y_thresh)`` floats that define where the plot
        changes to linear scale when using a symmetric log scale.

        :getter: Returns the current value of symLogThresh
        :setter: Sets the value of symLogThresh
        :type: tuple of float, length 2
        :raises ValueError: when setting an invalid value

        .. notes::

           This is a simplified example of how SymLog works::

             if x >= thresh:
                 x = Log10(x)
             elif x =< thresh:
                 x = -Log10(Abs(x))
             else:
                 x = x

        .. seealso::

           + :attr:`~wx.lib.plot.PolyPoints.symLogScale`
           + See http://matplotlib.org/examples/pylab_examples/symlog_demo.html
             for an example.
        """
        return self._symlogscale

    # TODO: Implement symmetric log scale threshold
    @symLogThresh.setter
    def symLogThresh(self, symlogscale, thresh):
        raise NotImplementedError("Symmetric Log Scale not yet implemented")

        if not isinstance(symlogscale, tuple) or len(symlogscale) != 2:
            raise ValueError("`symlogscale` must be a 2-tuple of bools")
        self._symlogscale = symlogscale

    @property
    def absScale(self):
        """
        A tuple of ``(x_axis_is_abs, y_axis_is_abs)`` booleans. If a value
        is ``True``, then that axis is plotted on an absolute value scale.

        :getter: Returns the current value of absScale
        :setter: Sets the value of absScale
        :type: tuple of bool, length 2
        :raises ValueError: when setting an invalid value
        """
        return self._absScale

    @absScale.setter
    def absScale(self, absscale):

        if not isinstance(absscale, tuple) and len(absscale) == 2:
            raise ValueError("`absscale` must be a 2-tuple of bools")
        self._absScale = absscale

    @property
    def points(self):
        """
        Get or set the plotted points.

        :getter: Returns the current value of points, adjusting for the
                 various scale options such as Log, Abs, or SymLog.
        :setter: Sets the value of points.
        :type: list of `(x, y)` pairs

        .. Note::

           Only set unscaled points - do not perform the log, abs, or symlog
           adjustments yourself.
        """
        data = np.array(self._points, copy=True)    # need the copy
                                                    # TODO: get rid of the
                                                    # need for copy

        # work on X:
        if self.absScale[0]:
            data = self._abs(data, 0)
        if self.logScale[0]:
            data = self._log10(data, 0)

        if self.symLogScale[0]:
            # TODO: implement symLogScale
            # Should symLogScale override absScale? My vote is no.
            # Should symLogScale override logScale? My vote is yes.
            #   - symLogScale could be a parameter passed to logScale...
            pass

        # work on Y:
        if self.absScale[1]:
            data = self._abs(data, 1)
        if self.logScale[1]:
            data = self._log10(data, 1)

        if self.symLogScale[1]:
            # TODO: implement symLogScale
            pass

        return data

    @points.setter
    def points(self, points):
        self._points = points

    def _log10(self, data, index):
        """ Take the Log10 of the data, dropping any negative values """
        data = np.compress(data[:, index] > 0, data, 0)
        data[:, index] = np.log10(data[:, index])
        return data

    def _abs(self, data, index):
        """ Take the Abs of the data """
        data[:, index] = np.abs(data[:, index])
        return data

    def boundingBox(self):
        """
        Returns the bouding box for the entire dataset as a tuple with this
        format::

            ((minX, minY), (maxX, maxY))

        :returns: boundingbox
        :rtype: numpy array of ``[[minX, minY], [maxX, maxY]]``
        """
        if len(self.points) == 0:
            # no curves to draw
            # defaults to (-1,-1) and (1,1) but axis can be set in Draw
            minXY = np.array([-1.0, -1.0])
            maxXY = np.array([1.0, 1.0])
        else:
            minXY = np.minimum.reduce(self.points)
            maxXY = np.maximum.reduce(self.points)
        return minXY, maxXY

    def scaleAndShift(self, scale=(1, 1), shift=(0, 0)):
        """
        Scales and shifts the data for plotting.

        :param scale: The values to scale the data by.
        :type scale: list of floats: ``[x_scale, y_scale]``
        :param shift: The value to shift the data by. This should be in scaled
                      units
        :type shift: list of floats: ``[x_shift, y_shift]``
        :returns: None
        """
        if len(self.points) == 0:
            # no curves to draw
            return

        # TODO: Can we remove the if statement alltogether? Does
        #       scaleAndShift ever get called when the current value equals
        #       the new value?

        # cast everything to list: some might be np.ndarray objects
        if (list(scale) != list(self.currentScale)
                or list(shift) != list(self.currentShift)):
            # update point scaling
            self.scaled = scale * self.points + shift
            self.currentScale = scale
            self.currentShift = shift
        # else unchanged use the current scaling

    def getLegend(self):
        return self.attributes['legend']

    def getClosestPoint(self, pntXY, pointScaled=True):
        """
        Returns the index of closest point on the curve, pointXY,
        scaledXY, distance x, y in user coords.

        if pointScaled == True, then based on screen coords
        if pointScaled == False, then based on user coords
        """
        if pointScaled:
            # Using screen coords
            p = self.scaled
            pxy = self.currentScale * np.array(pntXY) + self.currentShift
        else:
            # Using user coords
            p = self.points
            pxy = np.array(pntXY)
        # determine distance for each point
        d = np.sqrt(np.add.reduce((p - pxy) ** 2, 1))  # sqrt(dx^2+dy^2)
        pntIndex = np.argmin(d)
        dist = d[pntIndex]
        return [pntIndex,
                self.points[pntIndex],
                self.scaled[pntIndex] / self._pointSize,
                dist]


class PolyLine(PolyPoints):
    """
    Creates PolyLine object

    :param points: The points that make up the line
    :type points: list of ``[x, y]`` values
    :param **attr: keyword attributes

    ===========================  =============  ====================
    Keyword and Default          Description    Type
    ===========================  =============  ====================
    ``colour='black'``           Line color     :class:`wx.Colour`
    ``width=1``                  Line width     float
    ``style=wx.PENSTYLE_SOLID``  Line style     :class:`wx.PenStyle`
    ``legend=''``                Legend string  str
    ``drawstyle='line'``         see below      str
    ===========================  =============  ====================

    ==================  ==================================================
    Draw style          Description
    ==================  ==================================================
    ``'line'``          Draws an straight line between consecutive points
    ``'steps-pre'``     Draws a line down from point A and then right to
                        point B
    ``'steps-post'``    Draws a line right from point A and then down
                        to point B
    ``'steps-mid-x'``   Draws a line horizontally to half way between A
                        and B, then draws a line vertically, then again
                        horizontally to point B.
    ``'steps-mid-y'``   Draws a line vertically to half way between A
                        and B, then draws a line horizonatally, then
                        again vertically to point B.
                        *Note: This typically does not look very good*
    ==================  ==================================================

    .. warning::

       All methods except ``__init__`` are private.
    """

    _attributes = {'colour': 'black',
                   'width': 1,
                   'style': wx.PENSTYLE_SOLID,
                   'legend': '',
                   'drawstyle': 'line',
                   }
    _drawstyles = ("line", "steps-pre", "steps-post",
                   "steps-mid-x", "steps-mid-y")

    def __init__(self, points, **attr):
        PolyPoints.__init__(self, points, attr)

    def draw(self, dc, printerScale, coord=None):
        """
        Draw the lines.

        :param dc: The DC to draw on.
        :type dc: :class:`wx.DC`
        :param printerScale:
        :type printerScale: float
        :param coord: The legend coordinate?
        :type coord: ???
        """
        colour = self.attributes['colour']
        width = self.attributes['width'] * printerScale * self._pointSize[0]
        style = self.attributes['style']
        drawstyle = self.attributes['drawstyle']

        if not isinstance(colour, wx.Colour):
            colour = wx.Colour(colour)
        pen = wx.Pen(colour, width, style)
        pen.SetCap(wx.CAP_BUTT)
        dc.SetPen(pen)
        if coord is None:
            if len(self.scaled):  # bugfix for Mac OS X
                for c1, c2 in zip(self.scaled, self.scaled[1:]):
                    self._path(dc, c1, c2, drawstyle)
        else:
            dc.DrawLines(coord)  # draw legend line

    def getSymExtent(self, printerScale):
        """
        Get the Width and Height of the symbol.

        :param printerScale:
        :type printerScale: float
        """
        h = self.attributes['width'] * printerScale * self._pointSize[0]
        w = 5 * h
        return (w, h)

    def _path(self, dc, coord1, coord2, drawstyle):
        """
        Calculates the path from coord1 to coord 2 along X and Y

        :param dc: The DC to draw on.
        :type dc: :class:`wx.DC`
        :param coord1: The first coordinate in the coord pair
        :type coord1: list, length 2: ``[x, y]``
        :param coord2: The second coordinate in the coord pair
        :type coord2: list, length 2: ``[x, y]``
        :param drawstyle: The type of connector to use
        :type drawstyle: str
        """
        if drawstyle == 'line':
            # Straight line between points.
            line = [coord1, coord2]
        elif drawstyle == 'steps-pre':
            # Up/down to next Y, then right to next X
            intermediate = [coord1[0], coord2[1]]
            line = [coord1, intermediate, coord2]
        elif drawstyle == 'steps-post':
            # Right to next X, then up/down to Y
            intermediate = [coord2[0], coord1[1]]
            line = [coord1, intermediate, coord2]
        elif drawstyle == 'steps-mid-x':
            # need 3 lines between points: right -> up/down -> right
            mid_x = ((coord2[0] - coord1[0]) / 2) + coord1[0]
            intermediate1 = [mid_x, coord1[1]]
            intermediate2 = [mid_x, coord2[1]]
            line = [coord1, intermediate1, intermediate2, coord2]
        elif drawstyle == 'steps-mid-y':
            # need 3 lines between points: up/down -> right -> up/down
            mid_y = ((coord2[1] - coord1[1]) / 2) + coord1[1]
            intermediate1 = [coord1[0], mid_y]
            intermediate2 = [coord2[0], mid_y]
            line = [coord1, intermediate1, intermediate2, coord2]
        else:
            err_txt = "Invalid drawstyle '{}'. Must be one of {}."
            raise ValueError(err_txt.format(drawstyle, self._drawstyles))

        dc.DrawLines(line)


class PolySpline(PolyLine):
    """
    Creates PolySpline object

    :param points: The points that make up the spline
    :type points: list of ``[x, y]`` values
    :param **attr: keyword attributes

    ===========================  =============  ====================
    Keyword and Default          Description    Type
    ===========================  =============  ====================
    ``colour='black'``           Line color     :class:`wx.Colour`
    ``width=1``                  Line width     float
    ``style=wx.PENSTYLE_SOLID``  Line style     :class:`wx.PenStyle`
    ``legend=''``                Legend string  str
    ===========================  =============  ====================

    .. warning::

       All methods except ``__init__`` are private.
    """

    _attributes = {'colour': 'black',
                   'width': 1,
                   'style': wx.PENSTYLE_SOLID,
                   'legend': ''}

    def __init__(self, points, **attr):
        PolyLine.__init__(self, points, **attr)

    def draw(self, dc, printerScale, coord=None):
        """ Draw the spline """
        colour = self.attributes['colour']
        width = self.attributes['width'] * printerScale * self._pointSize[0]
        style = self.attributes['style']
        if not isinstance(colour, wx.Colour):
            colour = wx.Colour(colour)
        pen = wx.Pen(colour, width, style)
        pen.SetCap(wx.CAP_ROUND)
        dc.SetPen(pen)
        if coord is None:
            if len(self.scaled) >= 3:
                dc.DrawSpline(self.scaled)
        else:
            dc.DrawLines(coord)  # draw legend line


class PolyMarker(PolyPoints):
    """
    Creates a PolyMarker object.

    :param points: The marker coordinates.
    :type points: list of ``[x, y]`` values
    :param **attr: keyword attributes

    =================================  =============  ====================
    Keyword and Default                Description    Type
    =================================  =============  ====================
    ``marker='circle'``                see below      str
    ``size=2``                         Marker size    float
    ``colour='black'``                 Outline color  :class:`wx.Colour`
    ``width=1``                        Outline width  float
    ``style=wx.PENSTYLE_SOLID``        Outline style  :class:`wx.PenStyle`
    ``fillcolour=colour``              fill color     :class:`wx.Colour`
    ``fillstyle=wx.BRUSHSTYLE_SOLID``  fill style     :class:`wx.BrushStyle`
    ``legend=''``                      Legend string  str
    =================================  =============  ====================

    ===================  ==================================
    Marker               Description
    ===================  ==================================
    ``'circle'``         A circle of diameter ``size``
    ``'dot'``            A dot. Does not have a size.
    ``'square'``         A square with side length ``size``
    ``'triangle'``       An upward-pointed triangle
    ``'triangle_down'``  A downward-pointed triangle
    ``'cross'``          An "X" shape
    ``'plus'``           A "+" shape
    ===================  ==================================

    .. warning::

       All methods except ``__init__`` are private.
    """
    _attributes = {'colour': 'black',
                   'width': 1,
                   'size': 2,
                   'fillcolour': None,
                   'fillstyle': wx.BRUSHSTYLE_SOLID,
                   'marker': 'circle',
                   'legend': ''}

    def __init__(self, points, **attr):
        PolyPoints.__init__(self, points, attr)

    def draw(self, dc, printerScale, coord=None):
        """ Draw the points """
        colour = self.attributes['colour']
        width = self.attributes['width'] * printerScale * self._pointSize[0]
        size = self.attributes['size'] * printerScale * self._pointSize[0]
        fillcolour = self.attributes['fillcolour']
        fillstyle = self.attributes['fillstyle']
        marker = self.attributes['marker']

        if colour and not isinstance(colour, wx.Colour):
            colour = wx.Colour(colour)
        if fillcolour and not isinstance(fillcolour, wx.Colour):
            fillcolour = wx.Colour(fillcolour)

        dc.SetPen(wx.Pen(colour, width))
        if fillcolour:
            dc.SetBrush(wx.Brush(fillcolour, fillstyle))
        else:
            dc.SetBrush(wx.Brush(colour, fillstyle))
        if coord is None:
            if len(self.scaled):  # bugfix for Mac OS X
                self._drawmarkers(dc, self.scaled, marker, size)
        else:
            self._drawmarkers(dc, coord, marker, size)  # draw legend marker

    def getSymExtent(self, printerScale):
        """Width and Height of Marker"""
        s = 5 * self.attributes['size'] * printerScale * self._pointSize[0]
        return (s, s)

    def _drawmarkers(self, dc, coords, marker, size=1):
        f = getattr(self, "_{}".format(marker))
        f(dc, coords, size)

    def _circle(self, dc, coords, size=1):
        fact = 2.5 * size
        wh = 5.0 * size
        rect = np.zeros((len(coords), 4), np.float) + [0.0, 0.0, wh, wh]
        rect[:, 0:2] = coords - [fact, fact]
        dc.DrawEllipseList(rect.astype(np.int32))

    def _dot(self, dc, coords, size=1):
        dc.DrawPointList(coords)

    def _square(self, dc, coords, size=1):
        fact = 2.5 * size
        wh = 5.0 * size
        rect = np.zeros((len(coords), 4), np.float) + [0.0, 0.0, wh, wh]
        rect[:, 0:2] = coords - [fact, fact]
        dc.DrawRectangleList(rect.astype(np.int32))

    def _triangle(self, dc, coords, size=1):
        shape = [(-2.5 * size, 1.44 * size),
                 (2.5 * size, 1.44 * size), (0.0, -2.88 * size)]
        poly = np.repeat(coords, 3, 0)
        poly.shape = (len(coords), 3, 2)
        poly += shape
        dc.DrawPolygonList(poly.astype(np.int32))

    def _triangle_down(self, dc, coords, size=1):
        shape = [(-2.5 * size, -1.44 * size),
                 (2.5 * size, -1.44 * size), (0.0, 2.88 * size)]
        poly = np.repeat(coords, 3, 0)
        poly.shape = (len(coords), 3, 2)
        poly += shape
        dc.DrawPolygonList(poly.astype(np.int32))

    def _cross(self, dc, coords, size=1):
        fact = 2.5 * size
        for f in [[-fact, -fact, fact, fact], [-fact, fact, fact, -fact]]:
            lines = np.concatenate((coords, coords), axis=1) + f
            dc.DrawLineList(lines.astype(np.int32))

    def _plus(self, dc, coords, size=1):
        fact = 2.5 * size
        for f in [[-fact, 0, fact, 0], [0, -fact, 0, fact]]:
            lines = np.concatenate((coords, coords), axis=1) + f
            dc.DrawLineList(lines.astype(np.int32))


class PolyBarsBase(PolyPoints):
    """
    Base class for PolyBars and PolyHistogram.

    .. warning::

       All methods are private.
    """
    _attributes = {'edgecolour': 'black',
                   'edgewidth': 2,
                   'edgestyle': wx.PENSTYLE_SOLID,
                   'legend': '',
                   'fillcolour': 'red',
                   'fillstyle': wx.BRUSHSTYLE_SOLID,
                   'barwidth': 1.0
                   }

    def __init__(self, points, attr):
        """
        """
        PolyPoints.__init__(self, points, attr)

    def _scaleAndShift(self, data, scale=(1, 1), shift=(0, 0)):
        """same as override method, but retuns a value."""
        scaled = scale * data + shift
        return scaled

    def getSymExtent(self, printerScale):
        """Width and Height of Marker"""
        h = self.attributes['edgewidth'] * printerScale * self._pointSize[0]
        w = 5 * h
        return (w, h)

    def set_pen_and_brush(self, dc, printerScale):
        pencolour = self.attributes['edgecolour']
        penwidth = (self.attributes['edgewidth']
                    * printerScale * self._pointSize[0])
        penstyle = self.attributes['edgestyle']
        fillcolour = self.attributes['fillcolour']
        fillstyle = self.attributes['fillstyle']

        if not isinstance(pencolour, wx.Colour):
            pencolour = wx.Colour(pencolour)
        pen = wx.Pen(pencolour, penwidth, penstyle)
        pen.SetCap(wx.CAP_BUTT)

        if not isinstance(fillcolour, wx.Colour):
            fillcolour = wx.Colour(fillcolour)
        brush = wx.Brush(fillcolour, fillstyle)

        dc.SetPen(pen)
        dc.SetBrush(brush)

    def scale_rect(self, rect):
        # Scale the points to the plot area
        scaled_rect = self._scaleAndShift(rect,
                                          self.currentScale,
                                          self.currentShift)

        # Convert to (left, top, width, height) for drawing
        wx_rect = [scaled_rect[0][0],                       # X (left)
                   scaled_rect[0][1],                       # Y (top)
                   scaled_rect[1][0] - scaled_rect[0][0],   # Width
                   scaled_rect[1][1] - scaled_rect[0][1]]   # Height

        return wx_rect

    def draw(self, dc, printerScale, coord=None):
        pass


class PolyBars(PolyBarsBase):
    """
    Creates a PolyBars object.

    :param points: The data to plot.
    :type points: sequence of ``(center, height)`` points
    :param **attr: keyword attributes

    =================================  =============  =======================
    Keyword and Default                Description    Type
    =================================  =============  =======================
    ``barwidth=1.0``                   bar width      float or list of floats
    ``edgecolour='black'``             edge color     :class:`wx.Colour`
    ``edgewidth=1``                    edge width     float
    ``edgestyle=wx.PENSTYLE_SOLID``    edge style     :class:`wx.PenStyle`
    ``fillcolour='red'``               fill color     :class:`wx.Colour`
    ``fillstyle=wx.BRUSHSTYLE_SOLID``  fill style     :class:`wx.BrushStyle`
    ``legend=''``                      legend string  str
    =================================  =============  =======================

    .. important::

       If ``barwidth`` is a list of floats:

       + each bar will have a separate width
       + ``len(barwidth)`` must equal ``len(points)``.

    .. warning::

       All methods except ``__init__`` are private.
    """
    def __init__(self, points, **attr):
        PolyBarsBase.__init__(self, points, attr)

    def calc_rect(self, x, y, w):
        """ Calculate the rectangle for plotting. """
        return self.scale_rect([[x - w / 2, y],      # left, top
                                [x + w / 2, 0]])     # right, bottom

    def draw(self, dc, printerScale, coord=None):
        """ Draw the bars """
        self.set_pen_and_brush(dc, printerScale)
        barwidth = self.attributes['barwidth']

        if coord is None:
            if isinstance(barwidth, (int, float)):
                # use a single width for all bars
                pts = ((x, y, barwidth) for x, y in self.points)
            elif isinstance(barwidth, (list, tuple)):
                # use a separate width for each bar
                if len(barwidth) != len(self.points):
                    err_str = ("Barwidth ({} items) and Points ({} items) do "
                               "not have the same length!")
                    err_str = err_str.format(len(barwidth), len(self.points))
                    raise ValueError(err_str)
                pts = ((x, y, w) for (x, y), w in zip(self.points, barwidth))
            else:
                # invalid attribute type
                err_str = ("Invalid type for 'barwidth'. Expected float, "
                           "int, or list or tuple of (int or float). Got {}.")
                raise TypeError(err_str.format(type(barwidth)))

            rects = [self.calc_rect(x, y, w) for x, y, w in pts]
            dc.DrawRectangleList(rects)
        else:
            dc.DrawLines(coord)  # draw legend line


class PolyHistogram(PolyBarsBase):
    """
    Creates a PolyHistogram object.

    :param hist: The histogram data.
    :type hist: sequence of ``y`` values that define the heights of the bars
    :param binspec: The bin specification.
    :type binspec: sequence of ``x`` values that define the edges of the bins
    :param **attr: keyword attributes

    =================================  =============  =======================
    Keyword and Default                Description    Type
    =================================  =============  =======================
    ``edgecolour='black'``             edge color     :class:`wx.Colour`
    ``edgewidth=3``                    edge width     float
    ``edgestyle=wx.PENSTYLE_SOLID``    edge style     :class:`wx.PenStyle`
    ``fillcolour='blue'``              fill color     :class:`wx.Colour`
    ``fillstyle=wx.BRUSHSTYLE_SOLID``  fill style     :class:`wx.BrushStyle`
    ``legend=''``                      legend string  str
    =================================  =============  =======================

    .. tip::

       Use ``np.histogram()`` to easily create your histogram parameters::

         hist_data, binspec = np.histogram(data)
         hist_plot = PolyHistogram(hist_data, binspec)

    .. important::

       ``len(binspec)`` must equal ``len(hist) + 1``.

    .. warning::

       All methods except ``__init__`` are private.
    """
    def __init__(self, hist, binspec, **attr):
        if len(binspec) != len(hist) + 1:
            raise ValueError("Len(binspec) must equal len(hist) + 1")

        self.hist = hist
        self.binspec = binspec

        # define the bins and center x locations
        self.bins = list(pairwise(self.binspec))
        bar_center_x = (pair[0] + (pair[1] - pair[0])/2 for pair in self.bins)

        points = list(zip(bar_center_x, self.hist))
        PolyBarsBase.__init__(self, points, attr)

    def calc_rect(self, y, low, high):
        """ Calculate the rectangle for plotting. """
        return self.scale_rect([[low, y],       # left, top
                                [high, 0]])     # right, bottom

    def draw(self, dc, printerScale, coord=None):
        """ Draw the bars """
        self.set_pen_and_brush(dc, printerScale)

        if coord is None:
            rects = [self.calc_rect(y, low, high)
                     for y, (low, high)
                     in zip(self.hist, self.bins)]

            dc.DrawRectangleList(rects)
        else:
            dc.DrawLines(coord)  # draw legend line


class PolyBoxPlot(PolyPoints):
    """
    Creates a PolyBoxPlot object.

    :param data: Raw data to create a box plot from.
    :type data: sequence of int or float
    :param **attr: keyword attributes

    =================================  =============  =======================
    Keyword and Default                Description    Type
    =================================  =============  =======================
    ``colour='black'``                 edge color     :class:`wx.Colour`
    ``width=1``                        edge width     float
    ``style=wx.PENSTYLE_SOLID``        edge style     :class:`wx.PenStyle`
    ``legend=''``                      legend string  str
    =================================  =============  =======================

    .. note::

       ``np.NaN`` and ``np.inf`` values are ignored.

    .. admonition:: TODO

       + [ ] Figure out a better way to get multiple box plots side-by-side
         (current method is a hack).
       + [ ] change the X axis to some labels.
       + [ ] Change getClosestPoint to only grab box plot items and outlers?
         Currently grabs every data point.
       + [ ] Add more customization such as Pens/Brushes, outlier shapes/size,
         and box width.
       + [ ] Figure out how I want to handle log-y: log data then calcBP? Or
         should I calc the BP first then the plot it on a log scale?
    """
    _attributes = {'colour': 'black',
                   'width': 1,
                   'style': wx.PENSTYLE_SOLID,
                   'legend': '',
                   }

    def __init__(self, points, **attr):
        # Set various attributes
        self.box_width = 0.5

        # Determine the X position and create a 1d dataset.
        self.xpos = points[0, 0]
        points = points[:, 1]

        # Calculate the box plot points and the outliers
        self._bpdata = self.calcBpData(points)
        self._outliers = self.calcOutliers(points)
        points = np.concatenate((self._bpdata, self._outliers))
        points = np.array([(self.xpos, x) for x in points])

        # Create a jitter for the outliers
        self.jitter = (0.05 * np.random.random_sample(len(self._outliers))
                       + self.xpos - 0.025)

        # Init the parent class
        PolyPoints.__init__(self, points, attr)

    def _clean_data(self, data=None):
        """
        Removes NaN and Inf from the data.
        """
        if data is None:
            data = self.points

        # clean out NaN and infinity values.
        data = data[~np.isnan(data)]
        data = data[~np.isinf(data)]

        return data

    def boundingBox(self):
        """
        Returns bounding box for the plot.

        Override method.
        """
        xpos = self.xpos

        minXY = np.array([xpos - self.box_width / 2, self._bpdata.min * 0.95])
        maxXY = np.array([xpos + self.box_width / 2, self._bpdata.max * 1.05])
        return minXY, maxXY

    def getClosestPoint(self, pntXY, pointScaled=True):
        """
        Returns the index of closest point on the curve, pointXY,
        scaledXY, distance x, y in user coords.

        Override method.

        if pointScaled == True, then based on screen coords
        if pointScaled == False, then based on user coords
        """

        xpos = self.xpos

        # combine the outliers with the box plot data
        data_to_use = np.concatenate((self._bpdata, self._outliers))
        data_to_use = np.array([(xpos, x) for x in data_to_use])

        if pointScaled:
            # Use screen coords
            p = self.scaled
            pxy = self.currentScale * np.array(pntXY) + self.currentShift
        else:
            # Using user coords
            p = self._points
            pxy = np.array(pntXY)

        # determine distnace for each point
        d = np.sqrt(np.add.reduce((p - pxy) ** 2, 1))  # sqrt(dx^2+dy^2)
        pntIndex = np.argmin(d)
        dist = d[pntIndex]
        return [pntIndex,
                self.points[pntIndex],
                self.scaled[pntIndex] / self._pointSize,
                dist]

    def getSymExtent(self, printerScale):
        """Width and Height of Marker"""
        # TODO: does this need to be updated?
        h = self.attributes['width'] * printerScale * self._pointSize[0]
        w = 5 * h
        return (w, h)

    def calcBpData(self, data=None):
        """
        Box plot points:

        Median (50%)
        75%
        25%
        low_whisker = lowest value that's >= (25% - (IQR * 1.5))
        high_whisker = highest value that's <= 75% + (IQR * 1.5)

        outliers are outside of 1.5 * IQR

        Parameters
        ----------
        data : array-like
            The data to plot

        Returns
        -------
        bpdata : collections.namedtuple
            Descriptive statistics for data:
            (min_data, low_whisker, q25, median, q75, high_whisker, max_data)

        """
        data = self._clean_data(data)

        min_data = float(np.min(data))
        max_data = float(np.max(data))
        q25 = float(np.percentile(data, 25))
        q75 = float(np.percentile(data, 75))

        iqr = q75 - q25

        low_whisker = float(data[data >= q25 - 1.5 * iqr].min())
        high_whisker = float(data[data <= q75 + 1.5 * iqr].max())

        median = float(np.median(data))

        BPData = namedtuple("bpdata", ("min", "low_whisker", "q25", "median",
                                       "q75", "high_whisker", "max"))

        bpdata = BPData(min_data, low_whisker, q25, median,
                        q75, high_whisker, max_data)

        return bpdata

    def calcOutliers(self, data=None):
        """
        Calculates the outliers. Must be called after calcBpData.
        """
        data = self._clean_data(data)

        outliers = data
        outlier_bool = np.logical_or(outliers > self._bpdata.high_whisker,
                                     outliers < self._bpdata.low_whisker)
        outliers = outliers[outlier_bool]
        return outliers

    def _scaleAndShift(self, data, scale=(1, 1), shift=(0, 0)):
        """same as override method, but retuns a value."""
        scaled = scale * data + shift
        return scaled

    @TempStyle('pen')
    def draw(self, dc, printerScale, coord=None):
        """
        Draws a box plot on the DC.

        Notes
        -----
        The following draw order is required:

        1. First the whisker line
        2. Then the IQR box
        3. Lasly the median line.

        This is because

        + The whiskers are drawn as single line rather than two lines
        + The median line must be visable over the box if the box has a fill.

        Other than that, the draw order can be changed.
        """
        self._draw_whisker(dc, printerScale)
        self._draw_iqr_box(dc, printerScale)
        self._draw_median(dc, printerScale)     # median after box
        self._draw_whisker_ends(dc, printerScale)
        self._draw_outliers(dc, printerScale)

    @TempStyle('pen')
    def _draw_whisker(self, dc, printerScale):
        """Draws the whiskers as a single line"""
        xpos = self.xpos

        # We draw it as one line and then hide the middle part with
        # the IQR rectangle
        whisker_line = np.array([[xpos, self._bpdata.low_whisker],
                                 [xpos, self._bpdata.high_whisker]])

        whisker_line = self._scaleAndShift(whisker_line,
                                           self.currentScale,
                                           self.currentShift)

        whisker_pen = wx.Pen(wx.BLACK, 2, wx.PENSTYLE_SOLID)
        whisker_pen.SetCap(wx.CAP_BUTT)
        dc.SetPen(whisker_pen)
        dc.DrawLines(whisker_line)

    @TempStyle('pen')
    def _draw_iqr_box(self, dc, printerScale):
        """Draws the Inner Quartile Range box"""
        xpos = self.xpos
        box_w = self.box_width

        iqr_box = [[xpos - box_w / 2, self._bpdata.q75],  # left, top
                   [xpos + box_w / 2, self._bpdata.q25]]  # right, bottom

        # Scale it to the plot area
        iqr_box = self._scaleAndShift(iqr_box,
                                      self.currentScale,
                                      self.currentShift)

        # rectangles are drawn (left, top, width, height) so adjust
        iqr_box = [iqr_box[0][0],                   # X (left)
                   iqr_box[0][1],                   # Y (top)
                   iqr_box[1][0] - iqr_box[0][0],   # Width
                   iqr_box[1][1] - iqr_box[0][1]]   # Height

        box_pen = wx.Pen(wx.BLACK, 3, wx.PENSTYLE_SOLID)
        box_brush = wx.Brush(wx.GREEN, wx.BRUSHSTYLE_SOLID)
        dc.SetPen(box_pen)
        dc.SetBrush(box_brush)

        dc.DrawRectangleList([iqr_box])

    @TempStyle('pen')
    def _draw_median(self, dc, printerScale, coord=None):
        """Draws the median line"""
        xpos = self.xpos

        median_line = np.array(
            [[xpos - self.box_width / 2, self._bpdata.median],
             [xpos + self.box_width / 2, self._bpdata.median]]
        )

        median_line = self._scaleAndShift(median_line,
                                          self.currentScale,
                                          self.currentShift)

        median_pen = wx.Pen(wx.BLACK, 4, wx.PENSTYLE_SOLID)
        median_pen.SetCap(wx.CAP_BUTT)
        dc.SetPen(median_pen)
        dc.DrawLines(median_line)

    @TempStyle('pen')
    def _draw_whisker_ends(self, dc, printerScale):
        """Draws the end caps of the whiskers"""
        xpos = self.xpos
        fence_top = np.array(
            [[xpos - self.box_width * 0.2, self._bpdata.high_whisker],
             [xpos + self.box_width * 0.2, self._bpdata.high_whisker]]
        )

        fence_top = self._scaleAndShift(fence_top,
                                        self.currentScale,
                                        self.currentShift)

        fence_bottom = np.array(
            [[xpos - self.box_width * 0.2, self._bpdata.low_whisker],
             [xpos + self.box_width * 0.2, self._bpdata.low_whisker]]
        )

        fence_bottom = self._scaleAndShift(fence_bottom,
                                           self.currentScale,
                                           self.currentShift)

        fence_pen = wx.Pen(wx.BLACK, 2, wx.PENSTYLE_SOLID)
        fence_pen.SetCap(wx.CAP_BUTT)
        dc.SetPen(fence_pen)
        dc.DrawLines(fence_top)
        dc.DrawLines(fence_bottom)

    @TempStyle('pen')
    def _draw_outliers(self, dc, printerScale):
        """Draws dots for the outliers"""
        # Set the pen
        outlier_pen = wx.Pen(wx.BLUE, 5, wx.PENSTYLE_SOLID)
        dc.SetPen(outlier_pen)

        outliers = self._outliers

        # Scale the data for plotting
        pt_data = np.array([self.jitter, outliers]).T
        pt_data = self._scaleAndShift(pt_data,
                                      self.currentScale,
                                      self.currentShift)

        # Draw the outliers
        size = 0.5
        fact = 2.5 * size
        wh = 5.0 * size
        rect = np.zeros((len(pt_data), 4), np.float) + [0.0, 0.0, wh, wh]
        rect[:, 0:2] = pt_data - [fact, fact]
        dc.DrawRectangleList(rect.astype(np.int32))


class PlotGraphics(object):
    """
    Creates a PlotGraphics object.

    :param objects: The Poly objects to plot.
    :type objects: list of :class:`~wx.lib.plot.PolyPoints` objects
    :param title: The title shown at the top of the graph.
    :type title: str
    :param xLabel: The x-axis label.
    :type xLabel: str
    :param yLabel: The y-axis label.
    :type yLabel: str

    .. warning::

       All methods except ``__init__`` are private.
    """
    def __init__(self, objects, title='', xLabel='', yLabel=''):
        if type(objects) not in [list, tuple]:
            raise TypeError("objects argument should be list or tuple")
        self.objects = objects
        self._title = title
        self._xLabel = xLabel
        self._yLabel = yLabel
        self._pointSize = (1.0, 1.0)

    @property
    def logScale(self):
        if len(self.objects) == 0:
            return
        return [obj.logScale for obj in self.objects]

    @logScale.setter
    def logScale(self, logscale):
        # XXX: error checking done by PolyPoints class
#        if not isinstance(logscale, tuple) and len(logscale) != 2:
#            raise TypeError("logscale must be a 2-tuple of bools")
        if len(self.objects) == 0:
            return
        for obj in self.objects:
            obj.logScale = logscale

    def setLogScale(self, logscale):
        """
        Set the log scale boolean value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.polyobjects.PlotGraphics.logScale`
           property instead.
        """
        pendingDeprecation("self.logScale property")
        self.logScale = logscale

    @property
    def absScale(self):
        if len(self.objects) == 0:
            return
        return [obj.absScale for obj in self.objects]

    @absScale.setter
    def absScale(self, absscale):
        # XXX: error checking done by PolyPoints class
#        if not isinstance(absscale, tuple) and len(absscale) != 2:
#            raise TypeError("absscale must be a 2-tuple of bools")
        if len(self.objects) == 0:
            return
        for obj in self.objects:
            obj.absScale = absscale

    def boundingBox(self):
        p1, p2 = self.objects[0].boundingBox()
        for o in self.objects[1:]:
            p1o, p2o = o.boundingBox()
            p1 = np.minimum(p1, p1o)
            p2 = np.maximum(p2, p2o)
        return p1, p2

    def scaleAndShift(self, scale=(1, 1), shift=(0, 0)):
        for o in self.objects:
            o.scaleAndShift(scale, shift)

    def setPrinterScale(self, scale):
        """
        Thickens up lines and markers only for printing

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.polyobjects.PlotGraphics.printerScale`
           property instead.
        """
        pendingDeprecation("self.printerScale property")
        self.printerScale = scale

    def setXLabel(self, xLabel=''):
        """
        Set the X axis label on the graph

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.polyobjects.PlotGraphics.xLabel`
           property instead.
        """
        pendingDeprecation("self.xLabel property")
        self.xLabel = xLabel

    def setYLabel(self, yLabel=''):
        """
        Set the Y axis label on the graph

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.polyobjects.PlotGraphics.yLabel`
           property instead.
        """
        pendingDeprecation("self.yLabel property")
        self.yLabel = yLabel

    def setTitle(self, title=''):
        """
        Set the title at the top of graph

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.polyobjects.PlotGraphics.title`
           property instead.
        """
        pendingDeprecation("self.title property")
        self.title = title

    def getXLabel(self):
        """
        Get X axis label string

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.polyobjects.PlotGraphics.xLabel`
           property instead.
        """
        pendingDeprecation("self.xLabel property")
        return self.xLabel

    def getYLabel(self):
        """
        Get Y axis label string

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.polyobjects.PlotGraphics.yLabel`
           property instead.
        """
        pendingDeprecation("self.yLabel property")
        return self.yLabel

    def getTitle(self, title=''):
        """
        Get the title at the top of graph

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.polyobjects.PlotGraphics.title`
           property instead.
        """
        pendingDeprecation("self.title property")
        return self.title

    @property
    def printerScale(self):
        return self._printerScale

    @printerScale.setter
    def printerScale(self, scale):
        """Thickens up lines and markers only for printing"""
        self._printerScale = scale

    @property
    def xLabel(self):
        """Get the X axis label on the graph"""
        return self._xLabel

    @xLabel.setter
    def xLabel(self, text):
        self._xLabel = text

    @property
    def yLabel(self):
        """Get the Y axis label on the graph"""
        return self._yLabel

    @yLabel.setter
    def yLabel(self, text):
        self._yLabel = text

    @property
    def title(self):
        """Get the title at the top of graph"""
        return self._title

    @title.setter
    def title(self, text):
        self._title = text

    def draw(self, dc):
        for o in self.objects:
#            t=_time.perf_counter()          # profile info
            o._pointSize = self._pointSize
            o.draw(dc, self._printerScale)
#            print(o, "time=", _time.perf_counter()-t)

    def getSymExtent(self, printerScale):
        """Get max width and height of lines and markers symbols for legend"""
        self.objects[0]._pointSize = self._pointSize
        symExt = self.objects[0].getSymExtent(printerScale)
        for o in self.objects[1:]:
            o._pointSize = self._pointSize
            oSymExt = o.getSymExtent(printerScale)
            symExt = np.maximum(symExt, oSymExt)
        return symExt

    def getLegendNames(self):
        """Returns list of legend names"""
        lst = [None] * len(self)
        for i in range(len(self)):
            lst[i] = self.objects[i].getLegend()
        return lst

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, item):
        return self.objects[item]


# -------------------------------------------------------------------------
# Used to layout the printer page


class PlotPrintout(wx.Printout):
    """Controls how the plot is made in printing and previewing"""
    # Do not change method names in this class,
    # we have to override wx.Printout methods here!

    def __init__(self, graph):
        """graph is instance of plotCanvas to be printed or previewed"""
        wx.Printout.__init__(self)
        self.graph = graph

    def HasPage(self, page):
        if page == 1:
            return True
        else:
            return False

    def GetPageInfo(self):
        return (1, 1, 1, 1)  # disable page numbers

    def OnPrintPage(self, page):
        dc = self.GetDC()  # allows using floats for certain functions
#        print("PPI Printer",self.GetPPIPrinter())
#        print("PPI Screen", self.GetPPIScreen())
#        print("DC GetSize", dc.GetSize())
#        print("GetPageSizePixels", self.GetPageSizePixels())
        # Note PPIScreen does not give the correct number
        # Calulate everything for printer and then scale for preview
        PPIPrinter = self.GetPPIPrinter()        # printer dots/inch (w,h)
        # PPIScreen= self.GetPPIScreen()          # screen dots/inch (w,h)
        dcSize = dc.GetSize()                    # DC size
        if self.graph._antiAliasingEnabled and not isinstance(dc, wx.GCDC):
            try:
                dc = wx.GCDC(dc)
            except Exception:
                pass
            else:
                if self.graph._hiResEnabled:
                    # high precision - each logical unit is 1/20 of a point
                    dc.SetMapMode(wx.MM_TWIPS)
        pageSize = self.GetPageSizePixels()  # page size in terms of pixcels
        clientDcSize = self.graph.GetClientSize()

        # find what the margins are (mm)
        pgSetupData = self.graph.pageSetupData
        margLeftSize, margTopSize = pgSetupData.GetMarginTopLeft()
        margRightSize, margBottomSize = pgSetupData.GetMarginBottomRight()

        # calculate offset and scale for dc
        pixLeft = margLeftSize * PPIPrinter[0] / 25.4  # mm*(dots/in)/(mm/in)
        pixRight = margRightSize * PPIPrinter[0] / 25.4
        pixTop = margTopSize * PPIPrinter[1] / 25.4
        pixBottom = margBottomSize * PPIPrinter[1] / 25.4

        plotAreaW = pageSize[0] - (pixLeft + pixRight)
        plotAreaH = pageSize[1] - (pixTop + pixBottom)

        # ratio offset and scale to screen size if preview
        if self.IsPreview():
            ratioW = float(dcSize[0]) / pageSize[0]
            ratioH = float(dcSize[1]) / pageSize[1]
            pixLeft *= ratioW
            pixTop *= ratioH
            plotAreaW *= ratioW
            plotAreaH *= ratioH

        # rescale plot to page or preview plot area
        self.graph._setSize(plotAreaW, plotAreaH)

        # Set offset and scale
        dc.SetDeviceOrigin(pixLeft, pixTop)

        # Thicken up pens and increase marker size for printing
        ratioW = float(plotAreaW) / clientDcSize[0]
        ratioH = float(plotAreaH) / clientDcSize[1]
        aveScale = (ratioW + ratioH) / 2
        if self.graph._antiAliasingEnabled and not self.IsPreview():
            scale = dc.GetUserScale()
            dc.SetUserScale(scale[0] / self.graph._pointSize[0],
                            scale[1] / self.graph._pointSize[1])
        self.graph._setPrinterScale(aveScale)  # tickens up pens for printing

        self.graph._printDraw(dc)
        # rescale back to original
        self.graph._setSize()
        self.graph._setPrinterScale(1)
        self.graph.Redraw()  # to get point label scale and shift correct

        return True
