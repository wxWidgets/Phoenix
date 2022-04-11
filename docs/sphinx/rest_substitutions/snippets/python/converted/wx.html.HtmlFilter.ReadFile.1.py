
    def ReadFile(file):

        # file is a wx.FSFile in this case...
        return "<html><body><img src=\"" + file.GetLocation() + \
               "\"></body></html>"
