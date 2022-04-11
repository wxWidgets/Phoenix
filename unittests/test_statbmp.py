import unittest
from unittests import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')
pngFile2 = os.path.join(os.path.dirname(__file__), 'pointy.png')


#---------------------------------------------------------------------------

class statbmp_Tests(wtc.WidgetTestCase):

    def test_statbmpCtor(self):
        bmp = wx.Bitmap(pngFile)
        sb = wx.StaticBitmap(self.frame, -1, bmp)
        sb = wx.StaticBitmap(self.frame, bitmap=bmp)


    def test_statbmpDefaultCtor(self):
        bmp = wx.Bitmap(pngFile)
        sb = wx.StaticBitmap()
        sb.Create(self.frame, -1, bmp)


    def test_statbmpProperties(self):
        bmp = wx.Bitmap(pngFile)
        sb = wx.StaticBitmap(self.frame, bitmap=bmp)

        sb.Bitmap
        sb.Bitmap = wx.Bitmap(pngFile2)

        #sb.Icon   # TODO: this asserts if SetIcon hasn't been called

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
