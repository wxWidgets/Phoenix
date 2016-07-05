    
            wait = wx.BusyInfo("Please wait, working...")
    
            for i in xrange(10000):
                DoACalculation()

            del wait
