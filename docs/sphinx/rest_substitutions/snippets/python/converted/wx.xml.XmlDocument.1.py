
        def ScanDocument():

            doc = wx.xml.XmlDocument()
            if not doc.Load("myfile.xml"):
                return False

            # start processing the XML file
            if doc.GetRoot().GetName() != "myroot-node":
                return False

            # examine prologue
            prolog = doc.GetDocumentNode().GetChildren()
            while prolog:

                if prolog.GetType() == wx.xml.XML_PI_NODE and prolog.GetName() == "target":

                    # process Process Instruction contents
                    pi = prolog.GetContent()

                    # Other code here...

            child = doc.GetRoot().GetChildren()
            while child:

                if child.GetName() == "tag1":

                    # process text enclosed by tag1/tag1
                    content = child.GetNodeContent()

                    # Other code here...

                    # process attributes of tag1
                    attrvalue1 = child.GetAttribute("attr1", "default-value")
                    attrvalue2 = child.GetAttribute("attr2", "default-value")

                elif child.GetName() == "tag2":

                    # process tag2 ...
                    attrvalue3 = child.GetAttribute("attr3", "default-value")


                child = child.GetNext()

