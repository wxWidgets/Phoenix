
import sys
import wx

# use the numpy code instead of the raw access code for comparison
USE_NUMPY = False

# time the execution of making a bitmap?
TIMEIT = False
PASSES = 100

# how big to make the bitmaps
DIM = 100

# should we use a wx.GraphicsContext for painting?
TEST_GC = False

#----------------------------------------------------------------------
# attempt to import a numeric module if requested to

if USE_NUMPY:
    try:
        import numpy
        def makeByteArray(shape):
            return numpy.empty(shape, numpy.uint8)
        numtype = 'numpy'
    except ImportError:
        USE_NUMPY = False


#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        if TIMEIT:
            import timeit
            timeit.s = self # Put self in timeit's global namespace as
                            # 's' so it can be found in the code
                            # snippets being tested.
            if not USE_NUMPY:
                t = timeit.Timer("bmp = s.MakeBitmap(10, 20, 30)")
            else:
                t = timeit.Timer("bmp = s.MakeBitmap2(10, 20, 30)")
            log.write("Timing...\n")
            num = PASSES
            tm = t.timeit(num)
            log.write("%d passes creating %dx%d images in %f seconds\n"
                      "\t%f seconds per pass " % (num, DIM,DIM, tm, tm/num))

        if not USE_NUMPY:
            log.write("using raw access\n")
            self.redBmp   = self.MakeBitmap(178,  34,  34)
            self.greenBmp = self.MakeBitmap( 35, 142,  35)
            self.blueBmp  = self.MakeBitmap(  0,   0, 139)
        else:
            log.write("using %s\n" % numtype)
            self.redBmp   = self.MakeBitmap2(178,  34,  34)
            self.greenBmp = self.MakeBitmap2( 35, 142,  35)
            self.blueBmp  = self.MakeBitmap2(  0,   0, 139)


    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        if not TEST_GC:
            dc.DrawBitmap(self.redBmp,    50,  50, True)
            dc.DrawBitmap(self.greenBmp, 110, 110, True)
            dc.DrawBitmap(self.blueBmp,  170,  50, True)
            self.log.write("using wx.DC\n")
        else:
            gc = wx.GraphicsContext.Create(dc)
            gc.DrawBitmap(self.redBmp, 50, 50, DIM,DIM)
            gc.DrawBitmap(self.greenBmp, 110, 110, DIM,DIM)
            gc.DrawBitmap(self.blueBmp,  170,  50, DIM,DIM)
            self.log.write("using wx.GraphicsContext\n")


    def MakeBitmap(self, red, green, blue, alpha=128):
        # Create the bitmap that we will stuff pixel values into using
        # the raw bitmap access classes.
        bmp = wx.Bitmap(DIM, DIM, 32)

        # Create an object that facilitates access to the bitmap's
        # pixel buffer
        pixelData = wx.AlphaPixelData(bmp)
        if not pixelData:
            raise RuntimeError("Failed to gain raw access to bitmap data.")

        # We have two ways to access each pixel, first we'll use an
        # iterator to set every pixel to the colour and alpha values
        # passed in.
        for pixel in pixelData:
            pixel.Set(red, green, blue, alpha)

        # This block of code is another way to do the same as above,
        # but with the accessor interface instead of the Python
        # iterator.  It is a bit faster than the above because it
        # avoids the iterator/generator magic, but it is not nearly as
        # 'clean' looking ;-)
        #pixels = pixelData.GetPixels()
        #for y in range(DIM):
        #    pixels.MoveTo(pixelData, 0, y)
        #    for x in range(DIM):
        #        pixels.Set(red, green, blue, alpha)
        #        pixels.nextPixel()



        # Next we'll use the pixel accessor to set the border pixels
        # to be fully opaque
        pixels = pixelData.GetPixels()
        for x in range(DIM):
            pixels.MoveTo(pixelData, x, 0)
            pixels.Set(red, green, blue, wx.ALPHA_OPAQUE)
            pixels.MoveTo(pixelData, x, DIM-1)
            pixels.Set(red, green, blue, wx.ALPHA_OPAQUE)
        for y in range(DIM):
            pixels.MoveTo(pixelData, 0, y)
            pixels.Set(red, green, blue, wx.ALPHA_OPAQUE)
            pixels.MoveTo(pixelData, DIM-1, y)
            pixels.Set(red, green, blue, wx.ALPHA_OPAQUE)

        return bmp


    def MakeBitmap2(self, red, green, blue, alpha=128):
        # Make an array of bytes that is DIM*DIM in size, with enough
        # slots for each pixel to have a RGB and A value
        arr = makeByteArray( (DIM,DIM, 4) )

        # just some indexes to keep track of which byte is which
        R, G, B, A = range(4)

        # initialize all pixel values to the values passed in
        arr[:,:,R] = red
        arr[:,:,G] = green
        arr[:,:,B] = blue
        arr[:,:,A] = alpha

        # Set the alpha for the border pixels to be fully opaque
        arr[0,     0:DIM, A] = wx.ALPHA_OPAQUE  # first row
        arr[DIM-1, 0:DIM, A] = wx.ALPHA_OPAQUE  # last row
        arr[0:DIM, 0,     A] = wx.ALPHA_OPAQUE  # first col
        arr[0:DIM, DIM-1, A] = wx.ALPHA_OPAQUE  # last col

        # finally, use the array to create a bitmap
        bmp = wx.Bitmap.FromBufferRGBA(DIM, DIM, arr)
        return bmp



#----------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App()
    frm = wx.Frame(None, title="RawBitmap Test", size=(500,350))
    pnl = TestPanel(frm, sys.stdout)
    frm.Show()
    app.MainLoop()

