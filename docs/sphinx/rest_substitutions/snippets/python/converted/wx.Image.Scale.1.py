
            # get the bitmap from somewhere
            bmp = wx.Bitmap('my_png.png', wx.BITMAP_TYPE_PNG)

            # rescale it to have size of 32*32
            if bmp.GetWidth() != 32 or bmp.GetHeight() != 32:

                image = bmp.ConvertToImage()
                bmp = wx.Bitmap(image.Scale(32, 32))

                # another possibility:
                image.Rescale(32, 32)
                bmp = wx.Bitmap(image)

