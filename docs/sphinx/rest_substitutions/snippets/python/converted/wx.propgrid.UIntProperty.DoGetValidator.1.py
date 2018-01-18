
    class MyPropertyClass(wx.propgrid.UIntProperty):
        ...
        def DoGetValidator(self):
            validator = MyValidator(...)

            ... prepare validator...

            return validator
