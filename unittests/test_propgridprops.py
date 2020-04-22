import os
import unittest
from unittests import wtc
import wx.propgrid as pg

#---------------------------------------------------------------------------

class propgridprops_Tests(wtc.WidgetTestCase):

    def test_propgridprops01(self):
        o = pg.PGInDialogValidator()


    def test_propgridprops02(self):
        pg.PG_PROP_PASSWORD

        p1 = pg.StringProperty()
        p2 = pg.StringProperty('label', 'name', 'value')

        s = p2.ValueToString(12345)
        assert s == '12345'


    def test_propgridprops03(self):
        pg.PG_PROPERTY_VALIDATION_ERROR_MESSAGE
        pg.PG_PROPERTY_VALIDATION_SATURATE
        pg.PG_PROPERTY_VALIDATION_WRAP

        o = pg.NumericPropertyValidator(pg.NumericPropertyValidator.Signed)

        pg.NumericPropertyValidator.Signed
        pg.NumericPropertyValidator.Unsigned
        pg.NumericPropertyValidator.Float



    def test_propgridprops04(self):
        p = pg.IntProperty()


    def test_propgridprops05(self):
        p = pg.UIntProperty()


    def test_propgridprops06(self):
        p = pg.FloatProperty()


    def test_propgridprops07(self):
        pg.PG_PROP_USE_CHECKBOX
        pg.PG_PROP_USE_DCC
        p = pg.BoolProperty()


    def test_propgridprops08(self):
        pg.PG_PROP_STATIC_CHOICES

        p1 = pg.EnumProperty()
        p2 = pg.EnumProperty(label='label', name='name',
                             labels=['one', 'two', 'three'],
                             values=[1, 2, 3])


    def test_propgridprops09(self):
        p1 = pg.EditEnumProperty()
        p2 = pg.EditEnumProperty(label='label', name='name',
                                 labels=['one', 'two', 'three'],
                                 values=[1, 2, 3])


    def test_propgridprops10(self):
        p1 = pg.FlagsProperty()
        p2 = pg.FlagsProperty(label='label', name='name',
                              labels=['one', 'two', 'three'],
                              values=[1, 2, 3])


    @unittest.skip('class was removed?')
    def test_propgridprops11(self):
        da = pg.PGFileDialogAdapter()


    def test_propgridprops12(self):
        pg.PG_PROP_SHOW_FULL_FILENAME

        p1 = pg.FileProperty()
        value = '/foo/bar/value'
        p2 = pg.FileProperty('label', 'name', value)

        fn = p2.GetFileName()
        assert fn.replace(os.path.sep, '/') == value


    @unittest.skip('class was removed?')
    def test_propgridprops13(self):
        pg.PG_PROP_NO_ESCAPE
        da = pg.PGLongStringDialogAdapter()


    def test_propgridprops14(self):
        p1 = pg.LongStringProperty()


    def test_propgridprops15(self):
        p1 = pg.DirProperty()


    def test_propgridprops16(self):
        p1 = pg.ArrayStringProperty()
        p2 = pg.ArrayStringProperty(label='label', name='name',
                                    value=['one', 'two', 'three'])


    def test_propgridprops17(self):
        with self.assertRaises(TypeError):
            dlg = pg.PGArrayEditorDialog(self.frame, 'message', 'caption')
            dlg.Destroy()


    def test_propgridprops18(self):
        dlg = pg.PGArrayStringEditorDialog()
        dlg.Destroy()





#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
