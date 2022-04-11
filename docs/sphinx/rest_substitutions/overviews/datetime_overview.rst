.. include:: headings.inc


.. _date and time:

===========================================
|phoenix_title|  **Date and Time Overview**
===========================================

Introduction
------------

wxPython provides a set of powerful classes to work with dates and
times. Some of the supported features of :ref:`wx.DateTime` class are:

* Wide range: the range of supported dates goes from about 4714
  B.C. to some 480 million years in the future.

* Precision: not using floating point calculations anywhere ensures
  that the date calculations don't suffer from rounding errors.

* Many features: not only all usual calculations with dates are
  supported, but also more exotic week and year day calculations, work
  day testing, standard astronomical functions, conversion to and from
  strings in either strict or free format.

* Efficiency: objects of :ref:`wx.DateTime` are small (8 bytes) and
  working with them is fast.



All date/time classes at a glance
---------------------------------

There are 3 main classes related to date and time: except
:ref:`wx.DateTime` itself which represents an absolute moment in time,
there are also two classes - :ref:`wx.TimeSpan` and :ref:`wx.DateSpan` -
which represent the intervals of time.



DateTime characteristics
------------------------

:ref:`wx.DateTime` stores the time as a signed number of milliseconds
since the Epoch which is fixed, by convention, to Jan 1, 1970 -
however this is not visible to the class users (in particular, dates
prior to the Epoch are handled just as well (or as bad) as the dates
after it).  But it does mean that the best resolution which can be
achieved with this class is 1 millisecond.

The size of :ref:`wx.DateTime` object is 8 bytes because it is
represented as a 64 bit integer. The resulting range of supported
dates is thus approximately 580 million years, but due to the
current limitations in the Gregorian calendar support, only dates from
Nov 24, 4714BC are supported (this is subject to change if there is
sufficient interest in doing it).

Finally, the internal representation is time zone independent (always
in GMT) and the time zones only come into play when a date is broken
into year/month/day components. See more about timezones below (see
:ref:`Time zone considerations <time zone considerations>`).

Currently, the only supported calendar is Gregorian one (which is used
even for the dates prior to the historic introduction of this calendar
which was first done on Oct 15, 1582 but is, generally speaking,
country, and even region, dependent). Future versions will probably
have Julian calendar support as well and support for other calendars
(Maya, Hebrew, Chinese...) is not ruled out.



Difference between DateSpan and TimeSpan
----------------------------------------

While there is only one logical way to represent an absolute moment in
the time (and hence only one :ref:`wx.DateTime` class), there are at
least two methods to describe a time interval.

First, there is the direct and self-explaining way implemented by
:ref:`wx.TimeSpan`: it is just a difference in milliseconds between two
moments in time. Adding or subtracting such an interval to
:ref:`wx.DateTime` is always well-defined and is a fast operation.

But in the daily life other, calendar-dependent time interval
specifications are used. For example, 'one month later' is commonly
used.  However, it is clear that this is not the same as
:ref:`wx.TimeSpan` of 60\*60\*24\*31 seconds because 'one month later'
Feb 15 is Mar 15 and not Mar 17 or Mar 16 (depending on whether the
year is leap or not).

This is why there is another class for representing such intervals
called :ref:`wx.DateSpan`. It handles these sort of operations in the
most natural way possible, but note that manipulating with intervals
of this kind is not always well-defined. Consider, for example, Jan 31
+ '1 month': this will give Feb 28 (or 29), i.e. the last day of
February and not the non-existent Feb 31. Of course, this is what is
usually wanted, but you still might be surprised to notice that now
subtracting back the same interval from Feb 28 will result in Jan 28
and **not** Jan 31 we started with!

So, unless you plan to implement some kind of natural language parsing
in the program, you should probably use :ref:`wx.TimeSpan` instead of
:ref:`wx.DateSpan` (which is also more efficient). However,
:ref:`wx.DateSpan` may be very useful in situations when you do need to
understand what 'in a month' means - of course, it is just::

    wx.DateTime.Now() + wx.DateSpan.Month()




Date arithmetic
----------------

Many different operations may be performed with the dates, however not
all of them make sense. For example, multiplying a date by a number is
an invalid operation, even though multiplying either of the time span
classes by a number is perfectly valid.

