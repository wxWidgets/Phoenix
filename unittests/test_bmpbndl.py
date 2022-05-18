import unittest
from unittests import wtc
import wx
import os

icoFile = os.path.join(os.path.dirname(__file__), 'mondrian.ico')
pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class bmpbndl_Tests(wtc.WidgetTestCase):

    def test_BitmapBundleCtor1(self):
        b1 = wx.BitmapBundle()
        self.assertTrue( not b1.IsOk() )

    def test_BitmapBundleCtor2(self):
        b2 = wx.BitmapBundle(wx.Bitmap(5, 10, 32))
        self.assertTrue( b2.IsOk() )

    def test_BitmapBundleCtor3(self):
        b3 = wx.BitmapBundle(wx.Icon(icoFile))
        self.assertTrue( b3.IsOk() )

    def test_BitmapBundleCtor4(self):
        b4 = wx.BitmapBundle(wx.Image(pngFile))
        self.assertTrue( b4.IsOk() )

    def test_BitmapBundleVector(self):
        bmps = [wx.Bitmap(16,16,32),
                wx.Bitmap(24,24,32),
                wx.Bitmap(32,32,32),
                wx.Bitmap(64,64,32)]
        bb = wx.BitmapBundle.FromBitmaps(bmps)
        self.assertTrue( bb.IsOk() )
        b = bb.GetBitmap((32,32))
        self.assertTrue(b.IsOk())
        self.assertEqual(b.GetSize(), wx.Size(32,32))

    def test_BitmapBundle_ImplicitCtor(self):
        "Ensure that a wx.Bitmap can still be used where a wx.BitmapBundle is needed"
        bmp = wx.Bitmap(pngFile)
        btn = wx.Button(self.frame, -1, "Hello")
        btn.SetBitmap(bmp)


    def test_BitmapBundleImpl(self):
        "Test deriving a new class from wx.BitmapBundleImpl"
        class MyCustomBitmapBundleImpl(wx.BitmapBundleImpl):
            def __init__(self):
                super().__init__()
                self.img = wx.Image(pngFile)
                self.size = self.img.GetSize()

            def GetDefaultSize(self):
                # Report the best or default size for the bitmap
                return self.size

            def GetPreferredBitmapSizeAtScale(self, scale):
                # Return the size of the bitmap at the given display scale. It
                # doesn't need to be size*scale if there are unscaled bitmaps
                # near that size.
                return self.size * scale

            def GetBitmap(self, size):
                # Return the version of the bitmap at the desired size
                img = self.img.Scale(size.width, size.height)
                return wx.Bitmap(img)

        bb = wx.BitmapBundle.FromImpl(MyCustomBitmapBundleImpl())
        self.assertTrue( bb.IsOk() )
        b = bb.GetBitmap((32,32))
        self.assertTrue(b.IsOk())
        self.assertEqual(b.GetSize(), wx.Size(32,32))
        b = bb.GetBitmap((48,48))
        self.assertTrue(b.IsOk())
        self.assertEqual(b.GetSize(), wx.Size(48,48))


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
