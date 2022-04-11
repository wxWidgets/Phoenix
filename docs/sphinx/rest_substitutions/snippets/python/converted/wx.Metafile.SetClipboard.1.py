    
    dc = wx.MetafileDC()
    if dc.IsOk():
        self.Draw(dc)
        mf = dc.Close()
        if mf:
            mf.SetClipboard(dc.MaxX() + 10, dc.MaxY() + 10)

