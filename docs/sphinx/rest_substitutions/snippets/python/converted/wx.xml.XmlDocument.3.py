
        doc = wx.xml.XmlDocument()
        doc.Load("myfile.xml")
        doc.Save("myfile2.xml")  # myfile2.xml != myfile.xml
