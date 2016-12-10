import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class headerctrl_Tests(wtc.WidgetTestCase):

    def test_headerctrl1(self):
        wx.HD_ALLOW_REORDER
        wx.HD_ALLOW_HIDE
        wx.HD_DEFAULT_STYLE

        wx.wxEVT_COMMAND_HEADER_CLICK
        wx.wxEVT_COMMAND_HEADER_RIGHT_CLICK
        wx.wxEVT_COMMAND_HEADER_MIDDLE_CLICK
        wx.wxEVT_COMMAND_HEADER_DCLICK
        wx.wxEVT_COMMAND_HEADER_RIGHT_DCLICK
        wx.wxEVT_COMMAND_HEADER_MIDDLE_DCLICK
        wx.wxEVT_COMMAND_HEADER_SEPARATOR_DCLICK
        wx.wxEVT_COMMAND_HEADER_BEGIN_RESIZE
        wx.wxEVT_COMMAND_HEADER_RESIZING
        wx.wxEVT_COMMAND_HEADER_END_RESIZE
        wx.wxEVT_COMMAND_HEADER_BEGIN_REORDER
        wx.wxEVT_COMMAND_HEADER_END_REORDER
        wx.wxEVT_COMMAND_HEADER_DRAGGING_CANCELLED

        wx.EVT_HEADER_CLICK
        wx.EVT_HEADER_RIGHT_CLICK
        wx.EVT_HEADER_MIDDLE_CLICK
        wx.EVT_HEADER_DCLICK
        wx.EVT_HEADER_RIGHT_DCLICK
        wx.EVT_HEADER_MIDDLE_DCLICK
        wx.EVT_HEADER_SEPARATOR_DCLICK
        wx.EVT_HEADER_BEGIN_RESIZE
        wx.EVT_HEADER_RESIZING
        wx.EVT_HEADER_END_RESIZE
        wx.EVT_HEADER_BEGIN_REORDER
        wx.EVT_HEADER_END_REORDER
        wx.EVT_HEADER_DRAGGING_CANCELLED


    def test_headerctrl2(self):
        with self.assertRaises(TypeError):
            hc = wx.HeaderCtrl(self.frame)

    def test_headerctrl3(self):
        hc = wx.HeaderCtrlSimple()
        hc.Create(self.frame)

    def test_headerctrl4(self):
        hc = wx.HeaderCtrlSimple(self.frame)

        col = wx.HeaderColumnSimple("Hello")
        hc.AppendColumn(col)

        col = wx.HeaderColumnSimple("World")
        hc.AppendColumn(col)


    def test_headerctrl4(self):
        evt = wx.HeaderCtrlEvent()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
