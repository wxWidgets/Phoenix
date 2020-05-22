
    # Some function for redrawing using the given colour. Ideally, it
    # shouldn't do anything if the colour is the same as the one used
    # before.
    def Redraw(self, colour):
        ...

    def OnColourChanged(self, event):
        self.Redraw(event.GetColour())

    def SelectNewColour(self):
        data = wx.ColourData()
        data.SetColour(initialColourToUse)
        dlg = wx.ColourDialog(self, data)
        dlg.Bind(wx.EVT_COLOUR_CHANGED, self.OnColourChanged)
        if (dlg.ShowModal() == wx.ID_OK)
            # Colour did change.
        else
            # Colour didn't change.

        # This call is unnecessary under platforms generating
        # wx.EVT_COLOUR_CHANGED if the dialog was accepted and unnecessary
        # under the platforms not generating this event if it was cancelled,
        # so we could check for the different cases explicitly to avoid it,
        # but it's simpler to just always call it.
        Redraw(data.GetColour())
