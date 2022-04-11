

    class MyPropertyClass(wx.propgrid.FileProperty):
        ...
        def DoGetValidator(self):
            validator = MyValidator(...)

            ... prepare validator...

            return validator
