import unittest
from unittest import mock

import wx
import wx.stc as stc
import wx.py.editwindow as editwindow

from unittests import wtc

#---------------------------------------------------------------------------

class FakeAppearance:
    """Stand-in for wx.SystemAppearance, whose IsDark() result we need to
    control directly rather than relying on the real system/window manager
    dark mode setting."""
    def __init__(self, is_dark):
        self._is_dark = is_dark

    def IsDark(self):
        return self._is_dark

#---------------------------------------------------------------------------

class get_faces_Tests(unittest.TestCase):
    """
    Regression tests for Issue #2917: wx.py.editwindow.get_faces() should
    pick dark-friendly colors when the system appearance is dark, and should
    not blow up if called before a wx.App exists.
    """

    def test_light_appearance(self):
        with mock.patch.object(wx.SystemSettings, 'GetAppearance',
                                return_value=FakeAppearance(False)):
            faces = editwindow.get_faces()
        self.assertEqual(faces['backcol'], '#FFFFFF')
        self.assertEqual(faces['calltipbg'], '#FFFFB8')
        self.assertEqual(faces['calltipfg'], '#404040')

    def test_dark_appearance(self):
        with mock.patch.object(wx.SystemSettings, 'GetAppearance',
                                return_value=FakeAppearance(True)):
            faces = editwindow.get_faces()
        self.assertEqual(faces['backcol'], '#202020')
        self.assertEqual(faces['calltipbg'], '#2D2D2D')
        self.assertEqual(faces['calltipfg'], '#E0E0E0')

    def test_no_app_falls_back_to_light(self):
        # GetAppearance() raises wx.PyNoAppError if called before a wx.App
        # has been created; get_faces() should catch that and default to
        # the light palette instead of raising.
        with mock.patch.object(wx.SystemSettings, 'GetAppearance',
                                side_effect=wx.PyNoAppError):
            faces = editwindow.get_faces()
        self.assertEqual(faces['backcol'], '#FFFFFF')

#---------------------------------------------------------------------------

class EditWindow_DarkModeTests(wtc.WidgetTestCase):

    def test_dark_mode_colors_applied(self):
        with mock.patch.object(wx.SystemSettings, 'GetAppearance',
                                return_value=FakeAppearance(True)):
            editor = editwindow.EditWindow(self.frame)
        self.assertEqual(editor.FACES['backcol'], '#202020')
        self.assertEqual(editor.StyleGetBackground(stc.STC_STYLE_DEFAULT),
                          wx.Colour('#202020'))
        self.assertEqual(editor.StyleGetBackground(stc.STC_STYLE_CALLTIP),
                          wx.Colour('#2D2D2D'))
        self.assertEqual(editor.StyleGetForeground(stc.STC_STYLE_CALLTIP),
                          wx.Colour('#E0E0E0'))

    def test_light_mode_colors_applied(self):
        with mock.patch.object(wx.SystemSettings, 'GetAppearance',
                                return_value=FakeAppearance(False)):
            editor = editwindow.EditWindow(self.frame)
        self.assertEqual(editor.FACES['backcol'], '#FFFFFF')
        self.assertEqual(editor.StyleGetBackground(stc.STC_STYLE_DEFAULT),
                          wx.Colour('#FFFFFF'))
        self.assertEqual(editor.StyleGetBackground(stc.STC_STYLE_CALLTIP),
                          wx.Colour('#FFFFB8'))
        self.assertEqual(editor.StyleGetForeground(stc.STC_STYLE_CALLTIP),
                          wx.Colour('#404040'))

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
