import imp_unittest, unittest
import wtc
import wx
import wx.lib.expando

#---------------------------------------------------------------------------

class lib_expando_Tests(wtc.WidgetTestCase):

    def test_lib_expando1(self):
        pnl = wx.Panel(self.frame)
        w = wx.lib.expando.ExpandoTextCtrl(pnl, value="This is a test", pos=(10,10))
        bs1 = w.GetSize()
        
        w.AppendText("\nThis is a New Label")
        bs2 = w.GetSize()
        
        self.assertEqual(w.GetValue(), "This is a test\nThis is a New Label")
        self.assertEqual(w.GetNumberOfLines(), 3)
        self.assertTrue(bs2.height > bs1.height)
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
