import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class affinematrix2d_Tests(wtc.WidgetTestCase):

    def test_affinematrix2d1(self):
        m = wx.Matrix2D()
        am = wx.AffineMatrix2D()
        am.Set(m, (23, 25))
        values = am.Get()
        self.assertTrue(len(values) == 2)
        self.assertTrue(isinstance(values[0], wx.Matrix2D))
        self.assertTrue(isinstance(values[1], wx.Point2D))


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
