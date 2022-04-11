
    # Normal usage
    wait = wx.BusyInfo("Please wait, working...")
    for i in range(10000):
        DoACalculation()
    del wait

    # It can be used as a context manager too
    with wx.BusyInfo("Please wait, working..."):
        for i in range(10000):
        DoACalculation()
