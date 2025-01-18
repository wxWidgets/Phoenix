# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0330, C0103
#   E1101: Module X has no Y member
#   C0330: Wrong continued indentation
#   C0103: Invalid attribute/variable/method name
"""
utils.py
=========

This is a collection of utilities used by the :mod:`wx.lib.plot` package.

"""
__docformat__ = "restructuredtext en"

# Standard Library
import sys
import functools
import inspect
import itertools
from warnings import warn as _warn

# Third Party
import wx
import numpy as np

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class PlotPendingDeprecation(wx.wxPyDeprecationWarning):
    pass

class DisplaySide(object):
    """
    Generic class for describing which sides of a box are displayed.

    Used for fine-tuning the axis, ticks, and values of a graph.

    This class somewhat mimics a collections.namedtuple factory function in
    that it is an iterable and can have individual elements accessible by name.
    It differs from a namedtuple in a few ways:

    - it's mutable
    - it's not a factory function but a full-fledged class
    - it contains type checking, only allowing boolean values
    - it contains name checking, only allowing valid_names as attributes

    :param bottom: Display the bottom side
    :type bottom: bool
    :param left: Display the left side
    :type left: bool
    :param top: Display the top side
    :type top: bool
    :param right: Display the right side
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


# TODO: replace with wx.DCPenChanger/wx.DCBrushChanger, etc.
#       Alternatively, replace those with this function...
class TempStyle(object):
    """
    Decorator / Context Manager to revert pen or brush changes.

    Will revert pen, brush, or both to their previous values after a method
    call or block finish.

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

    def __enter__(self) -> Self:
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


def pendingDeprecation(new_func):
    """
    Raise `PendingDeprecationWarning` and display a message.

    Uses inspect.stack() to determine the name of the item that this
    is called from.

    :param new_func: The name of the function that should be used instead.
    :type new_func: string.
    """
    warn_txt = "`{}` is pending deprecation. Please use `{}` instead."
    _warn(warn_txt.format(inspect.stack()[1][3], new_func),
          PlotPendingDeprecation)


def scale_and_shift_point(x, y, scale=1, shift=0):
    """
    Creates a scaled and shifted 2x1 numpy array of [x, y] values.

    The shift value must be in the scaled units.

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


def set_displayside(value):
    """
    Wrapper around :class:`~wx.lib.plot._DisplaySide` that allows for "overloaded" calls.

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
    return DisplaySide(*_value)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

if __name__ == "__main__":
    raise RuntimeError("This module is not intended to be run by itself.")
