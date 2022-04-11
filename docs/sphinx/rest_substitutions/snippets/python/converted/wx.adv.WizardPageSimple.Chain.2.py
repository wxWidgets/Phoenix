
    # FirstPage is an instance of wx.adv.WizardPageSimple
    firstPage = FirstPage(self)
    firstPage.Chain(SecondPage).Chain(ThirdPage).Chain(LastPage)
