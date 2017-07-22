import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class stockgdi_Tests(wtc.WidgetTestCase):

    def test_stockgdi1(self):
        # ensure that all the stock objects have been created and also initialized
        for item in [ wx.NORMAL_FONT,
                      wx.SMALL_FONT,
                      wx.SWISS_FONT,
                      wx.ITALIC_FONT,

                      wx.BLACK_DASHED_PEN,
                      wx.BLACK_PEN,
                      wx.BLUE_PEN,
                      wx.CYAN_PEN,
                      wx.GREEN_PEN,
                      wx.YELLOW_PEN,
                      wx.GREY_PEN,
                      wx.LIGHT_GREY_PEN,
                      wx.MEDIUM_GREY_PEN,
                      wx.RED_PEN,
                      wx.TRANSPARENT_PEN,
                      wx.WHITE_PEN,

                      wx.BLACK_BRUSH,
                      wx.BLUE_BRUSH,
                      wx.CYAN_BRUSH,
                      wx.GREEN_BRUSH,
                      wx.YELLOW_BRUSH,
                      wx.GREY_BRUSH,
                      wx.LIGHT_GREY_BRUSH,
                      wx.MEDIUM_GREY_BRUSH,
                      wx.RED_BRUSH,
                      wx.TRANSPARENT_BRUSH,
                      wx.WHITE_BRUSH,

                      wx.BLACK,
                      wx.BLUE,
                      wx.CYAN,
                      wx.GREEN,
                      wx.YELLOW,
                      wx.LIGHT_GREY,
                      wx.RED,
                      wx.WHITE,

                      wx.CROSS_CURSOR,
                      wx.HOURGLASS_CURSOR,
                      wx.STANDARD_CURSOR,
                      ]:
            self.assertTrue(item.IsOk())

    def test_stockgdi2(self):
        wx.TheFontList
        wx.ThePenList
        wx.TheBrushList
        wx.TheColourDatabase


    def test_stockgdi3(self):
        b = wx.StockGDI.GetBrush(wx.StockGDI.BRUSH_GREEN)
        clr = wx.StockGDI.GetColour(wx.StockGDI.COLOUR_YELLOW)
        cur = wx.StockGDI.GetCursor(wx.StockGDI.CURSOR_HOURGLASS)
        p = wx.StockGDI.GetPen(wx.StockGDI.PEN_RED)
        f = wx.StockGDI.instance().GetFont(wx.StockGDI.FONT_NORMAL)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
