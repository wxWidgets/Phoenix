
    entries = [wx.AcceleratorEntry() for i in xrange(4)]
    
    entries[0].Set(wx.ACCEL_CTRL, 'N', ID_NEW_WINDOW)
    entries[1].Set(wx.ACCEL_CTRL, 'X', wx.ID_EXIT)
    entries[2].Set(wx.ACCEL_SHIFT, 'A', ID_ABOUT)
    entries[3].Set(wx.ACCEL_NORMAL, wx.WXK_DELETE, wx.ID_CUT)

    accel = wx.AcceleratorTable(entries)
    frame.SetAcceleratorTable(accel)