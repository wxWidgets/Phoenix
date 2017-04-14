import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class rawbmp_Tests(wtc.WidgetTestCase):

    def test_rawbmp1(self):
        DIM = 100
        red = 10
        green = 20
        blue = 30
        alpha = 128

        bmp = wx.Bitmap(DIM, DIM, 32)
        pixelData = wx.AlphaPixelData(bmp)
        self.assertTrue(pixelData)

        # Test using the __iter__ generator
        for pixel in pixelData:
            pixel.Set(red, green, blue, alpha)

        # This block of code is another way to do the same as above
        pixels = pixelData.GetPixels()
        for y in range(DIM):
            pixels.MoveTo(pixelData, 0, y)
            for x in range(DIM):
                pixels.Set(red, green, blue, alpha)
                pixels.nextPixel()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
