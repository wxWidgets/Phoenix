# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0330, C0103
#   E1101: Module X has no Y member
#   C0330: Wrong continued indentation
#   C0103: Invalid attribute/variable/method name
#
#-----------------------------------------------------------------------------
# Name:        wx.lib.plot.py
# Purpose:     Line, Bar and Scatter Graphs
#
# Author:      Gordon Williams
#
# Created:     2003/11/03
# Copyright:   (c) 2002
# Licence:     Use as you wish.
# Tags:        phoenix-port
#-----------------------------------------------------------------------------
# 12/15/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 compatability update.
# o Renamed to plot.py in the wx.lib directory.
# o Reworked test frame to work with wx demo framework. This saves a bit
#   of tedious cut and paste, and the test app is excellent.
#
# 12/18/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o wxScrolledMessageDialog -> ScrolledMessageDialog
#
# Oct 6, 2004  Gordon Williams (g_will@cyberus.ca)
#   - Added bar graph demo
#   - Modified line end shape from round to square.
#   - Removed FloatDCWrapper for conversion to ints and ints in arguments
#
# Oct 15, 2004  Gordon Williams (g_will@cyberus.ca)
#   - Imported modules given leading underscore to name.
#   - Added Cursor Line Tracking and User Point Labels.
#   - Demo for Cursor Line Tracking and Point Labels.
#   - Size of plot preview frame adjusted to show page better.
#   - Added helper functions PositionUserToScreen and PositionScreenToUser
#     in PlotCanvas.
#   - Added functions GetClosestPoints (all curves) and GetClosestPoint (only
#     closest curve) can be in either user coords or screen coords.
#
# Jun 22, 2009  Florian Hoech (florian.hoech@gmx.de)
#   - Fixed exception when drawing empty plots on Mac OS X
#   - Fixed exception when trying to draw point labels on Mac OS X (Mac OS X
#     point label drawing code is still slow and only supports wx.COPY)
#   - Moved label positions away from axis lines a bit
#   - Added PolySpline class and modified demo 1 and 2 to use it
#   - Added center and diagonal lines option (Set/GetEnableCenterLines,
#     Set/GetEnableDiagonals)
#   - Added anti-aliasing option with optional high-resolution mode
#     (Set/GetEnableAntiAliasing, Set/GetEnableHiRes) and demo
#   - Added option to specify exact number of tick marks to use for each axis
#     (SetXSpec(<number>, SetYSpec(<number>) -- work like 'min', but with
#     <number> tick marks)
#   - Added support for background and foreground colours (enabled via
#     SetBackgroundColour/SetForegroundColour on a PlotCanvas instance)
#   - Changed PlotCanvas printing initialization from occuring in __init__ to
#     occur on access. This will postpone any IPP and / or CUPS warnings
#     which appear on stderr on some Linux systems until printing
#     functionality is actually used.
#
# Aug 20, 2015  Douglas Thor (doug.thor@gmail.com)
#   - Implemented a drawstyle option to PolyLine that mimics matplotlib's
#     Line2dD.drawstyle option.
#   - Added significant customization options to PlotCanvas
#     - Gridlines, Axes, Centerline, diagonal, and ticks can now have
#       their Pen (color, width, and linestyle) set independently.
#     - Ticks, Axes, and AxesValues can now be turned on/off for each side.
#   - Added properties to replace getters/setters.
#   - All getters and setters now have deprecation warnings
#   - Fixed python3 FutureWarning for instances of 'x == None' (replaced with
#     'x is None')
#   - TODO: Fix printer scaling.
#   - Documentation updates
#   - Added Box Plot
#   - Added contect manager and decorator that gets and resets the pen before
#     and after a function call
#   - updated demo for new features
#
# May 27, 2016  Douglas Thor (doug.thor@gmail.com)
#   - Added PolyBars and PolyHistogram classes
#   - General Cleanup
#   - Added demos for PolyBars and PolyHistogram
#   - updated plotNN menu items status-bar text to be descriptive.
#   - increased default size of demo
#   - updated XSpec and YSpec to accept a list or tuple of (min, max) values.
#
# Jun 14, 2016 (Start)  Douglas Thor (doug.thor@gmail.com)
#   -

"""
This is a simple light weight plotting module that can be used with
Boa or easily integrated into your own wxPython application.  The
emphasis is on small size and fast plotting for large data sets.  It
has a reasonable number of features to do line and scatter graphs
easily as well as simple bar graphs.  It is not as sophisticated or
as powerful as SciPy Plt or Chaco.  Both of these are great packages
but consume huge amounts of computer resources for simple plots.
They can be found at http://scipy.com

This file contains two parts; first the re-usable library stuff, then,
after a ``if __name__ == '__main__'`` test, a simple frame and a few default
plots for examples and testing.

Based on wxPlotCanvas
Written by K.Hinsen, R. Srinivasan;
Ported to wxPython Harm van der Heijden, feb 1999

Major Additions Gordon Williams Feb. 2003 (g_will@cyberus.ca)

- More style options
- Zooming using mouse "rubber band"
- Scroll left, right
- Grid(graticule)
- Printing, preview, and page set up (margins)
- Axis and title labels
- Cursor xy axis values
- Doc strings and lots of comments
- Optimizations for large number of points
- Legends

Did a lot of work here to speed markers up. Only a factor of 4
improvement though. Lines are much faster than markers, especially
filled markers.  Stay away from circles and triangles unless you
only have a few thousand points.

+-----------------------------------+
| Times for 25,000 points           |
+===================================+
| Line                    | 0.078 s |
+-------------------------+---------+
| Markers                           |
+-------------------------+---------+
| Square                  | 0.22 s  |
+-------------------------+---------+
| dot                     | 0.10    |
+-------------------------+---------+
| circle                  | 0.87    |
+-------------------------+---------+
| cross, plus             | 0.28    |
+-------------------------+---------+
| triangle, triangle_down | 0.90    |
+-------------------------+---------+

Thanks to Chris Barker for getting this version working on Linux.

Zooming controls with mouse (when enabled):
    Left mouse drag - Zoom box.
    Left mouse double click - reset zoom.
    Right mouse click - zoom out centred on click location.


Major Addtions - Douglas Thor, August 2015 (doug.thor@gmail.com)

- Most items are now allow custom pens (color, width, linestyle)
- Added 'drawstyle' option to PolyLine that mimics MatPlotLib's
  Line2dD.drawstyle option.
- Added properties to replace getters/setters.
- All getters and setters now have deprecation warnings
- Fixed python3 FutureWarning for instances of 'x == None' (replaced with
  'x is None')
- Documentation updates
- Added Box Plot
- Added contect manager and decorator that gets and resets the pen before
  and after a function call
- updated demo for new features
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

    **Note: Can only be used on class methods.**

    Parameters:
    -----------
    which : {'both', 'pen', 'brush'}
        The item to save and revert after execution.
    dc : wx.DC object
        The DC to pull brush/pen information from.

    Usage:
    ------
    As a method decorator::

        @TempStyle()                        # same as @TempStyle('both')
        def func(self, dc, a, b, c):        # dc must be 1st arg (beside self)
            # edit pen and brush here

    As a context manager::

        with TempStyle('both', dc):
            # do stuff

    Notes:
    ------
    As of 2016-06-15, this can only be used as a decorator for **class
    methods**, not standard functions. There is a plan to try and remove
    this restriction, but I don't know when that will happen...

    Combination Decorator and Context Manager! Also makes Julienne fries!
    Will not break! Will not... It broke!
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


class SavePen(object):
    """
    Decorator which saves the dc Pen before calling a function and sets the
    pen back after the funcion, even if the function raises an exception.

    The DC to paint on **must** be the first argument of the function.

    Usage:
    -------
    ::

        @SavePen
        def func(dc, a, b, c):
            # edit pen here

    is the same as::

        def func(dc, a, b, c):
            prevPen = dc.GetPen()
            # edit pen here
            dc.SetPen(prevPen)

    See Also:
    ---------
    SaveBrush : Decorator to save a wx.Brush before calling a function.

    """
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        """
        This provides support for functions
        """
        dc = args[0]
        with SavedPen(dc):
            return self.func(*args, **kwargs)

    def __get__(self, obj, objtype):
        """
        And this provides support for instance methods
        """
        @functools.wraps(self.func)
        def wrapper(*args, **kwargs):
            dc = args[0]
            with SavedPen(dc):
                return self.func(obj, *args, **kwargs)
        return wrapper


class SavedPen(object):
    """
    Context Manager for saving the previous wx.Pen and resetting it after.

    Usage:
    ------

    ::

        with SavedPen(dc):
            # do stuff

    """
    def __init__(self, dc):
        self.dc = dc
        self.prevPen = None

    def __enter__(self):
        """ Save the pen """
        self.prevPen = self.dc.GetPen()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Set the pen back, even if the function errored """
        self.dc.SetPen(self.prevPen)
        return False            # return True means execptions are suppressed


class SaveBrush(object):
    """
    Decorator which saves the dc Brush before calling a function and sets the
    Brush back after the funcion, even if the function raises an exception.

    The DC to paint on **must** be the first argument of the function.

    Usage:
    -------
    ::

        @SaveBrush
        def func(dc, a, b, c):
            # edit Brush here

    is the same as::

        def func(dc, a, b, c):
            prevBrush = dc.GetBrush()
            # edit Brush here
            dc.SetBrush(prevBrush)

    See Also:
    ---------
    SavePen : Decorator to save a wx.Pen before calling a function.

    """
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        """
        This provides support for functions
        """
        dc = args[0]
        with SavedBrush(dc):
            return self.func(*args, **kwargs)

    def __get__(self, obj, objtype):
        """
        And this provides support for instance methods
        """
        @functools.wraps(self.func)
        def wrapper(*args, **kwargs):
            dc = args[0]
            with SavedBrush(dc):
                return self.func(obj, *args, **kwargs)
        return wrapper


