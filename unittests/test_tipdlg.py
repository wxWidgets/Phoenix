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
        wx.CallLater(25, self._closeTipDialog)
        wx.adv.ShowTip(self.frame, tp)
        
        
    def test_tipdlg2(self):
        class MyTipProvider(wx.adv.TipProvider):
            def GetTip(self):
                return "This is my tip"
            
        wx.CallLater(25, self._closeTipDialog)
        wx.adv.ShowTip(self.frame, MyTipProvider(0))

        
    def _closeTipDialog(self):
        #self.myYield()
        for w in wx.GetTopLevelWindows():
            if isinstance(w, wx.Dialog):
                w.EndModal(wx.ID_CANCEL)
                
                
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
