import unittest
from unittests import wtc
import wx
import os

icoFile = os.path.join(os.path.dirname(__file__), 'mondrian.ico')
pngFile = os.path.join(os.path.dirname(__file__), 'pointy.png')

#---------------------------------------------------------------------------

class iconbndl_Tests(wtc.WidgetTestCase):

    def test_iconbndl1(self):
        ib = wx.IconBundle()
        ib.AddIcon(icoFile)
        ib.AddIcon(wx.Icon(icoFile))
        i = ib.GetIcon()

    def test_iconbndl2(self):
        ib = wx.IconBundle(icoFile)
        ib2 = wx.IconBundle(ib)


    def test_iconbndl3(self):
        ib = wx.IconBundle(wx.Icon(icoFile))

    def test_iconbndl4(self):
        ib = wx.IconBundle()

        ib.Icon
        ib.IconCount

        wx.NullIconBundle


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
