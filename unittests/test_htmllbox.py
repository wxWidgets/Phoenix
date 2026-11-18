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


    def test_htmllboxRefreshRow(self):
        class MyHtmlListBox(wx.html.HtmlListBox):
            calls = []
            def OnGetItem(self, n):
                self.calls.append(n)
                return 'this is item <b>%d</b>' % n

        lb = MyHtmlListBox(self.frame)
        lb.SetItemCount(3)
        dc = wx.MemoryDC(wx.Bitmap(100, 100))
        rect = wx.Rect(0, 0, 100, 20)

        # Drawing an item caches its HTML cell, and RefreshRow() drops it
        lb.OnDrawItem(dc, rect, 1)
        del lb.calls[:]
        lb.OnDrawItem(dc, rect, 1)
        self.assertEqual(lb.calls, [])
        lb.RefreshRow(1)
        del lb.calls[:]
        lb.OnDrawItem(dc, rect, 1)
        self.assertEqual(lb.calls, [1])

        lb.RefreshRows(0, 2)
        del lb.calls[:]
        lb.OnDrawItem(dc, rect, 2)
        self.assertEqual(lb.calls, [2])


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
