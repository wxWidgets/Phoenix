import unittest
import wx
from unittests import wtc

#---------------------------------------------------------------------------

class Colour(wtc.WidgetTestCase):

    def test_default_ctor(self):
        c = wx.Colour()
        self.assertTrue(not c.IsOk())
        self.assertTrue(c.Get() == (-1,-1,-1,255))


    def test_rgb_ctor(self):
        c = wx.Colour(1,2,3)
        self.assertTrue(c.Get(False) == (1,2,3))


    def test_rgba_ctor(self):
        c = wx.Colour(1,2,3,4)
        self.assertTrue(c.Get() == (1,2,3,4))


    def test_copy_ctor(self):
        c1 = wx.Colour(1,2,3,4)
        c2 = wx.Colour(c1)
        self.assertTrue(c1 == c2)
        self.assertTrue(c1 is not c2)
        self.assertTrue(c1.Get() == c2.Get())


    def test_seq_ctor1(self):
        c = wx.Colour( [1,2,3,4] )
        self.assertTrue(c.Get() == (1,2,3,4))


    def test_seq_ctor2(self):
        c = wx.Colour( [1,2,3] )
        self.assertTrue(c.Get(False) == (1,2,3))


    def test_numpy_ctor(self):
        import numpy
        a = numpy.array( [1,2,3,4] )
        c = wx.Colour(a)
        self.assertTrue(c.Get() == (1,2,3,4))


    def test_GetPixel(self):
        c1 = wx.Colour(1,2,3,4)
        p = c1.GetPixel()


    def test_converters(self):
        # Ensure that other types that are sequence-like can't be
        # auto-converted, the copy constructor is good-enough for testing this
        with self.assertRaises(TypeError):
            p = wx.Colour(wx.Rect(1,2,3,4))


    def test_GetIM(self):
        # Test the immutable version returned by GetIM
        obj = wx.Colour(1,2,3,4)
        im = obj.GetIM()
        assert isinstance(im, tuple)
        assert im.red == obj.red
        assert im.green == obj.green
        assert im.blue == obj.blue
        assert im.alpha == obj.alpha
        obj2 = wx.Colour(im)
        assert obj == obj2


    if hasattr(wx, 'testColourTypeMap'):
        def test_ColourTypemaps(self):
            c = wx.testColourTypeMap('red')
            self.assertTrue(c.Get() == (0xff, 0, 0, 0xff))
            c = wx.testColourTypeMap('Blue:80')
            self.assertTrue(c.Get() == (0, 0, 0xff, 0x80))
            c = wx.testColourTypeMap('#112233')
            self.assertTrue(c.Get() == (0x11, 0x22, 0x33, 0xff))
            c = wx.testColourTypeMap('#11223344')
            self.assertTrue(c.Get() == (0x11, 0x22, 0x33, 0x44))
            c = wx.testColourTypeMap(None)
            self.assertTrue(c.Get() == (-1, -1, -1, 0xff))
            c = wx.testColourTypeMap( (1,2,3) )
            self.assertTrue(c.Get() == (1, 2, 3, 0xff))
            c = wx.testColourTypeMap( (1,2,3,4) )
            self.assertTrue(c.Get() == (1, 2, 3, 4))


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
