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


    def test_propgridproperty09(self):
        pg.PG_PROP_MODIFIED
        pg.PG_PROP_DISABLED
        pg.PG_PROP_HIDDEN
        pg.PG_PROP_CUSTOMIMAGE
        pg.PG_PROP_NOEDITOR
        pg.PG_PROP_COLLAPSED
        pg.PG_PROP_INVALID_VALUE
        pg.PG_PROP_WAS_MODIFIED
        pg.PG_PROP_AGGREGATE
        pg.PG_PROP_CHILDREN_ARE_COPIES
        pg.PG_PROP_PROPERTY
        pg.PG_PROP_CATEGORY
        pg.PG_PROP_MISC_PARENT
        pg.PG_PROP_READONLY
        pg.PG_PROP_COMPOSED_VALUE
        pg.PG_PROP_USES_COMMON_VALUE
        pg.PG_PROP_AUTO_UNSPECIFIED
        pg.PG_PROP_CLASS_SPECIFIC_1
        pg.PG_PROP_CLASS_SPECIFIC_2
        pg.PG_PROP_BEING_DELETED
        pg.PG_PROP_MAX
        pg.PG_PROP_PARENTAL_FLAGS


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
