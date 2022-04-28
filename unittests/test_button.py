import unittest
from unittests import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class ButtonTests(wtc.WidgetTestCase):

    def test_ButtonCtors(self):
        btn = wx.Button(self.frame, label='label')
        btn = wx.Button(self.frame, -1, 'label', (10,10), (100,-1), wx.BU_LEFT)
        bmp = wx.BitmapBundle(wx.Bitmap(pngFile))
        btn.SetBitmap(bmp)

    def test_ButtonProperties(self):
        btn = wx.Button(self.frame, label='label')

        # do the properties exist?
        btn.AuthNeeded
        btn.Bitmap
        btn.BitmapCurrent
        btn.BitmapDisabled
        btn.BitmapFocus
        btn.BitmapLabel
        btn.BitmapMargins
        btn.BitmapPressed
        btn.Label


    def test_ButtonDefaultCtor(self):
        btn = wx.Button()
        btn.Create(self.frame, -1, 'button label')



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
