
    def CanRead(file):

        # file is a wx.FSFile in this case...
        return (file.GetMimeType() == "application/x-ugh")


