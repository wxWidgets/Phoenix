import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class minifram_Tests(wtc.WidgetTestCase):

    def test_minifram1(self):
        f = wx.MiniFrame()
        f.Create(self.frame, title="Hello")
        f.Show()

    def test_minifram2(self):
        f = wx.MiniFrame(self.frame, title="Hello")
        f.Show()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
