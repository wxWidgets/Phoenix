import imp_unittest, unittest
import wtc
import wx
import random

import os
import wx.lib.agw.persist as PM

#---------------------------------------------------------------------------

class lib_agw_persist_persistencemanager_Tests(wtc.WidgetTestCase):

    def test_lib_agw_persist_persistencemanagerCtor(self):

        self._persistMgr = PM.PersistenceManager.Get()
        
        dirName = os.path.abspath(__file__)
        _configFile1 = os.path.join(dirName, "PersistTest1")
        self._persistMgr.SetPersistenceFile(_configFile1)
        
        # give the frame a Name for below
        self.frame.SetName('PersistTestFrame')
        
        self._persistMgr.RegisterAndRestoreAll(self.frame)
        
        
    def test_lib_agw_persist_persistencemanagerConstantsExist(self):
        PM.PM_SAVE_RESTORE_AUI_PERSPECTIVES
        PM.PM_SAVE_RESTORE_TREE_LIST_SELECTIONS
        PM.PM_PERSIST_CONTROL_VALUE
        PM.PM_RESTORE_CAPTION_FROM_CODE
        PM.PM_DEFAULT_STYLE
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
