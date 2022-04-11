import unittest
from unittests import wtc
import wx
import os
import six

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

def makeBuf(w, h, bpp=1, init=0):
    "Make a simple buffer for testing with"
    buf = bytearray([init] * (w*h*bpp))
    return buf


class BitmapTests(wtc.WidgetTestCase):

    def test_BitmapCtor1(self):
        b1 = wx.Bitmap()
        self.assertTrue( not b1.IsOk() )

    def test_BitmapCtor2(self):
        b2 = wx.Bitmap(5, 10, 32)
        self.assertTrue( b2.IsOk() )

    def test_BitmapCtor3(self):
        b3 = wx.Bitmap(wx.Size(5,10), 32)
        self.assertTrue( b3.IsOk() )

    def test_BitmapCtor4(self):
        b4 = wx.Bitmap((5,10), 32)
        self.assertTrue( b4.IsOk() )

    def test_BitmapCtor5(self):
        b5 = wx.Bitmap(pngFile)
        self.assertTrue( b5.IsOk() )

    def test_BitmapCtor6(self):
        img = wx.Image(pngFile)
        b6 = wx.Bitmap(img)
        self.assertTrue( b6.IsOk() )


    def test_EmptyBitmapFactory(self):
        # wx.EmptyBitmap is supposed to be deprecated, make sure it is.
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaises(wx.wxPyDeprecationWarning):
                b7 = wx.EmptyBitmap(5,10, 32)
                self.assertTrue( b7.IsOk() )



    def test_Bitmap__nonzero__(self):
        b1 = wx.Bitmap()
        self.assertTrue( not b1.IsOk() )
        b2 = wx.Bitmap(5, 10, 24)
        self.assertTrue( b2.IsOk() )
        if six.PY3:
            self.assertTrue( b2.__bool__() == b2.IsOk() )
        else:
            self.assertTrue( b2.__nonzero__() == b2.IsOk() )

        # check that the __nonzero__ method can be used with if statements
        nzcheck = False
        if b2:
            nzcheck = True
        self.assertTrue(nzcheck)
        nzcheck = False
        if not b1:
            nzcheck = True
        self.assertTrue(nzcheck)


    def test_BitmapNullBitmap(self):
        # just make sure this one exists
        wx.NullBitmap
        self.assertTrue(not wx.NullBitmap.IsOk())


    def test_BitmapSetMaskColour(self):
        b5 = wx.Bitmap(pngFile)
        b5.SetMaskColour(wx.Colour(1,2,3))
        b5.SetMaskColour('black')


    def test_BitmapMask(self):
        img = wx.Image(pngFile)
        img = img.ConvertToMono(0,0,0)
        bmp = wx.Bitmap(img, 1)
        m = wx.Mask()
        m = wx.Mask(bmp)
        m = wx.Mask(bmp, wx.Colour(1,2,3))


    @unittest.skipIf('wxGTK' in wx.PlatformInfo, 'wxMask constructor using palette index not supported on wxGTK')
    def test_BitmapMaskWithPalette(self):
        img = wx.Image(pngFile)
        img = img.ConvertToMono(0,0,0)
        bmp = wx.Bitmap(img, 1)
        rgb = bytearray(range(256))
        pal = wx.Palette(rgb, rgb, rgb)
        bmp.SetPalette(pal)
        m = wx.Mask(bmp, 4)


    def test_bitmapFormatConstants(self):
        wx.BitmapBufferFormat_RGB
        wx.BitmapBufferFormat_RGBA
        wx.BitmapBufferFormat_RGB32
        wx.BitmapBufferFormat_ARGB32

    @unittest.skipIf('wxMac' in wx.PlatformInfo, 'Changing exiting bitmap size not allowed on wxMac')
    def test_bitmapSetSize(self):
        b1 = wx.Bitmap(1,1)
        b1.SetSize((20,30))
        self.assertTrue(b1.GetSize() == (20,30))
        self.assertTrue(b1.Size == (20,30))
        b1.Size = (25,35)
        self.assertTrue(b1.GetSize() == (25,35))

    def test_bitmapHandle(self):
        b1 = wx.Bitmap(1,1)
        b1.Handle
        b1.GetHandle()


    def test_bitmapCopyFromBuffer1(self):
        w = h = 10
        buf = makeBuf(w,h,3)
        bmp = wx.Bitmap(w,h,24)
        bmp.CopyFromBuffer(buf, wx.BitmapBufferFormat_RGB)

    def test_bitmapCopyFromBuffer2(self):
        w = h = 10
        buf = makeBuf(w,h,4)
        bmp = wx.Bitmap(w,h,32)
        bmp.CopyFromBuffer(buf, wx.BitmapBufferFormat_RGBA)

    def test_bitmapCopyFromBuffer3(self):
        w = h = 10
        buf = makeBuf(w,h,4)
        bmp = wx.Bitmap(w,h,32)
        bmp.CopyFromBuffer(buf, wx.BitmapBufferFormat_ARGB32)


    def test_bitmapCopyToBuffer1(self):
        w = h = 10
        buf = makeBuf(w,h,3)
        bmp = wx.Bitmap(w,h,24)
        bmp.CopyToBuffer(buf, wx.BitmapBufferFormat_RGB)

    def test_bitmapCopyToBuffer2(self):
        w = h = 10
        buf = makeBuf(w,h,4)
        bmp = wx.Bitmap(w,h,32)
        bmp.CopyToBuffer(buf, wx.BitmapBufferFormat_RGBA)

    def test_bitmapCopyToBuffer3(self):
        w = h = 10
        buf = makeBuf(w,h,4)
        bmp = wx.Bitmap(w,h,32)
        bmp.CopyToBuffer(buf, wx.BitmapBufferFormat_ARGB32)


    def test_bitmapBufferFactory1(self):
        w = h = 10
        buf = makeBuf(w,h,3, 111)
        bmp = wx.Bitmap.FromBuffer(w, h, buf)
        self.assertTrue(bmp.IsOk())

    def test_bitmapBufferFactory2(self):
        w = h = 10
        buf = makeBuf(w,h,3, 111)
        alpha = makeBuf(w,h,1)
        bmp = wx.Bitmap.FromBufferAndAlpha(w, h, buf, alpha)
        self.assertTrue(bmp.IsOk())

    def test_bitmapBufferFactory3(self):
        w = h = 10
        buf = makeBuf(w,h,4, 111)
        bmp = wx.Bitmap.FromBufferRGBA(w, h, buf)
        self.assertTrue(bmp.IsOk())


    def test_bitmapBufferFactory4(self):
        # The array.array object does not support the new buffer protocol,
        # (at least as of 2.7) so this test shows if we can support the old
        # one too.
        import array
        w = h = 10
        buf = array.array('B', [123] * (w*h*4))
        bmp = wx.Bitmap.FromBufferRGBA(w, h, buf)
        self.assertTrue(bmp.IsOk())


    def test_bitmapBufferFactory5(self):
        # The array.array object does not support the new buffer protocol,
        # (at least as of 2.7) so this test shows if we can support the old
        # one too.
        import array
        w = h = 10
        buf = array.array('B', [10, 20, 30] * (w*h))
        bmp = wx.Bitmap.FromBuffer(w, h, buf)
        self.assertTrue(bmp.IsOk())
        img = bmp.ConvertToImage()
        self.assertEqual( (img.GetRed(1,2), img.GetGreen(1,2), img.GetBlue(1,2)),
                          (10,20,30) )


    def test_bitmapEmptyFactory1(self):
        w = h = 10
        bmp = wx.Bitmap.FromRGBA(w, h)
        self.assertTrue(bmp.IsOk())

    def test_bitmapEmptyFactory2(self):
        w = h = 10
        bmp = wx.Bitmap.FromRGBA(w, h, 1, 2, 3, 4)
        self.assertTrue(bmp.IsOk())



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
