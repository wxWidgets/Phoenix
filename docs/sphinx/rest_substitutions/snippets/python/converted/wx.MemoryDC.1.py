
        # Create a memory DC
        temp_dc = wx.MemoryDC()
        temp_dc.SelectObject(test_bitmap)

        # We can now draw into the memory DC...
        # Copy from this DC to another DC.
        old_dc.Blit(250, 50, BITMAP_WIDTH, BITMAP_HEIGHT, temp_dc, 0, 0)
