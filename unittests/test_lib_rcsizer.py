import unittest
from unittests import wtc
import wx
import wx.lib.rcsizer as rcs

#---------------------------------------------------------------------------

class lib_rcsizer_Tests(wtc.WidgetTestCase):

    def test_lib_rcsizerLayout(self):
        pnl = wx.Panel(self.frame)
        sizer = rcs.RowColSizer()
        spanned = wx.Window(pnl, size=(101, 30))
        centred = wx.Window(pnl, size=(20, 25))
        sizer.Add(spanned, row=0, col=0, colspan=2)
        sizer.Add(centred, row=1, col=1,
                  flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(1)
        pnl.SetSizer(sizer)

        self.assertEqual(sizer.CalcMin(), wx.Size(100, 55))

        pnl.SetSize((205, 112))
        pnl.Layout()
        self.assertEqual(centred.GetRect(), wx.Rect(117, 58, 20, 25))

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
