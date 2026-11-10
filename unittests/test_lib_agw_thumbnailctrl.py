import os
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

    def test_lib_agw_thumbnailctrlThumbInfo(self):
        # The info is shown in a tooltip, possibly before the image is loaded.
        thumb = ST.Thumb(os.path.dirname(__file__), 'toucan.png', imagehandler=ST.NativeImageHandler)
        self.assertIn('Modified: 0', thumb.GetInfo())
        self.assertIn('Dimensions: (0, 0)', thumb.GetInfo())

        thumb.LoadImage()
        thumb.Rotate(90)
        self.assertEqual(thumb.GetOriginalSize(), (thumb.GetImage().GetWidth(),
                                                   thumb.GetImage().GetHeight()))

    def test_lib_agw_thumbnailctrlShowDir(self):
        tnc = TNC.ThumbnailCtrl(self.frame, -1, imagehandler=TNC.NativeImageHandler)
        tnc.ShowDir(os.path.dirname(os.path.abspath(__file__)))
        self.assertIn('toucan.png', [item.GetFileName() for item in tnc._scrolled._items])

    def test_lib_agw_thumbnailctrlLargeThumbSize(self):
        st = ST.ScrolledThumbnail(self.frame, -1, imagehandler=ST.NativeImageHandler)
        st.SetThumbSize(400, 300, 4)
        self.assertEqual(st.GetThumbSize(), (400, 300, 4))

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
