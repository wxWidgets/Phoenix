import unittest
from unittests import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtextstyledlg_Tests(wtc.WidgetTestCase):


    def test_richtextstyledlg1(self):
        wx.richtext.RICHTEXT_ORGANISER_DELETE_STYLES
        wx.richtext.RICHTEXT_ORGANISER_CREATE_STYLES
        wx.richtext.RICHTEXT_ORGANISER_APPLY_STYLES
        wx.richtext.RICHTEXT_ORGANISER_EDIT_STYLES
        wx.richtext.RICHTEXT_ORGANISER_RENAME_STYLES
        wx.richtext.RICHTEXT_ORGANISER_OK_CANCEL
        wx.richtext.RICHTEXT_ORGANISER_RENUMBER
        wx.richtext.RICHTEXT_ORGANISER_SHOW_CHARACTER
        wx.richtext.RICHTEXT_ORGANISER_SHOW_PARAGRAPH
        wx.richtext.RICHTEXT_ORGANISER_SHOW_LIST
        wx.richtext.RICHTEXT_ORGANISER_SHOW_BOX
        wx.richtext.RICHTEXT_ORGANISER_SHOW_ALL
        wx.richtext.RICHTEXT_ORGANISER_ORGANISE
        wx.richtext.RICHTEXT_ORGANISER_BROWSE
        wx.richtext.RICHTEXT_ORGANISER_BROWSE_NUMBERING


    def test_richtextstyledlg2(self):
        sheet = wx.richtext.RichTextStyleSheet()
        rtc = wx.richtext.RichTextCtrl(self.frame)

        dlg = wx.richtext.RichTextStyleOrganiserDialog(
            wx.richtext.RICHTEXT_ORGANISER_ORGANISE,
            sheet, rtc, self.frame)
        dlg.Destroy()


    def test_richtextstyledlg3(self):
        sheet = wx.richtext.RichTextStyleSheet()
        rtc = wx.richtext.RichTextCtrl(self.frame)

        dlg = wx.richtext.RichTextStyleOrganiserDialog()
        dlg.Create(wx.richtext.RICHTEXT_ORGANISER_ORGANISE,
                   sheet, rtc, self.frame)
        dlg.Destroy()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
