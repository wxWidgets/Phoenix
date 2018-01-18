

            # some code in HandleTag for "MYITEMS"...

            self.Parser.PushTagHandler(self, "PARAM")
            self.ParseInner(tag)
            self.Parser.PopTagHandler()

            # back to working on "MYITEMS"...
