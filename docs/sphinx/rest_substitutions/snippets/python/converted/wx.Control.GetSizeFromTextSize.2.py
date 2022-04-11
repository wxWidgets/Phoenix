
    # Create a control for post code entry.
    postcode = wx.TextCtrl(self, -1, "")

    # And set its initial and minimal size to be big enough for
    # entering 5 digits.
    postcode.SetInitialSize(
        postcode.GetSizeFromTextSize(
            postcode.GetTextExtent("99999")))
