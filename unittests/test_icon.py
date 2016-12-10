import unittest
from unittests import wtc
import wx
import os

icoFile = os.path.join(os.path.dirname(__file__), 'mondrian.ico')
pngFile = os.path.join(os.path.dirname(__file__), 'pointy.png')

#---------------------------------------------------------------------------

class icon_Tests(wtc.WidgetTestCase):

    def test_icon1(self):
        i1 = wx.Icon(icoFile)
        i2 = wx.Icon(i1)

    def test_icon2(self):
        i = wx.Icon()
        i.CopyFromBitmap(wx.Bitmap(pngFile))

    def test_icon3(self):
        i = wx.Icon(icoFile)
        i.Depth
        i.Width
        i.Height
        i.Handle

        i.SetDepth(32)
        i.SetWidth(32)
        i.SetHeight(32)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
