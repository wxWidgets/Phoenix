import imp_unittest, unittest
import wtc
import wx
import os


pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class dc_Tests(wtc.WidgetTestCase):
    
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
        
        
    def test_DCClipper(self):
        dc = wx.ClientDC(self.frame)
        c = wx.DCClipper(dc, wx.Rect(10,10,25,25))
        del c
        c = wx.DCClipper(dc, (10,10,25,25))
        del c
        c = wx.DCClipper(dc, 10,10,25,25)
        del c
        r = wx.Region(10,10,25,25)
        c = wx.DCClipper(dc, r)
        del c
        

    def test_DCBrushChanger(self):
        dc = wx.ClientDC(self.frame)
        c = wx.DCBrushChanger(dc, wx.Brush('blue'))
        del c


    def test_DCPenChanger(self):
        dc = wx.ClientDC(self.frame)
        c = wx.DCPenChanger(dc, wx.Pen('blue'))
        del c


    def test_DCTextColourChanger(self):
        dc = wx.ClientDC(self.frame)
        c = wx.DCTextColourChanger(dc)
        c.Set('blue')
        del c
        c = wx.DCTextColourChanger(dc, 'blue')
        del c
        
        
    def test_DCFontChanger(self):
        dc = wx.ClientDC(self.frame)
        font = wx.FFont(12, wx.FONTFAMILY_SWISS)
        c = wx.DCFontChanger(dc)
        c.Set(font)
        del c
        c = wx.DCFontChanger(dc, font)
        del c
        

    def test_NativeWinHandle(self):
        dc = wx.ClientDC(self.frame)
        if 'wxMSW' in wx.PlatformInfo:
            h = dc.GetHDC()
            self.assertNotEqual(h, 0)
        else:
            with self.assertRaises(NotImplementedError):
                h = dc.GetHDC()
            
    def test_NativeGTKHandle(self):
        dc = wx.ClientDC(self.frame)
        if 'wxGTK' in wx.PlatformInfo:
            h = dc.GetGdkDrawable()
            self.assertNotEqual(h, 0)
        else:
            with self.assertRaises(NotImplementedError):
                h = dc.GetGdkDrawable()
            
    def test_NativeMacHandle(self):
        dc = wx.ClientDC(self.frame)
        if 'wxMac' in wx.PlatformInfo:
            h = dc.GetCGContext()
            self.assertNotEqual(h, 0)
        else:
            with self.assertRaises(NotImplementedError):
                h = dc.GetCGContext()
            
    def test_trickyStuff(self):
        # execute some tricky tweaks to make sure they work are as they are supposed to.
        dc = wx.ClientDC(self.frame)
        bmp = wx.Bitmap(pngFile)
        dc.DrawLabel("toucan", bmp, (10,10, 200, 100))
        
        values = dc.GetPartialTextExtents("Hello")
        self.assertTrue(type(values) == list)
        self.assertTrue(len(values) == 5)

    def test_dcPointLists(self):
        dc = wx.ClientDC(self.frame)

        dc.DrawLines([wx.Point(5,5), wx.Point(25,5), wx.Point(25,25), wx.Point(25,5), wx.Point(5,5)])
        dc.DrawLines([(15,15), (35,15), (35,35), (35,15), (15,15)])
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
