import unittest
from unittests import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtextprint_Tests(wtc.WidgetTestCase):

    def test_richtextprint1(self):
        wx.richtext.RICHTEXT_PAGE_ODD
        wx.richtext.RICHTEXT_PAGE_EVEN
        wx.richtext.RICHTEXT_PAGE_ALL
        wx.richtext.RICHTEXT_PAGE_LEFT
        wx.richtext.RICHTEXT_PAGE_CENTRE
        wx.richtext.RICHTEXT_PAGE_RIGHT


    def test_richtextprint2(self):
        hfd = wx.richtext.RichTextHeaderFooterData()


    def test_richtextprint3(self):
        p = wx.richtext.RichTextPrintout()


    def test_richtextprint4(self):
        p = wx.richtext.RichTextPrinting()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
