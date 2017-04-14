import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class vscroll_Tests(wtc.WidgetTestCase):

    def test_vscroll_VScrolledWindow1(self):
        with self.assertRaises(TypeError):
            w = wx.VScrolledWindow(self.frame)

    def test_vscroll_VScrolledWindow2(self):
        class MyScrolledWindow(wx.VScrolledWindow):
            def OnGetRowHeight(self, row):
                return 25

        w = MyScrolledWindow(self.frame)
        w.SetRowCount(100)


    def test_vscroll_HScrolledWindow1(self):
        with self.assertRaises(TypeError):
            w = wx.HScrolledWindow(self.frame)

    def test_vscroll_HScrolledWindow2(self):
        class MyScrolledWindow(wx.HScrolledWindow):
            def OnGetColumnWidth(self, row):
                return 80

        w = MyScrolledWindow(self.frame)
        w.SetColumnCount(100)


    def test_vscroll_HVScrolledWindow1(self):
        with self.assertRaises(TypeError):
            w = wx.HVScrolledWindow(self.frame)

    def test_vscroll_HVScrolledWindow2(self):
        class MyScrolledWindow(wx.HVScrolledWindow):
            def OnGetRowHeight(self, row):
                return 25
            def OnGetColumnWidth(self, row):
                return 80

        w = MyScrolledWindow(self.frame)
        w.SetRowCount(100)
        w.SetColumnCount(100)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
