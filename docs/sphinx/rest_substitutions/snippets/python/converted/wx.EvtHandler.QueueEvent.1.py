
                def FunctionInAWorkerThread(strs):

                    evt = wx.CommandEvent()

                    evt.SetString(strs)

                    wx.TheApp.QueueEvent(evt)

