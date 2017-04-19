import unittest
from unittests import wtc
import wx
import os


#---------------------------------------------------------------------------

class tooltip_Tests(wtc.WidgetTestCase):

    def test_tooltip(self):
        tip = wx.ToolTip('help message')
        self.frame.SetToolTip(tip)
        tip.Tip
        tip.Window
        tip.Tip = 'new help message'

    def test_tooltipStatics(self):
        wx.ToolTip.Enable(True)
        wx.ToolTip.SetAutoPop(2000)
        wx.ToolTip.SetDelay(2000)
        wx.ToolTip.SetMaxWidth(500)
        wx.ToolTip.SetReshow(2000)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
