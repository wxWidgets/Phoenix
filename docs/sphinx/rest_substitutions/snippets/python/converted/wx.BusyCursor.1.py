
        wait = wx.BusyCursor()

        for i in xrange(10000):
            DoACalculation()

        del wait
