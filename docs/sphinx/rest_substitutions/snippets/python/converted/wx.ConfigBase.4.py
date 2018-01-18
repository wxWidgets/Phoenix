
        def bar(config):

            config.Write("Test", 17)

            foo(config)

            # we're reading "/Foo/Data/Test" here! -1 will probably be returned...
            if config.ReadInt("Test", -1) != 17:
                raise Exception('Invalid Test')

