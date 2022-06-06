import unittest
from unittests import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtextbuffer_Tests(wtc.WidgetTestCase):

    def test_richtextbuffer01(self):
        wx.richtext.RICHTEXT_TYPE_ANY
        wx.richtext.RICHTEXT_TYPE_TEXT
        wx.richtext.RICHTEXT_TYPE_XML
        wx.richtext.RICHTEXT_TYPE_HTML
        wx.richtext.RICHTEXT_TYPE_RTF
        wx.richtext.RICHTEXT_TYPE_PDF
        wx.richtext.RICHTEXT_FIXED_WIDTH
        wx.richtext.RICHTEXT_FIXED_HEIGHT
        wx.richtext.RICHTEXT_VARIABLE_WIDTH
        wx.richtext.RICHTEXT_VARIABLE_HEIGHT
        wx.richtext.RICHTEXT_LAYOUT_SPECIFIED_RECT
        wx.richtext.RICHTEXT_DRAW_IGNORE_CACHE
        wx.richtext.RICHTEXT_DRAW_SELECTED
        wx.richtext.RICHTEXT_DRAW_PRINT
        wx.richtext.RICHTEXT_DRAW_GUIDELINES

        wx.richtext.RICHTEXT_FORMATTED
        wx.richtext.RICHTEXT_UNFORMATTED
        wx.richtext.RICHTEXT_CACHE_SIZE
        wx.richtext.RICHTEXT_HEIGHT_ONLY
        wx.richtext.RICHTEXT_SETSTYLE_NONE
        wx.richtext.RICHTEXT_SETSTYLE_WITH_UNDO
        wx.richtext.RICHTEXT_SETSTYLE_OPTIMIZE
        wx.richtext.RICHTEXT_SETSTYLE_PARAGRAPHS_ONLY
        wx.richtext.RICHTEXT_SETSTYLE_CHARACTERS_ONLY
        wx.richtext.RICHTEXT_SETSTYLE_RENUMBER
        wx.richtext.RICHTEXT_SETSTYLE_SPECIFY_LEVEL
        wx.richtext.RICHTEXT_SETSTYLE_RESET
        wx.richtext.RICHTEXT_SETSTYLE_REMOVE

        wx.richtext.RICHTEXT_SETPROPERTIES_NONE
        wx.richtext.RICHTEXT_SETPROPERTIES_WITH_UNDO
        wx.richtext.RICHTEXT_SETPROPERTIES_PARAGRAPHS_ONLY
        wx.richtext.RICHTEXT_SETPROPERTIES_CHARACTERS_ONLY
        wx.richtext.RICHTEXT_SETPROPERTIES_RESET
        wx.richtext.RICHTEXT_SETPROPERTIES_REMOVE

        wx.richtext.RICHTEXT_INSERT_NONE
        wx.richtext.RICHTEXT_INSERT_WITH_PREVIOUS_PARAGRAPH_STYLE
        wx.richtext.RICHTEXT_INSERT_INTERACTIVE
        wx.richtext.TEXT_ATTR_KEEP_FIRST_PARA_STYLE

        wx.richtext.RICHTEXT_HITTEST_NONE
        wx.richtext.RICHTEXT_HITTEST_BEFORE
        wx.richtext.RICHTEXT_HITTEST_AFTER
        wx.richtext.RICHTEXT_HITTEST_ON
        wx.richtext.RICHTEXT_HITTEST_OUTSIDE
        wx.richtext.RICHTEXT_HITTEST_NO_NESTED_OBJECTS
        wx.richtext.RICHTEXT_HITTEST_NO_FLOATING_OBJECTS
        wx.richtext.RICHTEXT_HITTEST_HONOUR_ATOMIC
        wx.richtext.TEXT_BOX_ATTR_FLOAT
        wx.richtext.TEXT_BOX_ATTR_CLEAR
        wx.richtext.TEXT_BOX_ATTR_COLLAPSE_BORDERS
        wx.richtext.TEXT_BOX_ATTR_VERTICAL_ALIGNMENT
        wx.richtext.TEXT_ATTR_UNITS_TENTHS_MM
        wx.richtext.TEXT_ATTR_UNITS_PIXELS
        wx.richtext.TEXT_ATTR_UNITS_PERCENTAGE
        wx.richtext.TEXT_ATTR_UNITS_POINTS
        wx.richtext.TEXT_ATTR_UNITS_MASK
        wx.richtext.TEXT_BOX_ATTR_POSITION_STATIC
        wx.richtext.TEXT_BOX_ATTR_POSITION_RELATIVE
        wx.richtext.TEXT_BOX_ATTR_POSITION_ABSOLUTE
        wx.richtext.TEXT_BOX_ATTR_POSITION_MASK


    def test_richtextbuffer02(self):
        tad = wx.richtext.TextAttrDimension()


    def test_richtextbuffer03(self):
        tad = wx.richtext.TextAttrDimension(123, wx.richtext.TEXT_ATTR_UNITS_TENTHS_MM)
        self.assertTrue(tad.IsValid())
        tad.Value
        tad.ValueMM
        tad.Units


    def test_richtextbuffer04(self):
        tads = wx.richtext.TextAttrDimensions()
        tads.Left.Value = 123
        tads.Left.IsValid()


    def test_richtextbuffer05(self):
        tas = wx.richtext.TextAttrSize()
        tas.SetWidth(wx.richtext.TextAttrDimension(123))
        assert tas.Width.IsValid()
        assert tas.Width.Value == 123


    def test_richtextbuffer06(self):
        c = wx.richtext.TextAttrDimensionConverter(123)


    def test_richtextbuffer07(self):
        wx.richtext.TEXT_BOX_ATTR_BORDER_NONE
        wx.richtext.TEXT_BOX_ATTR_BORDER_SOLID
        wx.richtext.TEXT_BOX_ATTR_BORDER_DOTTED
        wx.richtext.TEXT_BOX_ATTR_BORDER_DASHED
        wx.richtext.TEXT_BOX_ATTR_BORDER_DOUBLE
        wx.richtext.TEXT_BOX_ATTR_BORDER_GROOVE
        wx.richtext.TEXT_BOX_ATTR_BORDER_RIDGE
        wx.richtext.TEXT_BOX_ATTR_BORDER_INSET
        wx.richtext.TEXT_BOX_ATTR_BORDER_OUTSET
        wx.richtext.TEXT_BOX_ATTR_BORDER_STYLE
        wx.richtext.TEXT_BOX_ATTR_BORDER_COLOUR
        wx.richtext.TEXT_BOX_ATTR_BORDER_THIN
        wx.richtext.TEXT_BOX_ATTR_BORDER_MEDIUM
        wx.richtext.TEXT_BOX_ATTR_BORDER_THICK
        wx.richtext.TEXT_BOX_ATTR_FLOAT_NONE
        wx.richtext.TEXT_BOX_ATTR_FLOAT_LEFT
        wx.richtext.TEXT_BOX_ATTR_FLOAT_RIGHT
        wx.richtext.TEXT_BOX_ATTR_CLEAR_NONE
        wx.richtext.TEXT_BOX_ATTR_CLEAR_LEFT
        wx.richtext.TEXT_BOX_ATTR_CLEAR_RIGHT
        wx.richtext.TEXT_BOX_ATTR_CLEAR_BOTH
        wx.richtext.TEXT_BOX_ATTR_COLLAPSE_NONE
        wx.richtext.TEXT_BOX_ATTR_COLLAPSE_FULL
        wx.richtext.TEXT_BOX_ATTR_VERTICAL_ALIGNMENT_NONE
        wx.richtext.TEXT_BOX_ATTR_VERTICAL_ALIGNMENT_TOP
        wx.richtext.TEXT_BOX_ATTR_VERTICAL_ALIGNMENT_CENTRE
        wx.richtext.TEXT_BOX_ATTR_VERTICAL_ALIGNMENT_BOTTOM


    def test_richtextbuffer08(self):
        b = wx.richtext.TextAttrBorder()


    def test_richtextbuffer09(self):
        b = wx.richtext.TextAttrBorders()
        b.Left
        b.Right
        b.Top
        b.Bottom


    def test_richtextbuffer10(self):
        ba = wx.richtext.TextBoxAttr()


    def test_richtextbuffer11(self):
        t1 = wx.richtext.RichTextAttr()
        t2 = wx.richtext.RichTextAttr(t1)
        t3 = wx.richtext.RichTextAttr(wx.TextAttr())


    def test_richtextbuffer12(self):
        p = wx.richtext.RichTextProperties()
        p.SetProperty('foo', 'bar')
        p.SetProperty('num', 123)
        self.assertEqual(p.GetProperty('foo'), 'bar')


    def test_richtextbuffer13(self):
        t = wx.richtext.RichTextFontTable()


    def test_richtextbuffer14a(self):
        r1 = wx.richtext.RichTextRange()
        r2 = wx.richtext.RichTextRange(111, 222)
        r3 = wx.richtext.RichTextRange(r2)
        r3.Start
        r3.End

    def test_richtextbuffer14b(self):
        wx.richtext.RICHTEXT_ALL
        wx.richtext.RICHTEXT_NONE
        wx.richtext.RICHTEXT_NO_SELECTION

    def test_richtextbuffer14c(self):
        r = wx.richtext.RichTextRange(111, 222)
        start = r[0]
        end = r[1]
        self.assertEqual(start, 111)
        self.assertEqual(end, 222)

    def test_richtextbuffer14d(self):
        r = wx.richtext.RichTextRange(111, 222)
        start, end = r.Get()
        self.assertEqual(start, 111)
        self.assertEqual(end, 222)

    def test_richtextbuffer14e(self):
        r = wx.richtext.RichTextRange()
        self.assertEqual(r.Get(), (0,0))
        r[0] = 111
        r[1] = 222
        self.assertEqual(r.Get(), (111,222))


    def test_richtextbuffer15(self):
        s1 = wx.richtext.RichTextSelection()
        s2 = wx.richtext.RichTextSelection(s1)


    def test_richtextbuffer16(self):
        c = wx.richtext.RichTextDrawingContext(None)


    def test_richtextbuffer17(self):
        with self.assertRaises(TypeError):
            o1 = wx.richtext.RichTextObject()  # It's an ABC

    def test_richtextbuffer18(self):
        with self.assertRaises(TypeError):
            o1 = wx.richtext.RichTextCompositeObject()  # It's an ABC

    def test_richtextbuffer19(self):
        o1 = wx.richtext.RichTextParagraphLayoutBox()

    def test_richtextbuffer20(self):
        o1 = wx.richtext.RichTextBox()

    def test_richtextbuffer21(self):
        o1 = wx.richtext.RichTextField()

    def test_richtextbuffer22(self):
        with self.assertRaises(TypeError):
            o1 = wx.richtext.RichTextFieldType('foo')  # It's an ABC

    def test_richtextbuffer23(self):
        o1 = wx.richtext.RichTextFieldTypeStandard()

    def test_richtextbuffer24(self):
        o1 = wx.richtext.RichTextFieldTypeStandard('foo', 'bar')

    def test_richtextbuffer25(self):
        o1 = wx.richtext.RichTextLine(None)

    def test_richtextbuffer26(self):
        para = wx.richtext.RichTextParagraph()
        para.AllocateLine(0)
        para.AllocateLine(1)
        lines = para.GetLines()
        self.assertEqual(len(lines), 2)
        for l in lines:
            self.assertTrue(isinstance(l, wx.richtext.RichTextLine))

    def test_richtextbuffer27(self):
        o1 = wx.richtext.RichTextParagraph()

    def test_richtextbuffer28(self):
        o1 = wx.richtext.RichTextPlainText()

    def test_richtextbuffer29(self):
        o1 = wx.richtext.RichTextPlainText('some text')

    def test_richtextbuffer30(self):
        o1 = wx.richtext.RichTextImageBlock()

    def test_richtextbuffer31(self):
        o1 = wx.richtext.RichTextImage()

    def test_richtextbuffer32(self):
        o1 = wx.richtext.RichTextImage(wx.Image(100,75))

    def test_richtextbuffer33(self):
        o1 = wx.richtext.RichTextImage()
        o2 = wx.richtext.RichTextImage(o1)

    def test_richtextbuffer34(self):
        o1 = wx.richtext.RichTextBuffer()

    def test_richtextbuffer35(self):
        o1 = wx.richtext.RichTextObjectAddress()

    def test_richtextbuffer36(self):
        o1 = wx.richtext.RichTextCommand('name')

    def test_richtextbuffer37(self):
        c = wx.richtext.RichTextCommand('name')
        b = wx.richtext.RichTextBuffer()
        # TODO: finish this   a = wx.richtext.RichTextAction(c, 'name', 1234, b, )

    def test_richtextbuffer38(self):
        o1 = wx.richtext.RichTextBufferDataObject()

    def test_richtextbuffer39(self):
        o1 = wx.richtext.RichTextRenderer()

    def test_richtextbuffer39(self):
        o1 = wx.richtext.RichTextStdRenderer()



    def test_GetIM(self):
        # Test the immutable version returned by GetIM
        obj = wx.richtext.RichTextRange(1,2)
        im = obj.GetIM()
        assert isinstance(im, tuple)
        assert im.Start == obj.Start
        assert im.End == obj.End
        obj2 = wx.richtext.RichTextRange(im)
        assert obj == obj2





#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
