import unittest
from unittests import wtc

import wx.propgrid as pg

#---------------------------------------------------------------------------

class property_Tests(wtc.WidgetTestCase):

    def test_propgridproperty01(self):
        d = pg.PGPaintData()
        d.m_parent
        d.m_choiceItem
        d.m_drawnWidth
        d.m_drawnHeight


    def test_propgridproperty03(self):
        with self.assertRaises(TypeError):
            # it's an abstract class, so it can't be instantiated
            r = pg.PGCellRenderer()

        # check the nested enum values
        pg.PGCellRenderer.Selected
        pg.PGCellRenderer.ChoicePopup
        pg.PGCellRenderer.Control
        pg.PGCellRenderer.Disabled
        pg.PGCellRenderer.DontUseCellFgCol
        pg.PGCellRenderer.DontUseCellBgCol
        pg.PGCellRenderer.DontUseCellColours


    def test_propgridproperty04(self):
        r = pg.PGDefaultRenderer()


    def test_propgridproperty05(self):
        d = pg.PGCellData()


    def test_propgridproperty06(self):
        c = pg.PGCell()


    # def test_propgridproperty07(self):
    #     attrs = pg.PGAttributeStorage()
    #     attrs.Set('name',     'value')
    #     attrs.Set('one',      1)
    #     attrs.Set('two.one',  2.1)
    #     attrs.Set('true',     True)
    #     assert attrs.GetCount() == 4
    #     assert attrs.FindValue('name') == 'value'
    #     # TODO: Add some iteration tests


    def test_propgridproperty08(self):
        pg.PG_ATTR_DEFAULT_VALUE
        pg.PG_ATTR_MIN
        pg.PG_ATTR_MAX
        pg.PG_ATTR_UNITS
        pg.PG_ATTR_HINT
        pg.PG_ATTR_INLINE_HELP
        pg.PG_ATTR_AUTOCOMPLETE
        pg.PG_BOOL_USE_CHECKBOX
        pg.PG_BOOL_USE_DOUBLE_CLICK_CYCLING
        pg.PG_FLOAT_PRECISION
        pg.PG_STRING_PASSWORD
        pg.PG_UINT_BASE
        pg.PG_UINT_PREFIX
        pg.PG_FILE_WILDCARD
        pg.PG_FILE_SHOW_FULL_PATH
        pg.PG_FILE_SHOW_RELATIVE_PATH
        pg.PG_FILE_INITIAL_PATH
        pg.PG_FILE_DIALOG_TITLE
        pg.PG_FILE_DIALOG_STYLE
        pg.PG_DIR_DIALOG_MESSAGE
        pg.PG_ARRAY_DELIMITER
        pg.PG_DATE_FORMAT
        pg.PG_DATE_PICKER_STYLE
        pg.PG_ATTR_SPINCTRL_STEP
        pg.PG_ATTR_SPINCTRL_WRAP
        pg.PG_ATTR_SPINCTRL_MOTIONSPIN
        pg.PG_ATTR_MULTICHOICE_USERSTRINGMODE
        pg.PG_COLOUR_ALLOW_CUSTOM
        pg.PG_COLOUR_HAS_ALPHA

        pg.NullProperty
        pg.PGChoicesEmptyData


    def test_propgridproperty10(self):
        p1 = pg.PGProperty()
        p2 = pg.PGProperty('label', 'name')


    def test_propgridproperty11(self):
        c1 = pg.PropertyCategory()
        c2 = pg.PropertyCategory('label', 'name')


    def test_propgridproperty12(self):
        ce = pg.PGChoiceEntry()
        cd = pg.PGChoicesData()




#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
