
        def EmbedHTML(self):
            # self.embeddedHelpWindow is a wx.html.HtmlHelpWindow
            # self.embeddedHtmlHelp is a wx.html.HtmlHelpController

            # Create embedded HTML Help window
            self.embeddedHelpWindow = wx.html.HtmlHelpWindow
            self.embeddedHtmlHelp.UseConfig(config, rootPath) # Set your own config object here
            self.embeddedHtmlHelp.SetHelpWindow(self.embeddedHelpWindow)
            self.embeddedHelpWindow.Create(self, wx.ID_ANY, wx.DefaultPosition, self.GetClientSize(),
                                           wx.TAB_TRAVERSAL | wx.BORDER_NONE, wx.html.HF_DEFAULT_STYLE)
            self.embeddedHtmlHelp.AddBook("doc.zip")
