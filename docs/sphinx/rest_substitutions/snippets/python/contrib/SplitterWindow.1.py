##Andrea Gavana
#!/usr/bin/env python

# This sample shows how to create a "spli-split" window, i.e. a
# window split vertical which contains two windows split horizontally

import wx

class SplitterFrame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, title='SplitterWindow example')

        # Create the main splitter window (to be split vertically)
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(100)

        panel1 = wx.Panel(splitter, -1)

        static = wx.StaticText(panel1, -1, 'Hello World', pos=(10, 100))
        panel1.SetBackgroundColour(wx.WHITE)

        # Create the second splitter window (to be split horizontally)
        splitter2 = wx.SplitterWindow(splitter, -1, style=wx.SP_LIVE_UPDATE)
        splitter2.SetMinimumPaneSize(100)

        panel2 = wx.Panel(splitter2, -1)
        panel2.SetBackgroundColour(wx.BLUE)

        panel3 = wx.Panel(splitter2, -1)
        panel3.SetBackgroundColour(wx.RED)

        splitter2.SplitHorizontally(panel2, panel3)
        splitter.SplitVertically(panel1, splitter2)
        self.Centre()


if __name__ == '__main__':
    app = wx.App(0)
    frame = SplitterFrame()
    frame.Show()
    app.MainLoop()