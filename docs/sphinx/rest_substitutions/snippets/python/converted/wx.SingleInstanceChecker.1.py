
        def OnInit(self):

            self.name = "SingleApp-%s" % wx.GetUserId()
            self.instance = wx.SingleInstanceChecker(self.name)

            if self.instance.IsAnotherRunning():
                wx.MessageBox("Another instance is running", "ERROR")
                return False

            frame = SingleAppFrame(None, "SingleApp")
            frame.Show()
            return True