class SavedBrush(object):
    """
    Context Manager for saving the previous wx.Pen and resetting it after.

    Usage:
    ------

    ::

        with SavedBrush(dc):
            # do stuff

    """
    def __init__(self, dc):
        self.dc = dc
        self.prevBrush = None

    def __enter__(self):
        """ Save the Brush """
        self.prevBrush = self.dc.GetBrush()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Set the Brush back, even if the function errored """
        self.dc.SetBrush(self.prevBrush)
        return False            # return True means execptions are suppressed



class PendingDeprecation(object):
    """
    Decorator which warns the developer about methods that are
    pending deprecation.

    Usage:
    ------

    ::

        @PendingDeprecation("new_func")
        def old_func():
            pass

    prints the warning::

        `old_func` is pending deprecation. Please use new_func instead.

    """
    _warn_txt = "`{}` is pending deprecation. Please use `{}` instead."

    def __init__(self, new_func):
        self.new_func = new_func

    def __call__(self, func):
        """Support for functions"""
        self.func = func
        self._update_docs()

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

    Parameters:
    -----------
    bottom, left, top, right : bool
        Boolean values for a given side's display value.

    """
    # TODO: Do I want to replace with __slots__?
    #       Not much memory gain because this class is only called a small
    #       number of times, but it would remove the need for part of
    #       __setattr__...
    valid_names = ("bottom", "left", "right", "top")

    def __init__(self, bottom, left, top, right):
        # make sure that everything is boolean
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
    def LogScale(self):
        return self._logscale

    @LogScale.setter
    def LogScale(self, logscale):
        """
        Set to change the axes to plot Log10(values)

        Value must be a tuple of booleans (x_axis_bool, y_axis_bool)
        """
        if not isinstance(logscale, tuple) or len(logscale) != 2:
            raise ValueError("`logscale` must be a 2-tuple of bools")
        self._logscale = logscale

    @PendingDeprecation("self.LogScale property")
    def setLogScale(self, logscale):
        """
        Set to change the axes to plot Log10(values)

        Value must be a tuple of booleans (x_axis_bool, y_axis_bool)
        """
        self._logscale = logscale

    @property
    def SymLogScale(self):
        return self._symlogscale

    # TODO: Implement symmetric log scale
    @SymLogScale.setter
    def SymLogScale(self, symlogscale):
        """
        # Not implemented yet


        Set to change the axes to a symmetric log10 scale.

        Value must be a 2-tuple of booleans (x_axis_bool, y_axis_bool)

        A Symmetric Log scale uses the following properties:
        if x > 0:
            x = Log10(x)
        elif x < 0:
            x = -Log10(Abs(x))
        """
        raise NotImplementedError("Symmetric Log Scale not yet implemented")

        if not isinstance(symlogscale, tuple) or len(symlogscale) != 2:
            raise ValueError("`symlogscale` must be a 2-tuple of bools")
        self._symlogscale = symlogscale

    @property
    def AbsScale(self):
        return self._absScale

    @AbsScale.setter
    def AbsScale(self, absscale):
        """
        Set to change the axes to plot Abs(values)

        Value must be a tuple of booleans (x_axis_bool, y_axis_bool)
        """
        if not isinstance(absscale, tuple) and len(absscale) == 2:
            raise ValueError("`absscale` must be a 2-tuple of bools")
        self._absScale = absscale

    @property
    def points(self):
        """Returns the points, adjusting for log scale if LogScale is set"""
        data = np.array(self._points, copy=True)    # need the copy
                                                    # TODO: get rid of the
                                                    # need for copy

        # work on X:
        if self.AbsScale[0]:
            data = self._abs(data, 0)
        if self.LogScale[0]:
            data = self._log10(data, 0)

        if self.SymLogScale[0]:
            # TODO: implement SymLogScale
            # Should SymLogScale override AbsScale? My vote is no.
            # Should SymLogScale override LogScale? My vote is yes.
            #   - SymLogScale could be a parameter passed to LogScale...
            pass

        # work on Y:
        if self.AbsScale[1]:
            data = self._abs(data, 1)
        if self.LogScale[1]:
            data = self._log10(data, 1)

        if self.SymLogScale[1]:
            # TODO: implement SymLogScale
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

        Parameters:
        -----------
        None

        Returns:
        --------
        minXY, maxXY : numpy arrays of length 2
            The minimum and maximum X and Y values.

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

        Parameters:
        -----------
        scale : tuple of floats
            The (x_scale, y_scale) tuple to scale the data by

        shift : tuple of floats
            The (x_shift, y_shift) tuple to shift the data by.

        Returns:
        --------
        None

        """
        if len(self.points) == 0:
            # no curves to draw
            return
        if scale is not self.currentScale or shift is not self.currentShift:
            # XXX: why "is not" and not "!="?
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
    Class to define line type and style

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
        """
        Creates PolyLine object

        :param `points`: sequence (array, tuple or list) of (x,y) points
                         making up line
        :keyword `attr`: keyword attributes, default to:

         ==========================  ================================
         'colour'= 'black'           wx.Pen Colour any wx.Colour
         'width'= 1                  Pen width
         'style'= wx.PENSTYLE_SOLID  wx.Pen style
         'legend'= ''                Line Legend to display
         'drawstyle'= 'line'         How points are joined.
         ==========================  ================================

        Valid 'drawstyle' values are:

            'line'          Draws an straight line between consecutive points
            'steps-pre'     Draws a line down from point A and then right to
                            point B
            'steps-post'    Draws a line right from point A and then down
                            to point B
            'steps-mid-x'   Draws a line right to half way between A and B,
                            then draws a line vertically, then again right
                            to point B.
            'steps-mid-y'   Draws a line vertically to half way between A
                            and B, then draws a line horizonatally, then
                            again vertically to point B.
                            *Note: This typically does not look very good*

        """
        PolyPoints.__init__(self, points, attr)

    def draw(self, dc, printerScale, coord=None):
        """ Draw the lines """
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
                    self.path(dc, c1, c2, drawstyle)
        else:
            dc.DrawLines(coord)  # draw legend line

    def getSymExtent(self, printerScale):
        """Width and Height of Marker"""
        h = self.attributes['width'] * printerScale * self._pointSize[0]
        w = 5 * h
        return (w, h)

    def path(self, dc, coord1, coord2, drawstyle):
        """ calculates the path from coord1 to coord 2 along X and Y """
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
    Class to define line type and style.

    All methods except ``__init__`` are private.
    """

    _attributes = {'colour': 'black',
                   'width': 1,
                   'style': wx.PENSTYLE_SOLID,
                   'legend': ''}

    def __init__(self, points, **attr):
        """
        Creates PolyLine object

        :param `points`: sequence (array, tuple or list) of (x,y) points
                         making up spline
        :keyword `attr`: keyword attributes, default to:

         ==========================  ================================
         'colour'= 'black'           wx.Pen Colour any wx.Colour
         'width'= 1                  Pen width
         'style'= wx.PENSTYLE_SOLID  wx.Pen style
         'legend'= ''                Line Legend to display
         ==========================  ================================

        """
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
    Class to define marker type and style

    All methods except __init__ are private.
    """
    _attributes = {'colour': 'black',
                   'width': 1,
                   'size': 2,
                   'fillcolour': None,
                   'fillstyle': wx.BRUSHSTYLE_SOLID,
                   'marker': 'circle',
                   'legend': ''}

    def __init__(self, points, **attr):
        """
        Creates PolyMarker object

        :param `points`: sequence (array, tuple or list) of (x,y) points
        :keyword `attr`: keyword attributes, default to:

         ================================ ================================
         'colour'= 'black'                wx.Pen Colour any wx.Colour
         'width'= 1                       Pen width
         'size'= 2                        Marker size
         'fillcolour'= same as colour     wx.Brush Colour any wx.Colour
         'fillstyle'= wx.BRUSHSTYLE_SOLID wx.Brush fill style (use
                                          wx.BRUSHSTYLE_TRANSPARENT for
                                          no fill)
         'style'= wx.FONTFAMILY_SOLID     wx.Pen style
         'marker'= 'circle'               Marker shape
         'legend'= ''                     Line Legend to display
         ================================ ================================

         Marker Shapes:
         - 'circle'
         - 'dot'
         - 'square'
         - 'triangle'
         - 'triangle_down'
         - 'cross'
         - 'plus'
        """

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
        f = eval('self._' + marker)     # XXX: look into changing this
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
    Bar Chart.
    """
    def __init__(self, points, **attr):
        """
        Creates PolyBars object

        :param `points`: sequence (array, tuple or list) of (x, y) points
                         that define the bar.
                         x: the centerline of the bar.
                         y: the value of the bar (from y=0)
        :keyword `attr`: keyword attributes, default to:

         =================================  ================================
         'edgecolour' = 'black'             wx.Pen Colour: any wx.Colour
         'edgewidth' = 1                    wx.Pen width
         'edgestyle' = wx.PENSTYLE_SOLID    wx.Pen style
         'legend' = ''                      Line Legend to display
         'fillcolour' = 'red'               wx.Brush fill color: any wx.Colour
         'fillstyle' = wx.BRUSHSTYLE_SOLID  The fill style for the rectangle
         'barwidth' = 1.0                   The bar width. If a list of
                                            values, len(barwidth) must
                                            equal len(points).
         =================================  ================================
        """
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
    Histogram

    Special PolyBarsBase where the bars span the binspec.
    """
    def __init__(self, hist, binspec, **attr):
        """
        Creates PolyHistogram object

        :param `hist`: sequence (array, tuple or list) of y values
                       that define the heights of the bars (same as 1st
                       returned parameter from ``np.histogram(data)``).
        :param `binspec`: sequence of x values that define the edges of the
                          bins (same as 2nd returned parameter from
                          ``np.histogram(data)``).
                          len(binspec) must equal len(hist) + 1
        :keyword `attr`: keyword attributes, default to:

         =================================  ================================
         'edgecolour' = 'black'             wx.Pen Colour: any wx.Colour
         'edgewidth' = 3                    wx.Pen width
         'edgestyle' = wx.PENSTYLE_SOLID    wx.Pen style
         'legend' = ''                      Line Legend to display
         'fillcolour' = 'blue'              wx.Brush fill color: any wx.Colour
         'fillstyle' = wx.BRUSHSTYLE_SOLID  The fill style for the rectangle
         =================================  ================================

        """
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
    Class to contain box plots

    This class takes care of calculating the box plots.

    TODO:
    -----
    + [x] Separate out each draw into individual methods
    + [x] Fix the median line extending outside of the box on the right
    + [x] Allow for multiple box plots side-by-side
          - It's a hack, but it works.
    + [ ] change the X axis to some labels.
    + [x] Add getLegend method
          - Not Needed since we inherit from PolyPoints
    + [x] Add getClosestPoint method - links to box plot or outliers
          - Current method works and hits every point. Is that good enough?
    + [ ] Add customization
          - [ ] Pens and Fills for elements
          - [ ] outlier shapes(?) and sizes
          - [ ] box width
    + [ ] Get log-y working

    """
    _attributes = {'colour': 'black',
                   'width': 1,
                   'style': wx.PENSTYLE_SOLID,
                   'legend': '',
                   'drawstyle': 'line',
                   'size': 5,
                   }

    def __init__(self, points, **attr):
        """
        :param data: 1D data to plot.

        """
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

        Notes:
        ------
        # TODO: Verify how NaN is handled then decide how I want to handle it.

        """
        if data is None:
            data = self.points

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
        if data is None:
            data = self.points

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
        xpos = self.xpos

        # Set the pen
        outlier_pen = wx.Pen(wx.BLUE, 5, wx.PENSTYLE_SOLID)
        dc.SetPen(outlier_pen)

        outliers = self._outliers


#        jitter = 0.05 * np.random.random_sample(len(outliers)) + xpos - 0.025

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
    Container to hold PolyXXX objects and graph labels

    All methods except __init__ are private.
    """

    def __init__(self, objects, title='', xLabel='', yLabel=''):
        """Creates PlotGraphics object
        objects - list of PolyXXX objects to make graph
        title - title shown at top of graph
        xLabel - label shown on x-axis
        yLabel - label shown on y-axis
        """
        if type(objects) not in [list, tuple]:
            raise TypeError("objects argument should be list or tuple")
        self.objects = objects
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self._pointSize = (1.0, 1.0)

    @property
    def LogScale(self):
        # TODO: convert to try..except statement
#        try:
#        return [obj.LogScale for obj in self.objects]
#        except:     # what error would be returned?
#            return
        if len(self.objects) == 0:
            return
        return [obj.LogScale for obj in self.objects]

    @LogScale.setter
    def LogScale(self, logscale):
        # XXX: error checking done by PolyPoints class
