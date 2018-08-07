import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class choicebk_Tests(wtc.WidgetTestCase):

    def test_choicebk1(self):
        wx.CHB_DEFAULT
        wx.CHB_TOP
        wx.CHB_BOTTOM
        wx.CHB_LEFT
        wx.CHB_RIGHT
        wx.CHB_ALIGN_MASK

        wx.wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGED
        wx.wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGING
        wx.EVT_CHOICEBOOK_PAGE_CHANGED
        wx.EVT_CHOICEBOOK_PAGE_CHANGING


    def test_choicebk2(self):
        book = wx.Choicebook()
        book.Create(self.frame)


    def test_choicebk3(self):
        book = wx.Choicebook(self.frame)
        book.AddPage(wx.Panel(book), 'one')
        book.AddPage(wx.Panel(book), 'two')


    def test_choicebk4(self):
        book = wx.Choicebook(self.frame)
        book.AddPage(wx.Panel(book), 'one')
        book.AddPage(wx.Panel(book), 'two')

        choice = book.GetChoiceCtrl()
        assert isinstance(choice, wx.Choice)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
