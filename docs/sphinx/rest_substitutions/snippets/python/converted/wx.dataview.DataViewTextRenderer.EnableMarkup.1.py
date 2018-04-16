    
    renderer = wx.DataViewTextRenderer()
    renderer.EnableMarkup()
    dataViewCtrl.AppendColumn(wx.DataViewColumn("title", renderer, 0))
