import unittest
from unittests import wtc
import wx.ribbon

#---------------------------------------------------------------------------

class ribbon_page_Tests(wtc.WidgetTestCase):

    def test_ribbon_page1(self):
        bar = wx.ribbon.RibbonBar(self.frame)
        page = wx.ribbon.RibbonPage()
        page.Create(bar)


    def test_ribbon_page2(self):
        bar = wx.ribbon.RibbonBar(self.frame)
        page = wx.ribbon.RibbonPage(bar)

        rect = wx.Rect(0,0,0,0)
        page.AdjustRectToIncludeScrollButtons(rect)

        page.GetIcon()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