#        if not isinstance(logscale, tuple) and len(logscale) != 2:
#            raise TypeError("logscale must be a 2-tuple of bools")
        if len(self.objects) == 0:
            return
        for obj in self.objects:
            obj.LogScale = logscale

    @PendingDeprecation("self.LogScale property")
    def setLogScale(self, logscale):
        self.LogScale = logscale

    @property
    def AbsScale(self):
        if len(self.objects) == 0:
            return
        return [obj.AbsScale for obj in self.objects]

    @AbsScale.setter
    def AbsScale(self, absscale):
        # XXX: error checking done by PolyPoints class
#        if not isinstance(absscale, tuple) and len(absscale) != 2:
#            raise TypeError("absscale must be a 2-tuple of bools")
        if len(self.objects) == 0:
            return
        for obj in self.objects:
            obj.AbsScale = absscale

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

    @PendingDeprecation("self.PrinterScale property")
    def setPrinterScale(self, scale):
        """Thickens up lines and markers only for printing"""
        self.PrinterScale = scale

    @PendingDeprecation("self.XLabel property")
    def setXLabel(self, xLabel=''):
        """Set the X axis label on the graph"""
        self.XLabel = xLabel

    @PendingDeprecation("self.YLabel property")
    def setYLabel(self, yLabel=''):
        """Set the Y axis label on the graph"""
        self.YLabel = yLabel

    @PendingDeprecation("self.Title property")
    def setTitle(self, title=''):
        """Set the title at the top of graph"""
        self.Title = title

    @PendingDeprecation("self.XLabel property")
    def getXLabel(self):
        """Get x axis label string"""
        return self.XLabel

    @PendingDeprecation("self.YLabel property")
    def getYLabel(self):
        """Get y axis label string"""
        return self.YLabel

    @PendingDeprecation("self.Title property")
    def getTitle(self, title=''):
        """Get the title at the top of graph"""
        return self.Title

    @property
    def PrinterScale(self):
        return self._printerScale

    @PrinterScale.setter
    def PrinterScale(self, scale):
        """Thickens up lines and markers only for printing"""
        self._printerScale = scale

    @property
    def XLabel(self):
        """Get the X axis label on the graph"""
        return self.xLabel

    @XLabel.setter
    def XLabel(self, text):
        self.xLabel = text

    @property
    def YLabel(self):
        """Get the Y axis label on the graph"""
        return self.yLabel

    @YLabel.setter
    def YLabel(self, text):
        self.yLabel = text

    @property
    def Title(self):
        """Get the title at the top of graph"""
        return self.title

    @Title.setter
    def Title(self, text):
        self.title = text

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


#-------------------------------------------------------------------------
# Main window that you will want to import into your application.

class PlotCanvas(wx.Panel):
    """
    Subclass of a wx.Panel which holds two scrollbars and the actual
    plotting canvas (self.canvas). It allows for simple general plotting
    of data with zoom, labels, and automatic axis scaling.

    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name="plotCanvas"):
        """Constructs a panel, which can be a child of a frame or
        any other non-control window"""

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
        self.canvas.SetCursor(wx.CROSS_CURSOR)
        self.HandCursor = wx.Cursor(Hand.GetImage())
        self.GrabHandCursor = wx.Cursor(GrabHand.GetImage())
        self.MagCursor = wx.Cursor(MagPlus.GetImage())

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
    def GridPen(self):
        """Gets the grid's wx.Pen"""
        return self._gridPen

    @GridPen.setter
    def GridPen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._gridPen = pen

    @property
    def DiagonalPen(self):
        """Gets the diagonal wx.Pen"""
        return self._diagonalPen

    @DiagonalPen.setter
    def DiagonalPen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._diagonalPen = pen

    @property
    def CenterLinePen(self):
        """Gets the CenterLine wx.Pen"""
        return self._centerLinePen

    @CenterLinePen.setter
    def CenterLinePen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._centerLinePen = pen

    @property
    def AxesPen(self):
        """Gets the axes wx.Pen"""
        return self._axesPen

    @AxesPen.setter
    def AxesPen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._axesPen = pen

    @property
    def TickPen(self):
        """Gets the tick mark wx.Pen"""
        return self._tickPen

    @TickPen.setter
    def TickPen(self, pen):
        if not isinstance(pen, wx.Pen):
            raise TypeError("pen must be an instance of wx.Pen")
        self._tickPen = pen

    @property
    def TickLength(self):
        """Returns the tick length."""
        return self._tickLength

    @TickLength.setter
    def TickLength(self, length):
        """Set the tick legnth. Value must be int or float."""
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

    @PendingDeprecation("self.LogScale property")
    def setLogScale(self, logscale):
        self.LogScale = logscale

    @PendingDeprecation("self.LogScale property")
    def getLogScale(self):
        return self.LogScale

    @property
    def LogScale(self):
        return self._logscale

    @LogScale.setter
    def LogScale(self, logscale):
        if type(logscale) != tuple:
            raise TypeError(
                'logscale must be a tuple of bools, e.g. (False, False)')
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            graphics.LogScale = logscale
            self.last_draw = (graphics, None, None)
        self.XSpec = 'min'
        self.YSpec = 'min'
        self._logscale = logscale

    @property
    def AbsScale(self):
        return self._absScale

    @AbsScale.setter
    def AbsScale(self, absscale):
        if not isinstance(absscale, tuple):
            raise TypeError("absscale must be tuple of bools.")
        if self.last_draw is not None:
            graphics, xAxis, yAxis = self.last_draw
            graphics.AbsScale = absscale
            self.last_draw = (graphics, None, None)
        self.XSpec = 'min'
        self.YSpec = 'min'
        self._absScale = absscale

    @PendingDeprecation("self.FontSizeAxis property")
    def SetFontSizeAxis(self, point=10):
        """Set the tick and axis label font size (default is 10 point)"""
        self.FontSizeAxis = point

    @PendingDeprecation("self.FontSizeAxis property")
    def GetFontSizeAxis(self):
        """Get current tick and axis label font size in points"""
        return self.FontSizeAxis

    @property
    def FontSizeAxis(self):
        """Get current tick and axis label font size in points"""
        return self._fontSizeAxis

    @FontSizeAxis.setter
    def FontSizeAxis(self, value):
        """Set the tick and axis label font size (default is 10 point)"""
        self._fontSizeAxis = value

    @PendingDeprecation("self.FontSizeTitle property")
    def SetFontSizeTitle(self, point=15):
        """Set Title font size (default is 15 point)"""
#        self._fontSizeTitle = point
        self.FontSizeTitle = point

    @PendingDeprecation("self.FontSizeTitle property")
    def GetFontSizeTitle(self):
        """Get current Title font size in points"""
