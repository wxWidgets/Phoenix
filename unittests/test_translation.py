import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class translation_Tests(wtc.WidgetTestCase):

    def test_translation1(self):
        ldr = wx.FileTranslationsLoader()
        wx.GetTranslation('hello')

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
