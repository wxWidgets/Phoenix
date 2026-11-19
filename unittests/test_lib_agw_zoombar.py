import sys
import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.lib.agw.zoombar as ZB

#---------------------------------------------------------------------------

class lib_agw_zoombar_Tests(wtc.WidgetTestCase):

    def test_lib_agw_zoombarCtor(self):
        zb = ZB.ZoomBar(self.frame)

    def test_lib_agw_zoombarDestroyedEarly(self):
        # The bar lays itself out with a timer after it's created
        with mock.patch.object(sys, 'excepthook') as excepthook:
            zb = ZB.ZoomBar(self.frame)
            zb.Destroy()
            sw = wx.StopWatch()
            while sw.Time() < 400:
                wx.MilliSleep(10)
                self.myYield()
        self.assertFalse(excepthook.called)

    def test_lib_agw_thumbnailctrlEvents(self):
        ZB.EVT_ZOOMBAR


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
