import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class clntdatactnr_Tests(wtc.WidgetTestCase):

    def test_clntdatactnr1(self):
        data = wx.ClientDataContainer()
        data.SetClientData("This is a test")
        val = data.GetClientData()
        self.assertEqual(val, "This is a test")


    def test_clntdatactnr2(self):
        data = wx.ClientDataContainer()
        data.SetClientObject("This is a test")
        val = data.GetClientObject()
        self.assertEqual(val, "This is a test")


    def test_clntdatactnr3(self):
        data = wx.ClientDataContainer()
        data.SetClientData("This is a test")
        val = data.GetClientData()
        self.assertEqual(val, "This is a test")

        val = data.ClientData
        self.assertEqual(val, "This is a test")

        data.ClientData = "another test"
        val = data.ClientData
        self.assertEqual(val, "another test")


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
