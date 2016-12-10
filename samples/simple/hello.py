import sys, os, platform, wx
print(wx.version()); print(sys.version)

app = wx.App()
frm = wx.Frame(None, title="Hello World!", size=(400,275))
pnl = wx.Panel(frm)
pnl.BackgroundColour = 'sky blue'

st = wx.StaticText(pnl, -1, 'Hello World!', (15,10))
st.SetFont(wx.FFont(14, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD))

st = wx.StaticText(pnl, pos=(15,40),
        label='This is wxPython %s\nrunning on Python %s %s' %
        (wx.version(), sys.version.split(' ')[0], platform.architecture()[0]))
st.SetFont(wx.FFont(10, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD))

bmp = wx.Bitmap(os.path.join(os.path.dirname(__file__), 'phoenix_main.png'))
sb = wx.StaticBitmap(pnl, label=bmp, pos=(15,85))

frm.Show()
app.MainLoop()


