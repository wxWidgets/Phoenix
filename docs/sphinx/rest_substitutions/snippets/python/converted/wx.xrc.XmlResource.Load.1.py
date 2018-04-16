
        if not wx.xml.XmlResource.Get().Load("rc/*.xrc"):
            wx.LogError("Couldn't load resources!")
