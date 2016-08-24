#!/usr/bin/env python

import wx
import wx.adv
from wx.adv import CalendarCtrl, GenericCalendarCtrl, CalendarDateAttr

#----------------------------------------------------------------------

description = """\
This sample shows the wx.calendar.CalendarCtrl in a variety of styles
and modes.  If this platform supports a native calendar widget then
that is what is shown to the left.  However it may not support all of
the features and attributes of the older wx calendar, so we now have
the ability to explicitly use the generic widget via the
GenericCalendarCtrl class, and that is what is used for the two
calendars below.
""".replace('\n', ' ')


class TestPanel(wx.Panel):
    def __init__(self, parent, ID, log):
        wx.Panel.__init__(self, parent, ID)
        self.log = log

        native = self.cal = CalendarCtrl(self, -1, wx.DateTime().Today(),
                                    style=wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION)

        txt = wx.StaticText(self, -1, description)
        txt.Wrap(300)

        cal = GenericCalendarCtrl(self, -1, wx.DateTime().Today(),
                                  style = wx.adv.CAL_SHOW_HOLIDAYS
                                        | wx.adv.CAL_SUNDAY_FIRST
                                        | wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION
                                )

        cal2 = GenericCalendarCtrl(self, -1, wx.DateTime().Today())


        # Track a few holidays
        self.holidays = [(1,1), (10,31), (12,25) ]    # (these don't move around)
        self.OnChangeMonth()


        # bind some event handlers to each calendar
        for c in [native, cal, cal2]:
            c.Bind(wx.adv.EVT_CALENDAR,                 self.OnCalSelected)
            c.Bind(wx.adv.EVT_CALENDAR_MONTH,           self.OnChangeMonth)
            c.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,     self.OnCalSelChanged)
            c.Bind(wx.adv.EVT_CALENDAR_WEEKDAY_CLICKED, self.OnCalWeekdayClicked)

        # create some sizers for layout
        fgs = wx.FlexGridSizer(cols=2, hgap=50, vgap=50)
        fgs.Add(native)
        fgs.Add(txt)
        fgs.Add(cal)
        fgs.Add(cal2)
        box = wx.BoxSizer()
        box.Add(fgs, 1, wx.EXPAND|wx.ALL, 25)
        self.SetSizer(box)


    def OnCalSelected(self, evt):
        self.log.write('OnCalSelected: %s\n' % evt.Date)
        if evt.Date.month == wx.DateTime.Aug and evt.Date.day == 14:
            self.log.write("HAPPY BIRTHDAY!")

    def OnCalWeekdayClicked(self, evt):
        self.log.write('OnCalWeekdayClicked: %s\n' % evt.GetWeekDay())

    def OnCalSelChanged(self, evt):
        cal = evt.GetEventObject()
        self.log.write("OnCalSelChanged:\n\t%s: %s\n\t%s: %s" %
                       ("EventObject", cal.__class__,
                        "Date       ", cal.GetDate(),
                        ))

    def OnChangeMonth(self, evt=None):
        if evt is None:
            cal = self.cal
        else:
            cal = evt.GetEventObject()
        self.log.write('OnChangeMonth: %s\n' % cal.GetDate())
        cur_month = cal.GetDate().GetMonth() + 1   # convert wxDateTime 0-11 => 1-12
        for month, day in self.holidays:
            if month == cur_month:
                cal.SetHoliday(day)

        # August 14th is a special day, mark it with a blue square...
        if cur_month == 8:
            attr = CalendarDateAttr(border=wx.adv.CAL_BORDER_SQUARE,
                                          colBorder="blue")
            cal.SetAttr(14, attr)
        else:
            cal.ResetAttr(14)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, -1, log)
    return win

#----------------------------------------------------------------------


overview = """\
<html><body>
<h2>CalendarCtrl</h2>

Yet <i>another</i> calendar control.  This one is a wrapper around the C++
version described in the docs.  This one will probably be a bit more efficient
than the one in wxPython.lib.calendar, but I like a few things about it better,
so I think both will stay in wxPython.
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

