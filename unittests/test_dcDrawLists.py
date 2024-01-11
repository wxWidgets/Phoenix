import unittest
from unittests import wtc
import wx
import random
try:
    import numpy as np
    haveNumpy = True
except ImportError:
    haveNumpy = False

#---------------------------------------------------------------------------

w = 600
h = 400
num = 500

colornames = ["BLACK",
         "BLUE",
         "BLUE VIOLET",
         "BROWN",
         "CYAN",
         "DARK GREY",
         "DARK GREEN",
         "GOLD",
         "GREY",
         "GREEN",
         "MAGENTA",
         "NAVY",
         "PINK",
         "RED",
         "SKY BLUE",
         "VIOLET",
         "YELLOW",
         ]
pencache = {}
brushcache = {}

def makeRandomPoints():
    pnts = []

    for i in range(num):
        x = random.randint(0, w)
        y = random.randint(0, h)
        pnts.append( (x,y) )

    return pnts


def makeRandomLines():
    lines = []

    for i in range(num):
        x1 = random.randint(0, w)
        y1 = random.randint(0, h)
        x2 = random.randint(0, w)
        y2 = random.randint(0, h)
        lines.append( (x1,y1, x2,y2) )

    return lines


def makeRandomRectangles():
    rects = []

    for i in range(num):
        W = random.randint(10, w//2)
        H = random.randint(10, h//2)
        x = random.randint(0, w - W)
        y = random.randint(0, h - H)
        rects.append( (x, y, W, H) )

    return rects


def makeRandomPolygons():
    Np = 8 # number of points per polygon
    polys = []

    for i in range(num):
        poly = []

        for i in range(Np):
            x = random.randint(0, w)
            y = random.randint(0, h)
            poly.append( (x,y) )

        polys.append( poly )

    return polys


def makeRandomText():
    Np = 8 # number of characters in text
    text = []

    for i in range(num):
        word = []

        for i in range(Np):
            c = chr( random.randint(48, 122) )
            word.append( c )

        text.append( "".join(word) )

    return text


def makeRandomColors():
    colors = []
    for i in range(num):
        c = random.choice(colornames)
        colors.append(wx.Colour(c))
    return colors


def makeRandomPens():
    pens = []
    for i in range(num):
        c = random.choice(colornames)
        t = random.randint(1, 4)
        if (c,t) not in pencache:
            pencache[(c, t)] = wx.Pen(c, t)
        pens.append( pencache[(c, t)] )
    return pens


def makeRandomBrushes():
    brushes = []
    for i in range(num):
        c = random.choice(colornames)
        if c not in brushcache:
            brushcache[c] = wx.Brush(c)
        brushes.append( brushcache[c] )
    return brushes


#---------------------------------------------------------------------------


class dcDrawLists_Tests(wtc.WidgetTestCase):

    def test_dcDrawPointLists(self):
        pnl = wx.Panel(self.frame)
        self.frame.SetSize((w,h))
        dc = wx.ClientDC(pnl)
        dc.SetPen(wx.Pen("BLACK", 1))

        pens = makeRandomPens()

        dc.DrawPointList(makeRandomPoints())
        dc.DrawPointList(makeRandomPoints(), wx.Pen("RED", 1))
        dc.DrawPointList(makeRandomPoints(), pens)
        del dc


    @unittest.skipIf(not haveNumpy, "Numpy required for this test")
    def test_dcDrawPointArray(self):
        pnl = wx.Panel(self.frame)
        self.frame.SetSize((w,h))
        dc = wx.ClientDC(pnl)
        dc.SetPen(wx.Pen("BLACK", 1))

        pens = makeRandomPens()

        dc.DrawPointList(np.array(makeRandomPoints()))
        dc.DrawPointList(np.array(makeRandomPoints()), wx.Pen("RED", 1))
        dc.DrawPointList(np.array(makeRandomPoints()), pens)
        del dc


    def test_dcDrawLineLists(self):
        pnl = wx.Panel(self.frame)
        self.frame.SetSize((w,h))
        dc = wx.ClientDC(pnl)
        dc.SetPen(wx.Pen("BLACK", 1))

        pens = makeRandomPens()

        dc.DrawLineList(makeRandomLines())
        dc.DrawLineList(makeRandomLines(), wx.Pen("RED", 2))
        dc.DrawLineList(makeRandomLines(), pens)
        del dc


    def test_dcDrawRectangleLists(self):
        pnl = wx.Panel(self.frame)
        self.frame.SetSize((w,h))
        dc = wx.ClientDC(pnl)
        dc.SetPen(wx.Pen("BLACK", 1))
        dc.SetBrush( wx.Brush("RED") )

        pens = makeRandomPens()
        brushes = makeRandomBrushes()

        dc.DrawRectangleList(makeRandomRectangles())
        dc.DrawRectangleList(makeRandomRectangles(),pens)
        dc.DrawRectangleList(makeRandomRectangles(),pens[0],brushes)
        dc.DrawRectangleList(makeRandomRectangles(),pens,brushes[0])
        dc.DrawRectangleList(makeRandomRectangles(),None,brushes)
        del dc


    @unittest.skipIf(not haveNumpy, "Numpy required for this test")
    def test_dcDrawRectangleArray(self):
        pnl = wx.Panel(self.frame)
        self.frame.SetSize((w,h))
        dc = wx.ClientDC(pnl)
        dc.SetPen(wx.Pen("BLACK", 1))
        dc.SetBrush( wx.Brush("RED") )

        pens = makeRandomPens()
        brushes = makeRandomBrushes()

        dc.DrawRectangleList(np.array(makeRandomRectangles()))
        dc.DrawRectangleList(np.array(makeRandomRectangles()),pens)
        dc.DrawRectangleList(np.array(makeRandomRectangles()),pens[0],brushes)
        dc.DrawRectangleList(np.array(makeRandomRectangles()),pens,brushes[0])
        dc.DrawRectangleList(np.array(makeRandomRectangles()),None,brushes)
        del dc


    def test_dcDrawElipseLists(self):
        pnl = wx.Panel(self.frame)
        self.frame.SetSize((w,h))
        dc = wx.ClientDC(pnl)
        dc.SetPen(wx.Pen("BLACK", 1))
        dc.SetBrush( wx.Brush("RED") )

        pens = makeRandomPens()
        brushes = makeRandomBrushes()

        dc.DrawEllipseList(makeRandomRectangles())
        dc.DrawEllipseList(makeRandomRectangles(),pens)
        dc.DrawEllipseList(makeRandomRectangles(),pens[0],brushes)
        dc.DrawEllipseList(makeRandomRectangles(),pens,brushes[0])
        dc.DrawEllipseList(makeRandomRectangles(),None,brushes)
        del dc


    def test_dcDrawPloygonLists(self):
        pnl = wx.Panel(self.frame)
        self.frame.SetSize((w,h))
        dc = wx.ClientDC(pnl)
        dc.SetPen(wx.Pen("BLACK", 1))
        dc.SetBrush( wx.Brush("RED") )

        pens = makeRandomPens()
        brushes = makeRandomBrushes()
        polygons = makeRandomPolygons()

        dc.DrawPolygonList(polygons)
        dc.DrawPolygonList(polygons, pens)
        dc.DrawPolygonList(polygons, pens[0],brushes)
        dc.DrawPolygonList(polygons, pens,brushes[0])
        dc.DrawPolygonList(polygons, None,brushes)
        del dc


    def test_dcDrawTextLists(self):
        pnl = wx.Panel(self.frame)
        self.frame.SetSize((w,h))
        dc = wx.ClientDC(pnl)
        dc.SetBackgroundMode(wx.SOLID)

        points = makeRandomPoints()
        fore = makeRandomColors()
        back = makeRandomColors()
        texts = makeRandomText()

        dc.DrawTextList(texts, points, fore, back)
        del dc



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
