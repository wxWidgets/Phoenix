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
        rtc = wx.richtext.RichTextCtrl(self.frame)


    def test_richtextctrl4(self):
        rtc = wx.richtext.RichTextCtrl()
        rtc.Create(self.frame)
        

    def test_richtextctrl5(self):
        rtc = wx.richtext.RichTextCtrl(self.frame)

        rtc.SetValue('Hello World')
        self.assertEqual('Hello World', rtc.GetValue())
        self.assertEqual('Hello World', rtc.Value)


    def test_richtextctrl6(self):
        rtc = wx.richtext.RichTextCtrl(self.frame)
        rtc.SetValue('Hello World')
        
        rtc.SetSelection(2, 6)
        sel = rtc.GetSelection()
        self.assertIsInstance(sel, wx.richtext.RichTextSelection)
        selrange = sel.GetRange(0)
        self.assertIsInstance(selrange, wx.richtext.RichTextRange)
        start = selrange.Start
        end = start + selrange.Length
        self.assertEqual((start,end), (2,6))


    def test_richtextctrl7(self):
        wx.richtext.EVT_RICHTEXT_LEFT_CLICK
        wx.richtext.EVT_RICHTEXT_RIGHT_CLICK
        wx.richtext.EVT_RICHTEXT_MIDDLE_CLICK
        wx.richtext.EVT_RICHTEXT_LEFT_DCLICK
        wx.richtext.EVT_RICHTEXT_RETURN
        wx.richtext.EVT_RICHTEXT_CHARACTER
        wx.richtext.EVT_RICHTEXT_DELETE
        wx.richtext.EVT_RICHTEXT_STYLESHEET_CHANGING
        wx.richtext.EVT_RICHTEXT_STYLESHEET_CHANGED
        wx.richtext.EVT_RICHTEXT_STYLESHEET_REPLACING
        wx.richtext.EVT_RICHTEXT_STYLESHEET_REPLACED
        wx.richtext.EVT_RICHTEXT_CONTENT_INSERTED
        wx.richtext.EVT_RICHTEXT_CONTENT_DELETED
        wx.richtext.EVT_RICHTEXT_STYLE_CHANGED
        wx.richtext.EVT_RICHTEXT_STYLE_CHANGED
        wx.richtext.EVT_RICHTEXT_SELECTION_CHANGED
        wx.richtext.EVT_RICHTEXT_BUFFER_RESET
        wx.richtext.EVT_RICHTEXT_FOCUS_OBJECT_CHANGED
        

        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
