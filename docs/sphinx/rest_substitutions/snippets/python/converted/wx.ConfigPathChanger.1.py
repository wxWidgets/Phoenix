
        # this function loads some settings from the given wx.Config object
        # the path selected inside it is left unchanged
        def LoadMySettings(config):

            changer = wx.ConfigPathChanger(config, "/Foo/Data/SomeString")

            strs = config.Read("SomeString")

            if not strs:
                wx.LogError("Couldn't read SomeString!")
                return False

            # NOTE: without wx.ConfigPathChanger it would be easy to forget to
            #       set the old path back into the wx.Config object before this return!


            # do something useful with SomeString...

            return True  # again: wx.ConfigPathChanger dtor will restore the original wx.Config path

