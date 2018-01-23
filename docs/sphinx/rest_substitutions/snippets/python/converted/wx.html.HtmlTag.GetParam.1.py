
    # ... Some code here...

    # you have wx.HtmlTag variable tag which is equal to the
    # HTML tag <FONT SIZE=+2 COLOR="#0000FF">
    dummy = tag.GetParam("SIZE")
    # dummy == "+2"
    dummy = tag.GetParam("COLOR")
    # dummy == "#0000FF"
    dummy = tag.GetParam("COLOR", true)
    # dummy == "\"#0000FF\"" -- see the difference!!
