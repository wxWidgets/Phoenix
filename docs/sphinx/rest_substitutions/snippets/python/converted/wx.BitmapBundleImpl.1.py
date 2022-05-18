
        class MyCustomBitmapBundleImpl(wx.BitmapBundleImpl):
            def __init__(self):
                super().__init__()
                self.img = wx.Image(pngFile)
                self.size = self.img.GetSize()

            def GetDefaultSize(self):
                # Report the best or default size for the bitmap
                return self.size

            def GetPreferredBitmapSizeAtScale(self, scale):
                # Return the size of the bitmap at the given display scale. It
                # doesn't need to be size*scale if there are unscaled bitmaps
                # near that size.
                return self.size * scale

            def GetBitmap(self, size):
                # Return the version of the bitmap at the desired size
                img = self.img.Scale(size.width, size.height)
                return wx.Bitmap(img)



    toolBar.AddTool(wx.ID_OPEN, wx.BitmapBundle.FromImpl(MyCustomBitmapBundleImpl())
