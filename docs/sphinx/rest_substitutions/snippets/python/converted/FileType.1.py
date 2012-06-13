
        # provide the message parameters for the MIME type manager
        class MailMessageParameters(wx.FileType.MessageParameters):

            def __init__(self, filename, mimetype):

                wx.FileType.MessageParameters.__init__(self, filename, mimetype)


            def GetParamValue(self, name):
            
                # parameter names are not case-sensitive
                if name.lower() == "charset":
                    return "US-ASCII"
                else:
                    return wx.FileType.MessageParameters.GetParamValue(name)
            

