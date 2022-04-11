##Andrea Gavana
#!/usr/bin/env python

# This sample shows a simple example of how to use the
# "Bind" method to handle an event

import wx

class MainWindow(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title)

        # Bind the "close window" event to the OnClose handler
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Show()


    def OnClose(self, event):

        # This displays a message box asking the user to confirm
        # she wants to quit the application
        dlg = wx.MessageDialog(self, 'Are you sure you want to quit?', 'Question',
                               wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            self.Destroy()
        else:
            event.Veto()


app = wx.App(False)
frame = MainWindow(None, 'Bind example')
app.MainLoop()
