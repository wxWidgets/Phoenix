
        if wx.GetApp().GetComCtl32Version() >= 600 and wx.DisplayDepth() >= 32:
            # Use the 32-bit images
            wx.SystemOptions.SetOption("msw.remap", 2)
