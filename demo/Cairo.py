#!/usr/bin/env python

import wx
import math

try:
    import wx.lib.wxcairo as wxcairo
    import cairo
    haveCairo = True
except ImportError:
    haveCairo = False

from Main import opj

#----------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, evt):
        if self.IsDoubleBuffered():
            dc = wx.PaintDC(self)
        else:
            dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()

        self.Render(dc)


    def Render(self, dc):
        # Draw some stuff on the plain dc
        sz = self.GetSize()
        dc.SetPen(wx.Pen("navy", 1))
        x = y = 0
        while x < sz.width * 2 or y < sz.height * 2:
            x += 20
            y += 20
            dc.DrawLine(x, 0, 0, y)

        # now draw something with cairo
        ctx = wxcairo.ContextFromDC(dc)
        ctx.set_line_width(15)
        ctx.move_to(125, 25)
        ctx.line_to(225, 225)
        ctx.rel_line_to(-200, 0)
        ctx.close_path()
        ctx.set_source_rgba(0, 0, 0.5, 1)
        ctx.stroke()

        # and something else...
        ctx.arc(200, 200, 80, 0, math.pi*2)
        ctx.set_source_rgba(0, 1, 1, 0.5)
        ctx.fill_preserve()
        ctx.set_source_rgb(1, 0.5, 0)
        ctx.stroke()

        # here's a gradient pattern
        ptn = cairo.RadialGradient(315, 70, 25,
                                   302, 70, 128)
        ptn.add_color_stop_rgba(0, 1,1,1,1)
        ptn.add_color_stop_rgba(1, 0,0,0,1)
        ctx.set_source(ptn)
        ctx.arc(328, 96, 75, 0, math.pi*2)
        ctx.fill()

        # Draw some text
        face = wxcairo.FontFaceFromFont(
            wx.FFont(10, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD))
        ctx.set_font_face(face)
        ctx.set_font_size(60)
        ctx.move_to(360, 180)
        ctx.set_source_rgb(0, 0, 0)
        ctx.show_text("Hello")

        # Text as a path, with fill and stroke
        ctx.move_to(400, 220)
        ctx.text_path("World")
        ctx.set_source_rgb(0.39, 0.07, 0.78)
        ctx.fill_preserve()
        ctx.set_source_rgb(0,0,0)
        ctx.set_line_width(2)
        ctx.stroke()

        # Show iterating and modifying a (text) path
        ctx.new_path()
        ctx.move_to(0, 0)
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.set_font_size(30)
        text = "This path was warped..."
        ctx.text_path(text)
        tw, th = ctx.text_extents(text)[2:4]
        self.warpPath(ctx, tw, th, 360,300)
        ctx.fill()

        # Drawing a bitmap.  Note that we can easily load a PNG file
        # into a surface, but I wanted to show how to convert from a
        # wx.Bitmap here instead.  This is how to do it using just cairo:
        #img = cairo.ImageSurface.create_from_png(opj('bitmaps/toucan.png'))

        # And this is how to convert a wx.Btmap to a cairo image
        # surface.  NOTE: currently on Mac there appears to be a
        # problem using conversions of some types of images.  They
        # show up totally transparent when used. The conversion itself
        # appears to be working okay, because converting back to
        # wx.Bitmap or writing the image surface to a file produces
        # the expected result.  The other platforms are okay.
        bmp = wx.Bitmap(opj('bitmaps/toucan.png'))
        #bmp = wx.Bitmap(opj('bitmaps/splash.png'))
        img = wxcairo.ImageSurfaceFromBitmap(bmp)

        ctx.set_source_surface(img, 70, 230)
        ctx.paint()

        # this is how to convert an image surface to a wx.Bitmap
        bmp2 = wxcairo.BitmapFromImageSurface(img)
        dc.DrawBitmap(bmp2, 280, 300)


    def warpPath(self, ctx, tw, th, dx, dy):
        def f(x, y):
            xn = x - tw/2
            yn = y+ xn ** 3 / ((tw/2)**3) * 70
            return xn+dx, yn+dy

        path = ctx.copy_path()
        ctx.new_path()
        for type, points in path:
            if type == cairo.PATH_MOVE_TO:
                x, y = f(*points)
                ctx.move_to(x, y)

            elif type == cairo.PATH_LINE_TO:
                x, y = f(*points)
                ctx.line_to(x, y)

            elif type == cairo.PATH_CURVE_TO:
                x1, y1, x2, y2, x3, y3 = points
                x1, y1 = f(x1, y1)
                x2, y2 = f(x2, y2)
                x3, y3 = f(x3, y3)
                ctx.curve_to(x1, y1, x2, y2, x3, y3)

            elif type == cairo.PATH_CLOSE_PATH:
                ctx.close_path()

#----------------------------------------------------------------------

if not haveCairo:
    from wx.lib.msgpanel import MessagePanel
    def runTest(frame, nb, log):
        win = MessagePanel(
            nb, 'This demo requires either the PyCairo package or the\n'
                'cairocffi package, or there is some other unmet dependency.',
                'Sorry', wx.ICON_WARNING)
        return win
else:

    def runTest(frame, nb, log):
        win = TestPanel(nb, log)
        return win

#----------------------------------------------------------------------

if haveCairo:
    extra = "\n<h3>wx.lib.wxcairo</h3>\n%s" % (
        wxcairo.__doc__.replace('\n\n', '\n<p>'))
else:
    extra = '\n<p>See the docstring in the wx.lib.wxcairo module for details about installing dependencies.'


overview = """<html><body>
<h2><center>Cairo Integration</center></h2>

This sample shows how to draw on a DC using the cairo 2D graphics
library and either the PyCairo or cairocffi package which wrap the cairo
API.  For more information about cairo please see
http://cairographics.org/.

%s

</body></html>
""" % extra



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

