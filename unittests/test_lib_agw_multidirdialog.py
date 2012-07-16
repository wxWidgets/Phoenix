import imp_unittest, unittest
import wtc
import wx

import wx.lib.agw.multidirdialog as MDD

#---------------------------------------------------------------------------

class lib_agw_multidirdialog_Tests(wtc.WidgetTestCase):
        
    def test_lib_agw_multidirdialogCtor(self):
        dlg = MDD.MultiDirDialog(self.frame, title="Custom MultiDirDialog",
                                 agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)

    def test_lib_agw_multidirdialogMethods(self):
        dlg = MDD.MultiDirDialog(self.frame, title="Custom MultiDirDialog",
                                 agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)

        self.assertTrue(dlg.GetPaths() == [])
        
    def test_lib_agw_multidirdialogConstantsExist(self):
        MDD.DD_DEFAULT_STYLE
        MDD.DD_DIR_MUST_EXIST
        MDD.DD_MULTIPLE
        MDD.DD_NEW_DIR_BUTTON
        

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
