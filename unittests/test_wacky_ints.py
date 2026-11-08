import unittest
from unittests import wtc
import wx


#---------------------------------------------------------------------------

class wacky_ints_Tests(unittest.TestCase):

    @unittest.skipIf(not hasattr(wx, 'testSizetTypemap'), '')
    def test_wacky1(self):
        n = wx.testSizetTypemap(123456)
        self.assertEqual(n, 123456)

    @unittest.skipIf(not hasattr(wx, 'testIntPtrTypemap'), '')
    def test_wacky2(self):
        n = wx.testIntPtrTypemap(123456)
        self.assertEqual(n, 123456)

    @unittest.skipIf(not hasattr(wx, 'testUIntPtrTypemap'), '')
    def test_wacky3(self):
        n = wx.testUIntPtrTypemap(123456)
        self.assertEqual(n, 123456)

    @unittest.skipIf(not hasattr(wx, 'testTimeTTypemap'), '')
    def test_wackyTimeT(self):
        self.assertEqual(wx.testTimeTTypemap(1643756400), 1643756400)
        self.assertEqual(wx.testTimeTTypemap(-1), -1)
        with self.assertRaises(TypeError):
            wx.testTimeTTypemap(1.5)
        with self.assertRaises(OverflowError):
            wx.testTimeTTypemap(2**64)
        try:
            self.assertEqual(wx.testTimeTTypemap(2**40), 2**40)
        except OverflowError:
            pass  # time_t is 32 bits on this platform


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
