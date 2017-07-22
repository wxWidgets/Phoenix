import unittest
from unittests import wtc
import wx
import sys
import os

fileName = 'svgtest.svg'

#---------------------------------------------------------------------------

class SvgDCTests(wtc.WidgetTestCase):

    def test_SvgDC1(self):
        dc = wx.SVGFileDC(fileName)
        dc.DrawLine(0,0, 50,50)
        del dc

        os.remove(fileName)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
