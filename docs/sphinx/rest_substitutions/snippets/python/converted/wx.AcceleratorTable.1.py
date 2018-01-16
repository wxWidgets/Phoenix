
    entries = [wx.AcceleratorEntry() for i in xrange(4)]

    entries[0].Set(wx.ACCEL_CTRL, ord('N'), ID_NEW_WINDOW)
    entries[1].Set(wx.ACCEL_CTRL, ord('X'), wx.ID_EXIT)
    entries[2].Set(wx.ACCEL_SHIFT, ord('A'), ID_ABOUT)
    entries[3].Set(wx.ACCEL_NORMAL, wx.WXK_DELETE, wx.ID_CUT)

    accel = wx.AcceleratorTable(entries)
    frame.SetAcceleratorTable(accel)
