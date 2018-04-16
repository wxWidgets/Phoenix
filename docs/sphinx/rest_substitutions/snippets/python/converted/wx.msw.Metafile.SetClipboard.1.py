
    dc = wx.MetafileDC()
    if dc.IsOk():
        self.DoDrawing(dc)
        metafile = dc.Close()
        if metafile:
            success = metafile.SetClipboard(dc.MaxX() + 10, dc.MaxY() + 10)


