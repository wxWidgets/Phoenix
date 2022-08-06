
    class MyWindow(wx.Window):
        ...
        def OnPaint(self, event):
        bmp = wx.Bitmap();
        bmp.CreateWithDIPSize(self.GetClientSize(), self.GetDPIScaleFactor())

        memdc = wx.MemoryDC(bmp)
        ... use memdc to draw on the bitmap ...

        dc = wx.PaintDC(self)
        dc.DrawBitmap(bmp, wx.Point(0, 0))
