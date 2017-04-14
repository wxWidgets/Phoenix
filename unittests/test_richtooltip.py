import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class richtooltip_Tests(wtc.WidgetTestCase):

    def test_richtooltip1(self):
        wx.adv.TipKind_None
        wx.adv.TipKind_TopLeft
        wx.adv.TipKind_Top
        wx.adv.TipKind_TopRight
        wx.adv.TipKind_BottomLeft
        wx.adv.TipKind_Bottom
        wx.adv.TipKind_BottomRight
        wx.adv.TipKind_Auto


    def test_richtooltip2(self):
        tt = wx.adv.RichToolTip("The Title", "The richtooltip message.")
        tt.SetBackgroundColour('sky blue')
        tt.SetIcon(wx.ICON_WARNING)
        tt.SetTimeout(200)
        tt.ShowFor(self.frame)
        self.waitFor(300)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
