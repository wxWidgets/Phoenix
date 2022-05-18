
    # Create the combo control using its default ctor.
    combo = wx.ComboCtrl()

    # Create the custom main control using its default ctor too.
    someMainWindow = SomeWindow()

    # Set the custom main control before creating the combo.
    combo.SetMainControl(someMainWindow)

    # And only create it now: wx.TextCtrl won't be unnecessarily
    # created because the combo already has a main window.
    combo.Create(panel, wx.ID_ANY, wx.EmptyString)

    # Finally create the main window itself, now that its parent was
    # created.
    someMainWindow.Create(combo, ...)
