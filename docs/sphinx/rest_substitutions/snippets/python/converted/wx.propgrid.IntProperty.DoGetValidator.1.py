
    class MyPropertyClass(wx.propgrid.IntProperty):
        ...
        def DoGetValidator(self):
            validator = MyValidator(...)

            ... prepare validator...

            return validator
