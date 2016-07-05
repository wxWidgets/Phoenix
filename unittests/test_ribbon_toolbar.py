import unittest
from unittests import wtc
import wx.ribbon

#---------------------------------------------------------------------------

class ribbon_toolbar_Tests(wtc.WidgetTestCase):

    def test_ribbon_toolbar1(self):
        wx.ribbon.wxEVT_RIBBONTOOLBAR_CLICKED
        wx.ribbon.wxEVT_RIBBONTOOLBAR_DROPDOWN_CLICKED
        wx.ribbon.EVT_RIBBONTOOLBAR_CLICKED
        wx.ribbon.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED


    def test_ribbon_toolbar2(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        tbar = wx.ribbon.RibbonToolBar()
        tbar.Create(ribbon)


    def test_ribbon_toolbar3(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        tbar = wx.ribbon.RibbonToolBar(ribbon)


    def test_ribbon_toolbar4(self):
        evt = wx.ribbon.RibbonToolBarEvent()
        evt.Bar


    def test_ribbon_toolbar5(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        tbar = wx.ribbon.RibbonToolBar(ribbon)


        class _Data(object):
            def __init__(self, **kw):
                self.__dict__.update(kw)

        data1 = _Data(a=1, b=2, c=3)
        data2 = _Data(d=4)

        bmp = wx.Bitmap(16,16)
        tool1 = tbar.AddTool(101, bmp, "help string")
        tbar.SetToolClientData(101, data1)

        bmp = wx.Bitmap(16,16)
        tool2 = tbar.AddTool(102, bmp, help_string="help string", clientData=data2)

        data_out1 = tbar.GetToolClientData(101)
        self.assertEqual(data1.a, data_out1.a)
        self.assertTrue(data_out1 is data1)

        data_out2 = tbar.GetToolClientData(102)
        self.assertEqual(data2.d, data_out2.d)
        self.assertTrue(data_out2 is data2)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
