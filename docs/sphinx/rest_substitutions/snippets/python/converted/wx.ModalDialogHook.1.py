
    class MyModalDialogHook(wx.ModalDialogHook):

        def __init__(self, parent):

            wx.ModalDialogHook.__init__(self, parent)


        def Enter(self, dialog):

            # Just for demonstration purposes, intercept all uses of
            # wx.FileDialog. Notice that self doesn't provide any real
            # sandboxing, of course, the program can still read and write
            # files by not using wx.FileDialog to ask the user for their
            # names.
            if isinstance(dialog, wx.FileDialog):

                wx.LogError("Access to file system disallowed.")

                # Skip showing the file dialog entirely.
                return wx.ID_CANCEL


            self.lastEnter = wx.DateTime.Now()

            # Allow the dialog to be shown as usual.
            return wx.ID_NONE


        def Exit(self, dialog):

            # Again, just for demonstration purposes, show how long did
            # the user take to dismiss the dialog. Notice that we
            # shouldn't use wx.LogMessage() here as self would result in
            # another modal dialog call and hence infinite recursion. In
            # general, the hooks should be as unintrusive as possible.
            wx.LogDebug("%s dialog took %s to be dismissed",
                       dialog.GetClassInfo().GetClassName(),
                       (wx.DateTime.Now() - self.lastEnter).Format())



    if __name__ == '__main__':

        app = wx.App(0)
        self.myHook = MyModalDialogHook(None)
        self.myHook.Register()
        app.MainLoop()
