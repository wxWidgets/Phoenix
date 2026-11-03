import unittest
from unittests import wtc
import wx

try:
    import wx.lib.graphics as graphics
    haveCairo = graphics.cairo is not None
except ImportError:
    haveCairo = False

#---------------------------------------------------------------------------

@unittest.skipIf(not haveCairo, 'needs pycairo')
class lib_graphics_Tests(wtc.WidgetTestCase):

    def setUp(self):
        super().setUp()
        self.bmp = wx.Bitmap(50, 50)
        self.dc = wx.MemoryDC(self.bmp)
        self.gc = graphics.GraphicsContext.Create(self.dc)

    def tearDown(self):
        del self.gc
        self.dc.SelectObject(wx.NullBitmap)
        super().tearDown()

    def test_lib_graphicsLinearGradientFromColours(self):
        self.gc.CreateLinearGradientBrush(0, 0, 10, 10, 'red', wx.BLUE)

    def test_lib_graphicsRadialGradientFromColours(self):
        self.gc.CreateRadialGradientBrush(0, 0, 5, 5, 5, 'red', wx.BLUE)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
