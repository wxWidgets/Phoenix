import unittest
from unittests import wtc
import wx

import wx.lib.agw.labelbook as LB

#---------------------------------------------------------------------------

class lib_agw_labelbook_Tests(wtc.WidgetTestCase):

    def test_lib_agw_labelbookCtor(self):
        book = LB.LabelBook(self.frame)
        self.assertEqual(book.GetPageCount(), 0)

        book = LB.FlatImageBook(self.frame)
        self.assertEqual(book.GetPageCount(), 0)

    def test_lib_agw_labelbookPages(self):
        nb = LB.LabelBook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")
        nb.SetSelection(0)

        nb = LB.FlatImageBook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")
        nb.SetSelection(0)

    def test_lib_agw_labelbookTabPosition(self):
        nb = LB.LabelBook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")

        for style in [LB.INB_LEFT, LB.INB_RIGHT]:
            nb.SetAGWWindowStyleFlag(style)

        nb = LB.FlatImageBook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")

        for style in [LB.INB_LEFT, LB.INB_RIGHT, LB.INB_TOP, LB.INB_BOTTOM]:
            nb.SetAGWWindowStyleFlag(style)

    def test_lib_agw_labelbookDeletePages(self):
        nb = LB.LabelBook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")
        nb.DeleteAllPages()

        nb = LB.FlatImageBook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")

        for index in range(nb.GetPageCount()-1, -1, -1):
            nb.DeletePage(index)

    def test_lib_agw_labelbookConstantsExist(self):
        LB.INB_BOTTOM
        LB.INB_LEFT
        LB.INB_RIGHT
        LB.INB_TOP
        LB.INB_BORDER
        LB.INB_SHOW_ONLY_TEXT
        LB.INB_SHOW_ONLY_IMAGES
        LB.INB_FIT_BUTTON
        LB.INB_DRAW_SHADOW
        LB.INB_USE_PIN_BUTTON
        LB.INB_GRADIENT_BACKGROUND
        LB.INB_WEB_HILITE
        LB.INB_NO_RESIZE
        LB.INB_FIT_LABELTEXT
        LB.INB_BOLD_TAB_SELECTION
        LB.INB_DEFAULT_STYLE

        self.assertEqual(LB.INB_DEFAULT_STYLE, LB.INB_BORDER | LB.INB_TOP | LB.INB_USE_PIN_BUTTON)

        LB.INB_TAB_AREA_BACKGROUND_COLOUR
        LB.INB_ACTIVE_TAB_COLOUR
        LB.INB_TABS_BORDER_COLOUR
        LB.INB_TEXT_COLOUR
        LB.INB_ACTIVE_TEXT_COLOUR
        LB.INB_HILITE_TAB_COLOUR

        LB.INB_LABEL_BOOK_DEFAULT
        self.assertEqual(LB.INB_LABEL_BOOK_DEFAULT, LB.INB_DRAW_SHADOW | LB.INB_BORDER | LB.INB_USE_PIN_BUTTON | LB.INB_LEFT)

        # Pin button states
        LB.INB_PIN_NONE
        LB.INB_PIN_HOVER
        LB.INB_PIN_PRESSED

    def test_lib_agw_labelbookEvents(self):
        LB.EVT_IMAGENOTEBOOK_PAGE_CHANGED
        LB.EVT_IMAGENOTEBOOK_PAGE_CHANGING
        LB.EVT_IMAGENOTEBOOK_PAGE_CLOSING
        LB.EVT_IMAGENOTEBOOK_PAGE_CLOSED

        self.assertEqual(LB.EVT_IMAGENOTEBOOK_PAGE_CHANGED, wx.EVT_NOTEBOOK_PAGE_CHANGED)
        self.assertEqual(LB.EVT_IMAGENOTEBOOK_PAGE_CHANGING, wx.EVT_NOTEBOOK_PAGE_CHANGING)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