#        return self._fontSizeTitle
        return self.FontSizeTitle

    @property
    def FontSizeTitle(self):
        """Get current Title font size in points"""
        return self._fontSizeTitle

    @FontSizeTitle.setter
    def FontSizeTitle(self, pointsize):
        """Set Title font size (default is 15 point)"""
        self._fontSizeTitle = pointsize

    @PendingDeprecation("self.FontSizeLegend property")
    def SetFontSizeLegend(self, point=7):
        """Set Legend font size (default is 7 point)"""
        self.FontSizeLegend = point

    def GetFontSizeLegend(self):
        """Get current Legend font size in points"""
        return self.FontSizeLegend

    @property
    def FontSizeLegend(self):
        return self._fontSizeLegend

    @FontSizeLegend.setter
    def FontSizeLegend(self, point):
        self._fontSizeLegend = point

    @PendingDeprecation("self.ShowScrollbars property")
    def SetShowScrollbars(self, value):
        self.ShowScrollbars = value

    @PendingDeprecation("self.ShowScrollbars property")
    def GetShowScrollbars(self):
        """Set True to show scrollbars"""
        return self.ShowScrollbars

    @property
    def ShowScrollbars(self):
        return self.sb_vert.IsShown()

    @ShowScrollbars.setter
    def ShowScrollbars(self, value):
        """Set True to show scrollbars"""
        if not isinstance(value, bool):
            raise TypeError("Value should be True or False")
        if value == self.ShowScrollbars:
            # no change, so don't do anything
            return
        self.sb_vert.Show(value)
        self.sb_hor.Show(value)
        wx.CallAfter(self.Layout)

    @PendingDeprecation("self.UseScientificNotation property")
    def SetUseScientificNotation(self, useScientificNotation):
        self.UseScientificNotation = useScientificNotation

    @PendingDeprecation("self.UseScientificNotation property")
    def GetUseScientificNotation(self):
        return self.UseScientificNotation

    @property
    def UseScientificNotation(self):
        return self._useScientificNotation

    @UseScientificNotation.setter
    def UseScientificNotation(self, value):
        self._useScientificNotation = value

    @PendingDeprecation("self.EnableAntiAliasing property")
    def SetEnableAntiAliasing(self, enableAntiAliasing):
        self.EnableAntiAliasing = enableAntiAliasing

    @PendingDeprecation("self.EnableAntiAliasing property")
    def GetEnableAntiAliasing(self):
        return self.EnableAntiAliasing

    @property
    def EnableAntiAliasing(self):
        return self._antiAliasingEnabled

    @EnableAntiAliasing.setter
    def EnableAntiAliasing(self, value):
        """Set True to enable anti-aliasing."""
        self._antiAliasingEnabled = value
        self.Redraw()

    @PendingDeprecation("self.EnableHiRes property")
    def SetEnableHiRes(self, enableHiRes):
        self.EnableHiRes = enableHiRes

    @PendingDeprecation("self.EnableHiRes property")
    def GetEnableHiRes(self):
        return self._hiResEnabled

    @property
    def EnableHiRes(self):
        return self._hiResEnabled

    @EnableHiRes.setter
    def EnableHiRes(self, value):
        """
        Set True to enable high-resolution mode when using anti-aliasing.
        """
        self._hiResEnabled = value
        self.Redraw()

    @PendingDeprecation("self.EnableDrag property")
    def SetEnableDrag(self, value):
        self.EnableDrag = value

    @PendingDeprecation("self.EnableDrag property")
    def GetEnableDrag(self):
        return self.EnableDrag

    @property
    def EnableDrag(self):
        return self._dragEnabled

    @EnableDrag.setter
    def EnableDrag(self, value):
        """Set True to enable drag."""
        if not isinstance(value, bool):
            raise TypeError("Value must be a bool.")
        if value:
            if self.EnableZoom:
                self.EnableZoom = False
            self.SetCursor(self.HandCursor)
        else:
            self.SetCursor(wx.CROSS_CURSOR)
        self._dragEnabled = value

    @PendingDeprecation("self.EnableZoom property")
    def SetEnableZoom(self, value):
        self.EnableZoom = value

    @PendingDeprecation("self.EnableZoom property")
    def GetEnableZoom(self):
        """True if zooming enabled."""
        return self.EnableZoom

    @property
    def EnableZoom(self):
        return self._zoomEnabled

    @EnableZoom.setter
    def EnableZoom(self, value):
        """Set True to enable zooming."""
        if not isinstance(value, bool):
            raise TypeError("Value must be a bool.")
        if value:
            if self.EnableDrag:
                self.EnableDrag = False
            self.SetCursor(self.MagCursor)
        else:
            self.SetCursor(wx.CROSS_CURSOR)
        self._zoomEnabled = value

    @PendingDeprecation("self.EnableGrid property")
    def SetEnableGrid(self, value):
        self.EnableGrid = value

    @PendingDeprecation("self.EnableGrid property")
    def GetEnableGrid(self):
        """True if grid enabled."""
        return self.EnableGrid

    @property
    def EnableGrid(self):
        return self._gridEnabled

    @EnableGrid.setter
    def EnableGrid(self, value):
        """
        Set to enable grid.

        value must be a bool or 2-tuple of bools: (x_grid_bool, y_grid_bool)

        If Value is a bool, then both X and Y grids are turned on/off

        x_grid_bool: Tf True, gridlines in the vertical direction are shown.
        y_grid_bool: If True, gridlines in the horizontal direction are shown.
        """
        if isinstance(value, bool):
            value = (value, value)
        elif isinstance(value, tuple) and len(value) == 2:
            pass
        else:
            err_txt = "Value must be a bool or 2-tuple of bool."
            raise TypeError(err_txt)

        self._gridEnabled = value
        self.Redraw()

    @PendingDeprecation("self.EnableCenterLines property")
    def SetEnableCenterLines(self, value):
        self.EnableCenterLines = value

    @PendingDeprecation("self.EnableCenterLines property")
    def GetEnableCenterLines(self):
        """True if Centerlines are enabled."""
        return self.EnableCenterLines

    @property
    def EnableCenterLines(self):
        return self._centerLinesEnabled

    @EnableCenterLines.setter
    def EnableCenterLines(self, value):
        """Set True, 'Horizontal' or 'Vertical' to enable center line(s)."""
        if value not in [True, False, 'Horizontal', 'Vertical']:
            raise TypeError(
                "Value should be True, False, Horizontal or Vertical")
        self._centerLinesEnabled = value
        self.Redraw()

    @PendingDeprecation("self.EnableDiagonals property")
    def SetEnableDiagonals(self, value):
        self.EnableDiagonals = value

    @PendingDeprecation("self.EnableDiagonals property")
    def GetEnableDiagonals(self):
        """True if Diagonals enabled."""
        return self.EnableDiagonals

    @property
    def EnableDiagonals(self):
        return self._diagonalsEnabled

    @EnableDiagonals.setter
    def EnableDiagonals(self, value):
        """Set True, 'Bottomleft-Topright' or 'Bottomright-Topleft' to enable
        center line(s)."""
        # TODO: Rename Bottomleft-TopRight, Bottomright-Topleft
        if value not in [True, False,
                         'Bottomleft-Topright', 'Bottomright-Topleft']:
            raise TypeError(
                "Value should be True, False, Bottomleft-Topright or "
                "Bottomright-Topleft"
            )
        self._diagonalsEnabled = value
        self.Redraw()

    @PendingDeprecation("self.EnableLegend property")
    def SetEnableLegend(self, value):
        self.EnableLegend = value

    @PendingDeprecation("self.EnableLegend property")
    def GetEnableLegend(self):
        """True if Legend enabled."""
        return self.EnableLegend

    @property
    def EnableLegend(self):
        return self._legendEnabled

    @EnableLegend.setter
    def EnableLegend(self, value):
        """Set True to enable legend."""
        if value not in [True, False]:
            raise TypeError("Value should be True or False")
        self._legendEnabled = value
        self.Redraw()

    @PendingDeprecation("self.EnableTitle property")
    def SetEnableTitle(self, value):
        self.EnableTitle = value

    @PendingDeprecation("self.EnableTitle property")
    def GetEnableTitle(self):
        """True if title enabled."""
        return self.EnableTitle

    @property
    def EnableTitle(self):
        return self._titleEnabled

    @EnableTitle.setter
    def EnableTitle(self, value):
        """Set True to enable title."""
        if not isinstance(value, bool):
            raise TypeError("Value must be a bool.")
        self._titleEnabled = value
        self.Redraw()

    @PendingDeprecation("self.EnablePointLabel property")
    def SetEnablePointLabel(self, value):
        self.EnablePointLabel = value

    @PendingDeprecation("self.EnablePointLabel property")
    def GetEnablePointLabel(self):
        """True if pointLabel enabled."""
        return self.EnablePointLabel

    @property
    def EnablePointLabel(self):
        return self._pointLabelEnabled

    @EnablePointLabel.setter
    def EnablePointLabel(self, value):
        """Set True to enable pointLabel."""
        if not isinstance(value, bool):
            raise TypeError("Value must be a bool.")
        self._pointLabelEnabled = value
        self.Redraw()  # will erase existing pointLabel if present
        self.last_PointLabel = None

    @property
    def EnableAxes(self):
        """True if axes enabled."""
        return self._axesEnabled

    @EnableAxes.setter
    def EnableAxes(self, value):
        """Set True to enable axes.

        Acceptable values:
        bool : all axes
        2-tuple of bool : (bottom, left)
        4-tuple of bool : (bottom, left, top, right)

        """
        err_txt = ("Axis value must be a bool or a 2- or 4-tuple of bool")

        # TODO: Refactor - same as EnableAxesValues and EnableTicks
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
            raise ValueError(err_txt)
        self._axesEnabled = _DisplaySide(*_value)
        self.Redraw()

    @property
    def EnableAxesValues(self):
        """True if axes values are enabled."""
        return self._axesValuesEnabled

    @EnableAxesValues.setter
    def EnableAxesValues(self, value):
        """Set True to enable axes values.

        Acceptable values:
        bool : all axes values
        2-tuple of bool : (bottom, left)
        4-tuple of bool : (bottom, left, top, right)

        """
        err_txt = ("value must be a bool or a 2- or 4-tuple of bool")

        # TODO: Refactor - same as EnableAxes and EnableTicks
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
            raise ValueError(err_txt)
        self._axesValuesEnabled = _DisplaySide(*_value)
        self.Redraw()

    @property
    def EnableTicks(self):
        """True if tick marks are enabled."""
        return self._ticksEnabled

    @EnableTicks.setter
    def EnableTicks(self, value):
        """Set True to enable tick marks.

        Acceptable values:
        bool : ticks on all 4 sides
        2-tuple of bool : (bottom, left)
        4-tuple of bool : (bottom, left, top, right)

        """
        err_txt = ("value must be a bool or a 2- or 4-tuple of bool")

        # TODO: Refactor - same as EnableAxes and EnableAxesValues
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
            raise ValueError(err_txt)
        self._ticksEnabled = _DisplaySide(*_value)
        self.Redraw()

    @property
    def EnablePlotTitle(self):
        return self._titleEnabled

    @EnablePlotTitle.setter
    def EnablePlotTitle(self, value):
        if not isinstance(value, bool):
            raise TypeError("`value` must be boolean True or False")
        self._titleEnabled = value
        self.Redraw()

    @property
    def EnableXAxisLabel(self):
        return self._xAxisLabelEnabled

    @EnableXAxisLabel.setter
    def EnableXAxisLabel(self, value):
        if not isinstance(value, bool):
            raise TypeError("`value` must be boolean True or False")
        self._xAxisLabelEnabled = value
        self.Redraw()

    @property
    def EnableYAxisLabel(self):
        return self._yAxisLabelEnabled

    @EnableYAxisLabel.setter
    def EnableYAxisLabel(self, value):
        if not isinstance(value, bool):
            raise TypeError("`value` must be boolean True or False")
        self._yAxisLabelEnabled = value
        self.Redraw()

    @property
    def EnableAxesLabels(self):
        return self._axesLabelsEnabled

    @EnableAxesLabels.setter
    def EnableAxesLabels(self, value):
        if not isinstance(value, bool):
            raise TypeError("`value` must be boolean True or False")
        self._axesLabelsEnabled = value
        self.Redraw()

    @PendingDeprecation("self.PointLabelFunc property")
    def SetPointLabelFunc(self, func):
        """Sets the function with custom code for pointLabel drawing
            ******** more info needed ***************
        """
        self.PointLabelFunc = func

    @PendingDeprecation("self.PointLabelFunc property")
    def GetPointLabelFunc(self):
        """Returns pointLabel Drawing Function"""
        return self.PointLabelFunc

    @property
    def PointLabelFunc(self):
        return self._pointLabelFunc

    @PointLabelFunc.setter
    def PointLabelFunc(self, func):
        """Sets the function with custom code for pointLabel drawing
            ******** more info needed ***************
        """
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
        if self.LogScale[0]:
            x = np.power(10, x)
        if self.LogScale[1]:
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

    @PendingDeprecation("self.XSpec property")
    def SetXSpec(self, spectype='auto'):
        """
        xSpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:

        * 'none' - shows no axis or tick mark values
        * 'min' - shows min bounding box values
        * 'auto' - rounds axis range to sensible values
        * <number> - like 'min', but with <number> tick marks

        """
        self.XSpec = spectype

    @PendingDeprecation("self.YSpec property")
    def SetYSpec(self, spectype='auto'):
        """
        ySpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:

        * 'none' - shows no axis or tick mark values
        * 'min' - shows min bounding box values
        * 'auto' - rounds axis range to sensible values
        * <number> - like 'min', but with <number> tick marks

        """
        self.YSpec = spectype

    @PendingDeprecation("self.XSpec property")
    def GetXSpec(self):
        """Returns current XSpec for axis"""
        return self.XSpec

    @PendingDeprecation("self.YSpec property")
    def GetYSpec(self):
        """Returns current YSpec for axis"""
        return self.YSpec

    @property
    def XSpec(self):
        return self._xSpec

    @XSpec.setter
    def XSpec(self, value):
        """
        xSpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:

        * 'none' - shows no axis or tick mark values
        * 'min' - shows min bounding box values
        * 'auto' - rounds axis range to sensible values
        * <number> - like 'min', but with <number> tick marks
        * list or tuple - a list of (min, max) values. must be length 2

        """
        ok_values = ('none', 'min', 'auto')
        if value not in ok_values and not isinstance(value, (int, float)):
            if not isinstance(value, (list, tuple)) and len(value != 2):
                err_str = ("XSpec must be 'none', 'min', 'auto', "
                           "a number, or sequence of numbers (length 2)")
                raise TypeError(err_str)
        self._xSpec = value

    @property
    def YSpec(self):
        return self._ySpec

    @YSpec.setter
    def YSpec(self, value):
        """
        ySpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:

        * 'none' - shows no axis or tick mark values
        * 'min' - shows min bounding box values
        * 'auto' - rounds axis range to sensible values
        * <number> - like 'min', but with <number> tick marks
        * list or tuple - a list of (min, max) values. must be length 2

        """
        ok_values = ('none', 'min', 'auto')
        if value not in ok_values and not isinstance(value, (int, float)):
            if not isinstance(value, (list, tuple)) and len(value != 2):
                err_str = ("YSpec must be 'none', 'min', 'auto', "
                           "a number, or sequence of numbers (length 2)")
                raise TypeError(err_str)
        self._ySpec = value

    @PendingDeprecation("self.XMaxRange property")
    def GetXMaxRange(self):
        return self.XMaxRange

    @property
    def XMaxRange(self):
        xAxis = self._getXMaxRange()
        if self.LogScale[0]:
            xAxis = np.power(10, xAxis)
        return xAxis

    def _getXMaxRange(self):
        """Returns (minX, maxX) x-axis range for displayed graph"""
        graphics = self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        xAxis = self._axisInterval(self._xSpec, p1[0], p2[0])  # in user units
        return xAxis

    @PendingDeprecation("self.YMaxRange property")
    def GetYMaxRange(self):
        return self.YMaxRange

    @property
    def YMaxRange(self):
        yAxis = self._getYMaxRange()
        if self.LogScale[1]:
            yAxis = np.power(10, yAxis)
        return yAxis

    def _getYMaxRange(self):
        """Returns (minY, maxY) y-axis range for displayed graph"""
        graphics = self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        yAxis = self._axisInterval(self._ySpec, p1[1], p2[1])
        return yAxis

    @PendingDeprecation("self.XCurrentRange property")
    def GetXCurrentRange(self):
        return self.XCurrentRange

    @property
    def XCurrentRange(self):
        xAxis = self._getXCurrentRange()
        if self.LogScale[0]:
            xAxis = np.power(10, xAxis)
        return xAxis

    def _getXCurrentRange(self):
        """Returns (minX, maxX) x-axis for currently displayed
        portion of graph"""
        return self.last_draw[1]

    @PendingDeprecation("self.YCurrentRange property")
    def GetYCurrentRange(self):
        return self.YCurrentRange

    @property
    def YCurrentRange(self):
        yAxis = self._getYCurrentRange()
        if self.LogScale[1]:
            yAxis = np.power(10, yAxis)
        return yAxis

    def _getYCurrentRange(self):
        """Returns (minY, maxY) y-axis for currently displayed
        portion of graph"""
        return self.last_draw[2]

    def Draw(self, graphics, xAxis=None, yAxis=None, dc=None):
        """Wrapper around _Draw, which handles log axes"""

        graphics.LogScale = self.LogScale

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
            if self.LogScale[0]:
                xAxis = np.log10(xAxis)
        if yAxis is not None:
            if yAxis[0] == yAxis[1]:
                return
            if self.LogScale[1]:
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
            if self.LogScale[1]:
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
        graphics.PrinterScale = self.printerScale

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
        if self.EnablePlotTitle:
            title = graphics.Title
            titleWH = dc.GetTextExtent(title)
        else:
            titleWH = (0, 0)
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabel, yLabel = graphics.XLabel, graphics.YLabel
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

        Parameters:
        -----------
        dc :
            The Device Contect to draw on

        p1 : np array of length 2
            The lower-left hand corner of the plot, in plot coords.
            So, if the plot ranges from x=-10 to 10, and y=-5 to 5, then
            p1 = (-10, -5)

        p2 : np array of length 2
            The upper-right hand corner of the plot, in plot coords.
            So, if the plot ranges from x=-10 to 10, and y=-5 to 5, then
            p1 = (10, 5)

        scale : np array of length 2
            The [X, Y] scaling factor to convert plot coords to DC coords

        shift : np array of length 2
            The [X, Y] shift values to convert plot coords to DC coords.

        xticks, yticks :
            the x and y tick definitions

        """
        # increases thickness for printing only
        pen = self.GridPen
        penWidth = self.printerScale * pen.GetWidth()
        pen.SetWidth(penWidth)
        dc.SetPen(pen)

        x, y, width, height = self._point2ClientCoord(p1, p2)

        if self._xSpec != 'none':
            if self.EnableGrid[0]:
                for x, _ in xticks:
                    pt = scale * np.array([x, p1[1]]) + shift
                    dc.DrawLine(pt[0], pt[1], pt[0], pt[1] - height)

        if self._ySpec != 'none':
            if self.EnableGrid[1]:
                for y, label in yticks:
                    pt = scale * np.array([p1[0], y]) + shift
                    dc.DrawLine(pt[0], pt[1], pt[0] + width, pt[1])

    @TempStyle('pen')
    def _drawTicks(self, dc, p1, p2, scale, shift, xticks, yticks):
        """Draw the tick marks"""
        # TODO: add option for ticks to extend outside of graph
        #       - done via negative ticklength values?
        #           + works but the axes values cut off the ticks.
        # increases thickness for printing only
        # TODO: changes to XSpec and YSpec api.
        pen = self.TickPen
        penWidth = self.printerScale * pen.GetWidth()
        pen.SetWidth(penWidth)
        dc.SetPen(pen)

        # lengthen lines for printing
        yTickLength = 3 * self.printerScale * self._tickLength[1]
        xTickLength = 3 * self.printerScale * self._tickLength[0]

        ticks = self.EnableTicks
        if self.XSpec != 'none':        # I don't like this :-/
            if ticks.bottom:
                for x, label in xticks:
                    pt = scale * np.array([x, p1[1]]) + shift
                    dc.DrawLine(pt[0], pt[1], pt[0], pt[1] - xTickLength)
            if ticks.top:
                for x, label in xticks:
                    pt = scale * np.array([x, p2[1]]) + shift
                    dc.DrawLine(pt[0], pt[1], pt[0], pt[1] + xTickLength)

        if self.YSpec != 'none':
            if ticks.left:
                for y, label in yticks:
                    pt = scale * np.array([p1[0], y]) + shift
                    dc.DrawLine(pt[0], pt[1], pt[0] + yTickLength, pt[1])
            if ticks.right:
                for y, label in yticks:
                    pt = scale * np.array([p2[0], y]) + shift
                    dc.DrawLine(pt[0], pt[1], pt[0] - yTickLength, pt[1])

    @TempStyle('pen')
    def _drawCenterLines(self, dc, p1, p2, scale, shift):
        """Draws the center lines"""
        # increases thickness for printing only
        pen = self.CenterLinePen
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
        """Draws the diagonal lines"""
        pen = self.DiagonalPen
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
        """Draw the frame lines"""
        # increases thickness for printing only
        pen = self.AxesPen
        penWidth = self.printerScale * pen.GetWidth()
        pen.SetWidth(penWidth)
        dc.SetPen(pen)

        axes = self.EnableAxes
        if self.XSpec != 'none':
            if axes.bottom:
                lower, upper = p1[0], p2[0]
                a1 = scale * np.array([lower, p1[1]]) + shift
                a2 = scale * np.array([upper, p1[1]]) + shift
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])
            if axes.top:
                lower, upper = p1[0], p2[0]
                a1 = scale * np.array([lower, p2[1]]) + shift
                a2 = scale * np.array([upper, p2[1]]) + shift
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])

        if self.YSpec != 'none':
            if axes.left:
                lower, upper = p1[1], p2[1]
                a1 = scale * np.array([p1[0], lower]) + shift
                a2 = scale * np.array([p1[0], upper]) + shift
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])
            if axes.right:
                lower, upper = p1[1], p2[1]
                a1 = scale * np.array([p2[0], lower]) + shift
                a2 = scale * np.array([p2[0], upper]) + shift
                dc.DrawLine(a1[0], a1[1], a2[0], a2[1])

    @TempStyle('pen')
    def _drawAxesValues(self, dc, p1, p2, scale, shift, xticks, yticks):
        """ Draws the axes values """
        # TODO: More code duplication? Same as _drawGrid and _drawTicks?
        # TODO: replace dc.DrawText with dc.DrawTextList?
        # TODO: update the bounding boxes when adding right and top values
        axes = self.EnableAxesValues
        if self.XSpec != 'none':
            if axes.bottom:
                for x, label in xticks:
                    w = dc.GetTextExtent(label)[0]
                    pt = scale * np.array([x, p1[1]]) + shift
                    dc.DrawText(label,
                                pt[0] - w/2,
                                pt[1] + 2 * self._pointSize[1])
            if axes.top:
                for x, label in xticks:
                    w, h = dc.GetTextExtent(label)
                    pt = scale * np.array([x, p2[1]]) + shift
                    dc.DrawText(label,
                                pt[0] - w/2,
                                pt[1] - 2 * self._pointSize[1] - h)
        if self.YSpec != 'none':
            if axes.left:
                h = dc.GetCharHeight()
                for y, label in yticks:
                    w = dc.GetTextExtent(label)[0]
                    pt = scale * np.array([p1[0], y]) + shift
                    dc.DrawText(label,
                                pt[0] - w - 3 * self._pointSize[0],
                                pt[1] - 0.5 * h)
            if axes.right:
                h = dc.GetCharHeight()
                for y, label in yticks:
                    w = dc.GetTextExtent(label)[0]
                    pt = scale * np.array([p2[0], y]) + shift
                    dc.DrawText(label,
                                pt[0] + 3 * self._pointSize[0],
                                pt[1] - 0.5 * h)

    @TempStyle('pen')
    def _drawPlotAreaItems(self, dc, p1, p2, scale, shift, xticks, yticks):
        """Draws each frame element"""
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
        """Draws the plot title"""
        dc.SetFont(self._getFont(self._fontSizeTitle))
        titlePos = (
            self.plotbox_origin[0] + lhsW
            + (self.plotbox_size[0] - lhsW - rhsW) / 2. - titleWH[0] / 2.,
            self.plotbox_origin[1] - self.plotbox_size[1]
        )
        dc.DrawText(graphics.Title, titlePos[0], titlePos[1])

    def _drawAxesLabels(self, dc, graphics, lhsW, rhsW, bottomH, topH,
                        xLabelWH, yLabelWH):
        """Draws the axes labels"""
        # TODO: axes values get big when this is turned off
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabelPos = (
            self.plotbox_origin[0] + lhsW
            + (self.plotbox_size[0] - lhsW - rhsW) / 2. - xLabelWH[0] / 2.,
            self.plotbox_origin[1] - xLabelWH[1]
        )
        dc.DrawText(graphics.XLabel, xLabelPos[0], xLabelPos[1])
        yLabelPos = (
            self.plotbox_origin[0] - 3 * self._pointSize[0],
            self.plotbox_origin[1] - bottomH
            - (self.plotbox_size[1] - bottomH - topH) / 2. + yLabelWH[0] / 2.
        )
        if graphics.YLabel:  # bug fix for Linux
            dc.DrawRotatedText(
                graphics.YLabel, yLabelPos[0], yLabelPos[1], 90)

    @TempStyle('pen')
    def _drawPlotAreaLabels(self, dc, graphics, lhsW, rhsW, titleWH,
                            bottomH, topH, xLabelWH, yLabelWH):
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

        if not self.ShowScrollbars:
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


#----------------------------------------------------------------------
from wx.lib.embeddedimage import PyEmbeddedImage

MagPlus = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAOFJ"
    "REFUeJy1VdEOxCAIo27//8XbuKfuPASGZ0Zisoi2FJABbZM3bY8c13lo5GvbjioBPAUEB0Yc"
    "VZ0iGRRc56Ee8DcikEgrJD8EFpzRegQASiRtBtzuA0hrdRPYQxaEKyJPG6IHyiK3xnNZvUSS"
    "NvUuzgYh0il4y14nCFPk5XgmNbRbQbVotGo9msj47G3UXJ7fuz8Q8FAGEu0/PbZh2D3NoshU"
    "1VUydBGVZKMimlGeErdNGUmf/x7YpjMjcf8HVYvS2adr6aFVlCy/5Ijk9q8SeCR9isJR8SeJ"
    "8pv7S0Wu2Acr0qdj3w7DRAAAAABJRU5ErkJggg==")

GrabHand = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAARFJ"
    "REFUeJy1VdESgzAIS2j//4s3s5fRQ6Rad5M7H0oxCZhWSpK1TjwUBCBJAIBItL1fijlfe1yJ"
    "8noCGC9KgrXO7f0SyZEDAF/H2opsAHv9V/548nplT5Jo7YAFQKQ1RMWzmHUS96suqdBrHkuV"
    "uxpdJjCS8CfGXWdJ2glzcquKSR5c46QOtCpgNyIHj6oieAXg3282QvMX45hy8a8H0VonJZUO"
    "clesjOPg/dhBTq64o1Kacz4Ri2x5RKsf8+wcWQaJJL+A+xRcZHeQeBKjK+5EFiVJ4xy4x2Mn"
    "1Vk4U5/DWmfPieiqbye7a3tV/cCsWKu76K76KUFFchVnhigJ/hmktelm/m3e3b8k+Ec8PqLH"
    "CT4JRfyK9o1xYwAAAABJRU5ErkJggg==")

Hand = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAARBJ"
    "REFUeJytluECwiAIhDn1/Z942/UnjCGoq+6XNeWDC1xAqbKr6zyo61Ibds60J8GBT0yS3IEM"
    "ABuIpJTa4IOLiAAQksuKyixLH1ShHgTgZl8KiALxOsODPoEMkgJ25Su6zoO3ZrjRnI96OLIq"
    "k7dsqOCboDa4XV/nwQEQVeFtmMnvbSJja+oagKBUaLn9hzd7VipRa9ostIv0O1uhzzaqNJxk"
    "hViwDVxqg51kksMg9r2rDDIFwHCap130FBhdMzeAfWg//6Ki5WWQrHSv6EIUeVs0g3wT3J7r"
    "FmWQp/JJDXeRh2TXcJa91zAH2uN2mvXFsrIrsjS8rnftWmWfAiLIStuD9m9h9belvzgS/1fP"
    "X7075IwDENteAAAAAElFTkSuQmCC")


### -------------------------------------------------------------------------
### Examples and Demo Frame
### -------------------------------------------------------------------------
def _draw1Objects():
    """Sin, Cos, and Points"""
    # 100 points sin function, plotted as green circles
    data1 = 2. * np.pi * np.arange(-200, 200) / 200.
    data1.shape = (200, 2)
    data1[:, 1] = np.sin(data1[:, 0])
    markers1 = PolyMarker(data1,
                          legend='Green Markers',
                          colour='green',
                          marker='circle',
                          size=1,
                          )

    # 50 points cos function, plotted as red line and markers
    data1 = 2. * np.pi * np.arange(-100, 100) / 100.
    data1.shape = (100, 2)
    data1[:, 1] = np.cos(data1[:, 0])
    lines = PolySpline(data1, legend='Red Line', colour='red')
    markers3 = PolyMarker(data1,
                          legend='Red Dot',
                          colour='red',
                          marker='circle',
                          size=1,
                          )

    # A few more points...
    pi = np.pi
    pts = [(0., 0.), (pi / 4., 1.), (pi / 2, 0.), (3. * pi / 4., -1)]
    markers2 = PolyMarker(pts,
                          legend='Cross Legend',
                          colour='blue',
                          marker='cross',
                          )
    line2 = PolyLine(pts, drawstyle='steps-post')

    return PlotGraphics([markers1, lines, markers3, markers2, line2],
                        "Graph Title",
                        "X Axis",
                        "Y Axis")


def _draw2Objects():
    """Sin, Cos, Points, and lines between points"""
    # 100 points sin function, plotted as green dots
    data1 = 2. * np.pi * np.arange(200) / 200.
    data1.shape = (100, 2)
    data1[:, 1] = np.sin(data1[:, 0])
    line1 = PolySpline(data1,
                       legend='Green Line',
                       colour='green',
                       width=6,
                       style=wx.PENSTYLE_DOT)

    # 25 points cos function, plotted as red dot-dash with steps.
    data1 = 2. * np.pi * np.arange(50) / 50.
    data1.shape = (25, 2)
    data1[:, 1] = np.cos(data1[:, 0])
    line2 = PolyLine(data1,
                     legend='Red Line',
                     colour='red',
                     width=2,
                     style=wx.PENSTYLE_DOT_DASH,
                     drawstyle='steps-post',
                     )

    # data points for the 25pt cos function.
    pts2 = PolyMarker(data1,
                      legend='Red Points',
                      colour='red',
                      size=1.5,
                      )

    # A few more points...
    pi = np.pi
    pts = [(0., 0.), (pi / 4., 1.), (pi / 2, 0.), (3. * pi / 4., -1)]
    markers1 = PolyMarker(pts,
                          legend='Cross Hatch Square',
                          colour='blue',
                          width=3,
                          size=6,
                          fillcolour='red',
                          fillstyle=wx.CROSSDIAG_HATCH,
                          marker='square',
                          )
    marker_line = PolyLine(pts,
                           legend='Cross Hatch Square',
                           colour='blue',
                           width=3,
                           )

    return PlotGraphics([markers1, line1, line2, pts2, marker_line],
                        "Big Markers with Different Line Styles")


def _draw3Objects():
    """Various Marker Types"""
    markerList = ['circle', 'dot', 'square', 'triangle', 'triangle_down',
                  'cross', 'plus', 'circle']
    m = []
    for i in range(len(markerList)):
        m.append(PolyMarker([(2 * i + .5, i + .5)],
                            legend=markerList[i],
                            colour='blue',
                            marker=markerList[i])
                 )
    return PlotGraphics(m, "Selection of Markers", "Minimal Axis", "No Axis")


def _draw4Objects():
    """25,000 point line and markers"""
    # Points
    data1 = np.random.normal(loc=7.5e5, scale=70000, size=50000)
    data1.shape = (25000, 2)
    markers2 = PolyMarker(data1, legend='Dots', colour='blue',
                          marker='square',
                          size=1,
                          )

    # Line
    data1 = np.arange(5e5, 1e6, 10)
    data1.shape = (25000, 2)
    line1 = PolyLine(data1, legend='Wide Line', colour='green', width=4)

    return PlotGraphics([markers2, line1], "25,000 Points", "Value X", "")


def _draw5Objects():
    """Empty graph with axes but no points"""
    points = []
    line1 = PolyLine(points, legend='Wide Line', colour='green', width=5)
    return PlotGraphics([line1],
                        "Empty Plot With Just Axes",
                        "Value X",
                        "Value Y")


def _draw6Objects():
    """Faking a Bar graph"""
    points1 = [(1, 0), (1, 10)]
    line1 = PolyLine(points1, colour='green', legend='Feb.', width=10)
    points1g = [(2, 0), (2, 4)]
    line1g = PolyLine(points1g, colour='red', legend='Mar.', width=10)
    points1b = [(3, 0), (3, 6)]
    line1b = PolyLine(points1b, colour='blue', legend='Apr.', width=10)

    points2 = [(4, 0), (4, 12)]
    line2 = PolyLine(points2, colour='Yellow', legend='May', width=10)
    points2g = [(5, 0), (5, 8)]
    line2g = PolyLine(points2g, colour='orange', legend='June', width=10)
    points2b = [(6, 0), (6, 4)]
    line2b = PolyLine(points2b, colour='brown', legend='July', width=10)

    return PlotGraphics([line1, line1g, line1b, line2, line2g, line2b],
                        "Bar Graph - (Turn on Grid, Legend)",
                        "Months",
                        "Number of Students")


def _draw7Objects():
    """Log10 on both axes"""
    x = np.arange(-1000, 1000, 1)
    y1 = 4.5 * x ** 2
    y2 = 2.2 * x ** 3
    points1 = np.transpose([x, y1])
    points2 = np.transpose([x, y2])
    line1 = PolyLine(points1, legend='quadratic', colour='blue', width=1)
    line2 = PolyLine(points2, legend='cubic', colour='red', width=1)
    return PlotGraphics([line1, line2],
                        "double log plot",
                        "Value X",
                        "Value Y")


def _draw8Objects():
    """
    Box plot
    """
    data1 = np.array([912, 337, 607, 583, 512, 531, 558, 381, 621, 574,
                      538, 577, 679, 415, 454, 417, 635, 319, 350, 183,
                      863, 337, 607, 583, 512, 531, 558, 381, 621, 574,
                      538, 577, 679, 415, 454, 417, 635, 319, 350, 97])
    data2 = np.array([912, 337, 607, 583, 512, 531, 558, 381, 621, 574,
                      538, 532, 829, 82, 454, 417, 635, 319, 350, 183,
                      863, 337, 607, 583, 512, 531, 558, 866, 621, 574,
                      538, 577, 679, 415, 326, 417, 635, 319, 350, 97])

    data2 = data2 * 0.9

    data1 = np.array([(0, x) for x in data1])
    data2 = np.array([(1, x) for x in data2])

    data3 = np.random.gamma(2, 2, 500) * 30 + 100
    data3 = np.array([(2, x) for x in data3])

    boxplot = BoxPlot(data1, legend="Weights")
    boxplot2 = BoxPlot(data2, legend="Heights")
    boxplot3 = BoxPlot(data3, legend="GammaDistribution")
    return PlotGraphics([boxplot, boxplot2, boxplot3],
                        "Box Plot",
                        "",
                        "Value")

def _draw9Objects():
    """
    Histogram

    The following must be true:
    len(bspec) = len(hist_data) + 1
    """

    data = 2.25 * np.random.randn(50) + 3
    heights, bins = np.histogram(data, bins=10)

    hist_fixed_binsize = PolyHistogram(heights, bins)

    # Bins can also be arbitrary widths:
    hist_variable_binsize = PolyHistogram(
        [2, 3, 4, 6, 3],
        [18, 19, 22, 25, 26, 27],
        fillcolour=wx.BLUE,
        edgewidth=2,
        edgecolour=wx.RED,
    )

    return PlotGraphics(
        [hist_fixed_binsize, hist_variable_binsize],
        "Histogram with fixed binsize (left) and variable binsize (right)",
        "Value",
        "Count",
    )


def _draw10Objects():
    """
    A real bar graph
    """
    bar_height = np.array([1, 5, 8, 16, 12, 15, 18, 23, 4, 7, 9, 6])
    bar_location = np.array([0, 2, 4, 6, 8, 10, 11, 12, 16, 20, 30])
    data = list(zip(bar_location, bar_height))
    bars = [PolyBars(data)]

    return PlotGraphics(bars, "Histogram", "XValue", "Count")


class TestFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,
                          wx.DefaultPosition, (800, 600))

        # Now Create the menu bar and items
        self.mainmenu = wx.MenuBar()

        # -------------------------------------------------------------------
        ### "File" Menu Items ###############################################
        # -------------------------------------------------------------------
        menu = wx.Menu()
        menu.Append(200, 'Page Setup...', 'Setup the printer page')
        self.Bind(wx.EVT_MENU, self.OnFilePageSetup, id=200)
        menu.Append(201, 'Print Preview...', 'Show the current plot on page')
        self.Bind(wx.EVT_MENU, self.OnFilePrintPreview, id=201)
        menu.Append(202, 'Print...', 'Print the current plot')
        self.Bind(wx.EVT_MENU, self.OnFilePrint, id=202)
        menu.Append(203, 'Save Plot...', 'Save current plot')
        self.Bind(wx.EVT_MENU, self.OnSaveFile, id=203)
        menu.Append(205, 'E&xit', 'Enough of this already!')
        self.Bind(wx.EVT_MENU, self.OnFileExit, id=205)
        self.mainmenu.Append(menu, '&File')

        # -------------------------------------------------------------------
        ### "Plot" Menu Items ###############################################
        # -------------------------------------------------------------------
        menu = wx.Menu()
        menu.Append(206, 'Draw1 - sin, cos',
                    'Draw Sin and Cos curves')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw1, id=206)
        menu.Append(207, 'Draw2 - sin, cos, large joined markers',
                    'Draw Sin and Cos curves with some large joined makers')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw2, id=207)
        menu.Append(208, 'Draw3 - various markers',
                    'Demo various markers')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw3, id=208)
        menu.Append(209, 'Draw4 - 25k pts',
                    'Example of drawing many points quickly')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw4, id=209)
        menu.Append(210, 'Draw5 - empty plot',
                    'An empty plot')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw5, id=210)
        menu.Append(260, 'Draw6 - fake bar graph via lines',
                    'Fake a bar graph by using lines.')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw6, id=260)
        menu.Append(261, 'Draw7 - log-log',
                    'Plot a Log-Log graph')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw7, id=261)
        menu.Append(262, 'Draw8 - Box Plots',
                    'Show off some box plots')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw8, id=262)
        menu.Append(263, 'Draw9 - Histogram',
                    'Plot a histogram')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw9, id=263)
        menu.Append(264, 'Draw10 - real bar graph',
                    'Plot a real bar chart (not faked with lines)')
        self.Bind(wx.EVT_MENU, self.OnPlotDraw10, id=264)

        menu.AppendSeparator()

        menu.Append(211, '&Redraw', 'Redraw plots')
        self.Bind(wx.EVT_MENU, self.OnPlotRedraw, id=211)
        menu.Append(212, '&Clear', 'Clear canvas')
        self.Bind(wx.EVT_MENU, self.OnPlotClear, id=212)
        menu.Append(213, '&Scale', 'Scale canvas')
        self.Bind(wx.EVT_MENU, self.OnPlotScale, id=213)

        menu.AppendSeparator()

        menu.Append(225, 'Scroll Up 1', 'Move View Up 1 Unit')
        self.Bind(wx.EVT_MENU, self.OnScrUp, id=225)
        menu.Append(230, 'Scroll Rt 2', 'Move View Right 2 Units')
        self.Bind(wx.EVT_MENU, self.OnScrRt, id=230)
        menu.Append(235, '&Plot Reset', 'Reset to original plot')
        self.Bind(wx.EVT_MENU, self.OnReset, id=235)

        self.mainmenu.Append(menu, '&Plot')

        # -------------------------------------------------------------------
        ### "Options" Menu Items ############################################
        # -------------------------------------------------------------------

        menu = wx.Menu()

        menu.Append(214, 'Enable &Zoom',
                    'Enable Mouse Zoom', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableZoom, id=214)

        menu.Append(217, 'Enable &Drag',
                    'Activates dragging mode', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableDrag, id=217)

        menu.Append(222, 'Enable &Point Label',
                    'Show Closest Point', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnablePointLabel, id=222)

        menu.Append(223, 'Enable &Anti-Aliasing',
                    'Smooth output', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableAntiAliasing, id=223)

        menu.Append(224, 'Enable &High-Resolution AA',
                    'Draw in higher resolution', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableHiRes, id=224)

        menu.AppendSeparator()

        menu.Append(226, 'Enable Center Lines',
                    'Draw center lines', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableCenterLines, id=226)

        menu.Append(227, 'Enable Diagonal Lines',
                    'Draw diagonal lines', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableDiagonals, id=227)

        menu.Append(220, 'Enable &Legend',
                    'Turn on Legend', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableLegend, id=220)

        ### SubMenu for Grid
        submenu = wx.Menu()
        self.gridSubMenu = submenu

        submenu.AppendCheckItem(2151, "X Gridlines", "Enable X gridlines")
        submenu.AppendCheckItem(2152, "Y Gridlines", "Enable Y gridlines")
        submenu.AppendCheckItem(2153, "All Gridlines", "Enable All gridlines")
        submenu.Check(2151, True)
        submenu.Check(2152, True)
        submenu.Check(2153, True)

        self.Bind(wx.EVT_MENU, self.OnEnableGridX, id=2151)
        self.Bind(wx.EVT_MENU, self.OnEnableGridY, id=2152)
        self.Bind(wx.EVT_MENU, self.OnEnableGridAll, id=2153)

        menu.Append(215, 'Enable Grid', submenu, 'Turn on Grid')
#        self.Bind(wx.EVT_MENU, self.OnEnableGrid, id=215)

        ### SubMenu for Axes
        submenu = wx.Menu()
        submenu_items = ("Bottom", "Left", "Top", "Right",
                         "Bottom+Left", "All")
        self.axesSubMenu = submenu
        for _i, item in enumerate(submenu_items, 2401):
            submenu.AppendCheckItem(_i, item, "Enables {} axis".format(item))
            submenu.Check(_i, True)

        self.Bind(wx.EVT_MENU, self.OnEnableAxesBottom, id=2401)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesLeft, id=2402)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesTop, id=2403)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesRight, id=2404)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesBottomLeft, id=2405)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesAll, id=2406)

        menu.Append(240, 'Enable Axes', submenu,
                    'Enables the display of the Axes')

        submenu = wx.Menu()
        submenu_items = ("Bottom", "Left", "Top", "Right")
        help_txt = "Enables {} axis values"
        self.axesValuesSubMenu = submenu
        for _i, item in enumerate(submenu_items, 2451):
            submenu.AppendCheckItem(_i, item, help_txt.format(item))

        submenu.Check(2451, True)
        submenu.Check(2452, True)
        submenu.Check(2453, False)
        submenu.Check(2454, False)

        self.Bind(wx.EVT_MENU, self.OnEnableAxesValuesBottom, id=2451)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesValuesLeft, id=2452)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesValuesTop, id=2453)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesValuesRight, id=2454)

        menu.Append(245, 'Enable Axes Values', submenu,
                    'Enables the display of the axes values')

        submenu = wx.Menu()
        submenu_items = ("Bottom", "Left", "Top", "Right")
        help_txt = "Enables {} ticks"
        self.ticksSubMenu = submenu
        for _i, item in enumerate(submenu_items, 2501):
            submenu.AppendCheckItem(_i, item, help_txt.format(item))

        submenu.Check(2501, False)
        submenu.Check(2502, False)
        submenu.Check(2503, False)
        submenu.Check(2504, False)

        self.Bind(wx.EVT_MENU, self.OnEnableTicksBottom, id=2501)
        self.Bind(wx.EVT_MENU, self.OnEnableTicksLeft, id=2502)
        self.Bind(wx.EVT_MENU, self.OnEnableTicksTop, id=2503)
        self.Bind(wx.EVT_MENU, self.OnEnableTicksRight, id=2504)

        menu.Append(250, 'Enable Ticks', submenu,
                    'Enables the display of the ticks')

        menu.Append(255, 'Enable Plot Title',
                    'Enables the plot title', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnablePlotTitle, id=255)
        menu.Check(255, True)

        menu.Append(270, 'Enable Axes Labels',
                    'Enables the X and Y axes labels', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesLabels, id=270)
        menu.Check(270, True)

        menu.Append(271, 'Enable Log-Y',
                    'Changes the Y axis to log10 scale', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnLogY, id=271)
        menu.Append(272, 'Enable Log-X',
                    'Changes the X axis to log10 scale', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnLogX, id=272)

        menu.Append(273, 'Enable Abs(X)',
                    'Applies absolute value transform to X axis',
                    kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnAbsX, id=273)
        menu.Append(274, 'Enable Abs(Y)',
                    'Applies absolute value transform to Y axis',
                    kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnAbsY, id=274)

        menu.AppendSeparator()

        menu.Append(231, 'Set Gray Background',
                    'Change background colour to gray')
        self.Bind(wx.EVT_MENU, self.OnBackgroundGray, id=231)
        menu.Append(232, 'Set &White Background',
                    'Change background colour to white')
        self.Bind(wx.EVT_MENU, self.OnBackgroundWhite, id=232)
        menu.Append(233, 'Set Red Label Text',
                    'Change label text colour to red')
        self.Bind(wx.EVT_MENU, self.OnForegroundRed, id=233)
        menu.Append(234, 'Set &Black Label Text',
                    'Change label text colour to black')
        self.Bind(wx.EVT_MENU, self.OnForegroundBlack, id=234)

        self.mainmenu.Append(menu, '&Options')

        self.plot_options_menu = menu

        # -------------------------------------------------------------------
        ### "Help" Menu Items ############################################
        # -------------------------------------------------------------------
        menu = wx.Menu()
        menu.Append(300, '&About', 'About this thing...')
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, id=300)
        self.mainmenu.Append(menu, '&Help')

        self.SetMenuBar(self.mainmenu)

        # A status bar to tell people what's happening
        self.CreateStatusBar(1)

        self.client = PlotCanvas(self)
        # define the function for drawing pointLabels
#        self.client.SetPointLabelFunc(self.DrawPointLabel)
        self.client.PointLabelFunc = self.DrawPointLabel
        # Create mouse event for showing cursor coords in status bar
        self.client.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        # Show closest point when enabled
        self.client.canvas.Bind(wx.EVT_MOTION, self.OnMotion)

        self.Show(True)

    def DrawPointLabel(self, dc, mDataDict):
        """
        This is the fuction that defines how the pointLabels are plotted

        :param dc: DC that will be passed
        :param mDataDict: Dictionary of data that you want to use
                          for the pointLabel

        As an example I have decided I want a box at the curve point
        with some text information about the curve plotted below.
        Any wxDC method can be used.

        """
        # ----------
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush(wx.BLACK, wx.BRUSHSTYLE_SOLID))

        sx, sy = mDataDict["scaledXY"]  # scaled x,y of closest point
        # 10by10 square centered on point
        dc.DrawRectangle(sx - 5, sy - 5, 10, 10)
        px, py = mDataDict["pointXY"]
        cNum = mDataDict["curveNum"]
        pntIn = mDataDict["pIndex"]
        legend = mDataDict["legend"]
        # make a string to display
        s = "Crv# %i, '%s', Pt. (%.2f,%.2f), PtInd %i" % (
            cNum, legend, px, py, pntIn)
        dc.DrawText(s, sx, sy + 1)
        # -----------

    def OnMouseLeftDown(self, event):
        s = "Left Mouse Down at Point: (%.4f, %.4f)" % self.client._getXY(
            event)
        self.SetStatusText(s)
        event.Skip()  # allows plotCanvas OnMouseLeftDown to be called

    def OnMotion(self, event):
        # show closest point (when enbled)
        if self.client.EnablePointLabel:
            # make up dict with info for the pointLabel
            # I've decided to mark the closest point on the closest curve
            dlst = self.client.GetClosestPoint(
                self.client._getXY(event), pointScaled=True)
            if dlst != []:  # returns [] if none
                curveNum, legend, pIndex, pointXY, scaledXY, distance = dlst
                # make up dictionary to pass to my user function (see
                # DrawPointLabel)
                mDataDict = {"curveNum": curveNum,
                             "legend": legend,
                             "pIndex": pIndex,
                             "pointXY": pointXY,
                             "scaledXY": scaledXY}
                # pass dict to update the pointLabel
                self.client.UpdatePointLabel(mDataDict)
        event.Skip()  # go to next handler

    def OnFilePageSetup(self, event):
        self.client.PageSetup()

    def OnFilePrintPreview(self, event):
        self.client.PrintPreview()

    def OnFilePrint(self, event):
        self.client.Printout()

    def OnSaveFile(self, event):
        self.client.SaveFile()

    def OnFileExit(self, event):
        self.Close()

    def OnPlotDraw1(self, event):
        self.resetDefaults()
        self.client.Draw(_draw1Objects())

    def OnPlotDraw2(self, event):
        self.resetDefaults()
        self.client.Draw(_draw2Objects())

    def OnPlotDraw3(self, event):
        self.resetDefaults()
        self.client.SetFont(wx.Font(10,
                                    wx.FONTFAMILY_SCRIPT,
                                    wx.FONTSTYLE_NORMAL,
                                    wx.FONTWEIGHT_NORMAL)
                            )
        self.client.FontSizeAxis = 20
        self.client.FontSizeLegend = 12
        self.client.XSpec = 'min'
        self.client.YSpec = 'none'
        self.client.Draw(_draw3Objects())

    def OnPlotDraw4(self, event):
        self.resetDefaults()
        drawObj = _draw4Objects()
        self.client.Draw(drawObj)
# profile
#        start = _time.perf_counter()
# for x in range(10):
# self.client.Draw(drawObj)
##        print("10x of Draw4 took: %f sec."%(_time.perf_counter() - start))
# profile end

    def OnPlotDraw5(self, event):
        # Empty plot with just axes
        self.resetDefaults()
        drawObj = _draw5Objects()
        # make the axis X= (0,5), Y=(0,10)
        # (default with None is X= (-1,1), Y= (-1,1))
        self.client.Draw(drawObj, xAxis=(0, 5), yAxis=(0, 10))

    def OnPlotDraw6(self, event):
        # Bar Graph Example
        self.resetDefaults()
        # self.client.SetEnableLegend(True)   #turn on Legend
        # self.client.SetEnableGrid(True)     #turn on Grid
        self.client.XSpec = 'none'
        self.client.YSpec = 'auto'
        self.client.Draw(_draw6Objects(), xAxis=(0, 7))

    def OnPlotDraw7(self, event):
        # log scale example
        self.resetDefaults()
        self.plot_options_menu.Check(271, True)
        self.plot_options_menu.Check(272, True)
        self.client.LogScale = (True, True)
        self.client.Draw(_draw7Objects())

    def OnPlotDraw8(self, event):
        """Box Plot example"""
        self.resetDefaults()
        self.client.Draw(_draw8Objects())

    def OnPlotDraw9(self, event):
        """Histogram example"""
        self.resetDefaults()
        self.client.Draw(_draw9Objects())

    def OnPlotDraw10(self, event):
        """Bar Chart example"""
        self.resetDefaults()
        self.client.Draw(_draw10Objects())

    def OnPlotRedraw(self, event):
        self.client.Redraw()

    def OnPlotClear(self, event):
        self.client.Clear()

    def OnPlotScale(self, event):
        if self.client.last_draw is not None:
            graphics, xAxis, yAxis = self.client.last_draw
            self.client.Draw(graphics, (1, 3.05), (0, 1))

    def OnEnableZoom(self, event):
        self.client.EnableZoom = event.IsChecked()
        if self.mainmenu.IsChecked(217):
            self.mainmenu.Check(217, False)

    ### Grid Events ###

    def _checkOtherGridMenuItems(self):
        """ check or uncheck the submenu items """
        self.gridSubMenu.Check(2151, self.client.EnableGrid[0])
        self.gridSubMenu.Check(2152, self.client.EnableGrid[1])
        self.gridSubMenu.Check(2153, all(self.client.EnableGrid))

    def OnEnableGridX(self, event):
        old = self.client.EnableGrid
        self.client.EnableGrid = (event.IsChecked(), old[1])
        self._checkOtherGridMenuItems()

    def OnEnableGridY(self, event):
        old = self.client.EnableGrid
        self.client.EnableGrid = (old[0], event.IsChecked())
        self._checkOtherGridMenuItems()

    def OnEnableGridAll(self, event):
        self.client.EnableGrid = event.IsChecked()
        self._checkOtherGridMenuItems()
        self.gridSubMenu.Check(2151, event.IsChecked())
        self.gridSubMenu.Check(2152, event.IsChecked())

    def OnEnableDrag(self, event):
        self.client.EnableDrag = event.IsChecked()
        if self.mainmenu.IsChecked(214):
            self.mainmenu.Check(214, False)

    def OnEnableLegend(self, event):
        self.client.EnableLegend = event.IsChecked()

    def OnEnablePointLabel(self, event):
        self.client.EnablePointLabel = event.IsChecked()

    def OnEnableAntiAliasing(self, event):
        self.client.EnableAntiAliasing = event.IsChecked()

    def OnEnableHiRes(self, event):
        self.client.EnableHiRes = event.IsChecked()

    ### Axes Events ###

    def _checkOtherAxesMenuItems(self):
        """ check or uncheck the submenu items """
        self.axesSubMenu.Check(2401, self.client.EnableAxes[0])
        self.axesSubMenu.Check(2402, self.client.EnableAxes[1])
        self.axesSubMenu.Check(2403, self.client.EnableAxes[2])
        self.axesSubMenu.Check(2404, self.client.EnableAxes[3])
        self.axesSubMenu.Check(2405, all(self.client.EnableAxes[:2]))
        self.axesSubMenu.Check(2406, all(self.client.EnableAxes))

    def OnEnableAxesBottom(self, event):
        old = self.client.EnableAxes
        self.client.EnableAxes = (event.IsChecked(), old[1], old[2], old[3])
        self._checkOtherAxesMenuItems()

    def OnEnableAxesLeft(self, event):
        old = self.client.EnableAxes
        self.client.EnableAxes = (old[0], event.IsChecked(), old[2], old[3])
        self._checkOtherAxesMenuItems()

    def OnEnableAxesTop(self, event):
        old = self.client.EnableAxes
        self.client.EnableAxes = (old[0], old[1], event.IsChecked(), old[3])
        self._checkOtherAxesMenuItems()

    def OnEnableAxesRight(self, event):
        old = self.client.EnableAxes
        self.client.EnableAxes = (old[0], old[1], old[2], event.IsChecked())
        self._checkOtherAxesMenuItems()

    def OnEnableAxesBottomLeft(self, event):
        checked = event.IsChecked()
        old = self.client.EnableAxes
        self.client.EnableAxes = (checked, checked, old[2], old[3])
        self._checkOtherAxesMenuItems()

    def OnEnableAxesAll(self, event):
        checked = event.IsChecked()
        self.client.EnableAxes = (checked, checked, checked, checked)
        self._checkOtherAxesMenuItems()

    ### Ticks Events ###

    def _checkOtherTicksMenuItems(self):
        """ check or uncheck the submenu items """
        self.ticksSubMenu.Check(2501, self.client.EnableTicks[0])
        self.ticksSubMenu.Check(2502, self.client.EnableTicks[1])
        self.ticksSubMenu.Check(2503, self.client.EnableTicks[2])
        self.ticksSubMenu.Check(2504, self.client.EnableTicks[3])
#        self.ticksSubMenu.Check(2505, all(self.client.EnableTicks[:2]))
#        self.axesSubMenu.Check(2506, all(self.client.EnableTicks))

    def OnEnableTicksBottom(self, event):
        old = self.client.EnableTicks
        self.client.EnableTicks = (event.IsChecked(), old[1],
                                   old[2], old[3])
        self._checkOtherTicksMenuItems()

    def OnEnableTicksLeft(self, event):
        old = self.client.EnableTicks
        self.client.EnableTicks = (old[0], event.IsChecked(),
                                   old[2], old[3])
        self._checkOtherTicksMenuItems()

    def OnEnableTicksTop(self, event):
        old = self.client.EnableTicks
        self.client.EnableTicks = (old[0], old[1],
                                   event.IsChecked(), old[3])
        self._checkOtherTicksMenuItems()

    def OnEnableTicksRight(self, event):
        old = self.client.EnableTicks
        self.client.EnableTicks = (old[0], old[1],
                                   old[2], event.IsChecked())
        self._checkOtherTicksMenuItems()

    ### AxesValues Events ###

    def OnEnableAxesValuesBottom(self, event):
        old = self.client.EnableAxesValues
        self.client.EnableAxesValues = (event.IsChecked(), old[1],
                                        old[2], old[3])

    def OnEnableAxesValuesLeft(self, event):
        old = self.client.EnableAxesValues
        self.client.EnableAxesValues = (old[0], event.IsChecked(),
                                        old[2], old[3])

    def OnEnableAxesValuesTop(self, event):
        old = self.client.EnableAxesValues
        self.client.EnableAxesValues = (old[0], old[1],
                                        event.IsChecked(), old[3])

    def OnEnableAxesValuesRight(self, event):
        old = self.client.EnableAxesValues
        self.client.EnableAxesValues = (old[0], old[1],
                                        old[2], event.IsChecked())

    ### Other Events ###

    def OnEnablePlotTitle(self, event):
        self.client.EnablePlotTitle = event.IsChecked()

    def OnEnableAxesLabels(self, event):
        self.client.EnableAxesLabels = event.IsChecked()

    def OnEnableCenterLines(self, event):
        self.client.EnableCenterLines = event.IsChecked()

    def OnEnableDiagonals(self, event):
        self.client.EnableDiagonals = event.IsChecked()

    def OnBackgroundGray(self, event):
        self.client.SetBackgroundColour("#CCCCCC")
        self.client.Redraw()

    def OnBackgroundWhite(self, event):
        self.client.SetBackgroundColour("white")
        self.client.Redraw()

    def OnForegroundRed(self, event):
        self.client.SetForegroundColour("red")
        self.client.Redraw()

    def OnForegroundBlack(self, event):
        self.client.SetForegroundColour("black")
        self.client.Redraw()

    def OnLogX(self, event):
        self.client.LogScale = (event.IsChecked(), self.client.LogScale[1])
        self.client.Redraw()

    def OnLogY(self, event):
        self.client.LogScale = (self.client.LogScale[0], event.IsChecked())
        self.client.Redraw()

    def OnAbsX(self, event):
        self.client.AbsScale = (event.IsChecked(), self.client.AbsScale[1])
        self.client.Redraw()

    def OnAbsY(self, event):
        self.client.AbsScale = (self.client.AbsScale[0], event.IsChecked())
        self.client.Redraw()

    def OnScrUp(self, event):
        self.client.ScrollUp(1)

    def OnScrRt(self, event):
        self.client.ScrollRight(2)

    def OnReset(self, event):
        self.client.Reset()

    def OnHelpAbout(self, event):
        from wx.lib.dialogs import ScrolledMessageDialog
        about = ScrolledMessageDialog(self, __doc__, "About...")
        about.ShowModal()

    def resetDefaults(self):
        """Just to reset the fonts back to the PlotCanvas defaults"""
        self.client.SetFont(wx.Font(10,
                                    wx.FONTFAMILY_SWISS,
                                    wx.FONTSTYLE_NORMAL,
                                    wx.FONTWEIGHT_NORMAL)
                            )
        self.client.FontSizeAxis = 10
        self.client.FontSizeLegend = 7
        self.client.LogScale = (False, False)
        self.client.XSpec = 'auto'
        self.client.YSpec = 'auto'


def __test():

    class MyApp(wx.App):

        def OnInit(self):
            wx.InitAllImageHandlers()
            frame = TestFrame(None, -1, "PlotCanvas")
            # frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = MyApp(0)
    app.MainLoop()


if __name__ == '__main__':
    __test()
