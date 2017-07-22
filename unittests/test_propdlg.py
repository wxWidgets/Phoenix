import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class propdlg_Tests(wtc.WidgetTestCase):

    def test_propdlg1(self):
        # Constants
        wx.adv.PROPSHEET_DEFAULT
        wx.adv.PROPSHEET_NOTEBOOK
        wx.adv.PROPSHEET_TOOLBOOK
        wx.adv.PROPSHEET_CHOICEBOOK
        wx.adv.PROPSHEET_LISTBOOK
        wx.adv.PROPSHEET_BUTTONTOOLBOOK
        wx.adv.PROPSHEET_TREEBOOK
        wx.adv.PROPSHEET_SHRINKTOFIT


    def test_propgrid2(self):
        # Normal, simple usage
        dlg = wx.adv.PropertySheetDialog(self.frame, title="Property Sheet")
        dlg.SetSheetStyle(wx.adv.PROPSHEET_NOTEBOOK)
        dlg.Destroy()


    def test_propgrid3(self):
        # 2-Phase create
        dlg = wx.adv.PropertySheetDialog()
        dlg.Create(self.frame, title="Property Sheet")
        dlg.SetSheetStyle(wx.adv.PROPSHEET_NOTEBOOK)
        dlg.Destroy()


    def test_propgrid4(self):
        # Derived class
        class MyPropSheetDlg(wx.adv.PropertySheetDialog):
            def __init__(self, parent, title):
                wx.adv.PropertySheetDialog.__init__(self) # 1st phase

                # Setup
                self.SetSheetStyle(wx.adv.PROPSHEET_NOTEBOOK)
                self.SetSheetInnerBorder(10)
                self.SetSheetOuterBorder(15)

                self.Create(parent, title=title) # 2nd phase create

                # Create the stock buttons
                self.CreateButtons(wx.OK|wx.CANCEL)

                # Add some pages
                notebook = self.GetBookCtrl()
                notebook.AddPage(wx.Panel(notebook), "Page1")
                notebook.AddPage(wx.Panel(notebook), "Page2")

                # Do the layout
                self.LayoutDialog()


        dlg = MyPropSheetDlg(self.frame, "Property Sheet Dlg")
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
