import unittest
import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtextformatdlg_Tests(wtc.WidgetTestCase):

    @unittest.expectedFailure  # richtextformatdlg not implemented yet
    def test_richtextformatdlg1(self):
        wx.richtext.RICHTEXT_FORMAT_FONT           
        wx.richtext.RICHTEXT_FORMAT_TABS           
        wx.richtext.RICHTEXT_FORMAT_STYLE_EDITOR   
        wx.richtext.RICHTEXT_FORMAT_BULLETS        
        wx.richtext.RICHTEXT_FORMAT_INDENTS_SPACING
        

    @unittest.expectedFailure  # richtextformatdlg not implemented yet
    def test_richtextformatdlg2(self):
        dlg = wx.richtext.RichTextFormattingDialog(
            wx.richtext.RICHTEXT_FORMAT_FONT,
            self.frame)
        self.runDialog(dlg)
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
