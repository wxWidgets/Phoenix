

    if self.richTextCtrl.HasSelection():
        range = self.richTextCtrl.GetSelectionRange()
    else:
        range = wx.RichTextRange(0, self.richTextCtrl.GetLastPosition()+1)

    pages = wx.richtext.RICHTEXT_FORMAT_FONT \
            | wx.richtext.RICHTEXT_FORMAT_INDENTS_SPACING \
            | wx.richtext.RICHTEXT_FORMAT_TABS \
            | wx.richtext.RICHTEXT_FORMAT_BULLETS

    with wx.richtext.RichTextFormattingDialog(pages, self) as dlg:
        dlg.GetStyle(self.richTextCtrl, range)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.ApplyStyle(self.richTextCtrl, range)

