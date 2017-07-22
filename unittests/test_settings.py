import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class settings_Tests(wtc.WidgetTestCase):

    def test_settingsConstants(self):
        wx.SYS_OEM_FIXED_FONT
        wx.SYS_ANSI_FIXED_FONT
        wx.SYS_ANSI_VAR_FONT
        wx.SYS_SYSTEM_FONT
        wx.SYS_DEVICE_DEFAULT_FONT
        wx.SYS_DEFAULT_GUI_FONT

        wx.SYS_COLOUR_SCROLLBAR
        wx.SYS_COLOUR_BACKGROUND
        wx.SYS_COLOUR_ACTIVECAPTION
        wx.SYS_COLOUR_INACTIVECAPTION
        wx.SYS_COLOUR_MENU
        wx.SYS_COLOUR_WINDOW
        wx.SYS_COLOUR_WINDOWFRAME
        wx.SYS_COLOUR_MENUTEXT
        wx.SYS_COLOUR_WINDOWTEXT
        wx.SYS_COLOUR_CAPTIONTEXT
        wx.SYS_COLOUR_ACTIVEBORDER
        wx.SYS_COLOUR_INACTIVEBORDER
        wx.SYS_COLOUR_APPWORKSPACE
        wx.SYS_COLOUR_HIGHLIGHT
        wx.SYS_COLOUR_HIGHLIGHTTEXT
        wx.SYS_COLOUR_BTNFACE
        wx.SYS_COLOUR_BTNSHADOW
        wx.SYS_COLOUR_GRAYTEXT
        wx.SYS_COLOUR_BTNTEXT
        wx.SYS_COLOUR_INACTIVECAPTIONTEXT
        wx.SYS_COLOUR_BTNHIGHLIGHT
        wx.SYS_COLOUR_3DDKSHADOW
        wx.SYS_COLOUR_3DLIGHT
        wx.SYS_COLOUR_INFOTEXT
        wx.SYS_COLOUR_INFOBK
        wx.SYS_COLOUR_LISTBOX
        wx.SYS_COLOUR_HOTLIGHT
        wx.SYS_COLOUR_GRADIENTACTIVECAPTION
        wx.SYS_COLOUR_GRADIENTINACTIVECAPTION
        wx.SYS_COLOUR_MENUHILIGHT
        wx.SYS_COLOUR_MENUBAR
        wx.SYS_COLOUR_LISTBOXTEXT
        wx.SYS_COLOUR_LISTBOXHIGHLIGHTTEXT

        wx.SYS_COLOUR_DESKTOP
        wx.SYS_COLOUR_3DFACE
        wx.SYS_COLOUR_3DSHADOW
        wx.SYS_COLOUR_BTNHILIGHT
        wx.SYS_COLOUR_3DHIGHLIGHT
        wx.SYS_COLOUR_3DHILIGHT
        wx.SYS_COLOUR_FRAMEBK

        wx.SYS_MOUSE_BUTTONS
        wx.SYS_BORDER_X
        wx.SYS_BORDER_Y
        wx.SYS_CURSOR_X
        wx.SYS_CURSOR_Y
        wx.SYS_DCLICK_X
        wx.SYS_DCLICK_Y
        wx.SYS_DRAG_X
        wx.SYS_DRAG_Y
        wx.SYS_EDGE_X
        wx.SYS_EDGE_Y
        wx.SYS_HSCROLL_ARROW_X
        wx.SYS_HSCROLL_ARROW_Y
        wx.SYS_HTHUMB_X
        wx.SYS_ICON_X
        wx.SYS_ICON_Y
        wx.SYS_ICONSPACING_X
        wx.SYS_ICONSPACING_Y
        wx.SYS_WINDOWMIN_X
        wx.SYS_WINDOWMIN_Y
        wx.SYS_SCREEN_X
        wx.SYS_SCREEN_Y
        wx.SYS_FRAMESIZE_X
        wx.SYS_FRAMESIZE_Y
        wx.SYS_SMALLICON_X
        wx.SYS_SMALLICON_Y
        wx.SYS_HSCROLL_Y
        wx.SYS_VSCROLL_X
        wx.SYS_VSCROLL_ARROW_X
        wx.SYS_VSCROLL_ARROW_Y
        wx.SYS_VTHUMB_Y
        wx.SYS_CAPTION_Y
        wx.SYS_MENU_Y
        wx.SYS_NETWORK_PRESENT
        wx.SYS_PENWINDOWS_PRESENT
        wx.SYS_SHOW_SOUNDS
        wx.SYS_SWAP_BUTTONS
        wx.SYS_DCLICK_MSEC

        wx.SYS_CAN_DRAW_FRAME_DECORATIONS
        wx.SYS_CAN_ICONIZE_FRAME
        wx.SYS_TABLET_PRESENT

        wx.SYS_SCREEN_NONE

        wx.SYS_SCREEN_TINY
        wx.SYS_SCREEN_PDA
        wx.SYS_SCREEN_SMALL
        wx.SYS_SCREEN_DESKTOP


    def test_settingsGetFont(self):
        f = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        self.assertTrue(isinstance(f, wx.Font))

    def test_settingsGetColour(self):
        c = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        self.assertTrue(isinstance(c, wx.Colour))

    def test_settingsGetMetric(self):
        m = wx.SystemSettings.GetMetric(wx.SYS_BORDER_X)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
