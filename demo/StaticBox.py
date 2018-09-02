#!/usr/bin/env python

import wx

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        box1 = wx.StaticBox(self, -1, "This is a wx.StaticBox")

        # This gets the recommended amount of border space to use for items
        # within in the static box for the current platform.
        topBorder, otherBorder = box1.GetBordersForSizer()
        bsizer1 = wx.BoxSizer(wx.VERTICAL)
        bsizer1.AddSpacer(topBorder)

        t1 = wx.StaticText(box1, -1, "As of wxPython 2.9, wx.StaticBox can now be used as a parent like most other wx widgets. This is now the recommended way of using wx.StaticBox.")
        bsizer1.Add(t1, 1, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, otherBorder+10)
        box1.SetSizer(bsizer1)

        ## The OLD way.
        box2 = wx.StaticBox(self, -1, "This is a wx.StaticBox using wx.StaticBoxSizer")
        bsizer2 = wx.StaticBoxSizer(box2, wx.VERTICAL)

        t = wx.StaticText(self, -1, "Controls placed \"inside\" the box are really its siblings. This method of using wx.StaticBox is deprecated since wxPython 2.9, and can cause issues on some platforms.")
        bsizer2.Add(t, 1, wx.EXPAND|wx.TOP|wx.LEFT, 10)


        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(box1, 1, wx.EXPAND|wx.ALL, 25)
        border.Add(bsizer2, 1, wx.EXPAND|wx.ALL, 25)
        self.SetSizer(border)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.StaticBox</center></h2>

This control draws a box and can be used to group other controls.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

