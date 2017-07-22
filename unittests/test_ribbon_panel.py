import unittest
from unittests import wtc
import wx.ribbon

#---------------------------------------------------------------------------

class ribbon_panel_Tests(wtc.WidgetTestCase):

    def test_ribbon_panel1(self):
        wx.ribbon.RIBBON_PANEL_NO_AUTO_MINIMISE,
        wx.ribbon.RIBBON_PANEL_EXT_BUTTON,
        wx.ribbon.RIBBON_PANEL_MINIMISE_BUTTON,
        wx.ribbon.RIBBON_PANEL_STRETCH,
        wx.ribbon.RIBBON_PANEL_FLEXIBLE,
        wx.ribbon.RIBBON_PANEL_DEFAULT_STYLE

        wx.ribbon.wxEVT_RIBBONPANEL_EXTBUTTON_ACTIVATED
        wx.ribbon.EVT_RIBBONPANEL_EXTBUTTON_ACTIVATED


    def test_ribbon_panel2(self):
        evt = wx.ribbon.RibbonPanelEvent()
        self.assertTrue(evt.Panel is None)


    def test_ribbon_panel3(self):
        bar = wx.ribbon.RibbonBar(self.frame)
        p = wx.ribbon.RibbonPanel()
        p.Create(bar)


    def test_ribbon_panel4(self):
        bar = wx.ribbon.RibbonBar(self.frame)
        p = wx.ribbon.RibbonPanel(bar)

        p.GetMinimisedIcon()
        p.HasExtButton()
        p.IsMinimised()
        p.IsHovered()
        p.CanAutoMinimise()
        p.ShowExpanded()
        p.HideExpanded()

        p.ExpandedDummy
        p.ExpandedPanel



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
