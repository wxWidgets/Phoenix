import unittest
from unittests import wtc
import wx

import wx.lib.agw.rulerctrl as RC

#---------------------------------------------------------------------------

class lib_agw_rulerctrl_Tests(wtc.WidgetTestCase):

    def test_lib_agw_rulerctrlCtor(self):
        ruler = RC.RulerCtrl(self.frame, -1, orient=wx.HORIZONTAL, style=wx.SUNKEN_BORDER)

    def test_lib_agw_rulerctrlMethods(self):
        ruler = RC.RulerCtrl(self.frame, -1, orient=wx.VERTICAL, style=wx.STATIC_BORDER)

        # Some methods tests...
        self.assertEqual(ruler.GetFormat(), RC.RealFormat)

    def test_lib_agw_rulerctrlEvents(self):
        RC.EVT_INDICATOR_CHANGED
        RC.EVT_INDICATOR_CHANGING
        RC.wxEVT_INDICATOR_CHANGED
        RC.wxEVT_INDICATOR_CHANGING

    def drawRuler(self, size, orient=wx.HORIZONTAL, range=(0, 10), indicator=False):
        ruler = RC.RulerCtrl(self.frame, -1, size=size, orient=orient)
        ruler.SetBounds(0, 0, size[0], size[1])
        ruler.SetRange(*range)
        if indicator:
            ruler.AddIndicator(wx.ID_ANY, range[0])
        bmp = wx.Bitmap(100, 100)
        dc = wx.MemoryDC(bmp)
        ruler.Draw(dc)
        dc.SelectObject(wx.NullBitmap)

    def test_lib_agw_rulerctrlEmptyRange(self):
        self.drawRuler((300, 30), range=(0, 0), indicator=True)

    def test_lib_agw_rulerctrlZeroLength(self):
        self.drawRuler((0, 30))
        self.drawRuler((30, 0), orient=wx.VERTICAL)

    def test_lib_agw_rulerctrlLabelLongerThanRuler(self):
        self.drawRuler((30, 5), orient=wx.VERTICAL, range=(0, 1000))
        self.drawRuler((5, 30), range=(0, 100000))


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
