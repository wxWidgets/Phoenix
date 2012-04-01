##Chris Barker
#!/usr/bin/env python

"""
A simple test of the GridBagSizer

http://wiki.wxpython.org/index.cgi/WriteItYourself

"""

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition)

        Buttons = []
        for i in range(6):
            Buttons.append(wx.Button(self,-1, "Button %i"%(i)))

        sizer = wx.GridBagSizer(9, 9)
        sizer.Add(Buttons[0], (0, 0), wx.DefaultSpan,  wx.ALL, 5)
        sizer.Add(Buttons[1], (1, 1), (1,7), wx.EXPAND)
        sizer.Add(Buttons[2], (6, 6), (3,3), wx.EXPAND)
        sizer.Add(Buttons[3], (3, 0), (1,1), wx.ALIGN_CENTER)
        sizer.Add(Buttons[4], (4, 0), (1,1), wx.ALIGN_LEFT)
        sizer.Add(Buttons[5], (5, 0), (1,1), wx.ALIGN_RIGHT)

        sizer.AddGrowableRow(6)
        sizer.AddGrowableCol(6)

        self.SetSizerAndFit(sizer)
        self.Centre()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "wx.gridbagsizer.py")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

