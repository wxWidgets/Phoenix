import wxPhoenix as wx
app = wx.PySimpleApp()  # Should see a deprecation warning here
frm = wx.Frame(None)
frm.Show()
app.MainLoop()

