import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class printdlg_Tests(wtc.WidgetTestCase):

    # TODO: Add some better unittests here. In the meantime see
    # samples/printing/printing.py

    def test_printdlg1(self):
        dlg = wx.PrintDialog(self.frame)
        dlg.Destroy()


    def test_printdlg2(self):
        dlg = wx.PageSetupDialog(self.frame)
        dlg.Destroy()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
