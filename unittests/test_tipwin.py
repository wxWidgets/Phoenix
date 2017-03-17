import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class tipwin_Tests(wtc.WidgetTestCase):

    def test_tipwinCtor(self):
        w = wx.TipWindow(self.frame, "This is a tip message")
        w.SetBoundingRect(self.frame.GetRect())
        self.waitFor(200)
        # wxTipWindow constructor docs say:
        # "The tip is shown immediately after the window is constructed."
        assert w.IsShown()
        self.waitFor(100)
        w.Close()



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
