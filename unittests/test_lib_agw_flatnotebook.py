import unittest
from unittests import wtc
import wx

import wx.lib.agw.flatnotebook as FNB

#---------------------------------------------------------------------------

class lib_agw_flatnotebook_Tests(wtc.WidgetTestCase):

    def test_lib_agw_flatnotebookCtor(self):
        book = FNB.FlatNotebook(self.frame)
        self.assertEqual(book.GetPageCount(), 0)

    def test_lib_agw_flatnotebookPages(self):
        nb = FNB.FlatNotebook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")
        nb.SetSelection(0)

        self.assertEqual(nb.GetSelection(), 0)

    def test_lib_agw_flatnotebookTabStyles(self):
        nb = FNB.FlatNotebook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")

        styles = [FNB.FNB_VC71, FNB.FNB_VC8, FNB.FNB_FANCY_TABS, FNB.FNB_FF2, FNB.FNB_RIBBON_TABS]
        mirror = ~(FNB.FNB_VC71 | FNB.FNB_VC8 | FNB.FNB_FANCY_TABS | FNB.FNB_FF2 | FNB.FNB_RIBBON_TABS)

        for style in styles:
            nbstyle = nb.GetAGWWindowStyleFlag()
            nbstyle &= mirror
            nbstyle != style
            nb.SetAGWWindowStyleFlag(style)

            self.assertTrue(nb.HasAGWFlag(style))

    def test_lib_agw_flatnotebookDeletePages(self):
        nb = FNB.FlatNotebook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")
        nb.DeleteAllPages()

        self.assertEqual(nb.GetPageCount(), 0)

        nb = FNB.FlatNotebook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")

        for index in range(nb.GetPageCount()-1, -1, -1):
            nb.DeletePage(index)

        self.assertEqual(nb.GetPageCount(), 0)

    def test_lib_agw_flatnotebookMethods(self):
        nb = FNB.FlatNotebook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")

        nb.EnableTab(0, False)
        self.assertTrue(nb.GetEnabled(0) == False)

    def test_lib_agw_flatnotebookConstantsExist(self):

        FNB.FNB_VC71
        FNB.FNB_FANCY_TABS
        FNB.FNB_TABS_BORDER_SIMPLE
        FNB.FNB_NO_X_BUTTON
        FNB.FNB_NO_NAV_BUTTONS
        FNB.FNB_MOUSE_MIDDLE_CLOSES_TABS
        FNB.FNB_BOTTOM
        FNB.FNB_NODRAG
        FNB.FNB_VC8
        FNB.FNB_X_ON_TAB
        FNB.FNB_BACKGROUND_GRADIENT
        FNB.FNB_COLOURFUL_TABS
        FNB.FNB_DCLICK_CLOSES_TABS
        FNB.FNB_SMART_TABS
        FNB.FNB_DROPDOWN_TABS_LIST
        FNB.FNB_ALLOW_FOREIGN_DND
        FNB.FNB_HIDE_ON_SINGLE_TAB
        FNB.FNB_DEFAULT_STYLE
        FNB.FNB_FF2
        FNB.FNB_NO_TAB_FOCUS
        FNB.FNB_RIBBON_TABS
        FNB.FNB_HIDE_TABS
        FNB.FNB_NAV_BUTTONS_WHEN_NEEDED

    def test_lib_agw_flatnotebookEvents(self):

        FNB.EVT_FLATNOTEBOOK_PAGE_CHANGED
        FNB.EVT_FLATNOTEBOOK_PAGE_CHANGING
        FNB.EVT_FLATNOTEBOOK_PAGE_CLOSED
        FNB.EVT_FLATNOTEBOOK_PAGE_CLOSING
        FNB.EVT_FLATNOTEBOOK_PAGE_CONTEXT_MENU
        FNB.EVT_FLATNOTEBOOK_PAGE_DROPPED
        FNB.EVT_FLATNOTEBOOK_PAGE_DROPPED_FOREIGN

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
