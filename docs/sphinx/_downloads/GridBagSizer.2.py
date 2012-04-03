##Chris Barker
#!/usr/bin/env python

import wx

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        t = wx.TextCtrl(self)

        b1 = wx.Button(self, label="Button1")
        b2 = wx.Button(self, label="Button2")

        exitBut = wx.Button(self, label="Exit")
        exitBut.Bind(wx.EVT_BUTTON, self.OnCloseWindow)

        sizer = wx.GridBagSizer(10, 10)
        sizer.Add(t,  (0,0), span=(2,1), flag=wx.ALIGN_CENTER_VERTICAL )
        sizer.Add(b1, (0,1), span=(2,1), flag=wx.ALIGN_CENTER)
        sizer.Add(b2, (0,2), flag=wx.ALIGN_CENTER)

        sizer.Add(exitBut, (1,3))

        self.SetSizerAndFit(sizer)

        wx.EVT_CLOSE(self, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()

class App(wx.App):
    def OnInit(self):
        frame = TestFrame(None, title="GridBagSizer Test")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = App(0)
    app.MainLoop()


