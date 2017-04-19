import unittest
from unittests import wtc
import wx.ribbon

#---------------------------------------------------------------------------

class ribbon_gallery_Tests(wtc.WidgetTestCase):

    def test_ribbon_gallery1(self):
        wx.ribbon.RIBBON_GALLERY_BUTTON_NORMAL
        wx.ribbon.RIBBON_GALLERY_BUTTON_HOVERED
        wx.ribbon.RIBBON_GALLERY_BUTTON_ACTIVE
        wx.ribbon.RIBBON_GALLERY_BUTTON_DISABLED

        wx.ribbon.wxEVT_RIBBONGALLERY_HOVER_CHANGED
        wx.ribbon.wxEVT_RIBBONGALLERY_SELECTED
        wx.ribbon.wxEVT_RIBBONGALLERY_CLICKED

        wx.ribbon.EVT_RIBBONGALLERY_HOVER_CHANGED
        wx.ribbon.EVT_RIBBONGALLERY_SELECTED
        wx.ribbon.EVT_RIBBONGALLERY_CLICKED


    def test_ribbon_gallery2(self):
        evt = wx.ribbon.RibbonGalleryEvent()


    def test_ribbon_gallery3(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        g = wx.ribbon.RibbonGallery()
        g.Create(ribbon)


    def test_ribbon_gallery4(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        g = wx.ribbon.RibbonGallery(ribbon)
        item = g.Append(wx.Bitmap(16,16), 101)
        assert isinstance(item, wx.ribbon.RibbonGalleryItem)


    def test_ribbon_gallery5(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        g = wx.ribbon.RibbonGallery(ribbon)

        with self.assertRaises(AttributeError):
            g.SetItemClientObject

        with self.assertRaises(AttributeError):
            g.GetItemClientObject


    def test_ribbon_gallery6(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        g = wx.ribbon.RibbonGallery(ribbon)

        class _Data(object):
            def __init__(self, **kw):
                self.__dict__.update(kw)

        data = _Data(a=1, b=2, c=3)
        item = g.Append(wx.Bitmap(16,16), 102)
        g.SetItemClientData(item, data)
        data_out = g.GetItemClientData(item)
        self.assertEqual(data.a, data_out.a)
        self.assertTrue(data_out is data)


    def test_ribbon_gallery7(self):
        ribbon = wx.ribbon.RibbonBar(self.frame)
        g = wx.ribbon.RibbonGallery(ribbon)

        class _Data(object):
            def __init__(self, **kw):
                self.__dict__.update(kw)

        data = _Data(a=1, b=2, c=3)
        item = g.Append(wx.Bitmap(16,16), 102, data)
        data_out = g.GetItemClientData(item)
        self.assertEqual(data.a, data_out.a)
        self.assertTrue(data_out is data)




#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
