import unittest
from unittests import wtc
import wx

import wx.lib.agw.supertooltip as STT

#---------------------------------------------------------------------------

class lib_agw_supertooltip_Tests(wtc.WidgetTestCase):

    def test_lib_agw_supertooltipCtor(self):
        STT.SuperToolTip("a simple test message")


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
