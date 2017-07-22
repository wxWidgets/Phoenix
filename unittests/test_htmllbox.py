import unittest
from unittests import wtc
import wx
import wx.html

#---------------------------------------------------------------------------

class htmllbox_Tests(wtc.WidgetTestCase):

    def test_htmllbox1(self):
        lb = wx.html.SimpleHtmlListBox(self.frame, choices=['one', 'two', 'three'])

    def test_htmllbox2(self):
        lb = wx.html.SimpleHtmlListBox()
        lb.Create(self.frame, choices=['one', 'two', 'three'])

    def test_htmllbox3(self):
        class MyHtmlListBox(wx.html.HtmlListBox):
            def OnGetItem(self, n):
                return 'this is item <b>%d</b>' % n

        lb = MyHtmlListBox(self.frame)
        lb.SetItemCount(15)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
