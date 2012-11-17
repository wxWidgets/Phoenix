import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class variant_Tests(wtc.WidgetTestCase):

    @unittest.skipIf(not hasattr(wx, 'testVariantTypemap'), '')
    def test_variant1(self):
        n = wx.testVariantTypemap(123)
        self.assertTrue(isinstance(n, (int, long)))
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

        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
