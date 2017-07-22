import unittest
from unittests import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtextstyles_Tests(wtc.WidgetTestCase):

    def test_richtextstyles01(self):
        ctrl = wx.richtext.RichTextStyleListCtrl(self.frame)


    def test_richtextstyles02(self):
        ctrl = wx.richtext.RichTextStyleListCtrl()
        ctrl.Create(self.frame)


    def test_richtextstyles03(self):
        with self.assertRaises(TypeError):
            sdef = wx.richtext.RichTextStyleDefinition()


    def test_richtextstyles04(self):
        sdef = wx.richtext.RichTextParagraphStyleDefinition()


    def test_richtextstyles05(self):
        ctrl = wx.richtext.RichTextStyleListBox(self.frame)


    def test_richtextstyles06(self):
        ctrl = wx.richtext.RichTextStyleListBox()
        ctrl.Create(self.frame)


    def test_richtextstyles05(self):
        wx.richtext.RichTextStyleListBox.RICHTEXT_STYLE_ALL
        wx.richtext.RichTextStyleListBox.RICHTEXT_STYLE_PARAGRAPH
        wx.richtext.RichTextStyleListBox.RICHTEXT_STYLE_CHARACTER
        wx.richtext.RichTextStyleListBox.RICHTEXT_STYLE_LIST
        wx.richtext.RichTextStyleListBox.RICHTEXT_STYLE_BOX


    def test_richtextstyles6(self):
        ctrl = wx.richtext.RichTextStyleComboCtrl(self.frame)


    def test_richtextstyles07(self):
        ctrl = wx.richtext.RichTextStyleComboCtrl()
        ctrl.Create(self.frame)


    def test_richtextstyles08(self):
        sdef = wx.richtext.RichTextCharacterStyleDefinition()


    def test_richtextstyles09(self):
        sdef = wx.richtext.RichTextListStyleDefinition()


    def test_richtextstyles10(self):
        sdef = wx.richtext.RichTextStyleSheet()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
