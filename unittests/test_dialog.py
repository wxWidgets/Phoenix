import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class dialog_Tests(wtc.WidgetTestCase):

    def runDialog(self, dlg):
        # Add some buttons        
        ok = wx.Button(dlg, wx.ID_OK, pos=(10,10))
        cancel = wx.Button(dlg, wx.ID_CANCEL, pos=(100,10))

        if 'wxMac' not in wx.PortInfo:
            # Something is causing a hang when running one of these tests, so
            # for now we'll not actuall test ShowModal on Macs.
            # TODO: FIX THIS!!
            wx.CallLater(250, dlg.EndModal, wx.ID_OK)
            val = dlg.ShowModal()
            dlg.Destroy()
            self.assertTrue(val == wx.ID_OK)
            self.myYield()        
        
    
    def test_dialogDefaultCtor(self):
        dlg = wx.Dialog()
        dlg.Create(None, title='dialog')
        self.runDialog(dlg)
        
    def test_dialog1(self):
        dlg = wx.Dialog(self.frame, title='Hello')
        self.runDialog(dlg)

    def test_dialog2(self):
        dlg = wx.Dialog(self.frame, title='World')
        self.runDialog(dlg)
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
