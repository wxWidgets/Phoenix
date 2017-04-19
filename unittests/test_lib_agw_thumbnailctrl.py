import unittest
from unittests import wtc
import wx

import wx.lib.agw.thumbnailctrl as TNC

#---------------------------------------------------------------------------

class lib_agw_thumbnailctrl_Tests(wtc.WidgetTestCase):

    def test_lib_agw_thumbnailctrlCtor(self):
        tnc = TNC.ThumbnailCtrl(self.frame, -1, imagehandler=TNC.NativeImageHandler)

    def test_lib_agw_thumbnailctrlEvents(self):
        TNC.EVT_THUMBNAILS_CAPTION_CHANGED
        TNC.EVT_THUMBNAILS_DCLICK
        TNC.EVT_THUMBNAILS_POINTED
        TNC.EVT_THUMBNAILS_SEL_CHANGED
        TNC.EVT_THUMBNAILS_THUMB_CHANGED

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
