import unittest
from unittests import wtc
import wx
import os

#---------------------------------------------------------------------------

class graphics_Tests(wtc.WidgetTestCase):

    def test_gcCreate1(self):
        gc = wx.GraphicsContext.Create(wx.ClientDC(self.frame))
        self.assertTrue(gc.IsOk())


    def test_gcCreate2(self):
        bmp = wx.Bitmap(100,100)
        mdc = wx.MemoryDC(bmp)
        gc = wx.GraphicsContext.Create(mdc)
        self.assertTrue(gc.IsOk())

    def test_gcCreate3(self):
        img = wx.Image(100,100)
        gc = wx.GraphicsContext.Create(img)
        self.assertTrue(gc.IsOk())

    def test_gcCreate4(self):
        class MyPanel(wx.Panel):
            def __init__(self, parent):
                super(MyPanel, self).__init__(parent)
                self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
                self.Bind(wx.EVT_PAINT, self.OnPaint)
                self.painted = False
                self.gcIsOk = False

            def OnPaint(self, evt):
                dc = wx.AutoBufferedPaintDC(self)
                gc = wx.GraphicsContext.Create(dc)
                self.gcIsOk = gc.IsOk()
                self.painted = True

        panel = MyPanel(self.frame)
        self.myUpdate(panel)
        self.waitFor(100)
        self.assertTrue(panel.painted)
        self.assertTrue(panel.gcIsOk)


    def test_gcCreateBitmap(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        self.assertTrue(gc.IsOk())
        bmp = wx.Bitmap(100,100)
        gb = gc.CreateBitmap(bmp)
        self.assertTrue(gb.IsOk())
        self.assertTrue(isinstance(gb, wx.GraphicsBitmap))

        img = wx.Image(100,100)
        gb = gc.CreateBitmapFromImage(img)
        self.assertTrue(gb.IsOk())
        # CreateSubBitmap is not implemented for wxCairoRenderer
        if 'wxGTK' not in wx.PlatformInfo:
            gb = gc.CreateSubBitmap(gb, 5, 5, 25, 25)
            self.assertTrue(gb.IsOk())

        img = gb.ConvertToImage()
        self.assertTrue(img.IsOk())

    def test_gcCreateBrush(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        gb = gc.CreateBrush(wx.Brush('blue'))
        self.assertTrue(gb.IsOk())
        self.assertTrue(isinstance(gb, wx.GraphicsBrush))

    def test_gcCreateFont(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        gf = gc.CreateFont(wx.NORMAL_FONT)
        self.assertTrue(gf.IsOk())
        self.assertTrue(isinstance(gf, wx.GraphicsFont))

        gf = gc.CreateFont(15, 'Courier')
        self.assertTrue(gf.IsOk())

    def test_gcCreatePen(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        gp = gc.CreatePen(wx.RED_PEN)
        self.assertTrue(gp.IsOk())
        self.assertTrue(isinstance(gp, wx.GraphicsPen))


    def test_gcCreatePath(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        p = gc.CreatePath()
        self.assertTrue(p.IsOk())
        self.assertTrue(isinstance(p, wx.GraphicsPath))

    def test_gcCreateMatrix(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        m = gc.CreateMatrix()
        self.assertTrue(m.IsOk())
        self.assertTrue(isinstance(m, wx.GraphicsMatrix))

        values = m.Get()
        self.assertTrue(len(values) == 6)

        dx, dy = m.TransformDistance(5,6)
        x,y = m.TransformPoint(7,8)


    def test_gcTextExtents(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        gf = gc.CreateFont(wx.NORMAL_FONT)
        gc.SetFont(gf)

        ext = gc.GetPartialTextExtents("Hello")
        self.assertEqual(len(ext), 5)

        w, h, d, e = gc.GetFullTextExtent("Hello")
        w, h = gc.GetTextExtent("Hello")



    def test_gcStrokeLines1(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        gc.SetPen(wx.Pen('blue', 2))

        points = [ wx.Point2D(5,5),
                   wx.Point2D(50,5),
                   wx.Point2D(50,50),
                   wx.Point2D(5,5),
                   ]
        gc.StrokeLines(points)

    def test_gcStrokeLines2(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        gc.SetPen(wx.Pen('blue', 2))
        points = [ (5,5), (50,5), wx.Point2D(50,50), (5,5) ]
        gc.StrokeLines(points)

    def test_gcStrokeLines3(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        gc.SetPen(wx.Pen('blue', 2))

        with self.assertRaises(TypeError):
            points = [ (5,5), (50,5), 'not a point', (5,5) ]
            gc.StrokeLines(points)

    def test_gcDrawLines(self):
        self.waitFor(50)
        gc = wx.GraphicsContext.Create(self.frame)
        gc.SetPen(wx.Pen('blue', 2))
        points = [ (5,5), (50,5), wx.Point2D(50,50), (5,5) ]
        gc.DrawLines(points)


    def test_gcGradientStops(self):
        self.waitFor(50)
        gs1 = wx.GraphicsGradientStop('red', 0.25)
        gs2 = wx.GraphicsGradientStop('green', 0.50)
        gs3 = wx.GraphicsGradientStop('blue', 0.90)

        gs1.Colour
        gs1.Position

        stops = wx.GraphicsGradientStops()
        stops.Add(gs1)
        stops.Add(gs2)
        stops.Add('white', 0.75)
        stops.Add(gs3)

        self.assertEqual(len(stops), 6) # 2 existing, plus 4 added
        gs = stops[2]
        self.assertTrue(gs.Position == 0.5)

        gc = wx.GraphicsContext.Create(self.frame)
        b = gc.CreateLinearGradientBrush(0,0, 500, 100, stops)

    def test_gcNullObjects(self):
        wx.NullGraphicsPen
        wx.NullGraphicsBrush
        wx.NullGraphicsFont
        wx.NullGraphicsBitmap
        wx.NullGraphicsMatrix
        wx.NullGraphicsPath


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
