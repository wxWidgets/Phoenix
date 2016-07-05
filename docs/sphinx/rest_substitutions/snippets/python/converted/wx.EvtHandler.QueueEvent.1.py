    
                def FunctionInAWorkerThread(strs):
                
                    evt = wx.CommandEvent()
    
                    # NOT evt.SetString(strs) as this would be a shallow copy
                    evt.SetString(strs[:]) # make a deep copy
    
                    wx.TheApp.QueueEvent(evt)
                
