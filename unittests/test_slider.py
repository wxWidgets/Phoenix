import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class slider_Tests(wtc.WidgetTestCase):

    def test_sliderCtor(self):
        s1 = wx.Slider(self.frame)
        s2 = wx.Slider(self.frame, value=5, minValue=1, maxValue=10)

    def test_sliderDefaultCtor(self):
        s = wx.Slider()
        s.Create(self.frame)

    def test_sliderRange(self):
        s = wx.Slider(self.frame)
        s.SetRange(25, 75)
        self.assertTrue(s.GetRange() == (25, 75))
        self.assertTrue(s.GetMin() == 25)
        self.assertTrue(s.GetMax() == 75)
        self.assertTrue(s.Range == (25, 75))

    def test_sliderRange2(self):
        s = wx.Slider(self.frame)
        s.SetMin(25)
        s.SetMax(75)
        self.assertTrue(s.GetRange() == (25, 75))
        self.assertTrue(s.GetMin() == 25)
        self.assertTrue(s.GetMax() == 75)
        self.assertTrue(s.Range == (25, 75))


    def test_sliderFlags(self):
        wx.SL_HORIZONTAL
        wx.SL_VERTICAL
        wx.SL_TICKS
        wx.SL_AUTOTICKS
        wx.SL_LEFT
        wx.SL_TOP
        wx.SL_RIGHT
        wx.SL_BOTTOM
        wx.SL_BOTH
        wx.SL_SELRANGE
        wx.SL_INVERSE
        wx.SL_MIN_MAX_LABELS
        wx.SL_VALUE_LABEL
        wx.SL_LABELS

    def test_sliderProperties(self):
        s = wx.Slider(self.frame)
        s.LineSize
        s.Max
        s.Min
        s.PageSize
        s.SelEnd
        s.SelStart
        s.ThumbLength
        s.TickFreq
        s.Value
        s.Range

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
