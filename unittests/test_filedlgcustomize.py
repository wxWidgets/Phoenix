import ctypes
import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class filedlgcustomize_Tests(wtc.WidgetTestCase):

    @unittest.skipIf('wxOSX' in wx.PlatformInfo,
        "ShowModal() hangs on macOS: AppKit rejects the accessory-view "
        "mutation wxWidgets uses for extra controls (see filedlg.mm "
        "SetupExtraControls())")
    def test_filedlgcustomize1(self):
        class MyFileDialogCustomizeHook(wx.FileDialogCustomizeHook):
            def __init__(self):
                super().__init__()
                self.add_called = False
            def AddCustomControls(self, customizer):
                self.add_called = True

        hook = MyFileDialogCustomizeHook()
        title = 'Save Document'
        dlg = wx.FileDialog(None, title, '', 'file.my')
        dlg.SetCustomizeHook(hook)

        def closeDialog(attempt=0):
            if 'wxMSW' in wx.PlatformInfo:
                # Native IFileDialog on MSW isn't a real wx modal dialog, so
                # EndModal() asserts, and UIActionSimulator's synthetic
                # keystrokes depend on OS focus that CI runners don't
                # reliably give the dialog. Post WM_CLOSE straight to the
                # dialog's HWND (found by its title) instead, which doesn't
                # need focus.
                WM_CLOSE = 0x0010
                hwnd = ctypes.windll.user32.FindWindowW(None, title)
                if hwnd:
                    ctypes.windll.user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
                elif attempt < 20:
                    wx.CallLater(50, closeDialog, attempt + 1)
            else:
                dlg.EndModal(wx.ID_OK)

        wx.CallLater(250, closeDialog)
        dlg.ShowModal()
        assert(hook.add_called)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
