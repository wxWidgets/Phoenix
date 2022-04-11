
        collpane = wx.CollapsiblePane(self, wx.ID_ANY, "Details:")

        # add the pane with a zero proportion value to the 'sz' sizer which contains it
        sz.Add(collpane, 0, wx.GROW | wx.ALL, 5)

        # now add a test label in the collapsible pane using a sizer to layout it:
        win = collpane.GetPane()
        paneSz = wx.BoxSizer(wx.VERTICAL)
        paneSz.Add(wx.StaticText(win, wx.ID_ANY, "test!"), 1, wx.GROW | wx.ALL, 2)
        win.SetSizer(paneSz)
        paneSz.SetSizeHints(win)
