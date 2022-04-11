import unittest
from unittests import wtc
import wx
import os

#---------------------------------------------------------------------------

class gauge_Tests(wtc.WidgetTestCase):

    def test_gauge(self):
        g1 = wx.Gauge(self.frame)
        g2 = wx.Gauge(self.frame, range=1000, style=wx.GA_VERTICAL)

    def test_gaugeProperties(self):
        g = wx.Gauge(self.frame)

        g.Range
        g.Value



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
