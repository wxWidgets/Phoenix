import unittest
from unittests import wtc
import wx

import wx.lib.agw.flatmenu as FM

#---------------------------------------------------------------------------

class lib_agw_flatmenu_Tests(wtc.WidgetTestCase):

    def setUp(self):
        '''
        Monkey patch some methods which don't behave well without
        a MainLoop.  We could restore them in tearDown, but there's
        no need because self.frame will be destroyed in tearDown.
        '''
        super(lib_agw_flatmenu_Tests, self).setUp()

        self.realPushEventHandlerMethod = self.frame.PushEventHandler
        def MockPushEventHandler(handler): pass
        self.frame.PushEventHandler = MockPushEventHandler

        self.realPopEventHandlerMethod = self.frame.PopEventHandler
        def MockPopEventHandler(deleteHandler=False): pass
        self.frame.PopEventHandler = MockPopEventHandler

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


    def test_lib_agw_flatmenuOpen(self):
        def CreateLongPopupMenu(self):
            popMenu = FM.FlatMenu()
            sub = FM.FlatMenu()

            #-----------------------------------------------
            # Flat Menu test
            #-----------------------------------------------

            for ii in range(30):
                if ii == 0:
                    menuItem = FM.FlatMenuItem(popMenu, wx.ID_ANY, "Menu Item #%ld"%(ii+1), "", wx.ITEM_NORMAL, sub)
                    popMenu.AppendItem(menuItem)

                    for k in range(5):

                        menuItem = FM.FlatMenuItem(sub, wx.ID_ANY, "Sub Menu Item #%ld"%(k+1))
                        sub.AppendItem(menuItem)

                else:

                    menuItem = FM.FlatMenuItem(popMenu, wx.ID_ANY, "Menu Item #%ld"%(ii+1))
                    popMenu.AppendItem(menuItem)

            return popMenu

        popMenu = CreateLongPopupMenu(self)

        fPt = self.frame.GetPosition()
        popMenu.Popup(wx.Point(fPt.x, fPt.y), self.frame)
        popMenu.Dismiss(True, True)

        # Clear the capture since the test won't do a normal shudown of the flatmenu
        cap = wx.Window.GetCapture()
        if cap:
            cap.ReleaseMouse()


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
