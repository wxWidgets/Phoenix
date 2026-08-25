import unittest
from unittest import mock

import wx
import wx.stc as stc
import wx.lib.inspection

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

class InspectionInfoPanel_DarkModeTests(wtc.WidgetTestCase):
    """
    Regression tests for Issue #2917: InspectionInfoPanel gets its colors
    from wx.py.editwindow.get_faces(), which should pick dark-friendly
    colors when the system appearance is dark.
    """

    def test_dark_mode_background(self):
        with mock.patch.object(wx.SystemSettings, 'GetAppearance',
                                return_value=FakeAppearance(True)):
            panel = wx.lib.inspection.InspectionInfoPanel(self.frame)
        self.assertEqual(panel.StyleGetBackground(stc.STC_STYLE_DEFAULT),
                          wx.Colour('#202020'))

    def test_light_mode_background(self):
        with mock.patch.object(wx.SystemSettings, 'GetAppearance',
                                return_value=FakeAppearance(False)):
            panel = wx.lib.inspection.InspectionInfoPanel(self.frame)
        self.assertEqual(panel.StyleGetBackground(stc.STC_STYLE_DEFAULT),
                          wx.Colour('#FFFFFF'))

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
