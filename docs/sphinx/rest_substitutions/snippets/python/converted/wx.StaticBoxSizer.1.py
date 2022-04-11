
            def CreateControls(self):

                panel = wx.Panel(self)
                # Other controls here...

                sz = wx.StaticBoxSizer(wx.VERTICAL, panel, "Box")
                sz.Add(wx.StaticText(sz.GetStaticBox(), wx.ID_ANY,
                                     "This window is a child of the staticbox"))

                # Other code...

