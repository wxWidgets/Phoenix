
            def CreateControls(self):

                panel = wx.Panel(self)
                box = wx.StaticBox(panel, wx.ID_ANY, "StaticBox")

                text = wx.StaticText(box, wx.ID_ANY, "This window is a child of the staticbox")

                # Other code...
