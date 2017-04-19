import unittest
from unittests import wtc
import wx
import os

toolImgFiles = [os.path.join(os.path.dirname(__file__), 'LB01.png'),
                os.path.join(os.path.dirname(__file__), 'LB02.png'),
                os.path.join(os.path.dirname(__file__), 'LB03.png'),
                os.path.join(os.path.dirname(__file__), 'LB04.png'),
                ]

#---------------------------------------------------------------------------

class toolbook_Tests(wtc.WidgetTestCase):

    def test_toolbook1(self):
        wx.TBK_BUTTONBAR
        wx.TBK_HORZ_LAYOUT

        wx.wxEVT_COMMAND_TOOLBOOK_PAGE_CHANGED
        wx.wxEVT_COMMAND_TOOLBOOK_PAGE_CHANGING
        wx.EVT_TOOLBOOK_PAGE_CHANGED
        wx.EVT_TOOLBOOK_PAGE_CHANGING


    def test_toolbook2(self):
        book = wx.Toolbook()
        book.Create(self.frame)


    def test_toolbook3(self):
        book = wx.Toolbook(self.frame)

        il = wx.ImageList(32,32)
        for name in toolImgFiles:
            il.Add(wx.Bitmap(name))
        book.AssignImageList(il)

        book.AddPage(wx.Panel(book), 'one', imageId=0)
        book.AddPage(wx.Panel(book), 'two', imageId=1)
        book.AddPage(wx.Panel(book), 'three', imageId=2)
        book.AddPage(wx.Panel(book), 'four', imageId=3)

        book.GetToolBar()

        self.myYield()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
