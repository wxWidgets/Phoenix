    
        def AskUser(self):
        
            dlg = MyAskDialog(self)

            if dlg.ShowModal() == wx.ID_OK:
                # do something here
                print 'Hello'
                
            # else: dialog was cancelled or some another button pressed
    
            dlg.Destroy()
        
