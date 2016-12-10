import unittest
from unittests import wtc
import wx
import os


#---------------------------------------------------------------------------

class layout_Tests(wtc.WidgetTestCase):

    def test_layout(self):
        frame = self.frame
        panel = wx.Panel(frame)
        panel.BackgroundColour = 'blue'

        lc = wx.LayoutConstraints()
        lc.top.SameAs(frame, wx.Top, 10)
        lc.left.SameAs(frame, wx.Left, 10)
        lc.bottom.SameAs(frame, wx.Bottom, 10)
        lc.right.PercentOf(frame, wx.Right, 50)

        panel.SetConstraints(lc)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
