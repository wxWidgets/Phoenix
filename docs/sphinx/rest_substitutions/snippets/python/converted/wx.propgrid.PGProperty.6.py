
    class MyProperty(wx.propgrid.PGProperty):
        # All arguments of this ctor should have a default value -
        # use wx.propgrid.PG_LABEL for label and name
        def __init__(self,
                     label = wx.propgrid.PG_LABEL,
                     name = wx.propgrid.PG_LABEL,
                     value = ""):
            wx.propgrid.PGProperty.__init__(label, name)
            self.value = value

        def DoGetEditorClass(self):
            # Determines editor used by property.
            # You can replace 'TextCtrl' below with any of these
            # builtin-in property editor identifiers: Choice, ComboBox,
            # TextCtrlAndButton, ChoiceAndButton, CheckBox, SpinCtrl,
            # DatePickerCtrl.
            return wx.PGEditor_TextCtrl

        def ValueToString(self, value, argFlags):
            # TODO: Convert given property value to a string and return it
            return ""

        def StringToValue(self, text, argFlags):
            # TODO: Adapt string to property value and return it
            value = do_something(text)
            return (True, value)
