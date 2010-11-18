import unittest2
import wx


#---------------------------------------------------------------------------

class Point2D(unittest2.TestCase):
    
    def test_default_ctor(self):
        p = wx.Point2D()
        
    def test_xy_ctor(self):
        p = wx.Point2D(12.3, 45.6)
        
    def test_copy_ctor(self):
        p1 = wx.Point2D(1.23, 4.56)
        p2 = wx.Point2D(p1)
        self.assertTrue(p1 == p2)
        self.assertTrue(p1 is not p2)
        self.assertTrue(p1 == (1.23, 4.56))
        

        
class Rect2D(unittest2.TestCase):

    def test_default_ctor(self):
        r = wx.Rect2D()
        
    def test_xywh_ctor(self):
        r = wx.Rect2D(.5, .5, 100.1, 99.2)
        
    def test_copy_ctor(self):
        r1 = wx.Rect2D(.5, .5, 100.1, 99.2)
        r2 = wx.Rect2D(r1)
        self.assertTrue(r1 == r2)
        self.assertTrue(r1 is not r2)
        self.assertTrue(r1 == (.5, .5, 100.1, 99.2))
        
    
    
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest2.main()
    