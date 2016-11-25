#!/usr/bin/env python

import  wx
import images

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        panel = wx.Panel(self, -1)
        buttons = wx.BoxSizer(wx.HORIZONTAL)

        for word in "These are toggle buttons".split():
            b = wx.ToggleButton(panel, -1, word)
            self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle, b)
            buttons.Add(b, flag=wx.ALL, border=5)

        panel.SetAutoLayout(True)
        panel.SetSizer(buttons)
        buttons.Fit(panel)
        panel.Move((50,50))

        b = wx.ToggleButton(self, -1, "can have bitmaps too", pos=(50,125))
        b.SetBitmap(images.Mondrian.Bitmap)
        b.SetInitialSize() # adjust default size for the bitmap
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle, b)

    def OnToggle(self, evt):
        self.log.write("Button %d toggled\n" % evt.GetId())

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#----------------------------------------------------------------------


overview = """\
wx.ToggleButton is a button that stays pressed when clicked by the user.
In other words, it is similar to wxCheckBox in functionality but looks like a
wxButton.
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
