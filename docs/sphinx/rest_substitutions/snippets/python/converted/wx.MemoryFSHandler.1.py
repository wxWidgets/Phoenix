
        def OnAbout(self, event):

            bcur = wx.BeginBusyCursor()

            wx.FileSystem.AddHandler(wx.MemoryFSHandler)
            wx.MemoryFSHandler.AddFile("logo.pcx", wx.Bitmap("logo.pcx", wx.BITMAP_TYPE_PCX))
            wx.MemoryFSHandler.AddFile("about.htm",
                                       "<html><body>About: "
                                       "<img src=\"memory:logo.pcx\"></body></html>")

            dlg = wx.Dialog(self, -1, _("About"))

            topsizer = wx.BoxSizer(wx.VERTICAL)

            html = wx.html.HtmlWindow(dlg, size=wx.Size(380, 160), style=wx.HW_SCROLLBAR_NEVER)
            html.SetBorders(0)
            html.LoadPage("memory:about.htm")
            html.SetSize(html.GetInternalRepresentation().GetWidth(),
                         html.GetInternalRepresentation().GetHeight())

            topsizer.Add(html, 1, wx.ALL, 10)
            topsizer.Add(wx.StaticLine(dlg, -1), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
            topsizer.Add(wx.Button(dlg, wx.ID_OK, "Ok"),
                         0, wx.ALL | wx.ALIGN_RIGHT, 15)

            dlg.SetAutoLayout(True)
            dlg.SetSizer(topsizer)
            topsizer.Fit(dlg)
            dlg.Centre()
            dlg.ShowModal()

            wx.MemoryFSHandler.RemoveFile("logo.pcx")
            wx.MemoryFSHandler.RemoveFile("about.htm")

