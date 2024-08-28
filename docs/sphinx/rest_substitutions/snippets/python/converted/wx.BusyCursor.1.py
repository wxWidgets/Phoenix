
        # Normal usage
        wait = wx.BusyCursor()
        for i in range(10000):
            DoACalculation()
        del wait

        # It can be used as a context manager too
        with wx.BusyCursor():
            for i in range(10000):
                DoACalculation()
