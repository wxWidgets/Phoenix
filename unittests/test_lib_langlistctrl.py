import unittest
from unittests import wtc
import wx
import wx.lib.langlistctrl as lc

#---------------------------------------------------------------------------

class langlistctrl_Tests(wtc.WidgetTestCase):

    def test_langlistctrlCtor(self):
        theList = lc.LanguageListCtrl(self.frame, filter=lc.LC_ONLY,
                                      only=(wx.LANGUAGE_ENGLISH,
                                            wx.LANGUAGE_FRENCH),
                                      select=wx.LANGUAGE_ENGLISH)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
