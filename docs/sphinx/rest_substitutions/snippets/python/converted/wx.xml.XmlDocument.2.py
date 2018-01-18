
        doc = wx.xml.XmlDocument()
        doc.Load("myfile.xml", "UTF-8", wx.xml.XMLDOC_KEEP_WHITESPACE_NODES)

        # myfile2.xml will be identical to myfile.xml saving it self way:
        doc.Save("myfile2.xml", wx.xml.XML_NO_INDENTATION)
