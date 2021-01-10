import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class notebook_Tests(wtc.WidgetTestCase):

    def test_notebookCtor(self):
        nb = wx.Notebook(self.frame)

    def test_notebookDefaultCtor(self):
        nb = wx.Notebook()
        nb.Create(self.frame)

    def test_notebookStyles(self):
        wx.NB_DEFAULT
        wx.NB_TOP
        wx.NB_BOTTOM
        wx.NB_LEFT
        wx.NB_RIGHT

        wx.NB_FIXEDWIDTH
        wx.NB_MULTILINE
        wx.NB_NOPAGETHEME

        wx.NB_HITTEST_NOWHERE
        wx.NB_HITTEST_ONICON
        wx.NB_HITTEST_ONLABEL
        wx.NB_HITTEST_ONITEM
        wx.NB_HITTEST_ONPAGE

    def test_notebookEventTypes(self):
        wx.wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGED
        wx.wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGING
        wx.EVT_NOTEBOOK_PAGE_CHANGED
        wx.EVT_NOTEBOOK_PAGE_CHANGING

    def test_notebookPages(self):
        nb = wx.Notebook(self.frame, style=wx.NB_BOTTOM)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "Page1")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "Page2")
        nb.SetSelection(0)

    def test_notebookPageAlias(self):
        assert wx.NotebookPage is wx.Window

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
