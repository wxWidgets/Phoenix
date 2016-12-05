import unittest
from unittests import wtc
import wx
import wx.lib.scrolledpanel

#---------------------------------------------------------------------------

class lib_scrolledpanel_Tests(wtc.WidgetTestCase):

    def test_lib_scrolled1(self):
        pnl = wx.lib.scrolledpanel.ScrolledPanel(self.frame)

        vbox = wx.BoxSizer(wx.VERTICAL)
        w = wx.StaticText(pnl, -1, "This is a test", pos=(10, 10))

        vbox.Add(w, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(wx.StaticLine(pnl, -1, size=(1024, -1)), 0, wx.ALL, 5)

        pnl.SetSizer(vbox)

        pnl.SetupScrolling(scroll_x=True, scroll_y=False)
        self.assertEqual(pnl.GetScrollPixelsPerUnit(), (20, 0))

        pnl.SetupScrolling(scroll_x=False, scroll_y=True)
        self.assertEqual(pnl.GetScrollPixelsPerUnit(), (0, 20))

        pnl.SetupScrolling(scroll_x=True, scroll_y=True, rate_x=10, rate_y=50)
        self.assertEqual(pnl.GetScrollPixelsPerUnit(), (10, 50))

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
