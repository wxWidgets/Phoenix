#!/usr/bin/env python

import wx

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        self.count = 0

        label = wx.StaticText(self, -1, "This is a wx.Slider.")

        slider = wx.Slider(
            self, 100, 25, 1, 100, size=(250, -1),
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )

        slider.SetTickFreq(5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((1,20))
        sizer.Add(label, 0, wx.LEFT, 20)
        sizer.Add((1,10))
        sizer.Add(slider, 0, wx.LEFT, 20)
        self.SetSizer(sizer)



#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------




overview = """\
A slider is a control with a handle which can be pulled back and forth to
change the value.
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

