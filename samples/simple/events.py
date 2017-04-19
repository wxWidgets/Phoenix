
import wx
from six import print_

print_(wx.version())
#import os; print_('PID:', os.getpid()); raw_input('Ready to start, press enter...')


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self.Bind(wx.EVT_SIZE, self.onSize)
        wx.CallAfter(self.after, 1, 2, 3)

    def after(self, a, b, c):
        print_('Called via wx.CallAfter:', a, b, c)

    def onSize(self, evt):
        print_(repr(evt.Size))
        evt.Skip()

class MyApp(wx.App):
    def OnInit(self):
        print_('OnInit')
        frm = MyFrame(None, title="Hello with Events", size=(480,360))
        frm.Show()
        return True

    def OnExit(self):
        print_('OnExit')
        return 0

app = MyApp()
app.MainLoop()

