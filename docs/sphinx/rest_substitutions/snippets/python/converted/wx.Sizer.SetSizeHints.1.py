
        # In a frame's __init__
        ...
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(...)
        sizer.Add(...)
        panel.SetSizer(sizer)

        # Use the panel sizer to set the initial and minimal size of the
        # frame to fit its contents.
        sizer.SetSizeHints(self)
