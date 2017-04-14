import unittest
from unittests import wtc
import wx
import sys, os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class region_Tests(wtc.WidgetTestCase):

    def test_regionCtors(self):
        r = wx.Region()
        r = wx.Region(10, 10, 100, 100)
        r = wx.Region(wx.Point(10,10), wx.Point(100,100))
        r = wx.Region(wx.Rect(10,10, 100, 100))
        r2 = wx.Region(r)
        r = wx.Region([(10,10), (100, 10), (100, 100), (10, 100)])
        bmp = wx.Bitmap(pngFile)
        r = wx.Region(bmp)
        r = wx.Region(bmp, 'black')


    def test_regionIterator1(self):
        region = wx.Region([(10,10), (100, 100), (10, 100)])
        iterator = wx.RegionIterator(region)
        count = 0
        while iterator:
            rect = iterator.GetRect()
            self.assertTrue(isinstance(rect, wx.Rect))
            iterator.Next()
            count += 1
        self.assertTrue(count > 0)


    def test_regionIterator2(self):
        region = wx.Region([(10,10), (100, 100), (10, 100)])
        count = 0
        for rect in region:
            self.assertTrue(isinstance(rect, wx.Rect))
            count += 1
        self.assertTrue(count > 0)


    def test_regionOtherRandomStuff(self):
        region = wx.Region([(10,10), (100, 100), (10, 100)])
        bmp = wx.Bitmap(pngFile)
        region.Union(bmp)
        region.Contains(10, 20)
        region.Contains(wx.Point(10,20))
        region.Contains(wx.Rect(10,20,4,4))
        region.Subtract(wx.Rect(10,20,4,4))

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
