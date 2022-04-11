
            def DoLogRecord(self, level, msg, info):

                # let the previous logger show it
                if self.logOld and IsPassingMessages():
                    self.logOld.LogRecord(level, msg, info)

                # and also send it to the one
                if self.logNew and self.logNew != self:
                    self.logNew.LogRecord(level, msg, info)

