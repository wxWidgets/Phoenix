import unittest
from unittests import wtc
import wx
from wx.lib.wordwrap import wordwrap

#---------------------------------------------------------------------------

class lib_wordwrap_Tests(wtc.WidgetTestCase):

    def test_lib_wordwrap(self):
        dc = wx.MemoryDC(wx.Bitmap(10, 10))
        dc.SetFont(wx.NORMAL_FONT)
        width = dc.GetTextExtent('aaaa bbbb')[0]
        text = wordwrap('aaaa bbbb cccc dddd', width, dc)
        self.assertEqual(text.replace('\n', ' ').split(), ['aaaa', 'bbbb', 'cccc', 'dddd'])
        self.assertIn('\n', text)

    def test_lib_wordwrapNonBMP(self):
        dc = wx.MemoryDC(wx.Bitmap(10, 10))
        self.assertEqual(wordwrap('\U0001F610', 100, dc), '\U0001F610')
        text = wordwrap('\U0001F610 ' * 50, 100, dc)
        self.assertEqual(text.replace('\n', ' ').split(), ['\U0001F610'] * 50)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
