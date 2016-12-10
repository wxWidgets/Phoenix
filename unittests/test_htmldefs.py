import unittest
from unittests import wtc
import wx
import wx.html

#---------------------------------------------------------------------------

class htmldefs_Tests(wtc.WidgetTestCase):

    def test_htmldefs1(self):
        wx.html.HTML_ALIGN_LEFT
        wx.html.HTML_ALIGN_CENTER
        wx.html.HTML_ALIGN_RIGHT
        wx.html.HTML_ALIGN_BOTTOM
        wx.html.HTML_ALIGN_TOP
        wx.html.HTML_CLR_FOREGROUND
        wx.html.HTML_CLR_BACKGROUND
        wx.html.HTML_UNITS_PIXELS
        wx.html.HTML_UNITS_PERCENT
        wx.html.HTML_INDENT_LEFT
        wx.html.HTML_INDENT_RIGHT
        wx.html.HTML_INDENT_TOP
        wx.html.HTML_INDENT_BOTTOM
        wx.html.HTML_INDENT_HORIZONTAL
        wx.html.HTML_INDENT_VERTICAL
        wx.html.HTML_INDENT_ALL
        wx.html.HTML_COND_ISANCHOR
        wx.html.HTML_COND_ISIMAGEMAP
        wx.html.HTML_COND_USER
        wx.html.HW_SCROLLBAR_NEVER
        wx.html.HW_SCROLLBAR_AUTO
        wx.html.HW_NO_SELECTION
        wx.html.HW_DEFAULT_STYLE
        wx.html.HTML_OPEN
        wx.html.HTML_BLOCK
        wx.html.HTML_REDIRECT
        wx.html.HTML_URL_PAGE
        wx.html.HTML_URL_IMAGE
        wx.html.HTML_URL_OTHER

        wx.html.HTML_ALIGN_LEFT
        wx.html.HTML_ALIGN_RIGHT
        wx.html.HTML_ALIGN_JUSTIFY
        wx.html.HTML_ALIGN_TOP
        wx.html.HTML_ALIGN_BOTTOM
        wx.html.HTML_ALIGN_CENTER
        wx.html.HTML_CLR_FOREGROUND
        wx.html.HTML_CLR_BACKGROUND
        wx.html.HTML_CLR_TRANSPARENT_BACKGROUND
        wx.html.HTML_UNITS_PIXELS
        wx.html.HTML_UNITS_PERCENT
        wx.html.HTML_INDENT_LEFT
        wx.html.HTML_INDENT_RIGHT
        wx.html.HTML_INDENT_TOP
        wx.html.HTML_INDENT_BOTTOM
        wx.html.HTML_INDENT_HORIZONTAL
        wx.html.HTML_INDENT_VERTICAL
        wx.html.HTML_INDENT_ALL
        wx.html.HTML_COND_ISANCHOR
        wx.html.HTML_COND_ISIMAGEMAP
        wx.html.HTML_COND_USER

        wx.html.HTML_FIND_EXACT
        wx.html.HTML_FIND_NEAREST_BEFORE
        wx.html.HTML_FIND_NEAREST_AFTER
        wx.html.HTML_SCRIPT_NORMAL
        wx.html.HTML_SCRIPT_SUB
        wx.html.HTML_SCRIPT_SUP

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
