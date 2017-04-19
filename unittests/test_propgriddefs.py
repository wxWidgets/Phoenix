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

        pg.PG_FULL_VALUE
        pg.PG_REPORT_ERROR
        pg.PG_PROPERTY_SPECIFIC
        pg.PG_EDITABLE_VALUE
        pg.PG_COMPOSITE_FRAGMENT
        pg.PG_UNEDITABLE_COMPOSITE_FRAGMENT
        pg.PG_VALUE_IS_CURRENT
        pg.PG_PROGRAMMATIC_VALUE

        pg.PG_SETVAL_REFRESH_EDITOR
        pg.PG_SETVAL_AGGREGATED
        pg.PG_SETVAL_FROM_PARENT
        pg.PG_SETVAL_BY_USER

        pg.PG_LABEL
        pg.PG_LABEL_STRING
        pg.PG_NULL_BITMAP
        pg.PG_COLOUR_BLACK
        pg.PG_DEFAULT_IMAGE_SIZE

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
