import unittest
from unittests import wtc
import wx.ribbon

#---------------------------------------------------------------------------

class ribbon_bar_Tests(wtc.WidgetTestCase):

    def test_ribbon_bar1(self):
        wx.ribbon.RIBBON_BAR_SHOW_PAGE_LABELS
        wx.ribbon.RIBBON_BAR_SHOW_PAGE_ICONS
        wx.ribbon.RIBBON_BAR_FLOW_HORIZONTAL
        wx.ribbon.RIBBON_BAR_FLOW_VERTICAL
        wx.ribbon.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS
        wx.ribbon.RIBBON_BAR_SHOW_PANEL_MINIMISE_BUTTONS
        wx.ribbon.RIBBON_BAR_ALWAYS_SHOW_TABS
        wx.ribbon.RIBBON_BAR_SHOW_TOGGLE_BUTTON
        wx.ribbon.RIBBON_BAR_SHOW_HELP_BUTTON
        wx.ribbon.RIBBON_BAR_DEFAULT_STYLE
        wx.ribbon.RIBBON_BAR_FOLDBAR_STYLE
        wx.ribbon.RIBBON_BAR_PINNED
        wx.ribbon.RIBBON_BAR_MINIMIZED
        wx.ribbon.RIBBON_BAR_EXPANDED

        wx.ribbon.wxEVT_RIBBONBAR_PAGE_CHANGED
        wx.ribbon.wxEVT_RIBBONBAR_PAGE_CHANGING
        wx.ribbon.wxEVT_RIBBONBAR_TAB_MIDDLE_DOWN
        wx.ribbon.wxEVT_RIBBONBAR_TAB_MIDDLE_UP
        wx.ribbon.wxEVT_RIBBONBAR_TAB_RIGHT_DOWN
        wx.ribbon.wxEVT_RIBBONBAR_TAB_RIGHT_UP
        wx.ribbon.wxEVT_RIBBONBAR_TAB_LEFT_DCLICK
        wx.ribbon.wxEVT_RIBBONBAR_TOGGLED
        wx.ribbon.wxEVT_RIBBONBAR_HELP_CLICK

        wx.ribbon.EVT_RIBBONBAR_PAGE_CHANGED
        wx.ribbon.EVT_RIBBONBAR_PAGE_CHANGING
        wx.ribbon.EVT_RIBBONBAR_TAB_MIDDLE_DOWN
        wx.ribbon.EVT_RIBBONBAR_TAB_MIDDLE_UP
        wx.ribbon.EVT_RIBBONBAR_TAB_RIGHT_DOWN
        wx.ribbon.EVT_RIBBONBAR_TAB_RIGHT_UP
        wx.ribbon.EVT_RIBBONBAR_TAB_LEFT_DCLICK
        wx.ribbon.EVT_RIBBONBAR_TOGGLED
        wx.ribbon.EVT_RIBBONBAR_HELP_CLICK



    def test_ribbon_bar2(self):
        evt = wx.ribbon.RibbonBarEvent()
        evt.GetPage()
        evt.Page



    def test_ribbon_bar3(self):
        pti = wx.ribbon.RibbonPageTabInfo()
        pti.rect

        # Attempting to access pti.page can crash Python
        # pti.page might need some tweaking in etg/ribbon_bar.py
        # It has an unusual type in ext/wxWidgets/src/ribbon/bar.cpp:
        # WX_DEFINE_USER_EXPORTED_OBJARRAY(wxRibbonPageTabInfoArray)
        # pti.page

        pti.ideal_width
        pti.small_begin_need_separator_width
        pti.small_must_have_separator_width
        pti.minimum_width
        pti.active
        pti.hovered
        pti.highlight
        pti.shown



    def test_ribbon_bar4(self):
        bar = wx.ribbon.RibbonBar()
        bar.Create(self.frame)


    def test_ribbon_bar5(self):
        bar = wx.ribbon.RibbonBar(self.frame)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
