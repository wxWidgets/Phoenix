import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class vidmode_Tests(wtc.WidgetTestCase):

    def test_vidmode(self):
        vm = wx.VideoMode()
        vm = wx.VideoMode(1024, 768, 32)
        self.assertTrue(vm.w == 1024)
        self.assertTrue(vm.h == 768)
        self.assertTrue(vm.bpp == 32)

    def test_defaultVidmode(self):
        wx.DefaultVideoMode  # just testing that it exists

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
