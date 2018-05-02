import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class numdlg_Tests(wtc.WidgetTestCase):

    def test_numdlg1(self):
        dlg = wx.NumberEntryDialog(None, "Message", "Prompt", "Caption", 50, 0, 100)
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        self.assertEqual(dlg.GetValue(), 50)
        dlg.Destroy()

    def test_numdlg2(self):
        # Ideally we would call this but don't know how to dismiss the dialog
        wx.GetNumberFromUser

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
