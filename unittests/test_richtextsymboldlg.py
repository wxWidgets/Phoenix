import unittest
from unittests import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtextsymboldlg_Tests(wtc.WidgetTestCase):

    def test_richtextsymboldlg1(self):
        dlg = wx.richtext.SymbolPickerDialog('', '', '', self.frame)
        dlg.Show()
        dlg.Destroy()


    def test_richtextsymboldlg2(self):
        dlg = wx.richtext.SymbolPickerDialog()
        dlg.Create('', '', '', self.frame)
        dlg.Show()
        dlg.Destroy()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
