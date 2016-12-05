import unittest
from unittests import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtextformatdlg_Tests(wtc.WidgetTestCase):

    def test_richtextformatdlg1(self):
        wx.richtext.RICHTEXT_FORMAT_FONT
        wx.richtext.RICHTEXT_FORMAT_TABS
        wx.richtext.RICHTEXT_FORMAT_STYLE_EDITOR
        wx.richtext.RICHTEXT_FORMAT_BULLETS
        wx.richtext.RICHTEXT_FORMAT_INDENTS_SPACING


    def test_richtextformatdlg2(self):
        dlg = wx.richtext.RichTextFormattingDialog(
            wx.richtext.RICHTEXT_FORMAT_FONT,
            self.frame)
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
