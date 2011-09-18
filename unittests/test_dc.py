import imp_unittest
import wtc
import wx

# NOTE: The wx.DC tests are done in the test modules for the various DC types
# that inherit from wx.DC. The stuff tested here are just the other items
# generated from etg/dc.py

# TODO: It may make sense to make a mixin class here that does test various
# aspects and drawing APIs of a DC, and then have the other DC test cases mix
# with it and call its methods.


#---------------------------------------------------------------------------

class DCTests(wtc.WidgetTestCase):
    
    def test_ConstantsExist(self):
        wx.CLEAR
        wx.XOR
        wx.INVERT
        wx.OR_REVERSE
        wx.AND_REVERSE
        wx.COPY
        wx.AND
        wx.AND_INVERT
        wx.NO_OP
        wx.NOR
        wx.EQUIV
        wx.SRC_INVERT
        wx.OR_INVERT
        wx.NAND
        wx.OR
        wx.SET
        
        wx.FLOOD_SURFACE
        wx.FLOOD_BORDER

        wx.MM_TEXT
        wx.MM_METRIC
        wx.MM_LOMETRIC
        wx.MM_TWIPS
        wx.MM_POINTS
        
        
        
    def test_FontMetrics(self):
        fm = wx.FontMetrics()
        fm.height
        fm.ascent
        fm.descent
        fm.internalLeading
        fm.externalLeading
        fm.averageWidth
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
