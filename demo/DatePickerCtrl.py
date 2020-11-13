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

        dpc = wx.adv.DatePickerCtrl(self, size=(120,-1),
                                style = wx.adv.DP_DROPDOWN
                                      | wx.adv.DP_SHOWCENTURY
                                      | wx.adv.DP_ALLOWNONE )
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
        sizer.Add(dpc, 0, wx.ALL, 50)

        st = wx.StaticText(self,
            label="In some cases the widget used above will be a native date picker, so show the generic one too.")
        sizer.Add(st, 0, wx.LEFT, 50)

        dpc = wx.adv.DatePickerCtrlGeneric(self, size=(120,-1),
                                           style = wx.adv.DP_DROPDOWN
                                           | wx.adv.DP_SHOWCENTURY
                                           | wx.adv.DP_ALLOWNONE )
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
        sizer.Add((1,15))
        sizer.Add(dpc, 0, wx.LEFT, 50)


    def OnDateChanged(self, evt):
        self.log.write("OnDateChanged: %s\n" % evt.GetDate())

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.DatePickerCtrl</center></h2>

This control allows the user to select a date. Unlike
wx.calendar.CalendarCtrl, which is a relatively big control,
wx.DatePickerCtrl is implemented as a small window showing the
currently selected date. The control can be edited using the keyboard,
and can also display a popup window for more user-friendly date
selection, depending on the styles used and the platform.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

