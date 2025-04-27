
    class MyCustomBitmapBundleImpl(wx.BitmapBundleImpl):

        def GetDefaultSize():
            return wx.Size(32, 32)

        def GetPreferredBitmapSizeAtScale(self, scale):
            return self.DoGetPreferredSize(scale)

        def GetBitmap(self, size):
            # For consistency with GetNextAvailableScale(), we must have
            # bitmap variants for 32, 48 and 64px sizes.
            availableSizes =  [32, 48, 64]
            if (size.y <= 64)
                ... get the bitmap from somewhere ...
            else:
                n = self.GetIndexToUpscale(size)
                bitmap = ... get bitmap for availableSizes[n] ...
                wx.Bitmap.Rescale(bitmap, size)
            return bitmap

        def GetNextAvailableScale(self, idx):
            # The zero marks the end of available scales, and it means this
            # method won't be called again after the zero is returned.
            availableScales =  [1.0, 1.5, 2.0, 0]
            scale = availableScales[idx]
            idx += 1
            return (scale, idx)
