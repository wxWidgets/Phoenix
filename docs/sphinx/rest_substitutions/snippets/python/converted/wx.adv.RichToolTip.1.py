
        password = wx.TextCtrl(parent, style=wx.TE_PASSWORD)

        # Later on...
        tip = wx.adv.RichToolTip("Caps Lock is on",
                                 "You might have made an error in your password\n"
                                 "entry because Caps Lock is turned on.\n"
                                 "\n"
                                 "Press Caps Lock key to turn it off.")
        tip.SetIcon(wx.ICON_WARNING)
        tip.ShowFor(password)
