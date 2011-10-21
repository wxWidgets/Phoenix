import wx
print wx.version()
#import os; print 'PID:', os.getpid(); raw_input('Ready to start, press enter...')
 
app = wx.App()
frm = wx.Frame(None, title="Hello World!")

pnl = wx.Panel(frm)
pnl.BackgroundColour = 'sky blue'
st = wx.StaticText(pnl, -1, 'This is wxPython\n%s' % wx.version(), (15,15))
st.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD))

frm.Show()
app.MainLoop()

    
