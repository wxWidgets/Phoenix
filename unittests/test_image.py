import unittest
from unittests import wtc
import wx
import six
from six import BytesIO as FileLikeObject
import os


pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

def makeBuf(w, h, bpp=1, init=0):
    "Make a simple buffer for testing with"
    buf = bytearray([init] * (w*h*bpp))
    return buf


class image_Tests(wtc.WidgetTestCase):

    def test_imageCtor1(self):
        img = wx.Image()
        self.assertTrue(not img.IsOk())
        img.Create(100,100)
        self.assertTrue(img.IsOk())

    def test_imageCtor2(self):
        img = wx.Image(100,100)
        self.assertTrue(img.IsOk())

    def test_imageCtor3(self):
        img = wx.Image(wx.Size(100,100))
        self.assertTrue(img.IsOk())
        img = wx.Image((100,100))
        self.assertTrue(img.IsOk())


    def test_imageCtor4(self):
        w = h = 10
        buf = makeBuf(w,h,3)
        img = wx.Image(w, h, buf)
        self.assertTrue(img.IsOk())

    def test_imageCtor5(self):
        w = h = 10
        buf = makeBuf(w,h,3)
        alpha = makeBuf(w,h)
        img = wx.Image(w, h, buf, alpha)
        self.assertTrue(img.IsOk())

    def test_imageCtor4b(self):
        w = h = 10
        buf = makeBuf(w,h,3)
        img = wx.Image((w, h), buf)
        self.assertTrue(img.IsOk())

    def test_imageCtor4c(self):
        w = h = 10
        buf = makeBuf(w,h,3)
        with self.assertRaises(ValueError):
            # should be an exception here because the buffer is the wrong size
            img = wx.Image((w, h+1), buf)

    def test_imageCtor5b(self):
        w = h = 10
        buf = makeBuf(w,h,3)
        alpha = makeBuf(w,h)
        img = wx.Image((w, h), buf, alpha)
        self.assertTrue(img.IsOk())


    def test_imageCtor6(self):
        img = wx.Image(pngFile, wx.BITMAP_TYPE_PNG)
        self.assertTrue(img.IsOk())

    def test_imageCtor7(self):
        img = wx.Image(pngFile, 'image/png')
        self.assertTrue(img.IsOk())

    def test_imageCtor8(self):
        with open(pngFile, 'rb') as f:
            data = f.read()
        stream = FileLikeObject(data)
        img = wx.Image(stream, wx.BITMAP_TYPE_PNG)
        self.assertTrue(img.IsOk())

    def test_imageCtor9(self):
        with open(pngFile, 'rb') as f:
            data = f.read()
        stream = FileLikeObject(data)
        img = wx.Image(stream, 'image/png')
        self.assertTrue(img.IsOk())


    def test_imageSetData1(self):
        w = h = 10
        img = wx.Image(w,h)
        buf = makeBuf(w,h,3, init=2)
        img.SetData(buf)
        self.assertTrue(img.IsOk())
        self.assertTrue(img.GetRed(1,1) == 2)

    def test_imageSetData2(self):
        w = h = 10
        img = wx.Image(1,1)
        buf = makeBuf(w,h,3, init=2)
        img.SetData(buf, w, h)
        self.assertTrue(img.IsOk())
        self.assertTrue(img.GetRed(1,1) == 2)

    def test_imageSetAlpha1(self):
        w = h = 10
        img = wx.Image(w,h)
        buf = makeBuf(w,h, init=2)
        img.SetAlpha(buf)
        self.assertTrue(img.IsOk())
        self.assertTrue(img.GetRed(1,1) == 0)
        self.assertTrue(img.GetAlpha(1,1) == 2)

    def test_imageGetData(self):
        img = wx.Image(pngFile)
        data = img.GetData()
        self.assertEqual(len(data), img.Width * img.Height * 3)
        self.assertTrue(isinstance(data, bytearray))

    def test_imageGetAlpha(self):
        img = wx.Image(pngFile)
        data = img.GetAlpha()
        self.assertEqual(len(data), img.Width * img.Height)
        self.assertTrue(isinstance(data, bytearray))


    def test_imageGetDataBuffer(self):
        w = h = 10
        img = wx.Image(w, h)
        self.assertTrue(img.IsOk())
        data = img.GetDataBuffer()
        self.assertTrue(isinstance(data, memoryview))
        if six.PY2:
            data[0] = b'1'
            data[1] = b'2'
            data[2] = b'3'
            self.assertEqual(ord('1'), img.GetRed(0,0))
            self.assertEqual(ord('2'), img.GetGreen(0,0))
            self.assertEqual(ord('3'), img.GetBlue(0,0))
        else:
            data[0] = 1
            data[1] = 2
            data[2] = 3
            self.assertEqual(1, img.GetRed(0,0))
            self.assertEqual(2, img.GetGreen(0,0))
            self.assertEqual(3, img.GetBlue(0,0))


    def test_imageGetAlphaDataBuffer(self):
        w = h = 10
        img = wx.Image(w, h)
        img.InitAlpha()
        self.assertTrue(img.IsOk())
        data = img.GetAlphaBuffer()
        self.assertTrue(isinstance(data, memoryview))
        if six.PY2:
            data[0] = b'1'
            data[1] = b'2'
            data[2] = b'3'
            self.assertEqual(ord('1'), img.GetAlpha(0,0))
            self.assertEqual(ord('2'), img.GetAlpha(1,0))
            self.assertEqual(ord('3'), img.GetAlpha(2,0))
        else:
            data[0] = 1
            data[1] = 2
            data[2] = 3
            self.assertEqual(1, img.GetAlpha(0,0))
            self.assertEqual(2, img.GetAlpha(1,0))
            self.assertEqual(3, img.GetAlpha(2,0))


    def test_imageSetDataBuffer1(self):
        w = h = 10
        img = wx.Image(w,h)
        buf = makeBuf(w,h,3)
        img.SetDataBuffer(buf)
        buf[0] = 1
        buf[1] = 2
        buf[2] = 3
        self.assertEqual(1, img.GetRed(0,0))
        self.assertEqual(2, img.GetGreen(0,0))
        self.assertEqual(3, img.GetBlue(0,0))

    def test_imageSetDataBuffer2(self):
        w = h = 10
        img = wx.Image(1,1)
        buf = makeBuf(w,h,3)
        img.SetDataBuffer(buf, w, h)
        buf[0] = 1
        buf[1] = 2
        buf[2] = 3
        self.assertEqual(1, img.GetRed(0,0))
        self.assertEqual(2, img.GetGreen(0,0))
        self.assertEqual(3, img.GetBlue(0,0))

    def test_imageSetAlphaBuffer(self):
        w = h = 10
        img = wx.Image(w,h)
        buf = makeBuf(w,h)
        img.SetAlphaBuffer(buf)
        buf[0] = 1
        buf[1] = 2
        buf[2] = 3
        self.assertEqual(1, img.GetAlpha(0,0))
        self.assertEqual(2, img.GetAlpha(1,0))
        self.assertEqual(3, img.GetAlpha(2,0))


    def test_imageNestedClasses(self):
        rgb = wx.Image.RGBValue(1,2,3)
        self.assertEqual(rgb.red, 1)
        self.assertEqual(rgb.green, 2)
        self.assertEqual(rgb.blue, 3)
        rgb.red = 4
        rgb.green = 5
        rgb.blue = 6

        hsv = wx.Image.HSVValue(1.1, 1.2, 1.3)
        self.assertEqual(hsv.hue, 1.1)
        self.assertEqual(hsv.saturation, 1.2)
        self.assertEqual(hsv.value, 1.3)
        hsv.hue = 2.1
        hsv.saturation = 2.2
        hsv.value = 2.3


    def test_imageRGBHSV(self):
        rgb = wx.Image.RGBValue(1,2,3)
        hsv = wx.Image.RGBtoHSV(rgb)
        rgb = wx.Image.HSVtoRGB(hsv)
        self.assertEqual(rgb.red, 1)
        self.assertEqual(rgb.green, 2)
        self.assertEqual(rgb.blue, 3)


    def test_imageProperties(self):
        img = wx.Image(pngFile)
        self.assertTrue(img.IsOk())
        img.Width
        img.Height
        img.MaskRed
        img.MaskGreen
        img.MaskBlue
        img.Type


    def test_imageMethodChain(self):
        img = wx.Image(100,100).Rescale(75,75).Resize((100,100), (0,0), 40,60,80)
        self.assertTrue(img.IsOk())


    def test_imageOtherStuff(self):
        img = wx.Image(pngFile)
        self.assertTrue(img.IsOk())
        r, g, b = img.FindFirstUnusedColour()
        r, g, b = img.GetOrFindMaskColour()


    def test_imageHandlerDerivation(self):
        class TestImageHandler(wx.ImageHandler):
            def __init__(self):
                wx.ImageHandler.__init__(self)
                self.Name = "Foo File"
                self.Extension = "foo"
                self.MimeType = 'image/foo'
                self.Type = wx.BITMAP_TYPE_JPEG

            def DoCanRead(self, stream):
                return True

        imghndlr = TestImageHandler()
        wx.Image.AddHandler(imghndlr)

    def test_imageHandlerStandardDerivations(self):
        # checks that all of the standard wx derivations are available.
        wx.GIFHandler()
        wx.IFFHandler()
        wx.JPEGHandler()
        wx.PCXHandler()
        wx.PNGHandler()
        wx.PNMHandler()
        wx.TGAHandler()
        wx.TIFFHandler()
        wx.XPMHandler()

    def test_imageHandlerStandardDerivationsDerivation(self):
        for cls in (wx.GIFHandler, wx.IFFHandler, wx.JPEGHandler,
                    wx.PCXHandler, wx.PNGHandler, wx.PNMHandler,
                    wx.TGAHandler, wx.TIFFHandler,wx.XPMHandler):

            class TestImageHandler(cls):
                def __init__(self):
                    cls.__init__(self)
                    ext = cls.__name__.replace("Handler", "")
                    self.Name = "%s File" % ext
                    self.Extension = ext
                    self.MimeType = 'image/ext'

                    self.Type = getattr(wx, "BITMAP_TYPE_%s" % ext)

                def DoCanRead(self, stream):
                    return True

            imghndlr = TestImageHandler()
            wx.Image.AddHandler(imghndlr)

    def test_imageClear(self):
        img = wx.Image(100,100)
        img.Clear(255)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
