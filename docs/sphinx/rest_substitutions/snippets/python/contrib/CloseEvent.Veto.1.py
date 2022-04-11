##Andrea Gavana
#!/usr/bin/env python

# This sample makes the main frame "immortal", i.e., non-closable
# by the user. The main window can not be close by pressing Alt+F4
# or by clicking on the "X" button in the titlebar

import wx

class MainWindow(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title)

        # Bind the "close window" event to the OnClose handler
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Show()
        self.close_attempts = 0


    def OnClose(self, event):

        # Veto the event the user can not close the main
        # window in any way
        self.close_attempts += 1
        print('I am immortal %d'%self.close_attempts)
        event.Veto()


app = wx.App(False)
frame = MainWindow(None, 'Immortal Frame')
app.MainLoop()
