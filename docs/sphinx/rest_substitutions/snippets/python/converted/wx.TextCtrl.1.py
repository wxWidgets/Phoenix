
        text.SetDefaultStyle(wx.TextAttr(wx.RED))
        text.AppendText("Red text\n")
        text.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.LIGHT_GREY))
        text.AppendText("Red on grey text\n")
        text.SetDefaultStyle(wx.TextAttr(wx.BLUE))
        text.AppendText("Blue on grey text\n")
