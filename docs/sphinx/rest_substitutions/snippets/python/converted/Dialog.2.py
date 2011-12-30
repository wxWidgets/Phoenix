
        def AskUser(self):
        
            dlg = MyAskDialog(self)

            if dlg.ShowModal() == wx.ID_OK:
                # do something here
                print 'Hello'
                
            # no need to call Destroy() here
    
