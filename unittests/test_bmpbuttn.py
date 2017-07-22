import unittest
from unittests import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class BitmapButtonTests(wtc.WidgetTestCase):

    def test_BitmapButtonCtor(self):
        bmp = wx.Bitmap(pngFile)
        btn = wx.BitmapButton(self.frame, -1, bmp)


    def test_BitmapButtonDefaultCtor(self):
        bmp = wx.Bitmap(pngFile)
        btn = wx.BitmapButton()
        btn.Create(self.frame, -1, bmp)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
