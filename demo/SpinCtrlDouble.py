#!/usr/bin/env python

import wx

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        wx.StaticText(self, -1, "wx.SpinCtrlDouble:", pos=(25,25))
        spin = wx.SpinCtrlDouble(self, value='0.00', pos=(75,50), size=(80,-1),
                                 min=-5.0, max=25.25, inc=0.25)
        spin.SetDigits(2)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.SpinCtrlDouble</center></h2>

Essentially the same as a wx.SpinCtrl, except it can handle floating
point numbers, and fractional increments.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

