
        def foo(config):

            oldPath = config.GetPath()

            config.SetPath("/Foo/Data")
            # ...

            config.SetPath(oldPath)

