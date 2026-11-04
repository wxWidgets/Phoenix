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

    def test_lib_editorDrawCursor(self):
        ed = editor.Editor(self.frame, -1, size=(300, 200))
        ed.SetText(['abc'])
        ed.cx = 1
        ed.SetCharDimensions()
        bmp = wx.Bitmap(300, 200)
        dc = wx.MemoryDC(bmp)
        ed.Draw(dc)
        dc.SelectObject(wx.NullBitmap)
        img = bmp.ConvertToImage()

        def colourAt(col):
            x, y = int(ed.fw * (col + 0.1)), int(ed.fh * 0.1)
            return wx.Colour(img.GetRed(x, y), img.GetGreen(x, y), img.GetBlue(x, y))

        # The cursor's cell is filled with the text colour.
        self.assertEqual(colourAt(1), ed.fgColor)
        self.assertEqual(colourAt(0), ed.bgColor)

    def test_lib_editorSetScrollTimer(self):
        ed = editor.Editor(self.frame, -1)
        ed.SetScrollTimer()
        self.assertTrue(ed.scrollTimer.IsRunning())
        ed.scrollTimer.Stop()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
