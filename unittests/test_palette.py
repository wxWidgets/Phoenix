import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class palette_Tests(wtc.WidgetTestCase):

    def test_palette1(self):
        rgb = bytearray(range(256))
        p = wx.Palette(256, rgb, rgb, rgb)
        self.assertTrue(p.IsOk())
        self.assertTrue(p.GetColoursCount() == 256)
        self.assertTrue(p.GetPixel(42, 42, 42) == 42)
        self.assertTrue(p.GetRGB(64) == (64, 64, 64))
        with self.assertRaises(IndexError):
            p.GetRGB(257)


    # def test_palette2(self):
    #     rgb = list(range(256))
    #     p = wx.Palette(len(rgb), rgb, rgb, rgb)
    #     self.assertTrue(p.IsOk())


    def test_paletteCreate1(self):
        p = wx.Palette()
        with self.assertRaises(TypeError):
            p.Create(1, 2, 3)
        with self.assertRaises(ValueError):
            p.Create((1, 2, 3), (1, 2, 3), (1, 2))
        with self.assertRaises(TypeError):
            p.Create((1, 2, 3), ("1", "2", "3"), (1, 2, 3))
        with self.assertRaises(ValueError):
            p.Create((257, 2, 3), (1, 2, 3), (1, 2, 3))
        with self.assertRaises(ValueError):
            p.Create((1, 2, 3), (-1, 2, 3), (1, 2, 3))


    def test_paletteCreate2(self):
        p = wx.Palette()
        self.assertTrue(p.Create((1, 2, 3), [4, 5, 6], bytearray([7, 8, 9])))
        self.assertTrue(p.GetRGB(1) == (2, 5, 8))


    def test_nullPalette(self):
        wx.NullPalette

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
