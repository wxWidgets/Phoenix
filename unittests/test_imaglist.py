import unittest
from unittests import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'pointy.png')

#---------------------------------------------------------------------------

class image_Tests(wtc.WidgetTestCase):

    def test_imaglist(self):
        bmp = wx.Bitmap(pngFile)
        w, h = bmp.GetSize()
        i = wx.ImageList(w, h)
        i.Add(bmp)


    def test_imaglistConstants(self):
        wx.IMAGE_LIST_NORMAL
        wx.IMAGE_LIST_SMALL
        wx.IMAGE_LIST_STATE
        wx.IMAGELIST_DRAW_NORMAL
        wx.IMAGELIST_DRAW_TRANSPARENT
        wx.IMAGELIST_DRAW_SELECTED
        wx.IMAGELIST_DRAW_FOCUSED


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
