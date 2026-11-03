import unittest
from unittests import wtc
import wx
import wx.propgrid as pg

#---------------------------------------------------------------------------

class propgriddefs_Tests(wtc.WidgetTestCase):

    def test_propgriddefs1(self):
        pg.PG_INVALID_VALUE
        pg.PG_DONT_RECURSE
        pg.PG_BASE_OCT
        pg.PG_BASE_DEC
        pg.PG_BASE_HEX
        pg.PG_BASE_HEXL
        pg.PG_PREFIX_NONE
        pg.PG_PREFIX_0x
        pg.PG_PREFIX_DOLLAR_SIGN

        pg.PG_KEEP_STRUCTURE
        pg.PG_RECURSE
        pg.PG_INC_ATTRIBUTES
        pg.PG_RECURSE_STARTS
        pg.PG_FORCE
        pg.PG_SORT_TOP_LEVEL_ONLY

        pg.PG_LABEL
        pg.PG_LABEL_STRING
        pg.PG_NULL_BITMAP
        pg.PG_COLOUR_BLACK
        pg.PG_DEFAULT_IMAGE_SIZE

    def test_propgriddefsFlagsEnumsAcceptCombinations(self):
        flags = pg.PGPropValFormatFlags
        combined = flags.FullValue | flags.ValueIsCurrent
        self.assertIsInstance(combined, flags)
        self.assertEqual(combined, flags.FullValue.value | flags.ValueIsCurrent.value)
        self.assertIsInstance(flags(combined.value), flags)
        self.assertIs(flags(flags.FullValue.value), flags.FullValue)

    def test_propgriddefsCombinedFlagsFromCpp(self):
        seen = []

        class CustomProperty(pg.PGProperty):
            def __init__(self):
                super().__init__('custom', 'custom')
                self.SetValue('value')

            def ValueToString(self, value, flags=pg.PGPropValFormatFlags.Null):
                seen.append(flags)
                return 'text'

        grid = pg.PropertyGrid(self.frame)
        grid.Append(CustomProperty())
        self.assertEqual(grid.GetPropertyValues(as_strings=True), {'custom': 'text'})
        self.assertTrue(seen)

    def test_propgriddefsCombinedFlagsToCpp(self):
        flags = pg.PGPropValFormatFlags
        prop = pg.StringProperty('name', 'name', 'value')
        self.assertEqual(prop.ValueToString('value', flags.FullValue | flags.ValueIsCurrent), 'value')

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
