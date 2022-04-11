
        # using wx.Config instead of writing wx.FileConfig or wx.RegConfig enhances
        # portability of the code
        config = wx.Config("MyAppName")
        strs = config.Read("LastPrompt")

        # another example: using default values and the full path instead of just
        # key name: if the key is not found , the value 17 is returned
        value = config.ReadInt("/LastRun/CalculatedValues/MaxValue", 17)

        # at the end of the program we would save everything back
        config.Write("LastPrompt", strs)
        config.Write("/LastRun/CalculatedValues/MaxValue", value)
