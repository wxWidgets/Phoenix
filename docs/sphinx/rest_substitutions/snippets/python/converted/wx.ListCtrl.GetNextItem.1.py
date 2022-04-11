
            item = -1

            while 1:
                item = listctrl.GetNextItem(item,
                                            wx.LIST_NEXT_ALL,
                                            wx.LIST_STATE_SELECTED)
                if item == -1:
                    break

                # This item is selected - do whatever is needed with it
                wx.LogMessage("Item %ld is selected"%item)

