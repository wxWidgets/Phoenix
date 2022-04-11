
        items = ["meat", "fish", "fruits", "beer"]
        order = [3, 0, 1, 2]

        dlg = wx.RearrangeDialog(None,
                                 "You can also uncheck the items you don't like "
                                 "at all.",
                                 "Sort the items in order of preference",
                                 order, items)

        if dlg.ShowModal() == wx.ID_OK:
            order = dlg.GetOrder()
            for n in order:
                if n >= 0:
                    wx.LogMessage("Your most preferred item is \"%s\""%n)
                    break



