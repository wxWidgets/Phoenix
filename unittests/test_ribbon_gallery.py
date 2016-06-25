import unittest
import wtc
import wx.ribbon

#---------------------------------------------------------------------------

class ribbon_gallery_Tests(wtc.WidgetTestCase):

    def test_ribbon_gallery1(self):
        wx.ribbon.RIBBON_GALLERY_BUTTON_NORMAL
        wx.ribbon.RIBBON_GALLERY_BUTTON_HOVERED
        wx.ribbon.RIBBON_GALLERY_BUTTON_ACTIVE
        wx.ribbon.RIBBON_GALLERY_BUTTON_DISABLED


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
