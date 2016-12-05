import unittest
from unittests import wtc
import wx
import wx.adv
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class splash_Tests(wtc.WidgetTestCase):

    def test_splash1(self):
        wx.adv.SPLASH_CENTRE_ON_PARENT
        wx.adv.SPLASH_CENTRE_ON_SCREEN
        wx.adv.SPLASH_NO_CENTRE
        wx.adv.SPLASH_TIMEOUT
        wx.adv.SPLASH_NO_TIMEOUT
        wx.adv.SPLASH_CENTER_ON_PARENT
        wx.adv.SPLASH_CENTER_ON_SCREEN
        wx.adv.SPLASH_NO_CENTER


    def test_splash2(self):
        splash = wx.adv.SplashScreen(wx.Bitmap(pngFile),
                                     wx.adv.SPLASH_TIMEOUT|wx.adv.SPLASH_CENTRE_ON_SCREEN,
                                     250, self.frame)
        self.waitFor(300)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
