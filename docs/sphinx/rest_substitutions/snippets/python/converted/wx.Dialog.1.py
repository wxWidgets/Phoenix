    # In Python we don't have to worry about the stack vs. the heap, however
    # that means that dialogs do need to be destroyed. The typical pattern for
    # dialog usage looks something like this:
    def AskUser(self):
        try:
            dlg = MyAskDialog(self)
            if dlg.ShowModal() == wx.ID_OK:
                # do something here
                print('Hello')
            else:
                # handle dialog being cancelled or ended by some other button
                ...
        finally:
            # explicitly cause the dialog to destroy itself
            dlg.Destroy()
