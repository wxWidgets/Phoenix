
        # Create the initially empty label with the size big enough to show
        # the given string.
        dc = wx.ClientDC(self)
        text = wx.StaticText(
            self,
            size=dc.GetTextExtent("String of max length"),
            style=wx.ST_NO_AUTORESIZE
           )
