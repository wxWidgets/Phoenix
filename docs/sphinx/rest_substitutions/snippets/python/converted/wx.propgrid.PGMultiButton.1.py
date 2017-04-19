
    class SampleMultiButtonEditor(wx.propgrid.PGTextCtrlEditor):

        def GetName(self):
            return "SampleMultiButtonEditor"

        def CreateControls(self, propGrid, aProperty, pos, size):
            # Create and populate buttons-subwindow
            buttons = wx.propgrid.PGMultiButton(propGrid, size)

            # Add two regular buttons
            buttons.Add("...")
            buttons.Add("A")

            # Add a bitmap button
            buttons.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER))

            # Create the 'primary' editor control (textctrl in self case)
            wndList = wx.propgrid.PGTextCtrlEditor.CreateControls(
                            propGrid, aProperty, pos, buttons.GetPrimarySize())

            # Finally, move buttons-subwindow to correct position and make sure
            # returned wx.propgrid.PGWindowList contains our custom button list.
            buttons.Finalize(propGrid, pos)
            wndList.SetSecondary(buttons)
            return wndList


        def OnEvent(self, propGrid, aProperty, ctrl, event):
            if event.GetEventType() == wx.wxEVT_BUTTON:
                buttons = propGrid.GetEditorControlSecondary()
                if event.GetId() == buttons.GetButtonId(0):
                    # Do something when the first button is pressed
                    # Return true if the action modified the value in editor.
                    ...

                if event.GetId() == buttons.GetButtonId(1):
                    # Do something when the second button is pressed
                    ...

                if event.GetId() == buttons.GetButtonId(2):
                    # Do something when the third button is pressed
                    ...

            return wx.propgrid.PGTextCtrlEditor.OnEvent(propGrid, aProperty, ctrl, event)

