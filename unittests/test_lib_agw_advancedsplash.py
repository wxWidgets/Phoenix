import unittest
from unittests import wtc
import wx
import os

import wx.lib.agw.advancedsplash as AS

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class lib_agw_advancedsplash_Tests(wtc.WidgetTestCase):

    def test_lib_agw_advancedsplashCtor(self):
        splash = AS.AdvancedSplash(self.frame, -1, bitmap=wx.Bitmap(pngFile),
                                   agwStyle=AS.AS_TIMEOUT|AS.AS_CENTER_ON_SCREEN,
                                   timeout=250)
        self.waitFor(300)

    def test_lib_agw_advancedsplashConstantsExist(self):
        AS.AS_CENTER_ON_PARENT
        AS.AS_CENTER_ON_SCREEN
        AS.AS_NO_CENTER
        AS.AS_TIMEOUT
        AS.AS_NOTIMEOUT
        AS.AS_SHADOW_BITMAP


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
