
                class MyHeaderColumn(wx.HeaderColumn):

                    def __init__(self):

                        wx.HeaderColumn.__init__(self)


                    def SetWidth(self, width):

                        self.width = width


                    def GetWidth(self):

                        return self.width


                class MyHeaderCtrl(wx.HeaderCtrl):

                    def __init__(self, parent):

                        wx.HeaderCtrl.__init__(self, parent)
                        self.cols = []


                    def GetColumn(idx):

                        return self.cols[idx]


                    def UpdateColumnWidthToFit(self, idx, widthTitle):

                        # ... compute minimal width for column idx ...
                        widthContents = self.CalculateMinWidth(idx)
                        self.cols[idx].SetWidth(max(widthContents, widthTitle))

                        return True


