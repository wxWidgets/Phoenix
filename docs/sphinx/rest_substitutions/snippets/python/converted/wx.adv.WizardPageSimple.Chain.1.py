
            page3 = wx.RadioboxPage(wizard)
            page4 = wx.ValidationPage(wizard)

            wx.adv.WizardPageSimple.Chain(page3, page4)
