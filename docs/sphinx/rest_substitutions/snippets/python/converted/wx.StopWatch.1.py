
    sw = wx.StopWatch()
    CallLongRunningFunction()
    wx.LogMessage("The long running function took %dms to execute", sw.Time())
    sw.Pause()

    # stopwatch is stopped now ...
    sw.Resume()
    CallLongRunningFunction()
    wx.LogMessage("And calling it twice took %dms in all", sw.Time())
