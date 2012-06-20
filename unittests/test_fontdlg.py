import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class fontdlg_Tests(wtc.WidgetTestCase):

    def test_fontdlg1(self):
        data = wx.FontData()
        data.SetInitialFont(wx.FFont(15, wx.FONTFAMILY_TELETYPE))
        self.assertEqual(data.InitialFont.Family, wx.FONTFAMILY_TELETYPE)
        
        dlg = wx.FontDialog(self.frame, data)
        # TODO: find a safe way to test ShowModal on native dialogs
        dlg.Destroy()
        
        
    def test_fontdlg2(self):
        wx.GetFontFromUser
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
