

    class MyPropertyClass(wx.propgrid.PGProperty):
        ...
        def DoGetValidator(self):
            validator = MyValidator(...)

            ... prepare validator...

            return validator
