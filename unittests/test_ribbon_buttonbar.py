import unittest
import wtc
import wx.ribbon

#---------------------------------------------------------------------------

class ribbon_buttonbar_Tests(wtc.WidgetTestCase):

    def test_ribbon_buttonbar1(self):
        wx.ribbon.EVT_RIBBONBUTTONBAR_CLICKED
        wx.ribbon.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED

        wx.ribbon.wxEVT_RIBBONBUTTONBAR_CLICKED
        wx.ribbon.wxEVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED


    def test_ribbon_buttonbar2(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        bb = wx.ribbon.RibbonButtonBar()
        bb.Create(ribbon)


    def test_ribbon_buttonbar3(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        bb = wx.ribbon.RibbonButtonBar(ribbon)
        bmp = wx.Bitmap(16,16)
        b = bb.AddButton(100, "label", bmp, "help string")


    def test_ribbon_buttonbar4(self):
        evt = wx.ribbon.RibbonButtonBarEvent()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
