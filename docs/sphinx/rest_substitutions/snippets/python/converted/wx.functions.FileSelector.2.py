
        filename = wx.FileSelector("Choose a file to open")

        if filename.strip():
            # work with the file
            print filename

        # else: cancelled by user
