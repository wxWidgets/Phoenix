
    class MyPropertyClass(wx.propgrid.FloatProperty):
        ...
        def DoGetValidator(self):
            validator = MyValidator(...)

            ... prepare validator...

            return validator
