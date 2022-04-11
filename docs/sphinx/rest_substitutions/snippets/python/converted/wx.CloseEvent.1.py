
            def OnClose(self, event):

                if event.CanVeto() and self.fileNotSaved:

                    if wx.MessageBox("The file has not been saved... continue closing?",
                                     "Please confirm",
                                     wx.ICON_QUESTION | wx.YES_NO) != wx.YES:

                        event.Veto()
                        return

                self.Destroy()  # you may also do:  event.Skip()
                                # since the default event handler does call Destroy(), too

