
    # in a grid displaying music notation, use a solid black pen between
    # octaves (C0=row 127, C1=row 115 etc.)
    def GetRowGridLinePen(self, row):

        if row % 12 == 7:
            return wx.Pen(wx.BLACK, 1, wx.SOLID)
        else:
            return self.GetDefaultGridLinePen()
