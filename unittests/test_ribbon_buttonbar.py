import unittest
from unittests import wtc
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

        with self.assertRaises(AttributeError):
            bb.SetItemClientObject

        with self.assertRaises(AttributeError):
            bb.GetItemClientObject


    def test_ribbon_buttonbar4(self):
        evt = wx.ribbon.RibbonButtonBarEvent()


    def test_ribbon_buttonbar5(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        bb = wx.ribbon.RibbonButtonBar(ribbon)
        bmp = wx.Bitmap(16,16)
        btn = bb.AddButton(100, "label", bmp, "help string")

        class _Data(object):
            def __init__(self, **kw):
                self.__dict__.update(kw)

        data = _Data(a=1, b=2, c=3)
        bb.SetItemClientData(btn, data)
        data_out = bb.GetItemClientData(btn)
        self.assertEqual(data.a, data_out.a)
        self.assertTrue(data_out is data)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
