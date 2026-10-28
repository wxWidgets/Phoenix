import unittest
from unittests import wtc
import wx
import os

import wx.lib.agw.shortcuteditor as SE
#---------------------------------------------------------------------------

class lib_agw_shortcuteditor_Tests(wtc.WidgetTestCase):

    def test_lib_agw_rulerctrlCtor(self):
        dlg = SE.ShortcutEditor(self.frame)

    def test_lib_agw_shortcuteditorEvents(self):
        SE.EVT_SHORTCUT_CHANGING
        SE.EVT_SHORTCUT_CHANGED

    def test_lib_agw_shortcuteditorKeyNamesParse(self):
        for name in SE.KEYMAP.values():
            entry = wx.AcceleratorEntry()
            self.assertTrue(entry.FromString('Ctrl+' + name),
                            'wx does not recognize key name %r' % name)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()