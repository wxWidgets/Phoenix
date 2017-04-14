import unittest
from unittests import wtc
import wx
import wx.lib.throbber as th


from unittests import throbImages

#---------------------------------------------------------------------------

class lib_throbber_Tests(wtc.WidgetTestCase):

    def test_lib_throbber(self):
        pnl = wx.Panel(self.frame)
        images = [throbImages.catalog[i].GetBitmap()
                  for i in throbImages.index
                  if i not in ['eclouds', 'logo']]
        w = th.Throbber(pnl, -1, images, size=(36, 36))

    def test_lib_throbber_Events(self):
        th.EVT_UPDATE_THROBBER


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
