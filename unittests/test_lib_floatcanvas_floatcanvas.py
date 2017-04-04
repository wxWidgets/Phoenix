import unittest
from unittests import wtc
import wx

import wx.lib.floatcanvas.FloatCanvas as fc
import wx.lib.floatcanvas.NavCanvas as nc

import os
pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class lib_floatcanvas_floatcanvas_Tests(wtc.WidgetTestCase):

    def test_lib_floatcanvas_floatcanvasCtor(self):
        fccanvas = fc.FloatCanvas(self.frame)
        fccanvas.Destroy()

    def test_lib_floatcanvas_navcanvasCtor(self):
        self.navcanvas = nc.NavCanvas(self.frame)
        self.navcanvas.Destroy()

    def test_lib_floatcanvas_fc_arc(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.Arc((10, 10), (20, 20), (5, 5))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_arrow(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.Arrow((10, 10), 10, 10)

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_arrowline(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.ArrowLine((10, 10))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_bitmap(self):
        fccanvas = fc.FloatCanvas(self.frame)

        bmp = wx.Bitmap(pngFile)
        obj = fc.Bitmap(bmp, (2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_circle(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.Circle((2, 2),  2)

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_line(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.Line((2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_point(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.Point((2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_pointset(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.PointSet((2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_polygon(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.Polygon((2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_rectangle(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.Rectangle((2, 2),  (2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_recteclips(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.RectEllipse((2, 2), (2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_scaledbitmap(self):
        fccanvas = fc.FloatCanvas(self.frame)

        bmp = wx.Bitmap(pngFile)
        obj = fc.ScaledBitmap(bmp, (2, 2), 100)

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_scaledbitmap2(self):
        fccanvas = fc.FloatCanvas(self.frame)

        bmp = wx.Bitmap(pngFile)
        obj = fc.ScaledBitmap2(bmp, (2, 2), 100)

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_scaledtext(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.ScaledText("some text", (2, 2), 100)

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_scaledtextbox(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.ScaledTextBox("some text", (2, 2), 100)

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_spline(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.Spline((2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_squarepoint(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.SquarePoint((2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_fc_text(self):
        fccanvas = fc.FloatCanvas(self.frame)

        obj = fc.Text("some text", (2, 2))

        fccanvas.AddObject(obj)
        fccanvas.Destroy()

    def test_lib_floatcanvas_floatcanvasEvents(self):

        fc.EVT_FC_ENTER_WINDOW
        fc.EVT_FC_LEAVE_WINDOW
        fc.EVT_FC_LEFT_DOWN
        fc.EVT_FC_LEFT_UP
        fc.EVT_FC_LEFT_DCLICK
        fc.EVT_FC_MIDDLE_DOWN
        fc.EVT_FC_MIDDLE_UP
        fc.EVT_FC_MIDDLE_DCLICK
        fc.EVT_FC_RIGHT_DOWN
        fc.EVT_FC_RIGHT_UP
        fc.EVT_FC_RIGHT_DCLICK
        fc.EVT_FC_MOTION
        fc.EVT_FC_MOUSEWHEEL

        fc.EVT_FC_ENTER_OBJECT
        fc.EVT_FC_LEAVE_OBJECT

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
