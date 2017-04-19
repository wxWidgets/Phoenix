import unittest
from unittests import wtc
import wx
import os

import wx.lib.agw.aui.dockart as da

#---------------------------------------------------------------------------

class lib_agw_aui_dockart_Tests(wtc.WidgetTestCase):

    def test_lib_agw_aui_dockartCtor(self):
        da.ModernDockArt(self.frame)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
