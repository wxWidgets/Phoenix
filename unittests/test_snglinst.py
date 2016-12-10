import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class snglinst_Tests(wtc.WidgetTestCase):

    def test_snglinstCtor(self):
        si = wx.SingleInstanceChecker('PhoenixUnitTests')
        si.IsAnotherRunning()

    def test_snglinstDefaultCtor(self):
        si = wx.SingleInstanceChecker()
        si.Create('PhoenixUnitTests')
        si.IsAnotherRunning()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
