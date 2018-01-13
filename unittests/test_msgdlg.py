import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class msgdlg_Tests(wtc.WidgetTestCase):


    def test_msgdlg1(self):
        dlg = wx.MessageDialog(None, 'Message', 'Caption')
        dlg.Destroy()

    def test_msgdlg2(self):
        dlg = wx.MessageDialog(self.frame, 'Message', 'Caption')
        dlg.Destroy()

    def test_msgdlg3(self):
        dlg = wx.MessageDialog(None, 'Message', 'Caption')
        dlg.SetExtendedMessage('extended')
        dlg.SetMessage('message')
        dlg.SetOKCancelLabels('okidoky', 'bye-bye')
        self.assertEqual(dlg.GetExtendedMessage(), 'extended')
        self.assertEqual(dlg.GetMessage(), 'message')
        self.assertEqual(dlg.GetOKLabel(), 'okidoky')
        self.assertEqual(dlg.GetCancelLabel(), 'bye-bye')
        dlg.Destroy()

    def test_msgdlg3(self):
        wx.MessageBox

    def test_msgdlgProperties(self):
        dlg = wx.MessageDialog(None, 'Message', 'Caption')
        dlg.CancelLabel
        dlg.Caption
        dlg.EffectiveIcon
        dlg.ExtendedMessage
        dlg.HelpLabel
        dlg.Message
        dlg.MessageDialogStyle
        dlg.NoLabel
        dlg.OKLabel
        dlg.YesLabel
        dlg.Destroy()

    def test_msgdlgIconConstants(self):
        wx.ICON_EXCLAMATION
        wx.ICON_HAND
        wx.ICON_ERROR
        wx.ICON_QUESTION
        wx.ICON_INFORMATION
        wx.STAY_ON_TOP


    def test_msgdlgLabels1(self):
        dlg = wx.MessageDialog(None, 'Message', 'Caption')
        dlg.SetHelpLabel('help')
        dlg.SetOKCancelLabels('ok', 'cancel')
        dlg.SetOKLabel('ok')
        dlg.SetYesNoCancelLabels('yes', 'no', 'cancel')
        dlg.SetYesNoLabels('yes', 'no')

    def test_msgdlgLabels2(self):
        dlg = wx.MessageDialog(None, 'Message', 'Caption')
        dlg.SetHelpLabel(wx.ID_HELP)
        dlg.SetOKCancelLabels(wx.ID_OK, wx.ID_CANCEL)
        dlg.SetOKLabel(wx.ID_OK)
        dlg.SetYesNoCancelLabels(wx.ID_YES, wx.ID_NO, wx.ID_CANCEL)
        dlg.SetYesNoLabels(wx.ID_YES, wx.ID_NO)


    def test_gmsgdlg1(self):
        dlg = wx.GenericMessageDialog(None, 'Message', 'Caption')
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

    def test_gmsgdlg2(self):
        dlg = wx.GenericMessageDialog(self.frame, 'Message', 'Caption')
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

    def test_gmsgdlg3(self):
        dlg = wx.GenericMessageDialog(None, 'Message', 'Caption')
        dlg.SetExtendedMessage('extended')
        dlg.SetMessage('message')
        dlg.SetOKCancelLabels('okidoky', 'bye-bye')
        self.assertEqual(dlg.GetExtendedMessage(), 'extended')
        self.assertEqual(dlg.GetMessage(), 'message')
        self.assertEqual(dlg.GetOKLabel(), 'okidoky')
        self.assertEqual(dlg.GetCancelLabel(), 'bye-bye')
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
