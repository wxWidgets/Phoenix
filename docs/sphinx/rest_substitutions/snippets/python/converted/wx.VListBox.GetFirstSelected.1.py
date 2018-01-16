
            item, cookie = vlbox.GetFirstSelected()
            while item != wx.NOT_FOUND:
                # ... process item ...
                item, cookie = vlbox.GetNextSelected(cookie)