Here is what can be done:

* **Addition**: a :ref:`wx.TimeSpan` or :ref:`wx.DateSpan` can be added to
  :ref:`wx.DateTime` resulting in a new :ref:`wx.DateTime` object and also 2
  objects of the same span class can be added together giving another
  object of the same class.

* **Subtraction**: the same types of operations as above are allowed
  and, additionally, a difference between two :ref:`wx.DateTime` objects
  can be taken and this will yield :ref:`wx.TimeSpan`.

* **Multiplication**: a :ref:`wx.TimeSpan` or :ref:`wx.DateSpan` object can
  be multiplied by an integer number resulting in an object of the
  same type.

* **Unary minus**: a :ref:`wx.TimeSpan` or :ref:`wx.DateSpan` object may
  finally be negated giving an interval of the same magnitude but of
  opposite time direction.


For all these operations there are corresponding global (overloaded)
operators and also member functions which are synonyms for them:
`Add()`, `Subtract()` and `Multiply()`. Unary minus as well as
composite assignment operations (like +=) are only implemented as
members and `Neg()` is the synonym for unary minus.



.. _time zone considerations:

Time zone considerations
------------------------

Although the time is always stored internally in GMT, you will usually
work in the local time zone. Because of this, all :ref:`wx.DateTime`
constructors and setters which take the broken down date assume that
these values are for the local time zone. Thus::

    wx.DateTimeFromDMY(1, wx.DateTime.Jan, 1970)


will not correspond to the :ref:`wx.DateTime` Epoch unless you happen
to live in the UK. All methods returning the date components (year,
month, day, hour, minute, second...) will also return the correct
values for the local time zone by default, so, generally, doing the
natural things will lead to natural and correct results.

If you only want to do this, you may safely skip the rest of this
section. However, if you want to work with different time zones, you
should read it to the end.

In this (rare) case, you are still limited to the local time zone when
constructing :ref:`wx.DateTime` objects, i.e. there is no way to
construct a :ref:`wx.DateTime` corresponding to the given date in,
say, Pacific Standard Time. To do it, you will need to call
:meth:`wx.DateTime.ToTimezone` or :meth:`wx.DateTime.MakeTimezone`
methods to adjust the date for the target time zone. There are also
special versions of these functions :meth:`wx.DateTime.ToUTC` and
:meth:`wx.DateTime.MakeUTC` for the most common case - when the date
should be constructed in UTC.

You also can just retrieve the value for some time zone without
converting the object to it first. For this you may pass TimeZone
argument to any of the methods which are affected by the time zone
(all methods getting date components and the date formatting ones, for
example).  In particular, the `Format()` family of methods accepts a
TimeZone parameter and this allows to simply print time in any time
zone.

To see how to do it, the last issue to address is how to construct a
TimeZone object which must be passed to all these methods. First of
all, you may construct it manually by specifying the time zone offset
in seconds from GMT, but usually you will just use one of the
:ref:`Date and Time <date and time>` and let the conversion
constructor do the job.

I.e. you would just write::

    dt = wx.DateTimeFromDMY(8, wx.DateTime.May, 1977)
    print("The time is %s in local time zone" % dt.FormatTime())
    print("The time is %s in GMT" % dt.FormatTime(wx.DateTime.GMT))



.. _dst overview:

Daylight saving time (DST)
--------------------------

DST (a.k.a. 'summer time') handling is always a delicate task which is
better left to the operating system which is supposed to be configured
by the administrator to behave correctly. Unfortunately, when doing
calculations with date outside of the range supported by the standard
library, we are forced to deal with these issues ourselves.

Several functions are provided to calculate the beginning and end of
DST in the given year and to determine whether it is in effect at the
given moment or not, but they should not be considered as absolutely
correct because, first of all, they only work more or less correctly
for only a handful of countries (any information about other ones
appreciated!) and even for them the rules may perfectly well change in
the future.

The time zone handling methods (see :ref:`Time zone considerations
<time zone considerations>`) use these functions too, so they are
subject to the same limitations.



DateTime and Holidays
---------------------

.. todo:: WRITE THIS DOC PARAGRAPH.

