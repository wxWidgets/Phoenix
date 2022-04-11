

        # Some integer...
        l = value
        return wx.SpinCtrl(parent, wx.ID_ANY, "",
                           labelRect.GetTopLeft(), labelRect.GetSize(), 0, 0, 100, l)
