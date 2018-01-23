
        def ShowSimpleAboutDialog(self, event):

            info = wx.adv.AboutDialogInfo()
            info.SetName(_("My Program"))
            info.SetVersion(_("1.2.3 Beta"))
            info.SetDescription(_("This program does something great."))
            info.SetCopyright(wx.T("(C) 2007 Me <my@email.addre.ss>"))

            wx.adv.AboutBox(info)

