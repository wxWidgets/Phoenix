import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class aboutdlg_Tests(wtc.WidgetTestCase):

    def _makeInfo(self):
        info = wx.adv.AboutDialogInfo()
        info.SetVersion('1.2.3')
        info.SetName('My Goofy AboutBox Test')
        info.SetDevelopers(['Goofy', 'Mickey', 'Donald'])
        info.SetDescription('This is a very goofy application')
        info.SetCopyright('(c) by Goofy Enterprises, Inc.')
        info.SetLicence('free-for-all')
        return info


    def test_aboutdlgNative(self):
        if not 'wxMSW' in wx.PlatformInfo:
            info = self._makeInfo()
            wx.CallLater(25, self.closeDialogs)
            wx.adv.AboutBox(info, self.frame)


    def test_aboutdlgGeneric(self):
        info = self._makeInfo()
        wx.CallLater(25, self.closeDialogs)
        wx.adv.GenericAboutBox(info, self.frame)


    def test_aboutdlgProperties(self):
        info = self._makeInfo()
        assert info.Name == 'My Goofy AboutBox Test'
        assert info.Version == '1.2.3'
        assert info.LongVersion == 'Version 1.2.3'
        assert info.Description.startswith('This is a')
        assert info.Copyright.startswith('(c)')
        assert info.Licence == 'free-for-all'
        assert info.License == 'free-for-all'
        assert isinstance(info.Icon, wx.Icon)
        assert info.WebSiteURL == ''
        assert len(info.Developers) == 3
        assert 'Mickey' in info.Developers
        assert len(info.DocWriters) == 0
        assert len(info.Artists) == 0
        assert len(info.Translators) == 0



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
