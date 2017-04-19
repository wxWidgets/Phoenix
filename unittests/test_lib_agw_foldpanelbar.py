import unittest
from unittests import wtc
import wx

import wx.lib.agw.foldpanelbar as FPB

#---------------------------------------------------------------------------

class lib_agw_foldpanelbar_Tests(wtc.WidgetTestCase):

    def test_lib_agw_foldpanelbarCtor(self):
        panel_bar = FPB.FoldPanelBar(self.frame, -1, agwStyle=FPB.FPB_VERTICAL)

        fold_panel = panel_bar.AddFoldPanel("Thing")
        thing = wx.TextCtrl(fold_panel, -1, size=(400, -1), style=wx.TE_MULTILINE)

        panel_bar.AddFoldPanelWindow(fold_panel, thing)

    def test_lib_agw_foldpanelbarMethods(self):
        panel_bar = FPB.FoldPanelBar(self.frame, -1, agwStyle=FPB.FPB_VERTICAL)

        fold_panel = panel_bar.AddFoldPanel("Thing")
        thing = wx.TextCtrl(fold_panel, -1, size=(400, -1), style=wx.TE_MULTILINE)

        panel_bar.AddFoldPanelWindow(fold_panel, thing)

        # Some methods tests...
        self.assertTrue(panel_bar.IsVertical())
        self.assertEqual(panel_bar.GetCount(), 1)

        # Separators do not count as they are not "real" windows
        panel_bar.AddFoldPanelSeparator(fold_panel)
        self.assertEqual(panel_bar.GetCount(), 1)

        foldpanel = panel_bar.GetFoldPanel(0)
        self.assertTrue(foldpanel.IsExpanded())

        panel_bar.Collapse(foldpanel)
        self.assertTrue(not foldpanel.IsExpanded())


    def test_lib_agw_foldpanelbarConstantsExist(self):
        FPB.CAPTIONBAR_FILLED_RECTANGLE
        FPB.CAPTIONBAR_GRADIENT_H
        FPB.CAPTIONBAR_GRADIENT_V
        FPB.CAPTIONBAR_NOSTYLE
        FPB.CAPTIONBAR_RECTANGLE
        FPB.CAPTIONBAR_SINGLE
        FPB.FPB_ALIGN_LEFT
        FPB.FPB_ALIGN_WIDTH
        FPB.FPB_BMP_RIGHTSPACE
        FPB.FPB_COLLAPSE_TO_BOTTOM
        FPB.FPB_DEFAULT_LEFTLINESPACING
        FPB.FPB_DEFAULT_LEFTSPACING
        FPB.FPB_DEFAULT_RIGHTLINESPACING
        FPB.FPB_DEFAULT_RIGHTSPACING
        FPB.FPB_DEFAULT_SPACING
        FPB.FPB_EXCLUSIVE_FOLD
        FPB.FPB_EXTRA_X
        FPB.FPB_EXTRA_Y
        FPB.FPB_HORIZONTAL
        FPB.FPB_SINGLE_FOLD
        FPB.FPB_VERTICAL

    def test_lib_agw_foldpanelbarEvents(self):
        FPB.EVT_CAPTIONBAR
        FPB.wxEVT_CAPTIONBAR

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
