
    # connect to the media event
    self.Bind(wx.media.EVT_MEDIA_STOP, self.OnMediaStop, self.mediactrl)

    # ...
    def OnMediaStop(self, evt):
        if self.userWantsToSeek:
            self.mediactrl.SetPosition(someOtherPosition)
            evt.Veto()

