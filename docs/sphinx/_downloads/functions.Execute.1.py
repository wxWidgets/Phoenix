##Andrea Gavana
#!/usr/bin/env python

# This sample demonstrates a simple use of wx.Process/wx.Execute to
# monitor an external program stdout

import wx

class ProcessFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='Process/Execute example')

        panel = wx.Panel(self)
        self.label = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.btn = wx.Button(panel, label="Start")

        self.process = None

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, proportion=1, flag=wx.EXPAND)
        sizer.Add(self.btn, proportion=0, flag=wx.EXPAND)

        panel.SetSizerAndFit(sizer)
        self.Bind(wx.EVT_BUTTON, self.OnButton)

        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)

    def OnButton(self, event):
        self.btn.Enable(False)
        self.label.SetValue('')
        self.LongRunning()

    def LongRunning(self):
        """
        This runs in the GUI thread but uses wx.Process and
        wx.Execute to start and monitor a separate process.
        """

        cmd = 'python -u external_program.py'

        self.process = wx.Process(self)
        self.process.Redirect()

        wx.Execute(cmd, wx.EXEC_ASYNC, self.process)

    def OnIdle(self, event):
        """ This event handler catches the process stdout. """

        if self.process is not None:
            stream = self.process.GetInputStream()
            if stream.CanRead():
                text = stream.read()
                self.label.AppendText(text)

    def OnProcessEnded(self, event):

        stream = self.process.GetInputStream()

        if stream.CanRead():
            text = stream.read()
            self.label.AppendText(text)

        self.btn.Enable(True)
        self.label.AppendText('Finished')


if __name__ == "__main__":
    app = wx.App(0)
    frame = ProcessFrame(None)
    frame.Show()
    app.MainLoop()
