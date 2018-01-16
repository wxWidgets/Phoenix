
        # provide the message parameters for the MIME type manager
        class MailMessageParameters(wx.MessageParameters):

            def __init__(self, filename, mimetype):

                wx.MessageParameters.__init__(self, filename, mimetype)


            def GetParamValue(self, name):

                # parameter names are not case-sensitive
                if name.lower() == "charset":
                    return "US-ASCII"
                else:
                    return wx.MessageParameters.GetParamValue(name)


