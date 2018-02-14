
       info = wx.BusyInfo(
                wx.BusyInfoFlags()
                    .Parent(self)
                    .Icon(wx.ArtProvider.GetIcon(wx.ART_PRINT,
                                                 wx.ART_OTHER, wx.Size(128, 128)))
                    .Title("<b>Printing your document</b>")
                    .Text("Please wait...")
                    .Foreground(wx.WHITE)
                    .Background(wx.BLACK)
                    .Transparency(4 * wx.ALPHA_OPAQUE / 5)
            )
