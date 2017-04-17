import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class position_Tests(wtc.WidgetTestCase):

    def test_positionCtors(self):
        p = wx.Position()
        self.assertTrue(p.Get() == (0,0))
        self.assertTrue(p.Get() != (9,9))
        p2 = wx.Position(2, 3)
        self.assertTrue(p2.Get() == (2,3))

    def test_positionCopyCtor(self):
        p1 = wx.Position(3,4)
        p2 = wx.Position(p1)
        self.assertTrue(p1 is not p2)
        self.assertTrue(p1 == p2)

    def test_position_eq_hash(self):
        tupl1 = (0, 10)
        p1 = wx.Position(*tupl1)
        p12 = wx.Position(*tupl1)
        p2 = wx.Position(2, 10)
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

    def test_positionProperties1(self):
        p = wx.Position()
        p.Row
        p.Col

    def test_positionProperties2(self):
        p = wx.Position()
        p.Row = 11
        p.Col = 12
        self.assertTrue(p.Get() == (11, 12))

    def test_positionMath1(self):
        p1 = wx.Position(3,4)
        p2 = wx.Position(1,1)
        p1 -= p2
        self.assertTrue(p1.Get() == (2,3))
        p1 += p2
        self.assertTrue(p1.Get() == (3,4))

    def test_positionMath2(self):
        p1 = wx.Position(3,4)
        p2 = wx.Position(1,1)
        p3 = p1 + p2
        self.assertTrue(p3.Get() == (4,5))
        p4 = p3 - p2
        self.assertTrue(p4.Get() == (3,4))
        self.assertTrue(p4 == p1)


    def test_GetIM(self):
        # Test the immutable version returned by GetIM
        obj = wx.Position(1,2)
        im = obj.GetIM()
        assert isinstance(im, tuple)
        assert im.Row == obj.Row
        assert im.Col == obj.Col
        obj2 = wx.Position(im)
        assert obj == obj2




#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
