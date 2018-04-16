
    class MyPropertyClass(wx.propgrid.DirProperty):
        ...
        def DoGetValidator(self):
            validator = MyValidator(...)

            ... prepare validator...

            return validator
