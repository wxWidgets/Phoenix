
    class EncryptHook(wx.FileDialogCustomizeHook):

        def __init__(self):
            super().__init__()
            self.encrypt = False

        # Override to add custom controls using the provided customizer object.
        def AddCustomControls(self, customizer):

            # Suppose we can encrypt files when saving them.
            self.checkbox = customizer.AddCheckBox("Encrypt")

            # While self.checkbox is not really a wx.CheckBox, it looks almost like one
            # and, in particular, we can bind to custom control events as usual.
            self.checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheckbox)

            # The encryption parameters can be edited in a dedicated dialog.
            self.button = customizer.AddButton("Parameters...")
            self.button.Bind(wx.EVT_BUTTON, self.OnButton)

        def OnCheckbox(self, event):
            self.button.Enable(event.IsChecked())

        def OnButton(self, event):
            ... show the encryption parameters dialog here ...


        # Override this to save the values of the custom controls.
        def TransferDataFromCustomControls(self):
            # Save the checkbox value, as we won't be able to use it any more
            # once this function returns.
            self.encrypt = self.checkbox.GetValue()

    ...

    def SomeOtherEventHandlerFunc(self, event):

        dialog = wx.FileDialog(None, "Save document", "", "file.my",
                    "My files (*.my)|*.my", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        # This object may be destroyed before the dialog, but must remain alive
        # until ShowModal() returns. So you should hold a separate reference to
        # it.
        customizeHook = EncryptHook()
        dialog.SetCustomizeHook(customizeHook)

        if dialog.ShowModal() == wx.ID_OK:
            if (customizeHook.encrypt)
                ... save with encryption ...
            else:
                ... save without encryption ...

        dialog.Destroy()
