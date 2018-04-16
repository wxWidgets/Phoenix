
            class LogFormatterWithThread(wx.LogFormatter):
                def Format(level, msg, info):
                    return "[%d] %s(%d) : %s" % \
                           (info.threadId, info.filename, info.line, msg)


