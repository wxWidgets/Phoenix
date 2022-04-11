
            # do the window-specific processing after processing the update event
            def DoUpdateWindowUI(self, event):

                if event.GetSetEnabled():
                    self.Enable(event.GetEnabled())

                if event.GetSetText():

                    if event.GetText() != self.GetTitle():
                        self.SetTitle(event.GetText())


