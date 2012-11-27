import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class richmsgdlg_Tests(wtc.WidgetTestCase):

    def test_richmsgdlg1(self):
        dlg = wx.RichMessageDialog(None, 'Message', 'Caption')
        dlg.Destroy()
        
    def test_richmsgdlg2(self):
        dlg = wx.RichMessageDialog(self.frame, 'Message', 'Caption')
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
        
        dlg.Destroy()
    
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
