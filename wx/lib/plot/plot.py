# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0330, C0103
#   E1101: Module X has no Y member
#   C0330: Wrong continued indentation
#   C0103: Invalid attribute/variable/method name
#
"""
wx.lib.plot
===========

See ``README.md``.

"""
__docformat__ = "restructuredtext en"

import string as _string
import time as _time
import sys
import wx
import functools
import warnings
from collections import namedtuple
from warnings import warn as _warn

# Needs NumPy
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

# XXX: Comment out this line to disable deprecation warnings
warnings.simplefilter('default')


# TODO: New name: RevertStyle? SavedStyle? Something else?
class TempStyle(object):
    """
    Combination Decorator and Context Manager to revert pen or brush changes
    after a method call or block finish.

    :param which: The item to save and revert after execution. Can be
                  one of ``{'both', 'pen', 'brush'}``.
    :type which: str
    :param dc: The DC to get brush/pen info from.
    :type dc: :class:`wx.DC`

    ::

        # Using as a method decorator:
        @TempStyle()                        # same as @TempStyle('both')
        def func(self, dc, a, b, c):        # dc must be 1st arg (beside self)
            # edit pen and brush here

        # Or as a context manager:
        with TempStyle('both', dc):
            # do stuff

    .. Note::

       As of 2016-06-15, this can only be used as a decorator for **class
       methods**, not standard functions. There is a plan to try and remove
       this restriction, but I don't know when that will happen...


    .. epigraph::

       *Combination Decorator and Context Manager! Also makes Julienne fries!
       Will not break! Will not... It broke!*

       -- The Genie
    """
    _valid_types = {'both', 'pen', 'brush'}
    _err_str = (
        "No DC provided and unable to determine DC from context for function "
        "`{func_name}`. When `{cls_name}` is used as a decorator, the "
        "decorated function must have a wx.DC as a keyword arg 'dc=' or "
        "as the first arg."
    )

    def __init__(self, which='both', dc=None):
        if which not in self._valid_types:
            raise ValueError(
                "`which` must be one of {}".format(self._valid_types)
            )
        self.which = which
        self.dc = dc
        self.prevPen = None
        self.prevBrush = None

    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(instance, dc, *args, **kwargs):
            # fake the 'with' block. This solves:
            # 1.  plots only being shown on 2nd menu selection in demo
            # 2.  self.dc compalaining about not having a super called when
            #     trying to get or set the pen/brush values in __enter__ and
            #     __exit__:
            #         RuntimeError: super-class __init__() of type
            #         BufferedDC was never called
            self._save_items(dc)
            func(instance, dc, *args, **kwargs)
            self._revert_items(dc)

            #import copy                    # copy solves issue #1 above, but
            #self.dc = copy.copy(dc)        # possibly causes issue #2.

            #with self:
            #    print('in with')
            #    func(instance, dc, *args, **kwargs)

        return wrapper

    def __enter__(self):
        self._save_items(self.dc)
        return self

    def __exit__(self, *exc):
        self._revert_items(self.dc)
        return False    # True means exceptions *are* suppressed.

    def _save_items(self, dc):
        if self.which == 'both':
            self._save_pen(dc)
            self._save_brush(dc)
        elif self.which == 'pen':
            self._save_pen(dc)
        elif self.which == 'brush':
            self._save_brush(dc)
        else:
            err_str = ("How did you even get here?? This class forces "
                       "correct values for `which` at instancing..."
                       )
            raise ValueError(err_str)

    def _revert_items(self, dc):
        if self.which == 'both':
            self._revert_pen(dc)
            self._revert_brush(dc)
        elif self.which == 'pen':
            self._revert_pen(dc)
        elif self.which == 'brush':
            self._revert_brush(dc)
        else:
            err_str = ("How did you even get here?? This class forces "
                       "correct values for `which` at instancing...")
            raise ValueError(err_str)

    def _save_pen(self, dc):
        self.prevPen = dc.GetPen()

    def _save_brush(self, dc):
        self.prevBrush = dc.GetBrush()

    def _revert_pen(self, dc):
        dc.SetPen(self.prevPen)

    def _revert_brush(self, dc):
        dc.SetBrush(self.prevBrush)


