
        # Write some text to the clipboard
        if wx.TheClipboard.Open():

            # This data objects are held by the clipboard,
            # so do not delete them in the app.
            wx.TheClipboard.SetData(wx.TextDataObject("Some text"))
            wx.TheClipboard.Close()

        # Read some text
        if wx.TheClipboard.Open():

            if wx.TheClipboard.IsSupported(wx.DF_TEXT):
            
                data = wx.TextDataObject()
                wx.TheClipboard.GetData(data)
                wx.MessageBox(data.GetText())
            
            wx.TheClipboard.Close()

