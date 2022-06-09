import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class filedlgcustomize_Tests(wtc.WidgetTestCase):

    def test_filedlgcustomize1(self):
        class MyFileDialogCustomizeHook(wx.FileDialogCustomizeHook):
            def __init__(self):
                super().__init__()
                self.add_called = False
            def AddCustomControls(self, customizer):
                self.add_called = True

        hook = MyFileDialogCustomizeHook()
        dlg = wx.FileDialog(None, 'Save Document', '', 'file.my')
        dlg.SetCustomizeHook(hook)
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        assert(hook.add_called)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
