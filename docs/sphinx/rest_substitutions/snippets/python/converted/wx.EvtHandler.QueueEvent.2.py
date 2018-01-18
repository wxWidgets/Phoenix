
                def FunctionInAWorkerThread(strs):

                    evt = wx.ThreadEvent()
                    evt.SetString(strs)

                    # wx.ThreadEvent.Clone() makes sure that the internal wx.String
                    # member is not shared by other string instances:
                    wx.TheApp.QueueEvent(evt.Clone())