class PendingDeprecation(object):
    """
    Decorator which warns the developer about methods that are
    pending deprecation.

    :param new_func: The new class, method, or function that should be used.
    :type new_func: str

    ::

        @PendingDeprecation("new_func")
        def old_func():
            pass

        # prints the warning:
        # `old_func` is pending deprecation. Please use `new_func` instead.

    """
    _warn_txt = "`{}` is pending deprecation. Please use `{}` instead."

    def __init__(self, new_func):
        self.new_func = new_func

    def __call__(self, func):
        """Support for functions"""
        self.func = func
#        self._update_docs()

        @functools.wraps(self.func)
        def wrapper(*args, **kwargs):
            _warn(self._warn_txt.format(self.func.__name__, self.new_func),
                  PendingDeprecationWarning)
            return self.func(*args, **kwargs)
        return wrapper

    def _update_docs(self):
        """ Set the docs to that of the decorated function. """
        self.__name__ = self.func.__name__
        self.__doc__ = self.func.__doc__


class _DisplaySide(object):
    """
    Generic class for storing booleans describing which sides of a box are
    displayed. Used for fine-tuning the axis, ticks, and values of a graph.

    This class somewhat mimics a collections.namedtuple factory function in
    that it is an iterable and can have indiviual elements accessible by name.
    It differs from a namedtuple in a few ways:

    - it's mutable
    - it's not a factory function but a full-fledged class
    - it contains type checking, only allowing boolean values
    - it contains name checking, only allowing valid_names as attributes

    :param bottom: Display the bottom side?
    :type bottom: bool
    :param left: Display the left side?
    :type left: bool
    :param top: Display the top side?
    :type top: bool
    :param right: Display the right side?
    :type right: bool
    """
    # TODO: Do I want to replace with __slots__?
    #       Not much memory gain because this class is only called a small
    #       number of times, but it would remove the need for part of
    #       __setattr__...
    valid_names = ("bottom", "left", "right", "top")

    def __init__(self, bottom, left, top, right):
        if not all([isinstance(x, bool) for x in [bottom, left, top, right]]):
            raise TypeError("All args must be bools")
        self.bottom = bottom
        self.left = left
        self.top = top
        self.right = right

    def __str__(self):
        s = "{}(bottom={}, left={}, top={}, right={})"
        s = s.format(self.__class__.__name__,
                     self.bottom,
                     self.left,
                     self.top,
                     self.right,
                     )
        return s

    def __repr__(self):
        # for now, just return the str representation
        return self.__str__()

    def __setattr__(self, name, value):
        """
        Override __setattr__ to implement some type checking and prevent
        other attributes from being created.
        """
        if name not in self.valid_names:
            err_str = "attribute must be one of {}"
            raise NameError(err_str.format(self.valid_names))
        if not isinstance(value, bool):
            raise TypeError("'{}' must be a boolean".format(name))
        self.__dict__[name] = value

    def __len__(self):
        return 4

    def __hash__(self):
        return hash(tuple(self))

    def __getitem__(self, key):
        return (self.bottom, self.left, self.top, self.right)[key]

    def __setitem__(self, key, value):
        if key == 0:
            self.bottom = value
        elif key == 1:
            self.left = value
        elif key == 2:
            self.top = value
        elif key == 3:
            self.right = value
        else:
            raise IndexError("list index out of range")

    def __iter__(self):
        return iter([self.bottom, self.left, self.top, self.right])


#
# Plotting classes...
#
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

    @PendingDeprecation("self.logScale property")
    def setLogScale(self, logscale):
        """
        Set to change the axes to plot Log10(values)

        Value must be a tuple of booleans (x_axis_bool, y_axis_bool)
        """
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
            if len(self.scaled):  # bugfix for Mac OS X
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

        # need to create a series of points to be used by PolyPoints
        import itertools
        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = itertools.tee(iterable)
            next(b, None)
            return zip(a, b)

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


