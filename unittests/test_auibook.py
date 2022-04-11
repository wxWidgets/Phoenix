import unittest
from unittests import wtc
import wx
import wx.aui

#---------------------------------------------------------------------------

class auibook_Tests(wtc.WidgetTestCase):

    def test_auibook01(self):
        wx.aui.AUI_NB_TOP
        wx.aui.AUI_NB_LEFT
        wx.aui.AUI_NB_RIGHT
        wx.aui.AUI_NB_BOTTOM
        wx.aui.AUI_NB_TAB_SPLIT
        wx.aui.AUI_NB_TAB_MOVE
        wx.aui.AUI_NB_TAB_EXTERNAL_MOVE
        wx.aui.AUI_NB_TAB_FIXED_WIDTH
        wx.aui.AUI_NB_SCROLL_BUTTONS
        wx.aui.AUI_NB_WINDOWLIST_BUTTON
        wx.aui.AUI_NB_CLOSE_BUTTON
        wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
        wx.aui.AUI_NB_CLOSE_ON_ALL_TABS
        wx.aui.AUI_NB_MIDDLE_CLICK_CLOSE
        wx.aui.AUI_NB_DEFAULT_STYLE



    def test_auibook02(self):
        nb = wx.aui.AuiNotebook()
        nb.Create(self.frame)


    def test_auibook03(self):
        nb = wx.aui.AuiNotebook(self.frame)
        nb.AddPage(wx.Panel(nb), "Page")


    def test_auibook04(self):
        obj = wx.aui.AuiNotebookPage()


    def test_auibook05(self):
        obj = wx.aui.AuiTabContainerButton()


    def test_auibook06(self):
        obj = wx.aui.AuiTabContainer()


    def test_auibook07(self):
        with self.assertRaises(TypeError):
            obj = wx.aui.AuiTabArt()


    def test_auibook08(self):
        obj = wx.aui.AuiDefaultTabArt()


    def test_auibook09(self):
        obj = wx.aui.AuiSimpleTabArt()


    def test_auibook10(self):
        evt = wx.aui.AuiNotebookEvent()

        wx.aui.wxEVT_AUINOTEBOOK_PAGE_CLOSE
        wx.aui.wxEVT_AUINOTEBOOK_PAGE_CLOSED
        wx.aui.wxEVT_AUINOTEBOOK_PAGE_CHANGED
        wx.aui.wxEVT_AUINOTEBOOK_PAGE_CHANGING
        wx.aui.wxEVT_AUINOTEBOOK_BUTTON
        wx.aui.wxEVT_AUINOTEBOOK_BEGIN_DRAG
        wx.aui.wxEVT_AUINOTEBOOK_END_DRAG
        wx.aui.wxEVT_AUINOTEBOOK_DRAG_MOTION
        wx.aui.wxEVT_AUINOTEBOOK_ALLOW_DND
        wx.aui.wxEVT_AUINOTEBOOK_DRAG_DONE
        wx.aui.wxEVT_AUINOTEBOOK_TAB_MIDDLE_DOWN
        wx.aui.wxEVT_AUINOTEBOOK_TAB_MIDDLE_UP
        wx.aui.wxEVT_AUINOTEBOOK_TAB_RIGHT_DOWN
        wx.aui.wxEVT_AUINOTEBOOK_TAB_RIGHT_UP
        wx.aui.wxEVT_AUINOTEBOOK_BG_DCLICK

        wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE
        wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED
        wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED
        wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGING
        wx.aui.EVT_AUINOTEBOOK_BUTTON
        wx.aui.EVT_AUINOTEBOOK_BEGIN_DRAG
        wx.aui.EVT_AUINOTEBOOK_END_DRAG
        wx.aui.EVT_AUINOTEBOOK_DRAG_MOTION
        wx.aui.EVT_AUINOTEBOOK_ALLOW_DND
        wx.aui.EVT_AUINOTEBOOK_DRAG_DONE
        wx.aui.EVT_AUINOTEBOOK_TAB_MIDDLE_DOWN
        wx.aui.EVT_AUINOTEBOOK_TAB_MIDDLE_UP
        wx.aui.EVT_AUINOTEBOOK_TAB_RIGHT_DOWN
        wx.aui.EVT_AUINOTEBOOK_TAB_RIGHT_UP
        wx.aui.EVT_AUINOTEBOOK_BG_DCLICK


    def test_auibook11(self):
        nb = wx.aui.AuiNotebook(self.frame)
        nb.AddPage(wx.Panel(nb), "Page")
        nb.SetArtProvider(wx.aui.AuiDefaultTabArt())


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
