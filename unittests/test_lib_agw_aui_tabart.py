import unittest
from unittests import wtc
import wx
import os

import wx.lib.agw.aui.tabart as ta

#---------------------------------------------------------------------------

class lib_agw_aui_tabart_Tests(wtc.WidgetTestCase):

    def test_lib_agw_aui_tabartCtor(self):
        ta.AuiCommandCapture()
        ta.AuiDefaultTabArt()
        ta.AuiSimpleTabArt()
        ta.ChromeTabArt()
        ta.FF2TabArt()
        ta.VC71TabArt()
        ta.VC8TabArt()

    def test_lib_agw_aui_tabartClone(self):
        font = wx.Font(wx.FontInfo(13).Bold())
        for cls in (ta.AuiDefaultTabArt, ta.AuiSimpleTabArt, ta.VC71TabArt,
                    ta.FF2TabArt, ta.VC8TabArt, ta.ChromeTabArt):
            art = cls()
            art.SetNormalFont(font)
            art.SetSelectedFont(font)
            clone = art.Clone()
            self.assertIs(type(clone), cls)
            self.assertIsNot(clone, art)
            self.assertEqual(clone.GetNormalFont(), font)
            self.assertEqual(clone.GetSelectedFont(), font)

    def test_lib_agw_aui_tabartUniformBitmapSize(self):
        import wx.lib.agw.aui as aui
        nb = aui.AuiNotebook(self.frame)
        nb.SetUniformBitmapSize((16, 16))
        nb.AddPage(wx.Panel(nb), 'page')
        self.assertGreater(nb.GetTabCtrlHeight(), 16)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
