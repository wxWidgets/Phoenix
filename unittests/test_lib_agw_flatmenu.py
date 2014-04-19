import imp_unittest, unittest
import wtc
import wx

import wx.lib.agw.flatmenu as FM

#---------------------------------------------------------------------------

class lib_agw_flatmenu_Tests(wtc.WidgetTestCase):

    def test_lib_agw_flatmenuCtor(self):
        self._popUpMenu = FM.FlatMenu()

        # First we create the sub-menu item
        subMenu = FM.FlatMenu()
        subSubMenu = FM.FlatMenu()

        # Create the menu items
        menuItem = FM.FlatMenuItem(self._popUpMenu, 20001, "First Menu Item", "", wx.ITEM_CHECK)
        self._popUpMenu.AppendItem(menuItem)

        menuItem = FM.FlatMenuItem(self._popUpMenu, 20002, "Sec&ond Menu Item", "", wx.ITEM_CHECK)
        self._popUpMenu.AppendItem(menuItem)

        menuItem = FM.FlatMenuItem(self._popUpMenu, wx.ID_ANY, "Checkable-Disabled Item", "", wx.ITEM_CHECK)
        menuItem.Enable(False)
        self._popUpMenu.AppendItem(menuItem)

        menuItem = FM.FlatMenuItem(self._popUpMenu, 20003, "Third Menu Item", "", wx.ITEM_CHECK)
        self._popUpMenu.AppendItem(menuItem)

        self._popUpMenu.AppendSeparator()
                        
    def test_lib_agw_flatmenuConstantsExist(self):

        FM.FM_OPT_IS_LCD
        FM.FM_OPT_MINIBAR
        FM.FM_OPT_SHOW_CUSTOMIZE
        FM.FM_OPT_SHOW_TOOLBAR

    def test_lib_agw_flatmenuEvents(self):

        FM.EVT_FLAT_MENU_DISMISSED
        FM.EVT_FLAT_MENU_ITEM_MOUSE_OUT
        FM.EVT_FLAT_MENU_ITEM_MOUSE_OVER
        FM.EVT_FLAT_MENU_SELECTED
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
