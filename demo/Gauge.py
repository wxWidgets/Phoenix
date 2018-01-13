#!/usr/bin/env python

import wx

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        self.count = 0

        wx.StaticText(self, -1, "This example shows the wx.Gauge control.", (45, 15))

        self.g1 = wx.Gauge(self, -1, 50, (110, 50), (250, -1))
        self.g2 = wx.Gauge(self, -1, 75, (110, 95), (250, -1))

        if 'wxMac' not in wx.PlatformInfo:
            self.g3 = wx.Gauge(self, -1, 100, (110, 135), (-1, 100), wx.GA_VERTICAL)

        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        self.timer.Start(100)

    def __del__(self):
        self.timer.Stop()

    def TimerHandler(self, event):
        self.count = self.count + 1

        if self.count >= 50:
            self.count = 0

        self.g1.SetValue(self.count)
        self.g2.Pulse()
        if 'wxMac' not in wx.PlatformInfo:
            self.g3.Pulse()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = """\
A Gauge is a horizontal or vertical bar which shows a quantity in a graphical
fashion. It is often used to indicate progress through lengthy tasks, such as
file copying or data analysis.

When the Gauge is initialized, its "complete" value is usually set; at any rate,
before using the Gauge, the maximum value of the control must be set. As the task
progresses, the Gauge is updated by the program via the <code>SetValue</code> method.

This control is for use within a GUI; there is a seperate ProgressDialog class
to present the same sort of control as a dialog to the user.
"""

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

