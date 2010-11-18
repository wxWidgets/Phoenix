import unittest2
import wx


#---------------------------------------------------------------------------

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
        
#---------------------------------------------------------------------------


class Size(unittest2.TestCase):
    
    def test_default_ctor(self):
        s = wx.Size()
        self.assertTrue(s == (0,0))
         
    def test_wh_ctor(self):
        s = wx.Size(100,200)
        
    def test_copy_ctor(self):
        s1 = wx.Size(100,200)
        s2 = wx.Size(s1)
        self.assertTrue(s1 is not s2)
        self.assertTrue(s1 == s2)        
        
    def test_bogus_ctor(self):
        with self.assertRaises(TypeError):
            s = wx.Size("aa", "bb")
            
    def test_DecBy(self):
        s = wx.Size(100,100)
        s.DecBy(wx.Point(5,5))
        self.assertTrue(s == (95,95))
        s.DecBy(wx.Size(5,5))
        self.assertTrue(s == (90,90))        
        s.DecBy(5,5)
        self.assertTrue(s == (85,85))        
        s.DecBy(5)
        self.assertTrue(s == (80,80))     
        s.DecBy( (5,5) )
        self.assertTrue(s == (75,75))     
        
        
    def test_IncBy(self):
        s = wx.Size(50,50)
        s.IncBy(wx.Point(5,5))
        self.assertTrue(s == (55,55))
        s.IncBy(wx.Size(5,5))
        self.assertTrue(s == (60,60))        
        s.IncBy(5,5)
        self.assertTrue(s == (65,65))        
        s.IncBy(5)
        self.assertTrue(s == (70,70))        
        s.IncBy( (5,5) )
        self.assertTrue(s == (75,75))     
        
    def test_DecTo(self):
        s = wx.Size(5, 15)
        s.DecTo( (10,10) )
        self.assertTrue(s == (5,10))
        
    def test_IncTo(self):
        s = wx.Size(5, 15)
        s.IncTo( (10,10) )
        self.assertTrue(s == (10,15))
        
    def test_properties(self):
        s = wx.Size(23,34)
        self.assertTrue(s.width == 23 and s.height == 34)
        s.width += 1
        s.height += 1
        self.assertTrue(s == (24,35))
        
    def test_operators(self):
        s1 = wx.Size(100,200)
        s2 = wx.Size(30,40)
        s1 += s2
        s1 -= s2
        s1 *= 5
        s1 /= 5
        s1 == s2
        s1 != s2
        s = s1 * 5
        s = 5 * s1
        s = s1 + s2
        s = s1 - s2
        s = s1 / 5
        
    def test_DefaultSize(self):
        ds = wx.DefaultSize
        self.assertRaises(ds == (-1,-1))
        
    def test_GetSet(self):
        s = wx.Size(100,200)
        t = s.Get()
        self.assertTrue(type(t) == tuple)
        self.assertTrue(t == (100,200))
        s.Set(5,10)
        self.assertTrue(s.Get() == (5,10))
        
    def test_SetDefaults(self):
        s = wx.Size(50, -1)
        s.SetDefaults( (25,25) )
        self.assertTrue(s == (50,25))
        
    def test_FullySpecified(self):
        self.assertTrue(wx.Size(40,50).IsFullySpecified())
        self.assertTrue(not wx.Size(-1,50).IsFullySpecified())
        self.assertTrue(not wx.Size(40,-1).IsFullySpecified())
        
    def test_magic(self):
        s = wx.Size(5,6)
        self.assertTrue(str(s) == "(5, 6)")
        self.assertTrue(repr(s) == "wx.Size(5, 6)")
        self.assertTrue(len(s) == 2)
        w, h = s
        self.assertTrue(5 == 5 and h == 6)
        s[0] += 1  # tests both getitem and setitem
        s[1] += 2
        self.assertTrue(s == (6,8))
        with self.assertRaises(IndexError):
            s[2]
        
        
#---------------------------------------------------------------------------
        
        
class RealPoint(unittest2.TestCase):
    
    def test_default_ctor(self):
        p = wx.RealPoint()
        
    def test_xy_ctor(self):
        p = wx.RealPoint(12.3, 34.5)
        
    def test_Point_ctor(self):
        p = wx.RealPoint(wx.Point(3,5))
        p = wx.RealPoint( (3,5) )
        
    def test_copy_ctor(self):
        p1 = wx.RealPoint(12.3, 45.6)
        p2 = wx.RealPoint(p1)
        
    def test_properties(self):
        p = wx.RealPoint(12.3, 45.6)
        p.x += 2
        p.y += 2
        

    
#---------------------------------------------------------------------------
        
class Rect(unittest2.TestCase):
    
    def test_default_ctor(self):
        r = wx.Rect()
        
    def test_xywh_ctor(self):
        r = wx.Rect(1, 2, 3, 4)
        
    def test_possize_ctor(self):
        r = wx.Rect(wx.Point(10,10), wx.Size(100,100))
        self.assertTrue(r.width == 100 and r.height == 100)
        self.assertTrue(r.x == 10 and r.y == 10)
        self.assertTrue(r == wx.Rect(pos=(10,10), size=(100,100)))
        
    def test_tlbr_ctor(self):
        # TODO: we have to use keyword args here since wx.Point has sequence
        # protocol methods then it can also match the typemap for wxSize and
        # the other ctor is found first. Check if there is a way to fix or
        # work around this.
        r = wx.Rect(topLeft=wx.Point(10,10), bottomRight=wx.Point(100,100))
        self.assertTrue(r.width == 91 and r.height == 91)
        self.assertTrue(r.bottomRight == wx.Point(100,100))
        self.assertTrue(r.topLeft == wx.Point(10,10))

    def test_size_ctor(self):
        r = wx.Rect(wx.Size(50,100))
        self.assertTrue(r.width == 50 and r.height == 100)
        self.assertTrue(r.x == 0 and r.y == 0)
        
        
    # TODO: more tests!
        
        
        
#---------------------------------------------------------------------------
        

if __name__ == '__main__':
    unittest2.main()