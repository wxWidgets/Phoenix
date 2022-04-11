
        config = wx.Config("FooBarApp")

        # right now the current path is '/'
        conf.Write("RootEntry", 1)

        # go to some other place: if the group(s) don't exist, they will be created
        conf.SetPath("/Group/Subgroup")

        # create an entry in subgroup
        conf.Write("SubgroupEntry", 3)

        # '..' is understood
        conf.Write("../GroupEntry", 2)
        conf.SetPath("..")

        if conf.ReadInt("Subgroup/SubgroupEntry", 0) != 3:
            raise Exception('Invalid SubgroupEntry')

        # use absolute path: it is allowed, too
        if conf.ReadInt("/RootEntry", 0) != 1:
            raise Exception('Invalid RootEntry')

