import unittest
from unittests import wtc
import wx
import wx.lib.stattext

#---------------------------------------------------------------------------

class lib_stattext_Tests(wtc.WidgetTestCase):

    def test_lib_stattext1(self):
        pnl = wx.Panel(self.frame)
        w = wx.lib.stattext.GenStaticText(pnl, label="This is a test", pos=(10,10))
        bs1 = w.GetEffectiveMinSize()

        w.SetLabel("This is a New Label")
        w.SetFont(wx.FFont(16, wx.FONTFAMILY_ROMAN))
        bs2 = w.GetEffectiveMinSize()

        self.assertEqual(w.GetLabel(), "This is a New Label")
        self.assertEqual(w.Label,      "This is a New Label")
        self.assertTrue(bs2.height > bs1.height)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
