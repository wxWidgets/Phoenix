import imp_unittest, unittest
import wtc
import wx
import wx.adv
import os

tipFile = os.path.join(os.path.dirname(__file__), 'tips.txt')

#---------------------------------------------------------------------------

class tipdlg_Tests(wtc.WidgetTestCase):

    def test_tipdlg1(self):
        tp = wx.adv.CreateFileTipProvider(tipFile, 0);
        wx.CallLater(25, self.closeDialogs)
        wx.adv.ShowTip(self.frame, tp)
        
        
    def test_tipdlg2(self):
        class MyTipProvider(wx.adv.TipProvider):
            def GetTip(self):
                return "This is my tip"
            
        wx.CallLater(25, self.closeDialogs)
        wx.adv.ShowTip(self.frame, MyTipProvider(0))

                       
                
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
