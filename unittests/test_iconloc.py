import unittest
from unittests import wtc
import wx
import os

icoFile = os.path.join(os.path.dirname(__file__), 'mondrian.ico')
pngFile = os.path.join(os.path.dirname(__file__), 'pointy.png')

#---------------------------------------------------------------------------

class iconloc_Tests(wtc.WidgetTestCase):

    def test_iconloc1(self):
        loc = wx.IconLocation(icoFile)
        i = wx.Icon(loc)

    def test_iconloc2(self):
        loc = wx.IconLocation()
        loc.SetFileName(icoFile)
        i = wx.Icon(loc)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
