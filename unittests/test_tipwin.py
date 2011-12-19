import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class tipwin_Tests(wtc.WidgetTestCase):

    def test_tipwinCtor(self):
        w = wx.TipWindow(self.frame, "This is a tip message")
        w.SetBoundingRect(self.frame.GetRect())
        w.Show()
        self.myYield()
        w.Close()

        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
