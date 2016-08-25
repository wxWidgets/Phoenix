import unittest
from unittests import wtc

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

        pg.PG_VFB_STAY_IN_PROPERTY
        pg.PG_VFB_BEEP
        pg.PG_VFB_MARK_CELL
        pg.PG_VFB_SHOW_MESSAGE
        pg.PG_VFB_SHOW_MESSAGEBOX
        pg.PG_VFB_SHOW_MESSAGE_ON_STATUSBAR
        pg.PG_VFB_DEFAULT

        pg.PG_ACTION_INVALID
        pg.PG_ACTION_NEXT_PROPERTY
        pg.PG_ACTION_PREV_PROPERTY
        pg.PG_ACTION_EXPAND_PROPERTY
        pg.PG_ACTION_COLLAPSE_PROPERTY
        pg.PG_ACTION_CANCEL_EDIT
        pg.PG_ACTION_EDIT
        pg.PG_ACTION_PRESS_BUTTON
        pg.PG_ACTION_MAX

        pg.PG_DEFAULT_STYLE
        pg.PGMAN_DEFAULT_STYLE


    def test_propgrid03(self):
        pgrid = pg.PropertyGrid(self.frame)





#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
