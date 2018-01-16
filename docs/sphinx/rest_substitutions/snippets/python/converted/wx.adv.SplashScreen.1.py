
        bitmap = wx.Bitmap('splash16.png', wx.BITMAP_TYPE_PNG)

        splash = wx.adv.SplashScreen(bitmap, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                     6000, None, -1, wx.DefaultPosition, wx.DefaultSize,
                                     wx.BORDER_SIMPLE | wx.STAY_ON_TOP)

        wx.Yield()
