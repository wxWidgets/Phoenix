    
    with wx.WindowDisabler():
        wait = wx.BusyInfo("Please wait, working...")

        for i in range(100000):
            DoACalculation()

            if not (i % 1000):
                wx.GetApp().Yield()
