    
        def OnSaveAs(self, event):
        
            saveFileDialog = wx.FileDialog(self, "Save XYZ file", "", "",
                                           "XYZ files (*.xyz)|*.xyz", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    
            if saveFileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed idea...
            
            # save the current contents in the file
            # this can be done with e.g. wxPython output streams:
            output_stream = wx.FileOutputStream(saveFileDialog.GetPath())
            
            if not output_stream.IsOk():            
                wx.LogError("Cannot save current contents in file '%s'."%saveFileDialog.GetPath())
                return
            
