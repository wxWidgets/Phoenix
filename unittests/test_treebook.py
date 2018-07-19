import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class treebook_Tests(wtc.WidgetTestCase):

    def test_treebook1(self):
        wx.wxEVT_COMMAND_TREEBOOK_PAGE_CHANGED
        wx.wxEVT_COMMAND_TREEBOOK_PAGE_CHANGING
        wx.wxEVT_COMMAND_TREEBOOK_NODE_COLLAPSED
        wx.wxEVT_COMMAND_TREEBOOK_NODE_EXPANDED

        wx.EVT_TREEBOOK_PAGE_CHANGED
        wx.EVT_TREEBOOK_PAGE_CHANGING;
        wx.EVT_TREEBOOK_NODE_COLLAPSED;
        wx.EVT_TREEBOOK_NODE_EXPANDED;


    def test_treebook2(self):
        book = wx.Treebook()
        book.Create(self.frame)


    def test_treebook3(self):
        book = wx.Treebook(self.frame)
        book.AddPage(wx.Panel(book), 'one')
        book.AddPage(wx.Panel(book), 'two')
        book.AddSubPage(wx.Panel(book), 'three')


    def test_treebook4(self):
        book = wx.Treebook(self.frame)
        book.AddPage(wx.Panel(book), 'one')
        book.AddPage(wx.Panel(book), 'two')
        book.AddSubPage(wx.Panel(book), 'three')

        tree = book.GetTreeCtrl()
        assert isinstance(tree, wx.TreeCtrl)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
