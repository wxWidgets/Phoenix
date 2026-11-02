import unittest
from unittests import wtc
import wx

from wx.lib.mixins.imagelist import MagicImageList

#---------------------------------------------------------------------------

class ListWithImages(wx.ListCtrl, MagicImageList):
    pass


class lib_mixins_imagelist_Tests(wtc.WidgetTestCase):

    def test_lib_mixins_imagelistAddIcon(self):
        ctrl = ListWithImages(self.frame, style=wx.LC_REPORT)
        bmp = wx.Bitmap(16, 16)
        icon = wx.Icon(bmp)
        ctrl.SetupIcons([bmp, icon])
        self.assertEqual(ctrl.AddIcon(bmp), 0)
        self.assertEqual(ctrl.AddIcon(icon), 1)
        with self.assertRaises(ValueError):
            ctrl.AddIcon('not an icon')

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
