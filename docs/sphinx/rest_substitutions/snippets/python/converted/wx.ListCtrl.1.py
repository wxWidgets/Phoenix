
    listctrl = wx.ListCtrl(...)
    for i in range(3):
        listctrl.InsertColumn(i, wx.String.Format("Column %d", i))

    order = [ 2, 0, 1]
    listctrl.SetColumnsOrder(order)

    # Now listctrl.GetColumnsOrder() will return order and
    # listctrl.GetColumnIndexFromOrder(n) will return order[n] and
    # listctrl.GetColumnOrder() will return 1, 2 and 0 for the column 0, 1 and 2
    # respectively.
