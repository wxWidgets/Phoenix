import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class clntdatactnr_Tests(wtc.WidgetTestCase):

    def test_clntdatactnr1(self):
        data = wx.ClientDataContainer()
        data.SetClientData("This is a test")
        val = data.GetClientData()
        self.assertEqual(val, "This is a test")
        
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
