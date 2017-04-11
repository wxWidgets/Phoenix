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


    def test_eq_hash(self):
        tupl1 = (10, 20, 30, 40)
        clr1 = wx.Colour(*tupl1)
        clr12 = wx.Colour(*tupl1)
        clr2 = wx.Colour(10, 20, 30, 1)
        # __eq__ and __hash__ must both be defined
        # eq must assert that elements are of the same class
        self.assertFalse(clr1 == tupl1)
        self.assertTrue(hash(clr1) == hash(tupl1))
        # then within that class, hash must follow eq
        self.assertTrue(clr1 == clr12)
        self.assertFalse(id(clr1) == id(clr12))
        self.assertTrue(hash(clr1) == hash(clr12))

        self.assertFalse(clr1 == clr2)
        self.assertFalse(hash(clr1) == hash(clr2))


    def test_GetPixel(self):
        c1 = wx.Colour(1,2,3,4)
        p = c1.GetPixel()


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
