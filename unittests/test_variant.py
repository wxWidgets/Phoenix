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


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
