import unittest
import pytest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class tipwin_Tests(wtc.WidgetTestCase):

    def test_tipwinCtor(self):
        with pytest.warns(DeprecationWarning):
            w = wx.TipWindow(self.frame, "This is a tip message")
        w.SetBoundingRect(self.frame.GetRect())
        self.waitFor(100)
        w.Show()
        self.waitFor(100)
        w.Close()



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
