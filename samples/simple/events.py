
import wxPhoenix as wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self.Bind(wx.EVT_SIZE, self.onSize)
        
    def onSize(self, evt):
        print repr(evt.Size)
        
app = wx.App()
frm = MyFrame(None, title="Hello Events", size=(480,360))
frm.Show()
app.MainLoop()

