import unittest
from unittests import wtc
import wx.ribbon


#---------------------------------------------------------------------------

class ribbon_control_Tests(wtc.WidgetTestCase):

    def test_ribbon_control1(self):
        ctrl = wx.ribbon.RibbonControl()
        ctrl.Create(self.frame)



    def test_ribbon_control2(self):
        ctrl = wx.ribbon.RibbonControl(self.frame)

        ctrl.GetArtProvider()
        ctrl.IsSizingContinuous()
        ctrl.GetNextSmallerSize(wx.VERTICAL)
        ctrl.GetNextLargerSize(wx.HORIZONTAL)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
