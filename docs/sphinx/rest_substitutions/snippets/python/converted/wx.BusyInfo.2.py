
            disableAll = wx.WindowDisabler()
            wait = wx.BusyInfo("Please wait, working...")

            for i in xrange(10000):
                DoACalculation()

                if i % 1000 == 0:
                    wx.GetApp().Yield()

            del wait
