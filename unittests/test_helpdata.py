import unittest
from unittests import wtc
import wx
import wx.html

#---------------------------------------------------------------------------

class helpdata_Tests(wtc.WidgetTestCase):

    def test_helpdata1(self):
        obj = wx.html.HtmlBookRecord("file", "path", "title", "start")

    def test_helpdata2(self):
        obj = wx.html.HtmlHelpDataItem()

    def test_helpdata3(self):
        obj = wx.html.HtmlHelpData()


    def test_helpdata4(self):
        wx.html.HF_TOOLBAR,
        wx.html.HF_CONTENTS,
        wx.html.HF_INDEX,
        wx.html.HF_SEARCH,
        wx.html.HF_BOOKMARKS,
        wx.html.HF_OPEN_FILES,
        wx.html.HF_PRINT,
        wx.html.HF_FLAT_TOOLBAR,
        wx.html.HF_MERGE_BOOKS,
        wx.html.HF_ICONS_BOOK,
        wx.html.HF_ICONS_BOOK_CHAPTER,
        wx.html.HF_ICONS_FOLDER,
        wx.html.HF_DEFAULT_STYLE,
        wx.html.HF_EMBEDDED,
        wx.html.HF_DIALOG,
        wx.html.HF_FRAME,
        wx.html.HF_MODAL,
        wx.html.ID_HTML_PANEL,
        wx.html.ID_HTML_BACK,
        wx.html.ID_HTML_FORWARD,
        wx.html.ID_HTML_UPNODE,
        wx.html.ID_HTML_UP,
        wx.html.ID_HTML_DOWN,
        wx.html.ID_HTML_PRINT,
        wx.html.ID_HTML_OPENFILE,
        wx.html.ID_HTML_OPTIONS,
        wx.html.ID_HTML_BOOKMARKSLIST,
        wx.html.ID_HTML_BOOKMARKSADD,
        wx.html.ID_HTML_BOOKMARKSREMOVE,
        wx.html.ID_HTML_TREECTRL,
        wx.html.ID_HTML_INDEXPAGE,
        wx.html.ID_HTML_INDEXLIST,
        wx.html.ID_HTML_INDEXTEXT,
        wx.html.ID_HTML_INDEXBUTTON,
        wx.html.ID_HTML_INDEXBUTTONALL,
        wx.html.ID_HTML_NOTEBOOK,
        wx.html.ID_HTML_SEARCHPAGE,
        wx.html.ID_HTML_SEARCHTEXT,
        wx.html.ID_HTML_SEARCHLIST,
        wx.html.ID_HTML_SEARCHBUTTON,
        wx.html.ID_HTML_SEARCHCHOICE,
        wx.html.ID_HTML_COUNTINFO

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
