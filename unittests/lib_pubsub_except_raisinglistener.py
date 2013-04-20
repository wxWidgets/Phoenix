def getRaisingListener():
    def raisingListener():
        def nested():
            raise RuntimeError2('test')
        nested()

    return raisingListener