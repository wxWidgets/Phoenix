import unittest
from unittests import wtc
import wx

import wx.lib.agw.buttonpanel as BP

#---------------------------------------------------------------------------

class lib_agw_buttonpanel_Tests(wtc.WidgetTestCase):


    def test_lib_agw_buttonpanelCtor(self):
        bar = BP.ButtonPanel(self.frame, -1, 'sample text')
        btn = BP.ButtonInfo(bar, wx.ID_ANY,
                            wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (32, 32)),
                            text='Button 1')
        bar.AddButton(btn)

    def test_lib_agw_buttonpanelMethods(self):
        bar = BP.ButtonPanel(self.frame, -1, 'sample text')
        btn = BP.ButtonInfo(bar, wx.ID_ANY,
                            wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (32, 32)),
                            text='Button 1')
        bar.AddButton(btn)

        bar.SetBarText('')
        self.assertTrue(not bar.HasBarText())
        bar.RemoveText()
        self.assertTrue(not bar.HasBarText())

        self.assertTrue(bar.IsStandard())
        self.assertTrue(not bar.IsVertical())

    def test_lib_agw_buttonpanelScaledBitmap(self):
        # Like a macOS @2x image: 48x48 pixels drawn at 24x24 where the
        # platform uses DPI-independent pixels
        scaled = wx.Bitmap(48, 48)
        scaled.SetScaleFactor(2)
        plain = wx.Bitmap(*scaled.GetLogicalSize())
        bar = BP.ButtonPanel(self.frame, -1, 'sample text')
        sizes = []
        for bmp in (scaled, plain):
            btn = BP.ButtonInfo(bar, wx.ID_ANY, bmp, text='Button')
            bar.AddButton(btn)
            sizes.append(btn.GetBestSize())
        self.assertEqual(sizes[0], sizes[1])

    def test_lib_agw_buttonpanelSetAlignmentWithControl(self):
        bar = BP.ButtonPanel(self.frame, -1, 'sample text')
        btn = BP.ButtonInfo(bar, wx.ID_ANY,
                            wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (32, 32)),
                            text='Button 1')
        bar.AddButton(btn)
        bar.AddSeparator()
        ctrl = wx.TextCtrl(bar)
        bar.AddControl(ctrl)
        bar.DoLayout()

        for alignment in (BP.BP_ALIGN_RIGHT, BP.BP_ALIGN_TOP,
                          BP.BP_ALIGN_BOTTOM, BP.BP_ALIGN_LEFT):
            bar.SetAlignment(alignment)
            self.assertEqual(bar.GetAlignment(), alignment)
            self.assertEqual(bar.GetBarText(), 'sample text')
            self.assertIs(ctrl.GetContainingSizer(), bar.GetSizer())

    def test_lib_agw_buttonpanelConstantsExist(self):
        # ButtonPanel agwStyle
        BP.BP_DEFAULT_STYLE
        BP.BP_USE_GRADIENT

        # ButtonPanel alignments
        BP.BP_ALIGN_LEFT
        BP.BP_ALIGN_RIGHT
        BP.BP_ALIGN_TOP
        BP.BP_ALIGN_BOTTOM

        # HitTest flags
        BP.BP_HT_BUTTON
        BP.BP_HT_NONE

        # Caption gradient types
        BP.BP_GRADIENT_NONE
        BP.BP_GRADIENT_VERTICAL
        BP.BP_GRADIENT_HORIZONTAL

    def test_lib_agw_buttonpanelArtGetUnknownFont(self):
        art = BP.BPArt(0)
        self.assertEqual(art.GetFont(-1), wx.NullFont)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
