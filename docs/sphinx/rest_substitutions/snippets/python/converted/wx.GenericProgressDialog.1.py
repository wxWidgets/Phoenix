    
    progdlg = wx.ProgressDialog(...)
    for i in range(100):
        if not progdlg.Update(i):
            # Cancelled by user.
            break

    ... do something time-consuming (but not too much) ...

