
        logChain = wx.LogChain(wx.LogStderr)

        # all the log messages are sent to stderr and also processed as usually

        # don't delete logChain directly as this would leave a dangling
        # pointer as active log target, use SetActiveTarget() instead
