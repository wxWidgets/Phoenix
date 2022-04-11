import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class AppTraitsTests(wtc.WidgetTestCase):

    def test_AppTraits(self):
        t = self.app.GetTraits()
        self.assertTrue(t is not None)

        portID, major, minor, micro = t.GetToolkitVersion()
        assert portID in [ wx.PORT_MSW,
                           wx.PORT_MOTIF,
                           wx.PORT_GTK,
                           wx.PORT_DFB,
                           wx.PORT_X11,
                           wx.PORT_MAC,
                           wx.PORT_COCOA,
                           wx.PORT_QT,
                           ]

        t.HasStderr()
        t.IsUsingUniversalWidgets()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
