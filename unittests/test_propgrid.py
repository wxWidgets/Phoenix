import unittest
import pytest
from unittests import wtc

import wx
import wx.propgrid as pg

#---------------------------------------------------------------------------

class propgrid_Tests(wtc.WidgetTestCase):

    def test_propgrid01(self):
        obj = pg.PGValidationInfo()


    def test_propgrid02(self):
        pg.PG_AUTO_SORT
        pg.PG_HIDE_CATEGORIES
        pg.PG_ALPHABETIC_MODE
        pg.PG_BOLD_MODIFIED
        pg.PG_SPLITTER_AUTO_CENTER
        pg.PG_TOOLTIPS
        pg.PG_HIDE_MARGIN
        pg.PG_STATIC_SPLITTER
        pg.PG_STATIC_LAYOUT
        pg.PG_LIMITED_EDITING
        pg.PG_TOOLBAR
        pg.PG_DESCRIPTION
        pg.PG_NO_INTERNAL_BORDER

        pg.PG_EX_INIT_NOCAT
        pg.PG_EX_NO_FLAT_TOOLBAR
        pg.PG_EX_MODE_BUTTONS
        pg.PG_EX_HELP_AS_TOOLTIPS
        pg.PG_EX_NATIVE_DOUBLE_BUFFERING
        pg.PG_EX_AUTO_UNSPECIFIED_VALUES
        pg.PG_EX_WRITEONLY_BUILTIN_ATTRIBUTES
        pg.PG_EX_HIDE_PAGE_BUTTONS
        pg.PG_EX_MULTIPLE_SELECTION
        pg.PG_EX_ENABLE_TLP_TRACKING
        pg.PG_EX_NO_TOOLBAR_DIVIDER
        pg.PG_EX_TOOLBAR_SEPARATOR

        pg.PG_DEFAULT_STYLE
        pg.PGMAN_DEFAULT_STYLE


    def test_propgrid03(self):
        pgrid = pg.PropertyGrid(self.frame)


    def test_propgrid04_deprecatedPGActionConstants(self):
        # These wxPG_ACTION_XXX constants were dropped when wxWidgets moved
        # to the PGKeyboardAction enum, see issue #2941. They should still
        # be accessible, but raise a DeprecationWarning and return the
        # equivalent PGKeyboardAction value.
        expected = {
            'PG_ACTION_INVALID'           : pg.PGKeyboardAction.Invalid,
            'PG_ACTION_NEXT_PROPERTY'     : pg.PGKeyboardAction.NextProperty,
            'PG_ACTION_PREV_PROPERTY'     : pg.PGKeyboardAction.PrevProperty,
            'PG_ACTION_EXPAND_PROPERTY'   : pg.PGKeyboardAction.ExpandProperty,
            'PG_ACTION_COLLAPSE_PROPERTY' : pg.PGKeyboardAction.CollapseProperty,
            'PG_ACTION_CANCEL_EDIT'       : pg.PGKeyboardAction.CancelEdit,
            'PG_ACTION_EDIT'              : pg.PGKeyboardAction.Edit,
            'PG_ACTION_PRESS_BUTTON'      : pg.PGKeyboardAction.PressButton,
            'PG_ACTION_MAX'               : pg.PGKeyboardAction.PressButton + 1,
        }
        for name, value in expected.items():
            with pytest.warns(wx.wxPyDeprecationWarning):
                self.assertEqual(getattr(pg, name), value)

        with self.assertRaises(AttributeError):
            pg.PG_ACTION_THIS_DOES_NOT_EXIST



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
