
    panel = wx.Panel()      # Note: default constructor used.
    panel.Hide()            # Can be called before actually creating it.
    panel.Create(parent, wx.ID_ANY, ...) # Won't be shown yet.
    ... create all the panel children ...
    panel.Show()            # Now everything will be shown at once.
