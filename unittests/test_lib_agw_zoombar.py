import unittest
from unittests import wtc
import wx

import wx.lib.agw.zoombar as ZB

#---------------------------------------------------------------------------

class lib_agw_zoombar_Tests(wtc.WidgetTestCase):

    def test_lib_agw_zoombarCtor(self):
        zb = ZB.ZoomBar(self.frame)

    def test_lib_agw_thumbnailctrlEvents(self):
        ZB.EVT_ZOOMBAR


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
