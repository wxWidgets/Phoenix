import unittest
from unittests import wtc
import wx
import os


#---------------------------------------------------------------------------

class pen_Tests(wtc.WidgetTestCase):

    def test_penCtor1(self):
        p = wx.Pen()
        self.assertTrue(not p.IsOk())
        p.SetColour(wx.BLUE)
        p.SetWidth(1)
        p.SetStyle(wx.PENSTYLE_SOLID)
        self.assertTrue(p.IsOk())


    def test_penCtor2(self):
        p = wx.Pen(wx.BLUE)
        self.assertTrue(p.IsOk())
        self.assertTrue(p.GetColour() == wx.BLUE)

        p = wx.Pen('blue')
        self.assertTrue(p.IsOk())
        self.assertTrue(p.GetColour() == wx.BLUE)

        p = wx.Pen('#0000FF')
        self.assertTrue(p.IsOk())
        self.assertTrue(p.GetColour() == wx.BLUE)


    def test_penCtor3(self):
        p1 = wx.Pen(wx.BLUE, 2, wx.PENSTYLE_SOLID)
        p2 = wx.Pen(p1)
        self.assertTrue( p1 is not p2)
        self.assertTrue( p1 == p2)


    def test_penNull(self):
        wx.NullPen
        self.assertTrue(not wx.NullPen.IsOk())


    def test_penNonzero(self):
        p = wx.Pen(wx.BLUE)
        test = False
        if p:
            test = True
        self.assertTrue(test)


    def test_penStock(self):
        for p in [wx.RED_PEN, wx.BLUE_PEN, wx.CYAN_PEN, wx.GREEN_PEN,
                  wx.YELLOW_PEN, wx.BLACK_PEN, wx.WHITE_PEN,
                  wx.TRANSPARENT_PEN, wx.BLACK_DASHED_PEN, wx.GREY_PEN,
                  wx.MEDIUM_GREY_PEN, wx.LIGHT_GREY_PEN]:
            self.assertTrue(isinstance(p, wx.Pen))
            self.assertTrue(p.IsOk())


    def test_penDashes(self):
        p = wx.Pen()
        p.Style = wx.PENSTYLE_USER_DASH
        p.Width = 1
        dashes = [1,2,2,1]
        p.SetDashes(dashes)
        d = p.GetDashes()
        self.assertTrue(d == dashes)


    def test_penProperties(self):
        p = wx.Pen(wx.BLUE)
        p.Cap
        p.Colour
        p.Dashes
        p.Join
        p.Stipple
        p.Style
        p.Width


    def test_penConstants(self):
        wx.PENSTYLE_INVALID
        wx.PENSTYLE_SOLID
        wx.PENSTYLE_DOT
        wx.PENSTYLE_LONG_DASH
        wx.PENSTYLE_SHORT_DASH
        wx.PENSTYLE_DOT_DASH
        wx.PENSTYLE_USER_DASH
        wx.PENSTYLE_TRANSPARENT
        wx.PENSTYLE_STIPPLE_MASK_OPAQUE
        wx.PENSTYLE_STIPPLE_MASK
        wx.PENSTYLE_STIPPLE
        wx.PENSTYLE_BDIAGONAL_HATCH
        wx.PENSTYLE_CROSSDIAG_HATCH
        wx.PENSTYLE_FDIAGONAL_HATCH
        wx.PENSTYLE_CROSS_HATCH
        wx.PENSTYLE_HORIZONTAL_HATCH
        wx.PENSTYLE_VERTICAL_HATCH
        wx.PENSTYLE_FIRST_HATCH
        wx.PENSTYLE_LAST_HATCH

        wx.JOIN_INVALID
        wx.JOIN_BEVEL
        wx.JOIN_MITER
        wx.JOIN_ROUND

        wx.CAP_INVALID
        wx.CAP_ROUND
        wx.CAP_PROJECTING
        wx.CAP_BUTT


    def test_penOldStyleNames(self):
        p = wx.Pen('red', 1, wx.STIPPLE)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
