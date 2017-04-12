import unittest
import wx


#---------------------------------------------------------------------------

class Point2D(unittest.TestCase):

    def test_default_ctor(self):
        p = wx.Point2D()

    def test_xy_ctor(self):
        p = wx.Point2D(12.3, 45.6)

    def test_copy_ctor(self):
        p1 = wx.Point2D(1.23, 4.56)
        p2 = wx.Point2D(p1)
        self.assertTrue(p1 == p2)
        self.assertTrue(p1 is not p2)
        self.assertTrue(p1.Get() == (1.23, 4.56))

    def test_eq_hash(self):
        tupl1 = (0, 10)
        p1 = wx.Point2D(*tupl1)
        p12 = wx.Point2D(*tupl1)
        p2 = wx.Point2D(2, 10)
        # __eq__ and __hash__ must both be defined
        # eq must assert that elements are of the same class
        self.assertFalse(p1 == tupl1)
        self.assertTrue(hash(p1) == hash(tupl1))
        # then within that class, hash must follow eq
        self.assertTrue(p1 == p12)
        self.assertFalse(id(p1) == id(p12))
        self.assertTrue(hash(p1) == hash(p12))

        self.assertFalse(p1 == p2)
        self.assertFalse(hash(p1) == hash(p2))



class Rect2D(unittest.TestCase):

    def test_default_ctor(self):
        r = wx.Rect2D()

    def test_xywh_ctor(self):
        r = wx.Rect2D(.5, .5, 100.1, 99.2)

    def test_copy_ctor(self):
        r1 = wx.Rect2D(.5, .5, 100.1, 99.2)
        r2 = wx.Rect2D(r1)
        self.assertTrue(r1 == r2)
        self.assertTrue(r1 is not r2)
        self.assertTrue(r1.Get() == (.5, .5, 100.1, 99.2))

    def test_eq_hash(self):
        tupl1 = (1, 2, 3, 4)
        r1 = wx.Rect2D(*tupl1)
        r12 = wx.Rect2D(*tupl1)
        r2 = wx.Rect2D(1, 2, 4, 3)
        # __eq__ and __hash__ must both be defined
        # eq must assert that elements are of the same class
        self.assertFalse(r1 == tupl1)
        self.assertTrue(hash(r1) == hash(tupl1))
        # then within that class, hash must follow eq
        self.assertTrue(r1 == r12)
        self.assertFalse(id(r1) == id(r12))
        self.assertTrue(hash(r1) == hash(r12))

        self.assertFalse(r1 == r2)
        self.assertFalse(hash(r1) == hash(r2))



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
