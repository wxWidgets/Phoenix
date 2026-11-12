import unittest
from unittests import wtc
import wx

import wx.lib.foldmenu as foldmenu

#---------------------------------------------------------------------------

class lib_foldmenu_Tests(wtc.WidgetTestCase):

    def test_lib_foldmenu(self):
        bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16, 16))
        menu = foldmenu.FoldOutMenu(self.frame, wx.ID_ANY, bmp)
        clicked = []
        btnId = menu.AddButton(bmp, handler=clicked.append)

        menu.click(wx.CommandEvent())
        self.assertTrue(menu.popwin.IsShown())

        btn = menu.popwin.FindWindow(btnId)
        evt = wx.CommandEvent(wx.wxEVT_BUTTON, btnId)
        evt.SetEventObject(btn)
        btn.ProcessEvent(evt)
        self.assertEqual(len(clicked), 1)
        self.assertFalse(menu.popwin.IsShown())


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
