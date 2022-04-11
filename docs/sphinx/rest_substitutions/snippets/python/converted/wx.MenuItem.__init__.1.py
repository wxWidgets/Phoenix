
            # use all stock properties:
            helpMenu.Append(wx.ID_ABOUT)

            # use the stock label and the stock accelerator but not the stock help string:
            helpMenu.Append(wx.ID_ABOUT, "", "My custom help string")

            # use all stock properties except for the bitmap:
            mymenu = wx.MenuItem(helpMenu, wx.ID_ABOUT)
            mymenu.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_WARNING))
            helpMenu.Append(mymenu)
