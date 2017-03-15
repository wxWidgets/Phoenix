import unittest
from unittests import wtc
import wx

import six

#---------------------------------------------------------------------------

class variant_Tests(wtc.WidgetTestCase):

    @unittest.skipIf(not hasattr(wx, 'testVariantTypemap'), '')
    def test_variant1(self):
        n = wx.testVariantTypemap(123)
        self.assertTrue(isinstance(n, six.integer_types))
        self.assertEqual(n, 123)


    @unittest.skipIf(not hasattr(wx, 'testVariantTypemap'), '')
    def test_variant2(self):
        s = wx.testVariantTypemap("Hello")
        self.assertEqual(s, "Hello")


    @unittest.skipIf(not hasattr(wx, 'testVariantTypemap'), '')
    def test_variant3(self):
        d1 = dict(a=1, b=2, c=3)
        d2 = wx.testVariantTypemap(d1)
        self.assertEqual(d1, d2)

    @unittest.skipIf(not hasattr(wx, 'testVariantTypemap'), '')
    def test_variantNone(self):
        d1 = None
        d2 = wx.testVariantTypemap(d1)
        self.assertTrue(d2 is None)

    @unittest.skipIf(not hasattr(wx, 'testVariantTypemap'), '')
    def test_variantPyObject(self):
        class Data(object):
            def __init__(self):
                self.a = 123
        d1 = Data()
        d2 = wx.testVariantTypemap(d1)
        self.assertTrue(isinstance(d2, Data))
        self.assertEqual(d2.a, 123)
        self.assertTrue(d1 is d2)


    @unittest.skipIf(not hasattr(wx, 'testVariantTypemap'), '')
    def test_variantDateTime1(self):
        d1 = wx.DateTime(1,2,2003, 4,5,6)
        d2 = wx.testVariantTypemap(d1)
        self.assertEqual(d1, d2)
        self.assertTrue(isinstance(d2, wx.DateTime))


    @unittest.skipIf(not hasattr(wx, 'testVariantTypemap'), '')
    def test_variantDateTime2(self):
        import datetime
        d1 = datetime.datetime(2003,2,1, 4,5,6)
        d2 = wx.testVariantTypemap(d1)
        #print(wx.testVariantTypeName(d1))
        self.assertTrue(isinstance(d2, wx.DateTime))
        self.assertEqual(d2.year,   2003)
        self.assertEqual(d2.month,  wx.DateTime.Feb)
        self.assertEqual(d2.day,    1)
        self.assertEqual(d2.hour,   4)
        self.assertEqual(d2.minute, 5)
        self.assertEqual(d2.second, 6)


    @unittest.skipIf(not hasattr(wx, 'testVariantTypemap'), '')
    def test_variantArrayString1(self):
        a1 = "This is a test".split()
        a2 = wx.testVariantTypemap(a1)
        self.assertEqual(a1, a2)
        self.assertTrue(isinstance(a2, list))


    @unittest.skipIf(not hasattr(wx, 'testVariantTypeName'), '')
    def test_variantArrayString2(self):
        a = "This is a test".split()
        s = wx.testVariantTypeName(a)
        self.assertEqual(s, "arrstring")




#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
