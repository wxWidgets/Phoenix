import unittest
from unittests import wtc
import wx
import wx.adv
import os

tipFile = os.path.join(os.path.dirname(__file__), 'tips.txt')

#---------------------------------------------------------------------------

class tipdlg_Tests(wtc.WidgetTestCase):

    def test_tipdlg1(self):
        tp = wx.adv.CreateFileTipProvider(tipFile, 0);
        wx.CallLater(150, self.closeDialogs)
        wx.adv.ShowTip(self.frame, tp)
        self.myYield()


    def test_tipdlg2(self):
        class MyTipProvider(wx.adv.TipProvider):
            def GetTip(self):
                return "This is my tip"

        wx.CallLater(150, self.closeDialogs)
        wx.adv.ShowTip(self.frame, MyTipProvider(0))
        self.myYield()



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
