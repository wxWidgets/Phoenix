
        # Write some text to the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject("Some text"))
            wx.TheClipboard.Close()


        # Test if text content is available
        not_empty = wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_UNICODETEXT))


        # Read some text
        text_data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(text_data)
            wx.TheClipboard.Close()
        if success:
            return text_data.GetText()

