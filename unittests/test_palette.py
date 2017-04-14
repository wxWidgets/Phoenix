import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class palette_Tests(wtc.WidgetTestCase):

    def test_paletteCtor1(self):
        # test with a bytearray like the original impl
        rgb = bytearray(range(256))
        p = wx.Palette(rgb, rgb, rgb)
        self.assertTrue(p.IsOk())
        self.assertTrue(p.GetColoursCount() == 256)
        self.assertTrue(p.GetPixel(42, 42, 42) == 42)
        self.assertTrue(p.GetRGB(64) == (64, 64, 64))
        with self.assertRaises(IndexError):
            p.GetRGB(257)


    def test_paletteCtor2(self):
        # and do the same using a list
        rgb = list(range(256))
        p = wx.Palette(rgb, rgb, rgb)
        self.assertTrue(p.IsOk())
        self.assertTrue(p.GetColoursCount() == 256)
        self.assertTrue(p.GetPixel(42, 42, 42) == 42)
        self.assertTrue(p.GetRGB(64) == (64, 64, 64))
        with self.assertRaises(IndexError):
            p.GetRGB(257)


    def test_paletteCtor3(self):
        p = wx.Palette()


    def test_paletteCtor4(self):
        p1 = wx.Palette()
        p2 = wx.Palette(p1)


    def test_paletteCreate1(self):
        p = wx.Palette()
        with self.assertRaises(TypeError):      # not sequences
            p.Create(1, 2, 3)
        with self.assertRaises(ValueError):     # not the same length
            p.Create((1, 2, 3), (1, 2, 3), (1, 2))
        with self.assertRaises(TypeError):      # not integers
            p.Create((1, 2, 3), ("1", "2", "3"), (1, 2, 3))
        with self.assertRaises(ValueError):     # outside of 0..255 range
            p.Create((257, 2, 3), (1, 2, 3), (1, 2, 3))
        with self.assertRaises(ValueError):     # outside of 0..255 range
            p.Create((1, 2, 3), (-1, 2, 3), (1, 2, 3))

                                                # range is okay, checking start and end
        p.Create((1, 2, 3, 0), (1, 2, 3, 4), (1, 2, 3, 4))
        p.Create((1, 2, 3, 255), (1, 2, 3, 4), (1, 2, 3, 4))


    def test_paletteCreate2(self):
        p = wx.Palette()
        # 3 different kinds of sequences :)
        self.assertTrue(p.Create((1, 2, 3), [4, 5, 6], bytearray([7, 8, 9])))
        self.assertTrue(p.GetRGB(1) == (2, 5, 8))


    def test_nullPalette(self):
        wx.NullPalette

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
