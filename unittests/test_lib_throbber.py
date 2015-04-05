import imp_unittest, unittest
import wtc
import wx
import wx.lib.throbber as th


import throbImages
images = [throbImages.catalog[i].GetBitmap()
          for i in throbImages.index
          if i not in ['eclouds', 'logo']]

#---------------------------------------------------------------------------

class lib_throbber_Tests(wtc.WidgetTestCase):

    def test_lib_throbber(self):
        pnl = wx.Panel(self.frame)
        w = th.Throbber(pnl, -1, images, size=(36, 36))
        
    def test_lib_throbber_Events(self):
        th.EVT_UPDATE_THROBBER
        
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
