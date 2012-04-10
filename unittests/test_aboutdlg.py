import imp_unittest, unittest
import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class aboutdlg_Tests(wtc.WidgetTestCase):

    def _makeInfo(self):
        info = wx.adv.AboutDialogInfo()
        info.SetVersion('1.2.3')
        info.SetName('My Goofy App')
        info.SetDevelopers(['Goofy', 'Mickey', 'Donald'])
        info.SetDescription('This is a very goofy application')
        info.SetCopyright('(c) by Goofy Enterprises, Inc.')
        return info 

    def _closeDlg(self):
        for w in wx.GetTopLevelWindows():
            if isinstance(w, wx.Dialog):
                w.EndModal(wx.ID_OK)
    
    def test_aboutdlgNative(self):
        if not 'wxMSW' in wx.PlatformInfo():
            info = self._makeInfo()
            wx.CallLater(250, self._closeDlg)
            wx.adv.AboutBox(info, self.frame)
                     
    def test_aboutdlgGeneric(self):
        info = self._makeInfo()
        wx.CallLater(250, self._closeDlg)
        wx.adv.GenericAboutBox(info, self.frame)
                     
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
