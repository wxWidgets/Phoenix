import unittest
from unittests import wtc
import wx

import wx.lib.agw.scrolledthumbnail as ST
import wx.lib.agw.thumbnailctrl as TNC

#---------------------------------------------------------------------------

class lib_agw_thumbnailctrl_Tests(wtc.WidgetTestCase):

    def test_lib_agw_thumbnailctrlCtor(self):
        tnc = TNC.ThumbnailCtrl(self.frame, -1, imagehandler=TNC.NativeImageHandler)

    def test_lib_agw_thumbnailctrlEvents(self):
        ST.EVT_THUMBNAILS_SEL_CHANGED
        ST.EVT_THUMBNAILS_POINTED
        ST.EVT_THUMBNAILS_DCLICK
        ST.EVT_THUMBNAILS_THUMB_CHANGED
        ST.EVT_THUMBNAILS_CHAR

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
