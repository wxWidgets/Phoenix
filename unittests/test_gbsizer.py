import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class gbsizer_Tests(wtc.WidgetTestCase):

    def test_gbsizer_pos1(self):
        p1 = wx.GBPosition()
        p2 = wx.GBPosition(1,2)
        p3 = wx.GBPosition(p2)
        p4 = wx.GBPosition( (2,1) )

    def test_gbsizer_pos2(self):
        p1 = wx.GBPosition(3,4)
        p1.row
        p1.col
        p1.Row
        p1.Col
        p1.row = 5
        p1.col = 6
        self.assertTrue(p1.Row == 5 and p1.Col == 6)
        self.assertTrue(p1 == wx.GBPosition(5,6))
        self.assertTrue(p1 != wx.GBPosition(3,4))

    def test_gbsizer_pos3(self):
        p1 = wx.GBPosition(3,4)
        self.assertTrue(p1 == (3,4))
        self.assertTrue(p1.Get() == (3,4))
        p1.Set(5,6)
        self.assertTrue(p1 == (5,6))

    def test_gbsizer_pos4(self):
        p1 = wx.GBPosition(3,4)
        r,c = p1
        self.assertTrue(len(p1) == 2)
        p1[0] = 5
        p1[1] = 6
        self.assertTrue((p1.row, p1.col) == (5,6))




    def test_gbsizer_span1(self):
        s1 = wx.GBSpan()
        s2 = wx.GBSpan(1,2)
        s3 = wx.GBSpan(s2)
        s4 = wx.GBSpan( (2,1) )

    def test_gbsizer_span2(self):
        s1 = wx.GBSpan(3,4)
        s1.rowspan
        s1.colspan
        s1.Rowspan
        s1.Colspan
        s1.rowspan = 5
        s1.colspan = 6
        self.assertTrue(s1.Rowspan == 5 and s1.Colspan == 6)
        self.assertTrue(s1 == wx.GBSpan(5,6))
        self.assertTrue(s1 != wx.GBSpan(3,4))

    def test_gbsizer_span3(self):
        s1 = wx.GBSpan(3,4)
        self.assertTrue(s1 == (3,4))
        self.assertTrue(s1.Get() == (3,4))
        s1.Set(5,6)
        self.assertTrue(s1 == (5,6))

    def test_gbsizer_span4(self):
        s1 = wx.GBSpan(3,4)
        r,c = s1
        self.assertTrue(len(s1) == 2)
        s1[0] = 5
        s1[1] = 6
        self.assertTrue((s1.rowspan, s1.colspan) == (5,6))



    def test_gbsizer_sizer1(self):
        gbs = wx.GridBagSizer(2, 4)
        gbs.Add(wx.Panel(self.frame), (1,1), flag=wx.ALL, border=5) # window
        gbs.Add(wx.BoxSizer(), (1,2))                               # sizer
        gbs.Add(5, 25, (1,3))                                       # spacer
        item = wx.GBSizerItem(wx.Panel(self.frame), (1,4), (1,3))
        gbs.Add(item)                                               # item
        return gbs

    def test_gbsizer_sizer2(self):
        gbs = wx.GridBagSizer()
        gbs.Add(wx.Panel(self.frame), (1,1))
        with self.assertRaises(wx.wxAssertionError):
            gbs.Add(wx.Panel(self.frame), (0, 0), (2,2))

    def test_gbsizer_sizer3(self):
        gbs = wx.GridBagSizer(2, 4)
        gbs.Add(wx.Panel(self.frame), (1,1), flag=wx.ALL, border=5) # window
        gbs.Add(wx.BoxSizer(), (1,2))                               # sizer
        gbs.Add(5, 25, (1,3))                                       # spacer

        items = gbs.GetChildren()
        self.assertTrue(len(items) == 3)
        self.assertTrue(isinstance(items[0], wx.GBSizerItem))
        self.assertTrue(items[0].IsWindow())
        self.assertTrue(items[1].IsSizer())
        self.assertTrue(items[2].IsSpacer())
        self.assertTrue(items[0].Border == 5)


    def test_GetIM_position(self):
        # Test the immutable version returned by GetIM
        obj = wx.GBPosition(1,2)
        im = obj.GetIM()
        assert isinstance(im, tuple)
        assert im.row == obj.row
        assert im.col == obj.col
        obj2 = wx.GBPosition(im)
        assert obj == obj2

    def test_GetIM_span(self):
        # Test the immutable version returned by GetIM
        obj = wx.GBSpan(1,2)
        im = obj.GetIM()
        assert isinstance(im, tuple)
        assert im.rowspan == obj.rowspan
        assert im.colspan == obj.colspan
        obj2 = wx.GBSpan(im)
        assert obj == obj2



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
