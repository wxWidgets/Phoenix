
    class MyProperty(wx.propgrid.PGProperty):
        def __init__(self, label, name, value):
            wx.propgrid.PGProperty.__init__(self, label, name)
            self.SetValue(value)

