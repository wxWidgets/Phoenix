    
    # Create a document and add the root node.
    xmlDoc = wx.xml.XmlDocument()
    
    root = wx.xml.XmlNode(None, wx.xml.XML_ELEMENT_NODE, "Root")
    xmlDoc.SetRoot(root)
    
    # Add some XML.
    library = wx.xml.XmlNode(root, wx.xml.XML_ELEMENT_NODE, "Library")
    library.AddAttribute("type", "CrossPlatformList")
    name = wx.xml.XmlNode(library, wx.xml.XML_ELEMENT_NODE, "Name")
    name.AddChild(wx.xml.XmlNode(wx.xml.XML_TEXT_NODE, "", "wxPython"))
    
    # Write the output to a string.
    stream = io.StringIO()
    xmlDoc.Save(stream)
