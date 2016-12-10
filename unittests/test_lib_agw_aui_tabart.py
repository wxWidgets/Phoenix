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

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
