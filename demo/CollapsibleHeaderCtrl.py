#!/usr/bin/env python

import wx

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        # Create some controls
        self.chc = wx.CollapsibleHeaderCtrl(self, label='the label')
        setBtn = wx.Button(self, label='Set Collapsed')
        unsetBtn = wx.Button(self, label='Unset Collapsed')

        # Set up the layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, label='wx.CollapsibleHeaderCtrl: '),
                  wx.SizerFlags().CenterVertical())
        sizer.Add(self.chc, wx.SizerFlags().Border(wx.LEFT, 10))
        sizer.Add(setBtn, wx.SizerFlags().Border(wx.LEFT, 40))
        sizer.Add(unsetBtn, wx.SizerFlags().Border(wx.LEFT, 10))

        # Put it all in an outer box with a border
        box = wx.BoxSizer()
        box.Add(sizer, wx.SizerFlags(1).Border(wx.ALL, 30))
        self.SetSizer(box)

        # Set up the event handlers
        self.Bind(wx.EVT_BUTTON, self.OnSetBtn, setBtn)
        self.Bind(wx.EVT_BUTTON, self.OnUnsetBtn, unsetBtn)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckBtnStatus, setBtn)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckBtnStatus, unsetBtn)
        self.Bind(wx.EVT_COLLAPSIBLEHEADER_CHANGED, self.OnCollapseChanged)


    def OnSetBtn(self, evt):
        self.chc.SetCollapsed(True)

    def OnUnsetBtn(self, evt):
        self.chc.SetCollapsed(False)

    def OnCheckBtnStatus(self, evt):
        obj = evt.GetEventObject()
        collapsed = self.chc.IsCollapsed()
        if obj.Label.startswith('Set'):
            evt.Enable(not collapsed)
        if obj.Label.startswith('Unset'):
            evt.Enable(collapsed)

    def OnCollapseChanged(self, evt):
        self.log.write('OnCollapseChanged: {}'.format(self.chc.IsCollapsed()))


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.CollapsibleHeaderCtrl</center></h2>

A header control to be used above a collapsible pane.

The collapsible header usually consists of a small indicator of the collapsed
state and some label text beside it. This class is used by the generic
implementation of wx.CollapsiblePane but it may be used in more complex layouts
for other uses.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

