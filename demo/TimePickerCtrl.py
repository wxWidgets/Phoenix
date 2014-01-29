#!/usr/bin/env python

import wx
import wx.adv

#----------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.tpc = wx.adv.TimePickerCtrl(self, size=(120, -1),
                                style = wx.adv.TP_DEFAULT)
        self.Bind(wx.adv.EVT_TIME_CHANGED, self.OnTimeChanged, self.tpc)
        sizer.Add(self.tpc, 0, wx.ALL, 50)

    def OnTimeChanged(self, evt):
        self.log.write("OnTimeChanged: hour: %s min: %s sec: %s\n" % self.tpc.GetTime())

#----------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = """<html><body>
<h2><center>wx.TimePickerCtrl</center></h2>
<p>
This control allows the user to enter time.
</p>
<p>
It is similar to DatePickerCtrl but is used for time, and not date, selection.
 While GetValue and SetValue still work with values of type DateTime (because
 wxWidgets doesn't provide a time-only class), their date part is
 ignored by this control.
</p>
<p>
It is only available if USE_TIMEPICKCTRL is set to 1.
</p>
<p>
This control currently doesn't have any specific flags.
</p>
</body></html>
"""


if __name__ == '__main__':
    import sys
    import os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
