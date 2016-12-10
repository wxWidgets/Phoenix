import wx

class MyDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, *args, **kw)

        # Widgets
        txt = wx.StaticText(self, label="Hello.  I am a Dialog!  Hear me roar!")
        ok = wx.Button(self, wx.ID_OK)
        ok.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        # Layout
        self.Sizer = wx.BoxSizer(wx.VERTICAL)  # using the Sizer property
        self.Sizer.Add(txt, 0, wx.ALL, 10)
        self.Sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)

        # make a new sizer to hold the buttons
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add((1,1), 1)  # a spacer that gets a portion of the free space
        row.Add(ok)
        row.Add((1,1), 1)
        row.Add(cancel)
        row.Add((1,1), 1)

        # add that sizer to the main sizer
        self.Sizer.Add(row, 0, wx.EXPAND|wx.ALL, 10)

        # size the dialog to fit the content managed by the sizer
        self.Fit()


app = wx.App()
dlg = MyDialog(None, title="Hello Dialog")
val = dlg.ShowModal()
dlg.Destroy()
app.MainLoop()