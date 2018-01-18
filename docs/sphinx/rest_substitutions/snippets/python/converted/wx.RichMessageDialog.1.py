
    def ShowDialog(self):

        if dont_show:
            return

        dlg = wx.RichMessageDialog(self, "Welcome to my wonderful program!")
        dlg.ShowCheckBox("Don't show welcome dialog again")
        dlg.ShowModal() # return value ignored as we have "Ok" only anyhow

        if dlg.IsCheckBoxChecked():
            # ... make sure we won't show it again the next time ...
            dont_show = True
