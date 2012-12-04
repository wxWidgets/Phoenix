##Andrea Gavana
#!/usr/bin/env python

# This sample shows hot to take advantage of wx.CallAfter when running a
# separate thread and updating the GUI in the main thread

import wx
import threading
import time

class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='CallAfter example')

        panel = wx.Panel(self)
        self.label = wx.StaticText(panel, label="Ready")
        self.btn = wx.Button(panel, label="Start")
        self.gauge = wx.Gauge(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, proportion=1, flag=wx.EXPAND)
        sizer.Add(self.btn, proportion=0, flag=wx.EXPAND)
        sizer.Add(self.gauge, proportion=0, flag=wx.EXPAND)

        panel.SetSizerAndFit(sizer)
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        """ This event handler starts the separate thread. """
        self.btn.Enable(False)
        self.gauge.SetValue(0)
        self.label.SetLabel("Running")

        thread = threading.Thread(target=self.LongRunning)
        thread.start()

    def OnLongRunDone(self):
        self.gauge.SetValue(100)
        self.label.SetLabel("Done")
        self.btn.Enable(True)

    def LongRunning(self):
        """This runs in a different thread.  Sleep is used to
         simulate a long running task."""
        time.sleep(3)
        wx.CallAfter(self.gauge.SetValue, 20)
        time.sleep(5)
        wx.CallAfter(self.gauge.SetValue, 70)
        time.sleep(4)
        wx.CallAfter(self.OnLongRunDone)

if __name__ == "__main__":
    app = wx.App(0)
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()