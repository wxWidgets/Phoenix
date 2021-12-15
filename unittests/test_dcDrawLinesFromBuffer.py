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

def makeRandomLines():
    lines = []

    for i in range(num):
        x1 = random.randint(0, w)
        y1 = random.randint(0, h)
        x2 = random.randint(0, w)
        y2 = random.randint(0, h)
        lines.append( (x1,y1, x2,y2) )

    return lines





#---------------------------------------------------------------------------


class dcDrawLists_Tests(wtc.WidgetTestCase):

    @unittest.skipIf(not haveNumpy, "Numpy required for this test")
    def test_dcDrawLinesFromBuffer(self):
        pnl = wx.Panel(self.frame)
        self.frame.SetSize((w,h))
        dc = wx.ClientDC(pnl)
        dc.SetPen(wx.Pen("BLACK", 1))

        xs = np.linspace(0, w, w + 1)
        ys = np.sin(xs / w * 2 * np.pi)
        
        xs.shape = xs.size, 1
        ys.shape = ys.size, 1
        pts = np.append(xs, ys, 1)

        dc.DrawLinesFromBuffer(pts.astype('intc'))
        self.assertRaises(TypeError, dc.DrawLinesFromBuffer, 
                          pts.astype('int64') if np.intc(1).nbytes != np.int64(1).nbytes else pts.astype('int32'))
        self.assertRaises(TypeError, dc.DrawLinesFromBuffer, pts.tolist())
        del dc






#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
