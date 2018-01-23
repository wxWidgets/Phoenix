
    ctrl = self.FindWindow(ID_RICHTEXT_CTRL)

    attr = wx.TextAttr()
    attr.SetFlags(wx.TEXT_ATTR_FONT)
    ctrl.GetStyle(ctrl.GetInsertionPoint(), attr)

    currentFontName = ''
    if (attr.HasFont() and attr.GetFont().IsOk()):
        currentFontName = attr.GetFont().GetFaceName()

    # Don't set the initial font in the dialog (so the user is choosing
    # 'normal text', i.e. the current font) but do tell the dialog
    # what 'normal text' is.

    dlg = wx.richtext.SymbolPickerDialog("*", '', currentFontName, self)

    if dlg.ShowModal() == wx.ID_OK:

        if dlg.HasSelection():

            insertionPoint = ctrl.GetInsertionPoint()

            ctrl.WriteText(dlg.GetSymbol())

            if not dlg.UseNormalFont():

                font = attr.GetFont()
                font.SetFaceName(dlg.GetFontName())
                attr.SetFont(font)
                ctrl.SetStyle(insertionPoint, insertionPoint+1, attr)


