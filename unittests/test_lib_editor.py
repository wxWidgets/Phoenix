import unittest
from unittests import wtc
import wx

import wx.lib.editor as editor

#---------------------------------------------------------------------------

class lib_editor_Tests(wtc.WidgetTestCase):

    def test_lib_editorCtor(self):
        ed = editor.Editor(self.frame, -1)
        ed.SetText(['one', 'two'])
        self.assertEqual(ed.GetText(), ['one', 'two'])

    def test_lib_editorLineSplitter(self):
        self.assertEqual(editor.editor.LineSplitter('one\r\ntwo'), ['one', 'two'])

    def test_lib_editorPaste(self):
        ed = editor.Editor(self.frame, -1)
        ed.SetText(['ab'])
        ed.cx = 1
        if not wx.TheClipboard.Open():
            self.skipTest('The clipboard is not available')
        wx.TheClipboard.SetData(wx.TextDataObject('1\n2'))
        wx.TheClipboard.Close()
        ed.OnPaste(None)
        self.assertEqual(ed.GetText(), ['a1', '2b'])

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
