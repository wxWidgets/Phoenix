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

    def test_gbposition_eq_hash(self):
        tupl1 = (0, 10)
        p1 = wx.GBPosition(*tupl1)
        p12 = wx.GBPosition(*tupl1)
        p2 = wx.GBPosition(2, 10)
        # __eq__ and __hash__ must both be defined
        # eq must assert that elements are of the same class
        self.assertFalse(p1 == tupl1)
        self.assertTrue(hash(p1) == hash(tupl1))
        # then within that class, hash must follow eq
        self.assertTrue(p1 == p12)
        self.assertFalse(id(p1) == id(p12))
        self.assertTrue(hash(p1) == hash(p12))

        self.assertFalse(p1 == p2)
        self.assertFalse(hash(p1) == hash(p2))

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

    def test_gbspan_eq_hash(self):
        tupl1 = (0, 10)
        s1 = wx.GBSpan(*tupl1)
        s12 = wx.GBSpan(*tupl1)
        s2 = wx.GBSpan(2, 10)
        # __eq__ and __hash__ must both be defined
        # eq must assert that elements are of the same class
        self.assertFalse(s1 == tupl1)
        self.assertTrue(hash(s1) == hash(tupl1))
        # then within that class, hash must follow eq
        self.assertTrue(s1 == s12)
        self.assertFalse(id(s1) == id(s12))
        self.assertTrue(hash(s1) == hash(s12))

        self.assertFalse(s1 == s2)
        self.assertFalse(hash(s1) == hash(s2))

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

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
