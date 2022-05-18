import unittest
from unittests import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'pointy.png')

#---------------------------------------------------------------------------

class menuitem_Tests(wtc.WidgetTestCase):

    def test_menuitemCtor(self):
        m1 = wx.MenuItem()
        m2 = wx.MenuItem(None, -1, "Menu Item", "Help text", wx.ITEM_NORMAL)
        m2.SetBitmap(wx.BitmapBundle(wx.Bitmap(pngFile)))


    def test_menuitemProperties(self):
        m = wx.MenuItem()
        m.BackgroundColour
        m.Bitmap
        m.Font
        m.Help
        m.Id
        m.ItemLabel
        m.Kind
        m.MarginWidth
        m.Menu
        m.SubMenu
        m.TextColour
        m.Enabled


    def test_menuitemKinds(self):
        wx.ITEM_CHECK
        wx.ITEM_DROPDOWN
        wx.ITEM_NORMAL
        wx.ITEM_RADIO
        wx.ITEM_SEPARATOR

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
