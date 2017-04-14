    # Things can be made a little simpler in Python by using the dialog as a
    # context manager, using the with statement, like this:
    def AskUser(self):
        with MyAskDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                # do something here
                print('Hello')
            else:
                # handle dialog being cancelled or ended by some other button
                ...

        # The dialog is automatically destroyed on exit from the context manager