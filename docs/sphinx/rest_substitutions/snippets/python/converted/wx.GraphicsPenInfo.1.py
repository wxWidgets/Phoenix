    
    ctx = wx.GraphicsContext.Create(dc)
    pen = ctx.CreatePen(wx.GraphicsPenInfo(wx.BLUE).Width(1.25).Style(wx.PENSTYLE_DOT))
    ctx.SetPen(pen)
