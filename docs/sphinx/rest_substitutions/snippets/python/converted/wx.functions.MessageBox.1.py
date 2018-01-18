
        answer = wx.MessageBox("Quit program?", "Confirm",
                               wx.YES_NO | wx.CANCEL, main_frame)
        if answer == wx.YES:
            main_frame.Close()
