import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class listbook_Tests(wtc.WidgetTestCase):

    def test_listbook1(self):
        wx.LB_DEFAULT
        wx.LB_TOP
        wx.LB_BOTTOM
        wx.LB_LEFT
        wx.LB_RIGHT
        wx.LB_ALIGN_MASK

        wx.wxEVT_COMMAND_LISTBOOK_PAGE_CHANGED
        wx.wxEVT_COMMAND_LISTBOOK_PAGE_CHANGING
        wx.EVT_LISTBOOK_PAGE_CHANGED
        wx.EVT_LISTBOOK_PAGE_CHANGING


    def test_listbook2(self):
        book = wx.Listbook()
        book.Create(self.frame)


    def test_listbook3(self):
        book = wx.Listbook(self.frame)
        book.AddPage(wx.Panel(book), 'one')
        book.AddPage(wx.Panel(book), 'two')

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
