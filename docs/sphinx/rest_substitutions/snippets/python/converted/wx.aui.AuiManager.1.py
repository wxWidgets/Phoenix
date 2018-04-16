
    text1 = wx.TextCtrl(self)
    text2 = wx.TextCtrl(self)
    self.mgr.AddPane(text1, wx.LEFT, "Pane Caption")
    self.mgr.AddPane(text2, wx.BOTTOM, "Pane Caption")
    self.mgr.Update()
