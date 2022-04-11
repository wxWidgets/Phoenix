
        config = wx.Config("MyAppName")
        names = []

        # first enum all entries
        more, value, index = config.GetFirstEntry()

        while more:
            names.append(value)
            more, value, index = config.GetNextEntry(index)

        # ... we have all entry names in names...

        # now all groups...
        more, value, index = config.GetFirstGroup()

        while more:
            names.append(value)
            more, value, index = config.GetNextGroup(index)

        # ... we have all group (and entry) names in names...
