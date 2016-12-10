import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class dirdlg_Tests(wtc.WidgetTestCase):


    def test_dirdlg(self):
        dlg = wx.DirDialog(self.frame, 'message')
        dlg.Destroy()

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
