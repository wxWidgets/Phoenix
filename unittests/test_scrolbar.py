import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class scrolbar_Tests(wtc.WidgetTestCase):

    def test_scrolbarCtor(self):
        w = wx.ScrollBar(self.frame)
        w = wx.ScrollBar(self.frame, style=wx.SB_VERTICAL)
        self.assertTrue(w.IsVertical())


    def test_scrolbarDefaultCtor(self):
        w = wx.ScrollBar()
        w.Create(self.frame)


    def test_scrolbarProperties(self):
        w = wx.ScrollBar(self.frame)
        w.PageSize
        w.Range
        w.ThumbPosition
        w.ThumbSize

    def test_scrolbarEvents(self):
        # just testing that they exist for now...
        wx.EVT_SCROLL
        wx.EVT_SCROLL_TOP
        wx.EVT_SCROLL_BOTTOM
        wx.EVT_SCROLL_LINEUP
        wx.EVT_SCROLL_LINEDOWN
        wx.EVT_SCROLL_PAGEUP
        wx.EVT_SCROLL_PAGEDOWN
        wx.EVT_SCROLL_THUMBTRACK
        wx.EVT_SCROLL_THUMBRELEASE
        wx.EVT_SCROLL_CHANGED
        wx.EVT_COMMAND_SCROLL
        wx.EVT_COMMAND_SCROLL_TOP
        wx.EVT_COMMAND_SCROLL_BOTTOM
        wx.EVT_COMMAND_SCROLL_LINEUP
        wx.EVT_COMMAND_SCROLL_LINEDOWN
        wx.EVT_COMMAND_SCROLL_PAGEUP
        wx.EVT_COMMAND_SCROLL_PAGEDOWN
        wx.EVT_COMMAND_SCROLL_THUMBTRACK
        wx.EVT_COMMAND_SCROLL_THUMBRELEASE
        wx.EVT_COMMAND_SCROLL_CHANGED

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
