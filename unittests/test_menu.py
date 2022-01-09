import unittest
from unittests import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'pointy.png')

#---------------------------------------------------------------------------

class menu_Tests(wtc.WidgetTestCase):

    def makeMenu(self):
        m = wx.Menu()
        for label in "one two three four".split():
            m.Append(-1, label)
        return m

    def makeMenuWithSubmenu(self):
        m = self.makeMenu()
        m.AppendSeparator()
        m2 = self.makeMenu()
        m.AppendSubMenu(m2, 'submenu')
        return m


    def test_menu1(self):
        m = self.makeMenu()
        items = m.GetMenuItems()
        self.assertTrue(len(items) == 4)
        self.assertTrue(isinstance(items[0], wx.MenuItem))

    def test_menu2(self):
        m = self.makeMenuWithSubmenu()
        items = m.GetMenuItems()
        self.assertTrue(len(items) == 6)

    def test_menu3(self):
        m = self.makeMenuWithSubmenu()
        items = []
        for i in m.GetMenuItems():
            self.assertTrue(isinstance(i, wx.MenuItem))
            items.append(i)
        self.assertTrue(len(items) == 6)


    def test_menuBar1(self):
        mb = wx.MenuBar()
        for label in "one two three four".split():
            m = self.makeMenu()
            mb.Append(m, label)
        self.frame.SetMenuBar(mb)

    def test_menuBar2(self):
        mb = wx.MenuBar()
        for label in "one two three four".split():
            m = self.makeMenu()
            mb.Append(m, label)
        menus = mb.GetMenus()
        self.assertTrue(len(menus) == 4)
        menu, label = menus[0]
        self.assertTrue(isinstance(menu, wx.Menu))
        self.assertTrue(label == 'one')


    def test_menuBar3(self):
        mb = wx.MenuBar()
        for label in "one two three four".split():
            m = self.makeMenu()
            mb.Append(m, label)
        menu = m
        item = menu.FindItemByPosition(0)

        i, m = mb.FindItem(item.GetId())
        self.assertTrue(i is item)
        self.assertTrue(m is menu)
        i = mb.FindItemById(item.GetId())
        self.assertTrue(i is item)

        i, m = menu.FindItem(item.GetId())
        self.assertTrue(i is item)
        self.assertTrue(m is menu)
        i = menu.FindItemById(item.GetId())
        self.assertTrue(i is item)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
