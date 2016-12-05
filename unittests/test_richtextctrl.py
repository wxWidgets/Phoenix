import unittest
from unittests import wtc
import wx
import wx.richtext
import os

toucanFile = os.path.join(os.path.dirname(__file__), 'toucan.png')
smileFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

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




    def test_richtextctrl8(self):
        import wx.richtext as rt

        rtc = rt.RichTextCtrl(self.frame, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);

        rtc.Freeze()
        rtc.BeginSuppressUndo()

        rtc.BeginParagraphSpacing(0, 20)

        rtc.BeginAlignment(wx.TEXT_ALIGNMENT_CENTRE)
        rtc.BeginBold()

        rtc.BeginFontSize(14)
        rtc.WriteText("Welcome to wxRichTextCtrl, a wxWidgets control for editing and presenting styled text and images")
        rtc.EndFontSize()
        rtc.Newline()

        rtc.BeginItalic()
        rtc.WriteText("by Julian Smart")
        rtc.EndItalic()

        rtc.EndBold()

        rtc.Newline()
        rtc.WriteImage(wx.Image(toucanFile))

        rtc.EndAlignment()

        rtc.Newline()
        rtc.Newline()

        rtc.WriteText("What can you do with this thing? ")
        rtc.WriteImage(wx.Image(smileFile))
        rtc.WriteText(" Well, you can change text ")

        rtc.BeginTextColour((255, 0, 0))
        rtc.WriteText("colour, like this red bit.")
        rtc.EndTextColour()

        rtc.BeginTextColour((0, 0, 255))
        rtc.WriteText(" And this blue bit.")
        rtc.EndTextColour()

        rtc.WriteText(" Naturally you can make things ")
        rtc.BeginBold()
        rtc.WriteText("bold ")
        rtc.EndBold()
        rtc.BeginItalic()
        rtc.WriteText("or italic ")
        rtc.EndItalic()
        rtc.BeginUnderline()
        rtc.WriteText("or underlined.")
        rtc.EndUnderline()

        rtc.BeginFontSize(14)
        rtc.WriteText(" Different font sizes on the same line is allowed, too.")
        rtc.EndFontSize()

        rtc.WriteText(" Next we'll show an indented paragraph.")

        rtc.BeginLeftIndent(60)
        rtc.Newline()

        rtc.WriteText("It was in January, the most down-trodden month of an Edinburgh winter. An attractive woman came into the cafe, which is nothing remarkable.")
        rtc.EndLeftIndent()

        rtc.Newline()

        rtc.WriteText("Next, we'll show a first-line indent, achieved using BeginLeftIndent(100, -40).")

        rtc.BeginLeftIndent(100, -40)
        rtc.Newline()

        rtc.WriteText("It was in January, the most down-trodden month of an Edinburgh winter. An attractive woman came into the cafe, which is nothing remarkable.")
        rtc.EndLeftIndent()

        rtc.Newline()

        rtc.WriteText("Numbered bullets are possible, again using sub-indents:")

        rtc.BeginNumberedBullet(1, 100, 60)
        rtc.Newline()

        rtc.WriteText("This is my first item. Note that wxRichTextCtrl doesn't automatically do numbering, but this will be added later.")
        rtc.EndNumberedBullet()

        rtc.BeginNumberedBullet(2, 100, 60)
        rtc.Newline()

        rtc.WriteText("This is my second item.")
        rtc.EndNumberedBullet()

        rtc.Newline()

        rtc.WriteText("The following paragraph is right-indented:")

        rtc.BeginRightIndent(200)
        rtc.Newline()

        rtc.WriteText("It was in January, the most down-trodden month of an Edinburgh winter. An attractive woman came into the cafe, which is nothing remarkable.")
        rtc.EndRightIndent()

        rtc.Newline()

        rtc.WriteText("The following paragraph is right-aligned with 1.5 line spacing:")

        rtc.BeginAlignment(wx.TEXT_ALIGNMENT_RIGHT)
        rtc.BeginLineSpacing(wx.TEXT_ATTR_LINE_SPACING_HALF)
        rtc.Newline()

        rtc.WriteText("It was in January, the most down-trodden month of an Edinburgh winter. An attractive woman came into the cafe, which is nothing remarkable.")
        rtc.EndLineSpacing()
        rtc.EndAlignment()

        rtc.Newline()
        rtc.WriteText("Other notable features of wxRichTextCtrl include:")

        rtc.BeginSymbolBullet('*', 100, 60)
        rtc.Newline()
        rtc.WriteText("Compatibility with wxTextCtrl API")
        rtc.EndSymbolBullet()

        rtc.BeginSymbolBullet('*', 100, 60)
        rtc.Newline()
        rtc.WriteText("Easy stack-based BeginXXX()...EndXXX() style setting in addition to SetStyle()")
        rtc.EndSymbolBullet()

        rtc.BeginSymbolBullet('*', 100, 60)
        rtc.Newline()
        rtc.WriteText("XML loading and saving")
        rtc.EndSymbolBullet()

        rtc.BeginSymbolBullet('*', 100, 60)
        rtc.Newline()
        rtc.WriteText("Undo/Redo, with batching option and Undo suppressing")
        rtc.EndSymbolBullet()

        rtc.BeginSymbolBullet('*', 100, 60)
        rtc.Newline()
        rtc.WriteText("Clipboard copy and paste")
        rtc.EndSymbolBullet()

        rtc.BeginSymbolBullet('*', 100, 60)
        rtc.Newline()
        rtc.WriteText("wxRichTextStyleSheet with named character and paragraph styles, and control for applying named styles")
        rtc.EndSymbolBullet()

        rtc.BeginSymbolBullet('*', 100, 60)
        rtc.Newline()
        rtc.WriteText("A design that can easily be extended to other content types, ultimately with text boxes, tables, controls, and so on")
        rtc.EndSymbolBullet()

        rtc.Newline()

        rtc.WriteText("Note: this sample content was generated programmatically from within the MyFrame constructor in the demo. The images were loaded from inline XPMs. Enjoy wxRichTextCtrl!")

        rtc.Newline()
        rtc.Newline()
        rtc.BeginFontSize(12)
        rtc.BeginBold()
        rtc.WriteText("Additional comments by David Woods:")
        rtc.EndBold()
        rtc.EndFontSize()
        rtc.Newline()
        rtc.WriteText("I find some of the RichTextCtrl method names, as used above, to be misleading.  Some character styles are stacked in the RichTextCtrl, and they are removed in the reverse order from how they are added, regardless of the method called.  Allow me to demonstrate what I mean.")
        rtc.Newline()

        rtc.WriteText('Start with plain text. ')
        rtc.BeginBold()
        rtc.WriteText('BeginBold() makes it bold. ')
        rtc.BeginItalic()
        rtc.WriteText('BeginItalic() makes it bold-italic. ')
        rtc.EndBold()
        rtc.WriteText('EndBold() should make it italic but instead makes it bold. ')
        rtc.EndItalic()
        rtc.WriteText('EndItalic() takes us back to plain text. ')
        rtc.Newline()

        rtc.WriteText('Start with plain text. ')
        rtc.BeginBold()
        rtc.WriteText('BeginBold() makes it bold. ')
        rtc.BeginUnderline()
        rtc.WriteText('BeginUnderline() makes it bold-underline. ')
        rtc.EndBold()
        rtc.WriteText('EndBold() should make it underline but instead makes it bold. ')
        rtc.EndUnderline()
        rtc.WriteText('EndUnderline() takes us back to plain text. ')
        rtc.Newline()

        rtc.WriteText('According to Julian, this functions "as expected" because of the way the RichTextCtrl is written.  ')
        rtc.Newline()

        rtc.EndParagraphSpacing()

        rtc.EndSuppressUndo()
        rtc.Thaw()



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
