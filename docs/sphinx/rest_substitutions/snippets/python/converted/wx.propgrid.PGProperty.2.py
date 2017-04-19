
    def OnButtonClick(self, propGrid, value):
        dlgSize = wx.Size(... size of your dialog ...)
        dlgPos = propGrid.GetGoodEditorDialogPosition(self, dlgSize)

        # Create dialog dlg at dlgPos. Use value as initial string
        # value.
        with MyCustomDialog(None, title, pos=dlgPos, size=dlgSize) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                value = dlg.GetStringValue()
                return (True, value)
            return (False, value)
