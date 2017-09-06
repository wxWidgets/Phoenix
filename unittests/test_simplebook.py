import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class simplebook_Tests(wtc.WidgetTestCase):

    def test_simplebook01(self):
        nb = wx.Simplebook(self.frame)

    def test_simplebook02(self):
        nb = wx.Simplebook()
        nb.Create(self.frame)

    def test_simplebook03(self):
        nb = wx.Simplebook(self.frame)
        p1 = wx.Panel(nb)
        nb.AddPage(p1, "")
        p2 = wx.Panel(nb)
        nb.AddPage(p2, "")
        nb.ChangeSelection(0)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
