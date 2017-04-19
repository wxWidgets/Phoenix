    
        def OnOpen(self, event):
        
            if self.contentNotSaved:
            
                if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                                 wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                    return
                
                # else: proceed asking to the user the new file to open
            
                openFileDialog = wx.FileDialog(self, "Open XYZ file", "", "",
                                               "XYZ files (*.xyz)|*.xyz", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    
                if openFileDialog.ShowModal() == wx.ID_CANCEL:
                    return     # the user changed idea...
                
                # proceed loading the file chosen by the user
                # this can be done with e.g. wxPython input streams:
                input_stream = wx.FileInputStream(openFileDialog.GetPath())
                
                if not input_stream.IsOk():
                
                    wx.LogError("Cannot open file '%s'."%openFileDialog.GetPath())
                    return
                
            