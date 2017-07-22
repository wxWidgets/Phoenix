import unittest
from unittests import wtc
import wx
import os


#---------------------------------------------------------------------------

class stdpaths_Tests(wtc.WidgetTestCase):

    def test_stdpaths(self):
        sp = wx.StandardPaths.Get()
        sp.GetAppDocumentsDir()
        sp.GetConfigDir()
        sp.GetDataDir()
        sp.GetDocumentsDir()
        sp.GetExecutablePath()
        sp.GetInstallPrefix()
        sp.GetLocalDataDir()
        sp.GetPluginsDir()
        sp.GetResourcesDir()
        sp.GetTempDir()
        sp.GetUserConfigDir()
        sp.GetUserDataDir()
        sp.GetUserLocalDataDir()
        sp.SetInstallPrefix('/opt/foo')
        sp.GetLocalizedResourcesDir('fr')


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
