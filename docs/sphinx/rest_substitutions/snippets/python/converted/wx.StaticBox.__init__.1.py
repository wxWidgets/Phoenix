    
    # NOTE: wxPython doesn't yet support using a control in place of the label...
    panel = wx.Panel(self)
    checkbox = wx.CheckBox(panel, wx.ID_ANY, "Box checkbox")
    box = wx.StaticBox(panel, wx.ID_ANY, checkbox)

