import unittest
from unittests import wtc
import wx
import os

icoFile = os.path.join(os.path.dirname(__file__), 'mondrian.ico')
pngFile = os.path.join(os.path.dirname(__file__), 'pointy.png')

#---------------------------------------------------------------------------

class bmpbndl_Tests(wtc.WidgetTestCase):

    def test_BitmapBundleCtor1(self):
        b1 = wx.BitmapBundle()
        self.assertTrue( not b1.IsOk() )

    def test_BitmapBundleCtor2(self):
        b2 = wx.BitmapBundle(wx.Bitmap(5, 10, 32))
        self.assertTrue( b2.IsOk() )

    def test_BitmapBundleCtor3(self):
        b3 = wx.BitmapBundle(wx.Icon(icoFile))
        self.assertTrue( b3.IsOk() )

    def test_BitmapBundleCtor4(self):
        b4 = wx.BitmapBundle(wx.Image(pngFile))
        self.assertTrue( b4.IsOk() )

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
