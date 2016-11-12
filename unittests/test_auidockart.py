import unittest
from unittests import wtc
import wx
import wx.aui

#---------------------------------------------------------------------------

class auidockart_Tests(wtc.WidgetTestCase):

    def test_auidockart01(self):
        wx.aui.AUI_DOCKART_SASH_SIZE
        wx.aui.AUI_DOCKART_CAPTION_SIZE
        wx.aui.AUI_DOCKART_GRIPPER_SIZE
        wx.aui.AUI_DOCKART_PANE_BORDER_SIZE
        wx.aui.AUI_DOCKART_PANE_BUTTON_SIZE
        wx.aui.AUI_DOCKART_BACKGROUND_COLOUR
        wx.aui.AUI_DOCKART_SASH_COLOUR
        wx.aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR
        wx.aui.AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR
        wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR
        wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR
        wx.aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR
        wx.aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR
        wx.aui.AUI_DOCKART_BORDER_COLOUR
        wx.aui.AUI_DOCKART_GRIPPER_COLOUR
        wx.aui.AUI_DOCKART_CAPTION_FONT
        wx.aui.AUI_DOCKART_GRADIENT_TYPE
        wx.aui.AUI_GRADIENT_NONE
        wx.aui.AUI_GRADIENT_VERTICAL
        wx.aui.AUI_GRADIENT_HORIZONTAL
        wx.aui.AUI_BUTTON_STATE_NORMAL
        wx.aui.AUI_BUTTON_STATE_HOVER
        wx.aui.AUI_BUTTON_STATE_PRESSED
        wx.aui.AUI_BUTTON_STATE_DISABLED
        wx.aui.AUI_BUTTON_STATE_HIDDEN
        wx.aui.AUI_BUTTON_STATE_CHECKED
        wx.aui.AUI_BUTTON_CLOSE
        wx.aui.AUI_BUTTON_MAXIMIZE_RESTORE
        wx.aui.AUI_BUTTON_MINIMIZE
        wx.aui.AUI_BUTTON_PIN
        wx.aui.AUI_BUTTON_OPTIONS
        wx.aui.AUI_BUTTON_WINDOWLIST
        wx.aui.AUI_BUTTON_LEFT
        wx.aui.AUI_BUTTON_RIGHT
        wx.aui.AUI_BUTTON_UP
        wx.aui.AUI_BUTTON_DOWN
        wx.aui.AUI_BUTTON_CUSTOM1
        wx.aui.AUI_BUTTON_CUSTOM2
        wx.aui.AUI_BUTTON_CUSTOM3



    def test_auidockart02(self):
        with self.assertRaises(TypeError):
            da = wx.aui.AuiDockArt()


    def test_auidockart03(self):
        da = wx.aui.AuiDefaultDockArt()



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
