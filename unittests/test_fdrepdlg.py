import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class fdrepdlg_Tests(wtc.WidgetTestCase):

    def test_fdrepdlgConstants(self):
        wx.FR_DOWN
        wx.FR_WHOLEWORD
        wx.FR_MATCHCASE
        wx.FR_REPLACEDIALOG
        wx.FR_NOUPDOWN
        wx.FR_NOMATCHCASE
        wx.FR_NOWHOLEWORD

    def test_fdrepdlgDlg(self):
        data = wx.FindReplaceData()
        data.SetFindString('find string')
        data.SetReplaceString('replace')
        self.assertEqual(data.FindString, 'find string')

        dlg = wx.FindReplaceDialog(self.frame, data, 'Find Stuff')
        dlg.GetData()
        dlg.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
