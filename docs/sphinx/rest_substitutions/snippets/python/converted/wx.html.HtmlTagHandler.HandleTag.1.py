
    def HandleTag(self, tag):

        # change state of parser (e.g. set bold face)
        self.ParseInner(tag)
        # ...
        # restore original state of parser
