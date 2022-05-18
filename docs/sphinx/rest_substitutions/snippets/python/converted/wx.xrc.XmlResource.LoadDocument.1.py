
    xrc_data = ... # Retrieve it from wherever.
    xmlDoc = wx.xml.XmlDocument(io.BytesIO(xrc_data))
    if not xmlDoc.IsOk():
        ... handle invalid XML here ...
        return

    if not wx.XmlResource.Get().LoadDocument(xmlDoc):
        ... handle invalid XRC here ...
        return

    ... use the just loaded XRC as usual ...
