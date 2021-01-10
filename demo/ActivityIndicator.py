#!/usr/bin/env python

import wx

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        # Create some controls
        self.ai = wx.ActivityIndicator(self)
        self.ai.Start()
        startBtn = wx.Button(self, label='Start')
        stopBtn = wx.Button(self, label='Stop')

        # Set up the layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, label='wx.ActivityIndicator: '),
                  wx.SizerFlags().CenterVertical())
        sizer.Add(self.ai, wx.SizerFlags().Border(wx.LEFT, 10))
        sizer.Add(startBtn, wx.SizerFlags().Border(wx.LEFT, 40))
        sizer.Add(stopBtn, wx.SizerFlags().Border(wx.LEFT, 10))

        # Put it all in an outer box with a border
        box = wx.BoxSizer()
        box.Add(sizer, wx.SizerFlags(1).Border(wx.ALL, 30))
        self.SetSizer(box)

        # Set up the event handlers
        self.Bind(wx.EVT_BUTTON, self.OnStart, startBtn)
        self.Bind(wx.EVT_BUTTON, self.OnStop, stopBtn)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckBtnStatus, startBtn)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckBtnStatus, stopBtn)


    def OnStart(self, evt):
        self.ai.Start()


    def OnStop(self, evt):
        self.ai.Stop()


    def OnCheckBtnStatus(self, evt):
        obj = evt.GetEventObject()
        running = self.ai.IsRunning()
        if obj.Label == 'Start':
            evt.Enable(not running)
        if obj.Label == 'Stop':
            evt.Enable(running)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.ActivityIndicator</center></h2>

The wx.ActivityIndicator is a small platform-specifc control showing an
animation that can be used to indicate that the program is currently busy
performing some background task.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

