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


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
