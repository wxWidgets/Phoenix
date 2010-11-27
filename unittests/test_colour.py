import unittest2
import wxPhoenix as wx


#---------------------------------------------------------------------------

class Colour(unittest2.TestCase):
    def setUp(self):
        if hasattr(wx, 'InitializeStockLists'):
            wx.InitializeStockLists() # switch to wx.App once we have that class working
        
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
    unittest2.main()
