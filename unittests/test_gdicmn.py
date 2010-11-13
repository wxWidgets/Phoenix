import unittest2
import wx

class Point(unittest2.TestCase):
    
    def test_default_ctor(self):
        p = wx.Point()
        self.assertTrue(p == (0,0))
        
    def test_xy_ctor(self):
        p = wx.Point(123,456)
        
    def test_RealPoint_ctor(self):
        p = wx.Point(wx.RealPoint(1.2, 2.9))
        self.assertTrue(p == (1,2))
        
    def test_copy_ctor(self):
        p1 = wx.Point(3,4)
        p2 = wx.Point(p1)
        self.assertTrue(p1 is not p2)
        self.assertTrue(p1 == p2)
        
    def test_bogus_ctor1(self):
        with self.assertRaises(TypeError):
            p = wx.Point('fiddle-fadle')
        
    def test_bogus_ctor2(self):
        with self.assertRaises(TypeError):
            p = wx.Point(1,2,3)

    def test_DefaultPosition(self):
        wx.DefaultPosition
        self.assertTrue(wx.DefaultPosition == (-1,-1))
        
    def test_FullySpecified(self):
        p = wx.Point(1,2)
        self.assertTrue(p.IsFullySpecified())
        p = wx.Point(-1,2)
        self.assertTrue(not p.IsFullySpecified())
        
    def test_xy(self):
        p = wx.Point(2, 3)
        self.assertTrue(p.x == 2 and p.y == 3)
        p.x += 1
        p.y += 2
        self.assertTrue(p.x == 3 and p.y == 5)
        self.assertTrue(p == (3,5))
        
    def test_Get(self):
        p = wx.Point(5,6)
        self.assertTrue(type(p.Get()) == tuple)
        self.assertTrue(p.Get() == (5,6))
        
    def test_operators(self):
        p1 = wx.Point(100, 500)
        p2 = wx.Point(50, 100)
        p1 == p2
        p1 != p2
        p = p1 + p2
        p = p1 + wx.Size(5,5)
        p = -p1
        p = p1 - p2
        p = p1 - wx.Size(5,5)
        p = p1 * 5
        p = 5 * p1
        p = p1 / 5
        p1 += p2
        p1 -= p2
        
    def test_magic(self):
        p = wx.Point(5,6)
        self.assertTrue(str(p) == "(5, 6)")
        self.assertTrue(repr(p) == "wx.Point(5, 6)")
        self.assertTrue(len(p) == 2)
        x, y = p
        self.assertTrue(x == 5 and y == 6)
        p[0] += 1  # tests both getitem and setitem
        p[1] += 2
        self.assertTrue(p == (6,8))
        with self.assertRaises(IndexError):
            p[2]
        



if __name__ == '__main__':
    unittest2.main()