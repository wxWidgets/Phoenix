import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class fontmap_Tests(wtc.WidgetTestCase):

    def test_fontmap1(self):
        fm = wx.FontMapper.Get()
        self.assertTrue(fm is not None)

    def test_fontmap2(self):
        names = wx.FontMapper.GetAllEncodingNames(wx.FONTENCODING_SYSTEM)
        names = wx.FontMapper.GetAllEncodingNames(wx.FONTENCODING_ISO8859_1)

    def test_fontmap3(self):
        fm = wx.FontMapper.Get()
        enc = fm.CharsetToEncoding('ISO-8859-1')
        self.assertEqual(enc, wx.FONTENCODING_ISO8859_1)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    import os
    print('pid: %d' % os.getpid())
    unittest.main()
