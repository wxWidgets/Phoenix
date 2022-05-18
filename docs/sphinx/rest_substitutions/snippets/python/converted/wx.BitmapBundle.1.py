
        # In __init__ for a wx.Frame
        ...
        toolBar = self.CreateToolBar()
        bitmaps = [ wx.Bitmap('open_32x32.png'),
                    wx.Bitmap('open_32x32.png'),
                    wx.Bitmap('open_32x32.png') ]
        toolBar.AddTool(wx.ID_OPEN, wx.BitmapBundle.FromBitmaps(bitmaps))
