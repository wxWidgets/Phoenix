
    listctrl = wx.dataview.DataViewListCtrl(parent, wx.ID_ANY)

    listctrl.AppendToggleColumn("Toggle")
    listctrl.AppendTextColumn("Text")

    data = [True, "row 1"]
    listctrl.AppendItem(data)

    data = [False, "row 3"]
    listctrl.AppendItem(data)
