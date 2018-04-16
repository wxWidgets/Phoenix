
    page3 = RadioBoxPage(wizard)
    page4 = ValidationPage(wizard)

    wx.adv.WizardPageSimple.Chain(page3, page4)
