import unittest
from unittests import wtc
import wx
import os
import warnings

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


    def test_NativeHandle(self):
        dc = wx.MemoryDC(wx.Bitmap(10,10))
        h = dc.GetHandle()
        self.assertTrue(h is not None)
        self.assertNotEqual(int(h), 0)


    def test_NativeWinHandle(self):
        dc = wx.ClientDC(self.frame)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaises(wx.wxPyDeprecationWarning):
                try:
                    h = dc.GetHDC()
                except NotImplementedError:
                    pass


    def test_NativeGTKHandle(self):
        dc = wx.ClientDC(self.frame)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaises(wx.wxPyDeprecationWarning):
                try:
                    h = dc.GetGdkDrawable()
                except NotImplementedError:
                    pass

    def test_NativeMacHandle(self):
        dc = wx.MemoryDC(wx.Bitmap(10,10))
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaises(wx.wxPyDeprecationWarning):
                try:
                    h = dc.GetCGContext()
                except NotImplementedError:
                    pass


    def test_dcTextExtents(self):
        dc = wx.ClientDC(self.frame)

        size = dc.GetTextExtent('Test String')
        assert isinstance(size, wx.Size)
        assert size.Get() > (0,0)

        mlsize = dc.GetMultiLineTextExtent('Test String\n2nd line')
        assert isinstance(mlsize, wx.Size)
        assert mlsize.Get() > (0,0)
        assert mlsize.Get() > size.Get()


    def test_dcFullTextExtents(self):
        dc = wx.ClientDC(self.frame)

        size = dc.GetFullTextExtent('Test String')
        assert isinstance(size, tuple)
        assert len(size) == 4

        mlsize = dc.GetFullMultiLineTextExtent('Test String\n2nd line')
        assert isinstance(mlsize, tuple)
        assert len(mlsize) == 3



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
        dc.DrawLines( [(15,15), (35,15), (35,35), (35,15), (15,15)] )


    def test_dcContextManager(self):
        import wx.siplib
        with wx.ClientDC(self.frame) as dc:
            dc.DrawLine(0,0,100,100)

            # check ownership
            assert wx.siplib.ispyowned(dc)
            assert not wx.siplib.isdeleted(dc)

        # check the DC's ownership has changed
        assert not wx.siplib.ispyowned(dc)
        assert wx.siplib.isdeleted(dc)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
