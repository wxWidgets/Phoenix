import unittest
from unittests import wtc
import wx
import os

#---------------------------------------------------------------------------

class font_Tests(wtc.WidgetTestCase):

    def test_fontFlags(self):
        wx.FONTFAMILY_DEFAULT
        wx.FONTFAMILY_DECORATIVE
        wx.FONTFAMILY_ROMAN
        wx.FONTFAMILY_SCRIPT
        wx.FONTFAMILY_SWISS
        wx.FONTFAMILY_MODERN
        wx.FONTFAMILY_TELETYPE
        wx.FONTFAMILY_UNKNOWN

        wx.FONTSTYLE_NORMAL
        wx.FONTSTYLE_ITALIC
        wx.FONTSTYLE_SLANT

        wx.FONTWEIGHT_NORMAL
        wx.FONTWEIGHT_LIGHT
        wx.FONTWEIGHT_BOLD

        wx.FONTSIZE_XX_SMALL
        wx.FONTSIZE_X_SMALL
        wx.FONTSIZE_SMALL
        wx.FONTSIZE_MEDIUM
        wx.FONTSIZE_LARGE
        wx.FONTSIZE_X_LARGE
        wx.FONTSIZE_XX_LARGE

        wx.FONTFLAG_DEFAULT
        wx.FONTFLAG_ITALIC
        wx.FONTFLAG_SLANT
        wx.FONTFLAG_LIGHT
        wx.FONTFLAG_BOLD
        wx.FONTFLAG_ANTIALIASED
        wx.FONTFLAG_NOT_ANTIALIASED
        wx.FONTFLAG_UNDERLINED
        wx.FONTFLAG_STRIKETHROUGH

        wx.FONTENCODING_SYSTEM
        wx.FONTENCODING_DEFAULT
        wx.FONTENCODING_ISO8859_1
        wx.FONTENCODING_ISO8859_2
        wx.FONTENCODING_ISO8859_3
        wx.FONTENCODING_ISO8859_4
        wx.FONTENCODING_ISO8859_5
        wx.FONTENCODING_ISO8859_6
        wx.FONTENCODING_ISO8859_7
        wx.FONTENCODING_ISO8859_8
        wx.FONTENCODING_ISO8859_9
        wx.FONTENCODING_ISO8859_10
        wx.FONTENCODING_ISO8859_11
        wx.FONTENCODING_ISO8859_12
        wx.FONTENCODING_ISO8859_13
        wx.FONTENCODING_ISO8859_14
        wx.FONTENCODING_ISO8859_15
        wx.FONTENCODING_ISO8859_MAX
        wx.FONTENCODING_KOI8
        wx.FONTENCODING_KOI8_U
        wx.FONTENCODING_ALTERNATIVE
        wx.FONTENCODING_BULGARIAN
        wx.FONTENCODING_CP437
        wx.FONTENCODING_CP850
        wx.FONTENCODING_CP852
        wx.FONTENCODING_CP855
        wx.FONTENCODING_CP866
        wx.FONTENCODING_CP874
        wx.FONTENCODING_CP932
        wx.FONTENCODING_CP936
        wx.FONTENCODING_CP949
        wx.FONTENCODING_CP950
        wx.FONTENCODING_CP1250
        wx.FONTENCODING_CP1251
        wx.FONTENCODING_CP1252
        wx.FONTENCODING_CP1253
        wx.FONTENCODING_CP1254
        wx.FONTENCODING_CP1255
        wx.FONTENCODING_CP1256
        wx.FONTENCODING_CP1257
        wx.FONTENCODING_CP12_MAX
        wx.FONTENCODING_UTF7
        wx.FONTENCODING_UTF8
        wx.FONTENCODING_EUC_JP
        wx.FONTENCODING_UTF16BE
        wx.FONTENCODING_UTF16LE
        wx.FONTENCODING_UTF32BE
        wx.FONTENCODING_UTF32LE
        wx.FONTENCODING_MACROMAN
        wx.FONTENCODING_MACJAPANESE
        wx.FONTENCODING_MACCHINESETRAD
        wx.FONTENCODING_MACKOREAN
        wx.FONTENCODING_MACARABIC
        wx.FONTENCODING_MACHEBREW
        wx.FONTENCODING_MACGREEK
        wx.FONTENCODING_MACCYRILLIC
        wx.FONTENCODING_MACDEVANAGARI
        wx.FONTENCODING_MACGURMUKHI
        wx.FONTENCODING_MACGUJARATI
        wx.FONTENCODING_MACORIYA
        wx.FONTENCODING_MACBENGALI
        wx.FONTENCODING_MACTAMIL
        wx.FONTENCODING_MACTELUGU
        wx.FONTENCODING_MACKANNADA
        wx.FONTENCODING_MACMALAJALAM
        wx.FONTENCODING_MACSINHALESE
        wx.FONTENCODING_MACBURMESE
        wx.FONTENCODING_MACKHMER
        wx.FONTENCODING_MACTHAI
        wx.FONTENCODING_MACLAOTIAN
        wx.FONTENCODING_MACGEORGIAN
        wx.FONTENCODING_MACARMENIAN
        wx.FONTENCODING_MACCHINESESIMP
        wx.FONTENCODING_MACTIBETAN
        wx.FONTENCODING_MACMONGOLIAN
        wx.FONTENCODING_MACETHIOPIC
        wx.FONTENCODING_MACCENTRALEUR
        wx.FONTENCODING_MACVIATNAMESE
        wx.FONTENCODING_MACARABICEXT
        wx.FONTENCODING_MACSYMBOL
        wx.FONTENCODING_MACDINGBATS
        wx.FONTENCODING_MACTURKISH
        wx.FONTENCODING_MACCROATIAN
        wx.FONTENCODING_MACICELANDIC
        wx.FONTENCODING_MACROMANIAN
        wx.FONTENCODING_MACCELTIC
        wx.FONTENCODING_MACGAELIC
        wx.FONTENCODING_MACKEYBOARD
        wx.FONTENCODING_ISO2022_JP
        wx.FONTENCODING_MAX
        wx.FONTENCODING_MACMIN
        wx.FONTENCODING_MACMAX
        wx.FONTENCODING_UTF16
        wx.FONTENCODING_UTF32
        wx.FONTENCODING_UNICODE
        wx.FONTENCODING_GB2312
        wx.FONTENCODING_BIG5
        wx.FONTENCODING_SHIFT_JIS
        wx.FONTENCODING_EUC_KR


    def test_fontFlagsOld(self):
        wx.DEFAULT
        wx.DECORATIVE
        wx.ROMAN
        wx.SCRIPT
        wx.SWISS
        wx.MODERN
        wx.TELETYPE
        wx.NORMAL
        wx.LIGHT
        wx.BOLD
        wx.NORMAL
        wx.ITALIC
        wx.SLANT


    def test_font(self):
        f1 = wx.Font()
        f2 = wx.Font(f1)
        f3 = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        f4 = wx.Font(wx.Size(12,12), wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        f5 = wx.FFont(18, wx.FONTFAMILY_ROMAN)
        f6 = wx.Font.New(18, wx.FONTFAMILY_SWISS)
        # this ctor was removed
        #f7 = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD|wx.FONTFLAG_ITALIC)


    def test_fontFontinfo1(self):
        fi1 = wx.FontInfo().Family(wx.FONTFAMILY_ROMAN).Bold().Italic().Underlined().Strikethrough()
        fi2 = wx.FontInfo(12).FaceName('Ariel').Light().Encoding(wx.FONTENCODING_ISO8859_1)
        fi3 = wx.FontInfo((8,12)).AllFlags(wx.FONTFLAG_BOLD|wx.FONTFLAG_ITALIC)


    def test_fontFontinfo2(self):
        f1 = wx.Font(wx.FontInfo(12).Family(wx.FONTFAMILY_SWISS).Italic())


    def test_fontOk(self):
        f1 = wx.Font()
        f2 = wx.FFont(18, wx.FONTFAMILY_ROMAN)
        self.assertTrue(not f1.IsOk())
        self.assertTrue(    f2.IsOk())
        if f1:
            self.fail('f1 should not be True')
        if not f2:
            self.fail('f2 should not be False')


    def test_fontEquality(self):
        f1 = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        f2 = wx.FFont(18, wx.FONTFAMILY_ROMAN)
        f3 = wx.Font(wx.Size(12,12), wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        self.assertTrue(f1 == f2)
        self.assertTrue(f1 != f3)


    def test_fontProperties(self):
        f = wx.FFont(18, wx.FONTFAMILY_SWISS)
        f.Encoding
        f.FaceName
        f.Family
        f.NativeFontInfoDesc
        f.NativeFontInfoUserDesc
        f.PointSize
        f.PixelSize
        f.Style
        f.Weight


    def test_stockFonts(self):
        self.assertTrue(not wx.NullFont.IsOk())
        self.assertTrue(wx.NORMAL_FONT.IsOk())
        self.assertTrue(wx.SMALL_FONT.IsOk())
        self.assertTrue(wx.ITALIC_FONT.IsOk())
        self.assertTrue(wx.SWISS_FONT.IsOk())


    def test_fontFixedWidth(self):
        f = wx.FFont(10, wx.FONTFAMILY_TELETYPE)
        self.assertTrue(f.IsFixedWidth())


    def test_fontOldStyleNames(self):
        f = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
