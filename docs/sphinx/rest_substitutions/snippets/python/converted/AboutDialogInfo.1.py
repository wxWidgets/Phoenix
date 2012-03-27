    
        def OnAbout(self, event):
        
            aboutInfo = wx.AboutDialogInfo()
            aboutInfo.SetName("MyApp")
            aboutInfo.SetVersion(MY_APP_VERSION_STRING)
            aboutInfo.SetDescription(_("My wxPython-based application!"))
            aboutInfo.SetCopyright("(C) 1992-2012")
            aboutInfo.SetWebSite("http:#myapp.org")
            aboutInfo.AddDeveloper("My Self")
    
            wx.AboutBox(aboutInfo)
        
