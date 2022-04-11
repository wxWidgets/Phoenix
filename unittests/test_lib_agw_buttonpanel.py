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

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
