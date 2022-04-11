##Andrea Gavana
#!/usr/bin/env python

# This sample shows how to listen to a move change event for a
# top-level window (wx.Frame, wx.Dialog). This is MSW-specific

import wx

class MovingFrame(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title)

        wx.StaticText(self, label='x:', pos=(10, 10))
        wx.StaticText(self, label='y:', pos=(10, 30))

        self.st1 = wx.StaticText(self, label='', pos=(30, 10))
        self.st2 = wx.StaticText(self, label='', pos=(30, 30))

        self.Bind(wx.EVT_MOVE, self.OnMove)

        self.Show()

    def OnMove(self, event):

        # Capture the mouse position (in screen coordinates) and
        # assign its x, y values to the statictexts
        x, y = event.GetPosition()
        self.st1.SetLabel('%d'%x)
        self.st2.SetLabel('%d'%y)


app = wx.App(False)
frame = MovingFrame(None, 'MoveEvent example')
app.MainLoop()
