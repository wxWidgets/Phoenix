import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class textdlg_Tests(wtc.WidgetTestCase):

    def test_textdlg1(self):
        dlg = wx.TextEntryDialog(None, "Message", "Caption", "Value")
        dlg.SetValue("Hello")
        self.assertEqual(dlg.Value, "Hello")
        dlg.Destroy()

    def test_textdlg2(self):
        dlg = wx.PasswordEntryDialog(None, "Message", "Caption", "Value")
        dlg.SetValue("Hello")
        self.assertEqual(dlg.Value, "Hello")
        dlg.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
