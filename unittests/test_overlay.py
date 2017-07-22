import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class overlay_Tests(wtc.WidgetTestCase):

    def test_overlay1(self):
        o = wx.Overlay()
        dc = wx.ClientDC(self.frame)
        odc = wx.DCOverlay(o, dc)
        odc.Clear()
        del odc
        o.Reset()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
