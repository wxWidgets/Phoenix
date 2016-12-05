import unittest
from unittests import wtc
import wx
import wx.lib.expando

#---------------------------------------------------------------------------

class lib_expando_Tests(wtc.WidgetTestCase):

    def test_lib_expando1(self):
        pnl = wx.Panel(self.frame)
        w = wx.lib.expando.ExpandoTextCtrl(pnl, value="This is a test", pos=(10,10))
        bs1 = w.GetSize()

        w.AppendText("\nThis is a New Label")
        bs2 = w.GetSize()

        self.assertEqual(w.GetValue(), "This is a test\nThis is a New Label")

        # All we can test here is that we have more lines than we started
        # with, since different platforms may wrap at different spots in the
        # string.
        self.assertGreaterEqual(w.GetNumberOfLines(), 2)
        self.assertGreater(bs2.height, bs1.height)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
