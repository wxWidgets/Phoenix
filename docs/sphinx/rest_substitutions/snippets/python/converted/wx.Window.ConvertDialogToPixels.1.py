
        # The C++ convenience macro does not apply for Python, however you can
        # accomplish something similar with a function like this
        def DLG_UNIT(parent, point):
            return parent.ConvertDialogToPixels(point)
