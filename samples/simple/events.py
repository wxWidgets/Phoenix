from __future__ import print_function

import wx

print(wx.version())
#import os; print('PID:', os.getpid()); raw_input('Ready to start, press enter...')


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self.Bind(wx.EVT_SIZE, self.onSize)
        wx.CallAfter(self.after, 1, 2, 3)

    def after(self, a, b, c):
        print('Called via wx.CallAfter:', a, b, c)

    def onSize(self, evt):
        print(repr(evt.Size))
        evt.Skip()

class MyApp(wx.App):
    def OnInit(self):
        print('OnInit')
        frm = MyFrame(None, title="Hello with Events", size=(480,360))
        frm.Show()
        return True

    def OnExit(self):
        print('OnExit')
        return 0

app = MyApp()
app.MainLoop()

