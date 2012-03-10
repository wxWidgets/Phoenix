import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class toolbar_Tests(wtc.WidgetTestCase):

    def test_toolbar1(self):
        wx.TOOL_STYLE_BUTTON
        wx.TOOL_STYLE_SEPARATOR
        wx.TOOL_STYLE_CONTROL
 
        wx.TB_HORIZONTAL
        wx.TB_VERTICAL
        wx.TB_TOP
        wx.TB_LEFT
        wx.TB_BOTTOM
        wx.TB_RIGHT
        
        wx.TB_3DBUTTONS
        wx.TB_FLAT
        wx.TB_DOCKABLE
        wx.TB_NOICONS
        wx.TB_TEXT
        wx.TB_NODIVIDER
        wx.TB_NOALIGN
        wx.TB_HORZ_LAYOUT
        wx.TB_HORZ_TEXT
        wx.TB_NO_TOOLTIPS

        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
