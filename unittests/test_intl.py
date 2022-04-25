import unittest
from unittests import wtc
import wx
import os

#---------------------------------------------------------------------------

class intl_Tests(wtc.WidgetTestCase):

    def test_intlLanguageInfo(self):
        info = wx.Locale.GetLanguageInfo(wx.LANGUAGE_ENGLISH_US)
        info.CanonicalName
        info.Description
        info.LocaleName


    def test_intlLocale(self):
        loc = wx.Locale(wx.LANGUAGE_ENGLISH_US)
        self.assertTrue(loc.IsOk())
        loc.CanonicalName
        loc.Language
        loc.Locale
        loc.Name
        loc.SysName
        del loc


    def test_intlGetString(self):
        # This tests if we're able to pull translations from the wx message catalogs
        loc = wx.Locale(wx.LANGUAGE_SPANISH)
        st = loc.GetString('&Next')
        self.assertEqual(st, '&Siguiente')


    def test_intlConstants(self):
        # just a few of them to make sure the file is included properly
        wx.LANGUAGE_AFRIKAANS
        wx.LANGUAGE_ALBANIAN
        wx.LANGUAGE_AMHARIC


    def test_intlGetLocaleFunc(self):
        # check that this function exists
        l = wx.GetLocale()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
