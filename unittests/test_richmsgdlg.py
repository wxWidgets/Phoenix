import ctypes
import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

def _closeMSWTaskDialog(title, attempt=0):
    # Native TaskDialogIndirect() on MSW isn't a real wx modal dialog, so
    # EndModal() asserts. Post WM_CLOSE to it instead.
    WM_CLOSE = 0x0010
    hwnd = ctypes.windll.user32.FindWindowW(None, title)
    if hwnd:
        ctypes.windll.user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
    elif attempt < 20:
        wx.CallLater(50, _closeMSWTaskDialog, title, attempt + 1)


def _scheduleDialogClose(dlg, title):
    if 'wxMSW' in wx.PlatformInfo:
        wx.CallLater(250, _closeMSWTaskDialog, title)
    else:
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)


class richmsgdlg_Tests(wtc.WidgetTestCase):

    def test_richmsgdlg1(self):
        dlg = wx.RichMessageDialog(None, 'Message', 'Caption')
        _scheduleDialogClose(dlg, 'Caption')
        dlg.ShowModal()
        dlg.Destroy()

    def test_richmsgdlg2(self):
        dlg = wx.RichMessageDialog(self.frame, 'Message', 'Caption')
        _scheduleDialogClose(dlg, 'Caption')
        dlg.ShowModal()
        dlg.Destroy()

    def test_richmsgdlg3(self):
        dlg = wx.RichMessageDialog(None, 'Message', 'Caption')
        dlg.SetExtendedMessage('extended')
        dlg.SetMessage('message')
        dlg.SetOKCancelLabels('okidoky', 'bye-bye')
        self.assertEqual(dlg.GetExtendedMessage(), 'extended')
        self.assertEqual(dlg.GetMessage(), 'message')
        self.assertEqual(dlg.GetOKLabel(), 'okidoky')
        self.assertEqual(dlg.GetCancelLabel(), 'bye-bye')

        dlg.ShowCheckBox("Checkbox")
        dlg.ShowDetailedText("Detailed Text")
        self.assertEqual(dlg.GetCheckBoxText(), "Checkbox")
        self.assertEqual(dlg.GetDetailedText(), "Detailed Text")
        self.assertEqual(dlg.CheckBoxText, "Checkbox")
        self.assertEqual(dlg.DetailedText, "Detailed Text")

        _scheduleDialogClose(dlg, 'Caption')
        dlg.ShowModal()
        dlg.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
