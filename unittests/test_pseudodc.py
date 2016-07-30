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


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
