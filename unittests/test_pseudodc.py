import unittest
from unittests import wtc
import wx
import wx.adv

WAITFOR = 250

#---------------------------------------------------------------------------

class pseudodc_Tests(wtc.WidgetTestCase):

    def setUp(self):
        super(pseudodc_Tests, self).setUp()
        self.pnl = wx.Panel(self.frame)
        self.pnl.Bind(wx.EVT_PAINT, self._paintIt)
        self.pdc = wx.adv.PseudoDC()

        self.pdc.SetBackground(wx.Brush('pink'))
        self.pdc.Clear()
        self.pdc.SetPen(wx.Pen('navy', 2))
        self.pdc.SetBrush(wx.Brush('white'))


    def _paintIt(self, evt):
        # Paint event handler for the panel
        dc = wx.PaintDC(self.pnl)
        if 'wxMac' not in wx.PlatformInfo:
            dc = wx.GCDC(dc)
        self.pdc.DrawToDC(dc)

    def _showIt(self):
        self.pnl.Refresh()
        self.waitFor(WAITFOR)


    def test_pseudodc01(self):
        assert self.pdc.GetLen() == 4
        assert self.pdc.Len == 4


    def test_pseudodc02(self):
        self.pdc.DrawRectangle(10, 10, 50, 25)
        self.pdc.DrawRectangle(wx.Rect(10, 40, 50, 25))
        self.pdc.DrawRectangle((10, 70), (50,25))
        self._showIt()


    def test_pseudodc03(self):
        self.pdc.DrawRoundedRectangle(10, 10, 50, 25, 4.5)
        self.pdc.DrawRoundedRectangle(wx.Rect(10, 40, 50, 25), 4.5)
        self.pdc.DrawRoundedRectangle((10, 70), (50,25), 4.5)
        self._showIt()


    def test_pseudodc04(self):
        points = [ (10, 10),
                   (50, 10),
                   (50, 50),
                   (10, 50),
                   (10, 90),
                   (50, 90),
                   ]
        self.pdc.DrawLines(points)
        self._showIt()


    def test_pseudodc05(self):
        for offset in range(0, 300, 10):
            self.pdc.DrawLine(0, offset, offset, 0)
        self._showIt()


    def test_pseudodc06(self):
        for offset in range(0, 300, 10):
            self.pdc.DrawLine((0, offset), (offset, 0))
        self._showIt()


    def test_pseudodc07(self):
        points = [ (10, 10),
                   (25, 50),
                   (10, 75),
                   (75, 100)]
        self.pdc.DrawSpline(points)
        self._showIt()


    def test_pseudodc08(self):
        points = [ (10, 10),
                   (50, 10),
                   (50, 50),
                   (10, 50),
                   (10, 90),
                   (50, 90),
                   ]
        self.pdc.DrawPolygon(points)
        self._showIt()


    def test_pseudodc09(self):
        self.pdc.DrawEllipse(10, 10, 50, 25)
        self.pdc.DrawEllipse(wx.Rect(10, 40, 50, 25))
        self.pdc.DrawEllipse((10, 70), (50,25))
        self._showIt()


    def test_pseudodc10(self):
        self.pdc.SetId(123)
        self.test_pseudodc02()
        self.pdc.TranslateId(123, 25, 25)
        self._showIt()


    def test_pseudodcGradientFill(self):
        pdc = wx.adv.PseudoDC()
        pdc.SetId(1)
        pdc.GradientFillLinear(wx.Rect(0, 0, 50, 20), 'red', 'blue')
        pdc.GradientFillLinear(wx.Rect(0, 20, 50, 20), 'red', 'blue', wx.SOUTH)
        pdc.GradientFillConcentric(wx.Rect(50, 0, 50, 50), 'white', 'black')
        pdc.GradientFillConcentric(wx.Rect(100, 0, 50, 50), 'white', 'black',
                                   wx.Point(10, 10))
        bmp = wx.Bitmap(150, 50)
        img = None

        # Read the bitmap since GetPixel isn't implemented for wxGCDC on macOS
        def draw():
            nonlocal img
            dc = wx.MemoryDC(bmp)
            dc.SetBackground(wx.GREEN_BRUSH)
            dc.Clear()
            pdc.DrawToDC(dc)
            dc.SelectObject(wx.NullBitmap)
            img = bmp.ConvertToImage()

        def colour(x, y):
            return img.GetRed(x, y), img.GetGreen(x, y), img.GetBlue(x, y)

        def red_to_blue(c1, c2):
            return c1[0] > c1[2] and c2[2] > c2[0]

        draw()
        self.assertTrue(red_to_blue(colour(0, 5), colour(49, 5)))
        self.assertTrue(red_to_blue(colour(5, 20), colour(5, 39)))
        self.assertGreater(colour(75, 25)[0], colour(51, 1)[0])
        self.assertGreater(colour(110, 10)[0], colour(148, 48)[0])

        pdc.SetIdGreyedOut(1, True)
        draw()
        self.assertTrue(red_to_blue(colour(0, 5), colour(49, 5)))
        self.assertGreater(colour(0, 5)[1], 100)

        pdc.SetIdGreyedOut(1, False)
        pdc.TranslateId(1, 0, 10)
        draw()
        self.assertEqual(colour(5, 5), (0, 255, 0))
        self.assertGreater(colour(110, 20)[0], colour(110, 49)[0])


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
