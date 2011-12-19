import imp_unittest, unittest
import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

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
        self.fail("data buffer support TBI")
        import array
        w = h = 10
        buf = array.array('B', '\0' * (w*h*3))
        img = wx.Image(w, h, buf, True)
        self.assertTrue(img.IsOk())

    def test_imageCtor5(self):
        return
        self.fail("data buffer support TBI")
        import array
        w = h = 10
        buf = array.array('B', '\0' * (w*h*3))
        alpha = array.array('B', '\0' * (w*h))
        img = wx.Image(w, h, buf, alpha, True)
        self.assertTrue(img.IsOk())

    def test_imageCtor6(self):
        img = wx.Image(pngFile, wx.BITMAP_TYPE_PNG)
        self.assertTrue(img.IsOk())

    def test_imageCtor7(self):
        img = wx.Image(pngFile, 'image/png')
        self.assertTrue(img.IsOk())

    def test_imageCtor8(self):
        data = open(pngFile, 'rb').read()
        import StringIO
        stream = StringIO.StringIO(data)
        img = wx.Image(stream, wx.BITMAP_TYPE_PNG)
        self.assertTrue(img.IsOk())

    def test_imageCtor9(self):
        data = open(pngFile, 'rb').read()
        import StringIO
        stream = StringIO.StringIO(data)
        img = wx.Image(stream, 'image/png')
        self.assertTrue(img.IsOk())


        
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
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
