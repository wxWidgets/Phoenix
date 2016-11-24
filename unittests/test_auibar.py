import unittest
from unittests import wtc
import wx
import wx.aui

#---------------------------------------------------------------------------

class auibar_Tests(wtc.WidgetTestCase):

    def test_auibar01(self):
        wx.aui.AUI_TB_TEXT
        wx.aui.AUI_TB_NO_TOOLTIPS
        wx.aui.AUI_TB_NO_AUTORESIZE
        wx.aui.AUI_TB_GRIPPER
        wx.aui.AUI_TB_OVERFLOW
        wx.aui.AUI_TB_VERTICAL
        wx.aui.AUI_TB_HORZ_LAYOUT
        wx.aui.AUI_TB_HORIZONTAL
        wx.aui.AUI_TB_PLAIN_BACKGROUND
        wx.aui.AUI_TB_HORZ_TEXT
        wx.aui.AUI_ORIENTATION_MASK
        wx.aui.AUI_TB_DEFAULT_STYLE
        wx.aui.AUI_TBART_SEPARATOR_SIZE
        wx.aui.AUI_TBART_GRIPPER_SIZE
        wx.aui.AUI_TBART_OVERFLOW_SIZE
        wx.aui.AUI_TBTOOL_TEXT_LEFT
        wx.aui.AUI_TBTOOL_TEXT_RIGHT
        wx.aui.AUI_TBTOOL_TEXT_TOP
        wx.aui.AUI_TBTOOL_TEXT_BOTTOM



    def test_auibar02(self):
        evt = wx.aui.AuiToolBarEvent()


    def test_auibar03(self):
        wx.aui.wxEVT_AUITOOLBAR_TOOL_DROPDOWN
        wx.aui.wxEVT_AUITOOLBAR_OVERFLOW_CLICK
        wx.aui.wxEVT_AUITOOLBAR_RIGHT_CLICK
        wx.aui.wxEVT_AUITOOLBAR_MIDDLE_CLICK
        wx.aui.wxEVT_AUITOOLBAR_BEGIN_DRAG

        wx.aui.EVT_AUITOOLBAR_TOOL_DROPDOWN
        wx.aui.EVT_AUITOOLBAR_OVERFLOW_CLICK
        wx.aui.EVT_AUITOOLBAR_RIGHT_CLICK
        wx.aui.EVT_AUITOOLBAR_MIDDLE_CLICK
        wx.aui.EVT_AUITOOLBAR_BEGIN_DRAG



    def test_auibar04(self):
        obj = wx.aui.AuiToolBarItem()


    def test_auibar05(self):
        with self.assertRaises(TypeError):
            obj = wx.aui.AuiToolBarArt()


    def test_auibar06(self):
        obj = wx.aui.AuiDefaultToolBarArt()



    def test_auibar07(self):
        tbar = wx.aui.AuiToolBar(self.frame)


    def test_auibar08(self):
        tbar = wx.aui.AuiToolBar()
        tbar.Create(self.frame)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
