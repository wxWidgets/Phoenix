# -*- coding: utf-8 -*-
# Name:         CDate.py
# Purpose:      Date and Calendar classes
#
# Author:       Lorne White (email: lwhite1@planet.eon.net)
#
# Created:
# Version       0.2 08-Nov-1999
# Licence:      wxWindows license
# Tags:         phoenix-port, py3-port, documented, unittest
#----------------------------------------------------------------------------
# Updated:      01-Dec-2004
# Action:       Cast the year variable to an integer under the Date Class
# Reason:       When the year was compared in the isleap() function, if it was
#               in a string format, then an error was raised.
#
"""Date and calendar classes and date utitility methods."""
import time

# I18N
import wx
_ = wx.GetTranslation


Month = {0: None,
         1: _('January'), 2: _('February'), 3: _('March'),
         4: _('April'), 5: _('May'), 6: _('June'),
         7: _('July'), 8: _('August'), 9: _('September'),
         10: _('October'), 11: _('November'), 12: _('December')}

# Number of days per month (except for February in leap years)
mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Full and abbreviated names of weekdays
day_name = [_('Sunday'), _('Monday'), _('Tuesday'), _('Wednesday'),
            _('Thursday'), _('Friday'), _('Saturday')]
day_abbr = [_('Sun'), _('Mon'), _('Tue'), _('Wed'), _('Thu'), _('Fri'),
            _('Sat')]


def leapdays(y1, y2):
    """
    Return number of leap years in range [y1, y2]
    Assume y1 <= y2 and no funny (non-leap century) years
    """
    return (y2 + 3) / 4 - (y1 + 3) / 4


def isleap(year):
    """Verify if year is a leap year.

    :param int `year`: the year to check
    :return: True or False

    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def FillDate(val):
    s = str(val)
    if len(s) < 2:
        s = '0' + s
    return s


def julianDay(year, month, day):
    """Convert a date to Julian

    :param int `year`: the year
    :param int `month`: the month
    :param int `day`: the day

    :returns: the julian date number

    """
    b = 0
    if month > 12:
        year = year + month / 12
        month = month % 12
    elif month < 1:
        month = -month
        year = year - month / 12 - 1
        month = 12 - month % 12
    if year > 0:
        yearCorr = 0
    else:
        yearCorr = 3
    if month < 3:
        year = year - 1
        month = month + 12
    if year * 10000 + month * 100 + day > 15821014:
        b = 2 - year / 100 + year / 400
    return (1461 * year - yearCorr) / 4 + 306001 * (month + 1) / 10000 + day + 1720994 + b


def TodayDay():
    date = time.localtime(time.time())
    year = date[0]
    month = date[1]
    day = date[2]
    julian = julianDay(year, month, day)
    daywk = dayOfWeek(julian)
    daywk = day_name[daywk]
    return(daywk)


def FormatDay(value):
    date = FromFormat(value)
    daywk = DateCalc.dayOfWeek(date)
    daywk = day_name[daywk]
    return(daywk)


def FromJulian(julian):
    """Convert a julian date

    :param int `julian`: the julian date to convert

    :returns: year, month day as integers

    """
    if (julian < 2299160):
        b = julian + 1525
    else:
        alpha = (4 * julian - 7468861) / 146097
        b = julian + 1526 + alpha - alpha / 4
    c = (20 * b - 2442) / 7305
    d = 1461 * c / 4
    e = 10000 * (b - d) / 306001
    day = int(b - d - 306001 * e / 10000)
    if e < 14:
        month = int(e - 1)
    else:
        month = int(e - 13)
    if month > 2:
        year = c - 4716
    else:
        year = c - 4715
    year = int(year)
    return year, month, day


def dayOfWeek(julian):
    """Get day of week from a julian day

    :param `julian`: the julian day

    :returns: the day of week as an integer and Monday = 1

    """
    return int((julian + 1) % 7)


def daysPerMonth(month, year):
    """Get the number of days for the month.

    :param int `month`: the month
    :param int `year`: the year

    :returns: the number of days in the requested month

    """
    ndays = mdays[month] + (month == 2 and isleap(year))
    return ndays


class now(object):
    """A now date class"""
    def __init__(self):
        """
        Default class constructor.
        """
        self.date = time.localtime(time.time())
        self.year = self.date[0]
        self.month = self.date[1]
        self.day = self.date[2]
        self.hour = self.date[3]
        self.minutes = self.date[4]
        self.secondes = self.date[5]
        self.day_of_week = self.date[6]

        self.julian = julianDay(self.year, self.month, self.day)


class Date(object):
    """A date class"""
    def __init__(self, year, month, day):
        """
        Default class constructor.

        :param `year`: the year as an int or string
        :param `month`: the month as an int or string
        :param `day`: the day as an int or string

        """
        self.julian = julianDay(year, month, day)
        self.month = int(month)
        self.year = int(year)
        self.day = int(day)
        self.day_of_week = dayOfWeek(self.julian)
        self.days_in_month = daysPerMonth(self.month, self.year)
