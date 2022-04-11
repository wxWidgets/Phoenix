
            dlg = wx.MessageDialog(parent, message, caption)
            if dlg.SetYesNoLabels("&Quit", "&Don't quit"):
                dlg.SetMessage("What do you want to do?")
            else: # buttons have standard "Yes"/"No" values, so rephrase the question
                dlg.SetMessage("Do you really want to quit?")
