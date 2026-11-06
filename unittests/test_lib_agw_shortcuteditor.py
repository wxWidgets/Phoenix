import unittest
from unittests import wtc
import wx
import os
from unittest import mock

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

    def test_lib_agw_shortcuteditorHTMLHelp(self):
        dlg = SE.ShortcutEditor(self.frame)
        dlg.OnHTMLHelp(None)
        self.assertIsNotNone(dlg.htmlWindow)
        dlg.htmlWindow.Destroy()
        dlg.Destroy()

    def test_lib_agw_shortcuteditorAcceleratorTableRoundTrip(self):
        ids = [wx.NewIdRef() for _ in range(3)]
        accels = [('Accel 1', wx.ACCEL_CTRL, wx.WXK_F5, ids[0]),
                  ('Accel 2', wx.ACCEL_ALT, ord('C'), ids[1]),
                  ('Accel 3', wx.ACCEL_SHIFT, wx.WXK_F7, ids[2])]
        dlg = SE.ShortcutEditor(self.frame)
        dlg.FromAcceleratorTable(accels)
        shortcuts = dlg.GetShortcutManager().children[-1].children
        shortcuts[1].SetAccelerator('Ctrl+D')
        shortcuts[2].SetAccelerator(SE.DISABLED_STRING)

        window = mock.Mock()
        with mock.patch.object(wx, 'AcceleratorTable') as table:
            dlg.ToAcceleratorTable(window)
        dlg.Destroy()

        table.assert_called_once_with([(wx.ACCEL_CTRL, wx.WXK_F5, ids[0]),
                                       (wx.ACCEL_CTRL, ord('D'), ids[1])])
        window.SetAcceleratorTable.assert_called_once_with(table.return_value)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()