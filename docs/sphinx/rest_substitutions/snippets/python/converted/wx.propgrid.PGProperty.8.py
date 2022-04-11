
    import wx.propgrid as wxpg

    class MyProperty(wxpg.PGProperty):

        def __init__(self, label=wxpg.PG_LABEL, name=wxpg.PG_LABEL, value=0):
            wxpg.PGProperty.__init__(self, label, name)
            self.my_value = int(value)

        def DoGetEditorClass(self):
            """
            Determines what editor should be used for this property type. This
            is one way to specify one of the stock editors.
            """
            return wxpg.PropertyGridInterface.GetEditorByName("TextCtrl")

        def ValueToString(self, value, flags):
            """
            Convert the given property value to a string.
            """
            return str(value)

        def StringToValue(self, st, flags):
            """
            Convert a string to the correct type for the property.

            If failed, return False or (False, None). If success, return tuple
            (True, newValue).
            """
            try:
                val = int(st)
                return (True, val)
            except (ValueError, TypeError):
                pass
            except:
                raise
            return (False, None)

