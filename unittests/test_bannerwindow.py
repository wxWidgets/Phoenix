import unittest
from unittests import wtc
import wx
import wx.adv
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class bannerwindow_Tests(wtc.WidgetTestCase):

    def test_bannerwindow1(self):
        banner = wx.adv.BannerWindow(self.frame, dir=wx.LEFT)
        banner.SetBitmap(wx.BitmapBundle(wx.Bitmap(pngFile)))

    def test_bannerwindow2(self):
        banner = wx.adv.BannerWindow(self.frame, dir=wx.LEFT)
        banner.SetText('Message Title', 'The message itself: blah, blah, blah')
        banner.SetGradient('white', 'blue')


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
