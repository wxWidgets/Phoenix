import unittest
from unittests import wtc

import wx.propgrid as pg

#---------------------------------------------------------------------------

class propgrideditors_Tests(wtc.WidgetTestCase):


    def test_propgrideditors01(self):
        wl = pg.PGWindowList(self.frame)
        assert wl.GetPrimary() is self.frame
        assert wl.GetSecondary() is None

        wl = pg.PGWindowList(self.frame, None)
        assert wl.GetPrimary() is self.frame
        assert wl.GetSecondary() is None


    def test_propgrideditors02(self):
        with self.assertRaises(TypeError):
            # it's an abstract class, so it can't be instantiated
            ed = pg.PGEditor()

        class MyEditor(pg.PGEditor):
            def CreateControls(self, propgrid, prop, pos, size):
                return pg.PGWindowList()
            def UpdateControl(self, prop, ctrl):
                pass
            def OnEvent(self, propgrid, prop, wnd, event):
                return False

        ed = MyEditor()


    def test_propgrideditors03(self):
        ed = pg.PGTextCtrlEditor()


    def test_propgrideditors04(self):
        ed = pg.PGChoiceEditor()


    def test_propgrideditors05(self):
        ed = pg.PGComboBoxEditor()


    def test_propgrideditors06(self):
        ed = pg.PGChoiceAndButtonEditor()


    def test_propgrideditors07(self):
        ed = pg.PGTextCtrlAndButtonEditor()


    def test_propgrideditors08(self):
        ed = pg.PGCheckBoxEditor()


    def test_propgrideditors09(self):
        with self.assertRaises(TypeError):
            # it's an abstract class, so it can't be instantiated
            da = pg.PGEditorDialogAdapter()

        class MyAdapter(pg.PGEditorDialogAdapter):
            def DoShowDialog(self, propGrid, prop):
                return False

        da = MyAdapter()


    def test_propgrideditors10(self):
        pgrid = pg.PropertyGrid(self.frame)
        mb = pg.PGMultiButton(pgrid, (100,25))


    def test_propgrideditors11(self):
        # Just make sure these exist
        pg.PGEditor_TextCtrl
        pg.PGEditor_Choice
        pg.PGEditor_ComboBox
        pg.PGEditor_TextCtrlAndButton
        pg.PGEditor_CheckBox
        pg.PGEditor_ChoiceAndButton
        pg.PGEditor_SpinCtrl
        pg.PGEditor_DatePickerCtrl



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
