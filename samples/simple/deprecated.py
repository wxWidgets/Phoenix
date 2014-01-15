import wx
print(wx.version())

class TestPanel(wx.PyPanel):
    def __init__(self, *args, **kw):
        wx.PyPanel.__init__(self, *args, **kw)  # You should see a deprecation warning here
        self.BackgroundColour = "#66CDAA"

app = wx.PySimpleApp()  # You should see a deprecation warning here

frm = wx.Frame(None)
pnl = TestPanel(frm)
frm.Show()

app.MainLoop()

