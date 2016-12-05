import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class colordlg_Tests(wtc.WidgetTestCase):

    def test_colordlg1(self):
        data = wx.ColourData()
        dlg = wx.ColourDialog(self.frame, data)
        dlg.Destroy()

    def test_colordlg2(self):
        wx.GetColourFromUser


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
