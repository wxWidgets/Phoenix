    # Without a class
    dlg = wx.Dialog()
    wx.xml.XmlResource.Get().LoadDialog(dlg, mainFrame, "my_dialog")
    dlg.ShowModal()

    # Or, as a class
    class MyDialog(wx.Dialog):
        def __init__(self, parent):
            super().__init__()
            wx.xml.XmlResource.Get().LoadDialog(self, parent, "my_dialog")
