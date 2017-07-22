import unittest
from unittests import wtc
import wx

import wx.lib.agw.multidirdialog as MDD

#---------------------------------------------------------------------------

class lib_agw_multidirdialog_Tests(wtc.WidgetTestCase):

    def test_lib_agw_multidirdialogCtor(self):
        dlg = MDD.MultiDirDialog(self.frame, title="Custom MultiDirDialog",
                                 agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

    def test_lib_agw_multidirdialogMethods(self):
        dlg = MDD.MultiDirDialog(self.frame, title="Custom MultiDirDialog",
                                 agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)

        self.assertTrue(isinstance(dlg.GetPaths(), list))

        # it looks like the generic dir ctrl may start out with an item
        # selected, so allow for that here
        self.assertTrue(len(dlg.GetPaths()) in [0,1])
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()


    def test_lib_agw_multidirdialogConstantsExist(self):
        MDD.DD_DEFAULT_STYLE
        MDD.DD_DIR_MUST_EXIST
        MDD.DD_MULTIPLE
        MDD.DD_NEW_DIR_BUTTON


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
