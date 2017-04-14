import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class filehistory_Tests(wtc.WidgetTestCase):

    def test_filehistory1(self):
        fh = wx.FileHistory()
        for fn in "one two three four".split():
            fh.AddFileToHistory(fn)

        self.assertEqual(fh.GetCount(), 4)
        self.assertEqual(fh.Count, 4)
        self.assertEqual(fh.GetHistoryFile(1), 'three')  # they are in LIFO order
        m = wx.Menu()
        fh.AddFilesToMenu(m)


    def test_filehistory2(self):
        fh = wx.FileHistory()
        for fn in "one two three four".split():
            fh.AddFileToHistory(fn)

        menu1 = wx.Menu()
        menu2 = wx.Menu()
        fh.UseMenu(menu1)
        fh.UseMenu(menu2)
        fh.AddFilesToMenu()

        lst = fh.GetMenus()
        self.assertTrue(isinstance(lst, wx.FileHistoryMenuList))
        self.assertTrue(len(lst) == 2)
        self.assertTrue(len(list(lst)) == 2)
        self.assertTrue(isinstance(lst[0], wx.Menu))
        self.assertTrue(isinstance(lst[1], wx.Menu))
        self.assertTrue(lst[0] is menu1)
        self.assertTrue(lst[1] is menu2)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