class BoxPlot(PolyPoints):
    """
    Creates a BoxPlot object.

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

        Parameters:
        -----------
        data : array-like
            The data to plot

        Returns:
        --------
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

        Notes:
        ------
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
        # TODO: convert to try..except statement
#        try:
#        return [obj.logScale for obj in self.objects]
#        except:     # what error would be returned?
#            return
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

    @PendingDeprecation("self.logScale property")
    def setLogScale(self, logscale):
        """
        Set the log scale boolean value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotGraphics.logScale` property
           instead.
        """
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

    @PendingDeprecation("self.printerScale property")
    def setPrinterScale(self, scale):
        """
        Thickens up lines and markers only for printing

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotGraphics.printerScale` property
           instead.
        """
        self.printerScale = scale

    @PendingDeprecation("self.xLabel property")
    def setXLabel(self, xLabel=''):
        """
        Set the X axis label on the graph

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotGraphics.xLabel` property
           instead.
       """
        self.xLabel = xLabel

    @PendingDeprecation("self.yLabel property")
    def setYLabel(self, yLabel=''):
        """
        Set the Y axis label on the graph

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotGraphics.yLabel` property
           instead.
       """
        self.yLabel = yLabel

    @PendingDeprecation("self.title property")
    def setTitle(self, title=''):
        """
        Set the title at the top of graph

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotGraphics.title` property
           instead.
        """
        self.title = title

    @PendingDeprecation("self.xLabel property")
    def getXLabel(self):
        """
        Get X axis label string

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotGraphics.xLabel` property
           instead.
        """
        return self.xLabel

    @PendingDeprecation("self.yLabel property")
    def getYLabel(self):
        """
        Get Y axis label string

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotGraphics.yLabel` property
           instead.
        """
        return self.yLabel

    @PendingDeprecation("self.title property")
    def getTitle(self, title=''):
        """
        Get the title at the top of graph

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotGraphics.title` property
           instead.
        """
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


def scale_and_shift_point(x, y, scale=1, shift=0):
    """
    Creates a scaled and shifted 2x1 numpy array of [x, y] values.

    :param float `x`:        The x value of the unscaled, unshifted point
    :param float `y`:        The y valye of the unscaled, unshifted point
    :param np.array `scale`: The scale factor to use ``[x_sacle, y_scale]``
    :param np.array `shift`: The offset to apply ``[x_shift, y_shift]``.
                             Must be in scaled units

    :returns: a numpy array of 2 elements
    :rtype: np.array

    .. note::
       :math:`new = (scale * old) + shift`
    """
    point = scale * np.array([x, y]) + shift
    return point


def _set_displayside(value):
    """
    Wrapper around :class:`~wx.lib.plot._DisplaySide` that allowing for
    "overloaded" calls.

    If ``value`` is a boolean: all 4 sides are set to ``value``

    If ``value`` is a 2-tuple: the bottom and left sides are set to ``value``
    and the other sides are set to False.

    If ``value`` is a 4-tuple, then each item is set individually: ``(bottom,
    left, top, right)``

    :param value: Which sides to display.
    :type value:   bool, 2-tuple of bool, or 4-tuple of bool
    :raises: `TypeError` if setting an invalid value.
    :raises: `ValueError` if the tuple has incorrect length.
    :rtype: :class:`~wx.lib.plot._DisplaySide`
    """
    err_txt = ("value must be a bool or a 2- or 4-tuple of bool")

    # TODO: for 2-tuple, do not change other sides? rather than set to False.
    if isinstance(value, bool):
        # turns on or off all axes
        _value = (value, value, value, value)
    elif isinstance(value, tuple):
        if len(value) == 2:
            _value = (value[0], value[1], False, False)
        elif len(value) == 4:
            _value = value
        else:
            raise ValueError(err_txt)
    else:
        raise TypeError(err_txt)
    return _DisplaySide(*_value)


#-------------------------------------------------------------------------
# Main window that you will want to import into your application.

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

        # set curser as cross-hairs
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
        self._ticksEnabled = _DisplaySide(False, False, False, False)
        self._axesEnabled = _DisplaySide(True, True, True, True)
        self._axesValuesEnabled = _DisplaySide(True, True, False, False)

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
                               self._pointSize[0],
                               wx.PENSTYLE_DOT)

        self._centerLinePen = wx.Pen(wx.RED,
                                     self._pointSize[0],
                                     wx.PENSTYLE_SHORT_DASH)

        self._axesPen = wx.Pen(wx.BLACK,
                               self._pointSize[0],
                               wx.PENSTYLE_SOLID)

        self._tickPen = wx.Pen(wx.BLACK,
                               self._pointSize[0],
                               wx.PENSTYLE_SOLID)
        self._tickLength = tuple(x * 3 for x in self._pointSize)

        self._diagonalPen = wx.Pen(wx.BLUE,
                                   self._pointSize[0],
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
        :type:   int or float
        :raise:  `TypeError` when setting a value that is not an int or float.
        """
        return self._tickLength

    @tickLength.setter
    def tickLength(self, length):
        if not isinstance(length, (int, float)):
            raise TypeError("`length` must be an integer or float")
        self._tickWidth = length

    # SaveFile
    def SaveFile(self, fileName=''):
        """
        Saves the file to the type specified in the extension. If no file
        name is specified a dialog box is provided.  Returns True if
        sucessful, otherwise False.

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

        fType = _string.lower(fileName[-3:])
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
                                     wx.SAVE | wx.OVERWRITE_PROMPT,
                                     )

            if dlg1.ShowModal() == wx.ID_OK:
                fileName = dlg1.GetPath()
                fType = _string.lower(fileName[-3:])
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

    @PendingDeprecation("self.logScale property")
    def setLogScale(self, logscale):
        """
        Set the log scale boolean value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.logScale` property instead.
        """
        self.logScale = logscale

    @PendingDeprecation("self.logScale property")
    def getLogScale(self):
        """
        Set the log scale boolean value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.logScale` property instead.
        """
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

    @PendingDeprecation("self.fontSizeAxis property")
    def SetFontSizeAxis(self, point=10):
        """
        Set the tick and axis label font size (default is 10 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.fontSizeAxis` property
           instead.
        """
        self.fontSizeAxis = point

    @PendingDeprecation("self.fontSizeAxis property")
    def GetFontSizeAxis(self):
        """
        Get current tick and axis label font size in points

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.fontSizeAxis` property
           instead.
        """
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

    @PendingDeprecation("self.fontSizeTitle property")
    def SetFontSizeTitle(self, point=15):
        """
        Set Title font size (default is 15 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.fontSizeTitle` property
           instead.
        """
        self.fontSizeTitle = point

    @PendingDeprecation("self.fontSizeTitle property")
    def GetFontSizeTitle(self):
        """
        Get Title font size (default is 15 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.fontSizeTitle` property
           instead.
        """
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

    @PendingDeprecation("self.fontSizeLegend property")
    def SetFontSizeLegend(self, point=7):
        """
        Set legend font size (default is 7 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.fontSizeLegend' property
           instead.
        """
        self.fontSizeLegend = point

    def GetFontSizeLegend(self):
        """
        Get legend font size (default is 7 point)

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.fontSizeLegend' property
           instead.
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

    @PendingDeprecation("self.showScrollbars property")
    def SetShowScrollbars(self, value):
        """
        Set the showScrollbars value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.showScrollbars` property
           instead.
        """
        self.showScrollbars = value

    @PendingDeprecation("self.showScrollbars property")
    def GetShowScrollbars(self):
        """
        Get the showScrollbars value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.showScrollbars` property
           instead.
        """
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
        # XXX: should have sb_hor.IsShown() as well.
        return self.sb_vert.IsShown()

    @showScrollbars.setter
    def showScrollbars(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value should be True or False")
        if value == self.showScrollbars:
            # no change, so don't do anything
            return
        self.sb_vert.Show(value)
        self.sb_hor.Show(value)
        wx.CallAfter(self.Layout)

    @PendingDeprecation("self.useScientificNotation property")
    def SetUseScientificNotation(self, useScientificNotation):
        """
        Set the useScientificNotation value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.useScientificNotation`
           property instead.
        """
        self.useScientificNotation = useScientificNotation

    @PendingDeprecation("self.useScientificNotation property")
    def GetUseScientificNotation(self):
        """
        Get the useScientificNotation value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.useScientificNotation`
           property instead.
        """
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

    @PendingDeprecation("self.enableAntiAliasing property")
    def SetEnableAntiAliasing(self, enableAntiAliasing):
        """
        Set the enableAntiAliasing value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableAntiAliasing`
           property instead.
        """
        self.enableAntiAliasing = enableAntiAliasing

    @PendingDeprecation("self.enableAntiAliasing property")
    def GetEnableAntiAliasing(self):
        """
        Get the enableAntiAliasing value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableAntiAliasing`
           property instead.
        """
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

    @PendingDeprecation("self.enableHiRes property")
    def SetEnableHiRes(self, enableHiRes):
        """
        Set the enableHiRes value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableHiRes` property
           instead.
        """
        self.enableHiRes = enableHiRes

    @PendingDeprecation("self.enableHiRes property")
    def GetEnableHiRes(self):
        """
        Get the enableHiRes value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableHiRes` property
           instead.
        """
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

    @PendingDeprecation("self.enableDrag property")
    def SetEnableDrag(self, value):
        """
        Set the enableDrag value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableDrag` property
           instead.
        """
        self.enableDrag = value

    @PendingDeprecation("self.enableDrag property")
    def GetEnableDrag(self):
        """
        Get the enableDrag value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableDrag` property
           instead.
        """
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
           :attr:`~wx.lib.plot.PlotCanvas.enableZoom`. Setting one will
           disable the other.

        .. seealso::
           :attr:`~wx.lib.plot.PlotCanvas.enableZoom`
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

    @PendingDeprecation("self.enableZoom property")
    def SetEnableZoom(self, value):
        """
        Set the enableZoom value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableZoom` property
           instead.
        """
        self.enableZoom = value

    @PendingDeprecation("self.enableZoom property")
    def GetEnableZoom(self):
        """
        Get the enableZoom value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableZoom` property
           instead.
        """
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
           :attr:`~wx.lib.plot.PlotCanvas.enableDrag`. Setting one will
           disable the other.

        .. seealso::
           :attr:`~wx.lib.plot.PlotCanvas.enableDrag`
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

    @PendingDeprecation("self.enableGrid property")
    def SetEnableGrid(self, value):
        """
        Set the enableGrid value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableGrid` property
           instead.
        """
        self.enableGrid = value

    @PendingDeprecation("self.enableGrid property")
    def GetEnableGrid(self):
        """
        Get the enableGrid value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableGrid` property
           instead.
        """
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

    @PendingDeprecation("self.enableCenterLines property")
    def SetEnableCenterLines(self, value):
        """
        Set the enableCenterLines value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableCenterLines`
           property instead.
        """
        self.enableCenterLines = value

    @PendingDeprecation("self.enableCenterLines property")
    def GetEnableCenterLines(self):
        """
        Get the enableCenterLines value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableCenterLines`
           property instead.
        """
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

    @PendingDeprecation("self.enableDiagonals property")
    def SetEnableDiagonals(self, value):
        """
        Set the enableDiagonals value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableDiagonals`
           property instead.
        """
        self.enableDiagonals = value

    @PendingDeprecation("self.enableDiagonals property")
    def GetEnableDiagonals(self):
        """
        Get the enableDiagonals value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableDiagonals`
           property instead.
        """
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

    @PendingDeprecation("self.enableLegend property")
    def SetEnableLegend(self, value):
        """
        Set the enableLegend value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableLegend`
           property instead.
        """
        self.enableLegend = value

    @PendingDeprecation("self.enableLegend property")
    def GetEnableLegend(self):
        """
        Get the enableLegend value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableLegend`
           property instead.
        """
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

    @PendingDeprecation("self.enableTitle property")
    def SetEnableTitle(self, value):
        """
        Set the enableTitle value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableTitle` property
           instead.
        """
        self.enableTitle = value

    @PendingDeprecation("self.enableTitle property")
    def GetEnableTitle(self):
        """
        Get the enableTitle value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enableTitle` property
           instead.
        """
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

    @PendingDeprecation("self.enablePointLabel property")
    def SetEnablePointLabel(self, value):
        """
        Set the enablePointLabel value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enablePointLabel`
           property instead.
        """
        self.enablePointLabel = value

    @PendingDeprecation("self.enablePointLabel property")
    def GetEnablePointLabel(self):
        """
        Set the enablePointLabel value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enablePointLabel`
           property instead.
        """
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
        self._axesEnabled = _set_displayside(value)
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
        self._axesValuesEnabled = _set_displayside(value)
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
        self._ticksEnabled = _set_displayside(value)
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

    @PendingDeprecation("self.pointLabelFunc property")
    def SetPointLabelFunc(self, func):
        """
        Set the enablePointLabel value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enablePointLabel`
           property instead.
        """
        self.pointLabelFunc = func

    @PendingDeprecation("self.pointLabelFunc property")
    def GetPointLabelFunc(self):
        """
        Get the enablePointLabel value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.enablePointLabel`
           property instead.
        """
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

    @PendingDeprecation("self.xSpec property")
    def SetXSpec(self, spectype='auto'):
        """
        Set the xSpec value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.xSpec` property instead.
        """
        self.xSpec = spectype

    @PendingDeprecation("self.ySpec property")
    def SetYSpec(self, spectype='auto'):
        """
        Set the ySpec value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.ySpec` property instead.
        """
        self.ySpec = spectype

    @PendingDeprecation("self.xSpec property")
    def GetXSpec(self):
        """
        Get the xSpec value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.xSpec` property instead.
        """
        return self.xSpec

    @PendingDeprecation("self.ySpec property")
    def GetYSpec(self):
        """
        Get the ySpec value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.ySpec` property instead.
        """
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
           :attr:`~wx.lib.plot.PlotCanvas.ySpec`
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
           :attr:`~wx.lib.plot.PlotCanvas.xSpec`
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

    @PendingDeprecation("self.xMaxRange property")
    def GetXMaxRange(self):
        """
        Get the xMaxRange value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.xMaxRange` property instead.
        """
        return self.xMaxRange

    @property
    def xMaxRange(self):
        """
        The plots' maximum X range as a tuple of ``(min, max)``.

        :getter: Returns the value of xMaxRange.

        .. seealso::
           :attr:`~wx.lib.plot.PlotCanvas.yMaxRange`
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

    @PendingDeprecation("self.yMaxRange property")
    def GetYMaxRange(self):
        """
        Get the yMaxRange value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.yMaxRange` property instead.
        """
        return self.yMaxRange

    @property
    def yMaxRange(self):
        """
        The plots' maximum Y range as a tuple of ``(min, max)``.

        :getter: Returns the value of yMaxRange.

        .. seealso::
           :attr:`~wx.lib.plot.PlotCanvas.xMaxRange`
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

    @PendingDeprecation("self.xCurrentRange property")
    def GetXCurrentRange(self):
        """
        Get the xCurrentRange value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.xCurrentRange` property
           instead.
        """
        return self.xCurrentRange

    @property
    def xCurrentRange(self):
        """
        The plots' X range of the currently displayed portion as
        a tuple of ``(min, max)``

        :getter: Returns the value of xCurrentRange.

        .. seealso::
           :attr:`~wx.lib.plot.PlotCanvas.yCurrentRange`
        """
        xAxis = self._getXCurrentRange()
        if self.logScale[0]:
            xAxis = np.power(10, xAxis)
        return xAxis

    def _getXCurrentRange(self):
        """Returns (minX, maxX) x-axis for currently displayed
        portion of graph"""
        return self.last_draw[1]

    @PendingDeprecation("self.yCurrentRange property")
    def GetYCurrentRange(self):
        """
        Get the yCurrentRange value.

        .. deprecated:: Feb 27, 2016

           Use the :attr:`~wx.lib.plot.PlotCanvas.yCurrentRange` property
           instead.
        """
        return self.yCurrentRange

    @property
    def yCurrentRange(self):
        """
        The plots' Y range of the currently displayed portion as
        a tuple of ``(min, max)``

        :getter: Returns the value of yCurrentRange.

        .. seealso::
           :attr:`~wx.lib.plot.PlotCanvas.xCurrentRange`
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
                except Exception:
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

        # saves most recient values
        self.last_draw = (graphics, np.array(xAxis), np.array(yAxis))

        # Get ticks and textExtents for axis if required
        if self._xSpec is not 'none':
            xticks = self._xticks(xAxis[0], xAxis[1])
        else:
            xticks = None
        if xticks:
            # w h of x axis text last number on axis
            xTextExtent = dc.GetTextExtent(xticks[-1][1])
        else:
            xTextExtent = (0, 0)  # No text for ticks
        if self._ySpec is not 'none':
            yticks = self._yticks(yAxis[0], yAxis[1])
        else:
            yticks = None
        if yticks:
            if self.logScale[1]:
                yTextExtent = dc.GetTextExtent('-2e-2')
            else:
                yTextExtentBottom = dc.GetTextExtent(yticks[0][1])
                yTextExtentTop = dc.GetTextExtent(yticks[-1][1])
                yTextExtent = (max(yTextExtentBottom[0], yTextExtentTop[0]),
                               max(yTextExtentBottom[1], yTextExtentTop[1]))
        else:
            yticks = None
            yTextExtent = (0, 0)  # No text for ticks

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
        scale = (self.plotbox_size - textSize_scale) / \
            (p2 - p1) * np.array((1, -1))
        shift = -p1 * scale + self.plotbox_origin + \
            textSize_shift * np.array((1, -1))
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
        dc.SetClippingRegion(ptx * self._pointSize[0],
                             pty * self._pointSize[1],
                             rectWidth * self._pointSize[0] + 2,
                             rectHeight * self._pointSize[1] + 1)
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
            cn = [curveNum] + \
                [obj.getLegend()] + obj.getClosestPoint(pntXY, pointScaled)
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
            if np.sometrue(
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
                fullrange, pagesize = self.sb_vert.GetRange(
                ), self.sb_vert.GetPageSize()
                sbpos = fullrange - pagesize - sbpos
                dist = sbpos * self._sb_xunit - \
                    (self._getXCurrentRange()[0] - self._sb_xfullrange)
                self.ScrollUp(dist)

            if evt.GetOrientation() == wx.HORIZONTAL:
                dist = sbpos * self._sb_xunit - \
                    (self._getXCurrentRange()[0] - self._sb_xfullrange[0])
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
        if sys.platform != "darwin":
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
        if sys.platform == "darwin":
            self._Buffer = tmp_Buffer

    def _drawLegend(self, dc, graphics, rhsW, topH, legendBoxWH,
                    legendSymExt, legendTextExt):
        """Draws legend symbols and text"""
        # top right hand corner of graph box is ref corner
        trhc = self.plotbox_origin + \
            (self.plotbox_size - [rhsW, topH]) * [1, -1]
        # border space between legend sym and graph box
        legendLHS = .091 * legendBoxWH[0]
        # 1.1 used as space between lines
        lineHeight = max(legendSymExt[1], legendTextExt[1]) * 1.1
        dc.SetFont(self._getFont(self._fontSizeLegend))
        for i in range(len(graphics)):
            o = graphics[i]
            s = i * lineHeight
            if isinstance(o, PolyMarker) or isinstance(o, BoxPlot):
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
            dc.DrawText(o.getLegend(), pnt[0], pnt[1])
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
        dc.DrawRectangle(ptx, pty, rectWidth, rectHeight)
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
        pen.SetWidth(penWidth)
        dc.SetPen(pen)

        x, y, width, height = self._point2ClientCoord(p1, p2)

        if self._xSpec != 'none':
            if self.enableGrid[0]:
                for x, _ in xticks:
                    pt = scale_and_shift_point(x, p1[1], scale, shift)
                    dc.DrawLine(pt[0], pt[1], pt[0], pt[1] - height)

        if self._ySpec != 'none':
            if self.enableGrid[1]:
                for y, label in yticks:
                    pt = scale_and_shift_point(p1[0], y, scale, shift)
                    dc.DrawLine(pt[0], pt[1], pt[0] + width, pt[1])

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
        pen.SetWidth(penWidth)
        dc.SetPen(pen)

        # lengthen lines for printing
        yTickLength = 3 * self.printerScale * self._tickLength[1]
        xTickLength = 3 * self.printerScale * self._tickLength[0]

        ticks = self.enableTicks
        if self.xSpec != 'none':        # I don't like this :-/
            if ticks.bottom:
                lines = []
                for x, label in xticks:
                    pt = scale_and_shift_point(x, p1[1], scale, shift)
                    lines.append((pt[0], pt[1], pt[0], pt[1] - xTickLength))
                dc.DrawLineList(lines)
            if ticks.top:
                lines = []
                for x, label in xticks:
                    pt = scale_and_shift_point(x, p2[1], scale, shift)
                    lines.appned((pt[0], pt[1], pt[0], pt[1] + xTickLength))
                dc.DrawLineList(lines)

        if self.ySpec != 'none':
            if ticks.left:
                lines = []
                for y, label in yticks:
                    pt = scale_and_shift_point(p1[0], y, scale, shift)
                    lines.append((pt[0], pt[1], pt[0] + yTickLength, pt[1]))
                dc.DrawLineList(lines)
            if ticks.right:
                lines = []
                for y, label in yticks:
                    pt = scale_and_shift_point(p2[0], y, scale, shift)
                    lines.append((pt[0], pt[1], pt[0] - yTickLength, pt[1]))
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
        pen.SetWidth(penWidth)
        dc.SetPen(pen)

        if self._centerLinesEnabled in ('Horizontal', True):
            y1 = scale[1] * p1[1] + shift[1]
            y2 = scale[1] * p2[1] + shift[1]
            y = (y1 - y2) / 2.0 + y2
            dc.DrawLine(scale[0] * p1[0] + shift[0],
                        y,
                        scale[0] * p2[0] + shift[0],
                        y)
        if self._centerLinesEnabled in ('Vertical', True):
            x1 = scale[0] * p1[0] + shift[0]
            x2 = scale[0] * p2[0] + shift[0]
            x = (x1 - x2) / 2.0 + x2
            dc.DrawLine(x,
                        scale[1] * p1[1] + shift[1],
                        x,
                        scale[1] * p2[1] + shift[1])

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
        pen.SetWidth(penWidth)
        dc.SetPen(pen)

        if self._diagonalsEnabled in ('Bottomleft-Topright', True):
            dc.DrawLine(scale[0] * p1[0] + shift[0],
                        scale[1] * p1[1] + shift[1],
                        scale[0] * p2[0] + shift[0],
                        scale[1] * p2[1] + shift[1])
        if self._diagonalsEnabled in ('Bottomright-Topleft', True):
            dc.DrawLine(scale[0] * p1[0] + shift[0],
                        scale[1] * p2[1] + shift[1],
                        scale[0] * p2[0] + shift[0],
                        scale[1] * p1[1] + shift[1])

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
        pen.SetWidth(penWidth)
        dc.SetPen(pen)

        axes = self.enableAxes
        if self.xSpec != 'none':
            if axes.bottom:
                lower, upper = p1[0], p2[0]
                a1 = scale_and_shift_point(lower, p1[1], scale, shift)
                a2 = scale_and_shift_point(upper, p1[1], scale, shift)
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])
            if axes.top:
                lower, upper = p1[0], p2[0]
                a1 = scale_and_shift_point(lower, p2[1], scale, shift)
                a2 = scale_and_shift_point(upper, p2[1], scale, shift)
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])

        if self.ySpec != 'none':
            if axes.left:
                lower, upper = p1[1], p2[1]
                a1 = scale_and_shift_point(p1[0], lower, scale, shift)
                a2 = scale_and_shift_point(p1[0], upper, scale, shift)
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])
            if axes.right:
                lower, upper = p1[1], p2[1]
                a1 = scale_and_shift_point(p2[0], lower, scale, shift)
                a2 = scale_and_shift_point(p2[0], upper, scale, shift)
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])

    @TempStyle('pen')
    def _drawAxesValues(self, dc, p1, p2, scale, shift, xticks, yticks):
        """
        Draws the axes values

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
                        (pt[0] - w/2, pt[1] + 2 * self._pointSize[1])
                    )
                dc.DrawTextList(labels, coords)

            if axes.top:
                labels = [tick[1] for tick in xticks]
                coords = []
                for x, label in xticks:
                    w, h = dc.GetTextExtent(label)
                    pt = scale_and_shift_point(x, p2[1], scale, shift)
                    coords.append(
                        (pt[0] - w/2, pt[1] - 2 * self._pointSize[1] - h)
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
                        (pt[0] - w - 3 * self._pointSize[0], pt[1] - 0.5 * h)
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
                        (pt[0] + 3 * self._pointSize[0], pt[1] - 0.5 * h)
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
        dc.DrawText(graphics.title, titlePos[0], titlePos[1])

    def _drawAxesLabels(self, dc, graphics, lhsW, rhsW, bottomH, topH,
                        xLabelWH, yLabelWH):
        """
        Draws the axes labels
        """
        # TODO: axes values get big when this is turned off
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabelPos = (
            self.plotbox_origin[0] + lhsW
            + (self.plotbox_size[0] - lhsW - rhsW) / 2. - xLabelWH[0] / 2.,
            self.plotbox_origin[1] - xLabelWH[1]
        )
        dc.DrawText(graphics.xLabel, xLabelPos[0], xLabelPos[1])
        yLabelPos = (
            self.plotbox_origin[0] - 3 * self._pointSize[0],
            self.plotbox_origin[1] - bottomH
            - (self.plotbox_size[1] - bottomH - topH) / 2. + yLabelWH[0] / 2.
        )
        if graphics.yLabel:  # bug fix for Linux
            dc.DrawRotatedText(
                graphics.yLabel, yLabelPos[0], yLabelPos[1], 90)

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

            self.sb_hor.SetScrollbar(pos, pagesize, sbfullrange, pagesize)
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
            self.sb_vert.SetScrollbar(pos, pagesize, sbfullrange, pagesize)
            self._sb_yunit = unit
            needScrollbars = needScrollbars or (pagesize != sbfullrange)
        else:
            self.sb_vert.SetScrollbar(0, 1000, 1000, 1000)

        self.SetShowScrollbars(needScrollbars)
        self._adjustingSB = False

#-------------------------------------------------------------------------
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



