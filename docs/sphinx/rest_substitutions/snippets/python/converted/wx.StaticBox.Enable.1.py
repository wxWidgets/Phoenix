
    check = wx.CheckBox(parent, wx.ID_ANY, "Use the box")
    box = wx.StaticBox(parent, wx.ID_ANY, check)
    check.Bind(wx.EVT_CHECKBOX, lambda evt: box.Enable(evt.IsChecked()))

