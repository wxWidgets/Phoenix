#!/usr/bin/env python

import wx
import wx.lib.resizewidget as rw

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        rw1 = rw.ResizeWidget(self)
        rw2 = rw.ResizeWidget(self)
        self.rw2 = rw2

        # This one we will reparent to the ResizeWidget...
        tst = wx.Panel(self)
        tst.SetBackgroundColour('pink')
        wx.StaticText(tst, -1, "a panel,\nwith limits")
        tst.SetMinSize((80,35))
        tst.SetMaxSize((200,100))
        rw1.SetManagedChild(tst)

        # This one we will create as a child of the resizer to start with
        lb = wx.ListBox(rw2, size=(100,70),
                        choices="zero one two three four five six seven eight nine".split())

        # now make a sizer with a bunch of other widgets
        fgs = wx.FlexGridSizer(cols=4, vgap=5, hgap=5)
        for i in range(16):
            if i == 5:
                fgs.Add(rw1)
            elif i == 10:
                fgs.Add(rw2)
            else:
                fgs.Add(wx.Button(self))

        self.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(fgs, 0, wx.ALL, 10)

        self.Bind(rw.EVT_RW_LAYOUT_NEEDED, self.OnLayoutNeeded)


    def OnLayoutNeeded(self, evt):
        self.Layout()

    def OnButton(self, evt):
        self.rw2.EnableResize(not self.rw2.IsResizeEnabled())


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>ResizeWidget</center></h2>
<p>%s</p>
</body></html>
""" % rw.__doc__



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

