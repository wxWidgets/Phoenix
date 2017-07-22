import unittest
from unittests import wtc
import wx

import wx.lib.fancytext as FT

#---------------------------------------------------------------------------
test_str = ('<font style="italic" family="swiss" color="red" weight="bold" >'
            'some  |<sup>23</sup> <angle/>text<sub>with <angle/> subscript</sub>'
            '</font> some other text')


class lib_fancytext_Tests(wtc.WidgetTestCase):

    def test_lib_fancytext_DateCtor(self):
        sft = FT.StaticFancyText(self.frame, -1, "text to test", wx.Brush("light grey", wx.BRUSHSTYLE_SOLID))

    def test_lib_fancytext_Methods(self):
        self.frame.Bind(wx.EVT_PAINT, self.OnPaint)

        FT.RenderToBitmap(test_str, background=None, enclose=True)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self.frame)
        FT.GetExtent(test_str, dc=dc, enclose=True)
        FT.GetFullExtent(test_str, dc=dc, enclose=True)
        FT.RenderToDC(test_str, dc, 0, 10, enclose=True)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
