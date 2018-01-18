
        class MyRearrangeDialog(wx.RearrangeDialog):

            def __init__(self, parent):

                wx.RearrangeDialog.__init__(self, parent)

                panel = wx.Panel(self)
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                sizer.Add(wx.StaticText(panel, wx.ID_ANY,
                                        "Column width in pixels:"))
                sizer.Add(wx.TextCtrl(panel, wx.ID_ANY, ""))
                panel.SetSizer(sizer)
                self.AddExtraControls(panel)


                # ... code to update the text control with the currently selected
                # item width and to react to its changes omitted ...

