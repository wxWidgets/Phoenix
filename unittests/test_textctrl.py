import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class textctrl_Tests(wtc.WidgetTestCase):

    def test_textctrlFlags(self):
        wx.TE_NO_VSCROLL
        wx.TE_READONLY
        wx.TE_MULTILINE
        wx.TE_PROCESS_TAB
        wx.TE_LEFT
        wx.TE_CENTER
        wx.TE_RIGHT
        wx.TE_CENTRE
        wx.TE_RICH
        wx.TE_PROCESS_ENTER
        wx.TE_PASSWORD
        wx.TE_AUTO_URL
        wx.TE_NOHIDESEL
        wx.TE_DONTWRAP
        wx.TE_CHARWRAP
        wx.TE_WORDWRAP
        wx.TE_BESTWRAP


    def test_textctrlCtor(self):
        t = wx.TextCtrl(self.frame)
        t = wx.TextCtrl(self.frame, -1, "Hello")
        t = wx.TextCtrl(self.frame, style=wx.TE_READONLY)
        t = wx.TextCtrl(self.frame, style=wx.TE_PASSWORD)
        t = wx.TextCtrl(self.frame, style=wx.TE_MULTILINE)


    def test_textctrlDefaultCtor(self):
        t = wx.TextCtrl()
        t.Create(self.frame)


    def test_textctrlProperties(self):
        t = wx.TextCtrl(self.frame)

        t.DefaultStyle
        t.NumberOfLines
        t.Hint
        t.InsertionPoint
        t.LastPosition
        t.Margins
        t.StringSelection
        t.Value


    def test_textctrlTextAttr(self):
        ta = wx.TextAttr()
        ta2 = wx.TextAttr(ta)
        ta3 = wx.TextAttr('black', 'white', wx.NORMAL_FONT, wx.TEXT_ALIGNMENT_RIGHT)

    def test_textctrlTextAttrProperties(self):
        ta = wx.TextAttr()

        ta.Alignment
        ta.BackgroundColour
        ta.BulletFont
        ta.BulletName
        ta.BulletNumber
        ta.BulletStyle
        ta.BulletText
        ta.CharacterStyleName
        ta.Flags
        ta.Font
        ta.FontEncoding
        ta.FontFaceName
        ta.FontFamily
        ta.FontSize
        ta.FontStyle
        ta.FontUnderlined
        ta.FontWeight
        ta.LeftIndent
        ta.LeftSubIndent
        ta.LineSpacing
        ta.ListStyleName
        ta.OutlineLevel
        ta.ParagraphSpacingAfter
        ta.ParagraphSpacingBefore
        ta.ParagraphStyleName
        ta.RightIndent
        ta.Tabs
        ta.TextColour
        ta.TextEffectFlags
        ta.TextEffects
        ta.URL


    def test_textctrlNativeCaret(self):
        t = wx.TextCtrl(self.frame)
        t.ShowNativeCaret
        t.HideNativeCaret

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
