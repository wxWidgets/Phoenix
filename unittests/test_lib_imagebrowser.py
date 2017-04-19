import unittest
from unittests import wtc
import wx
import wx.lib.imagebrowser as ib
import os

#---------------------------------------------------------------------------

class imagebrowser_Tests(wtc.WidgetTestCase):

    def test_imagebrowserDlg(self):
        # a typical use case
        dlg = ib.ImageDialog(self.frame, set_dir=os.getcwd())
        dlg.Destroy()

    def test_imagebrowserDlgGetters(self):
        dlg = ib.ImageDialog(None)
        dlg.GetFile()
        dlg.GetDirectory()
        dlg.Destroy()

    def test_imagebrowserDlgChangeTypes(self):
        dlg = ib.ImageDialog(None)
        dlg.ChangeFileTypes((("GIF (*.gif)", "*.gif"),
                             ("PNG (*.png)", "*.png")))
        dlg.Destroy()

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
