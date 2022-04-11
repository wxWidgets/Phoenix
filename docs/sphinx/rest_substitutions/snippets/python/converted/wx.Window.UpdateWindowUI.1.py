
            def OnInternalIdle(self):

                if wx.UpdateUIEvent.CanUpdate(self):
                    self.UpdateWindowUI(wx.UPDATE_UI_FROMIDLE)

