import imp_unittest, unittest
import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtextctrl_Tests(wtc.WidgetTestCase):

    def test_richtextctrl1(self):
        wx.richtext.RE_READONLY
        wx.richtext.RE_MULTILINE
        wx.richtext.RE_CENTER_CARET
        wx.richtext.RE_CENTRE_CARET    
        wx.richtext.RICHTEXT_SHIFT_DOWN
        wx.richtext.RICHTEXT_CTRL_DOWN
        wx.richtext.RICHTEXT_ALT_DOWN
        wx.richtext.RICHTEXT_EX_NO_GUIDELINES
        

    def test_richtextctrl2(self):
        info = wx.richtext.RichTextContextMenuPropertiesInfo()
        obj = wx.richtext.RichTextParagraph()
        info.AddItem('Name', obj)
        
    
    def test_richtextctrl3(self):
        pass

    def test_richtextctrl4(self):
        pass

    def test_richtextctrl5(self):
        pass

    def test_richtextctrl6(self):
        pass
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
