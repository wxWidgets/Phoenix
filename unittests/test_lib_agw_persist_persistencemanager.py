import unittest
from unittests import wtc
import wx
import random

import os
import wx.lib.agw.persist as PM

#---------------------------------------------------------------------------

class lib_agw_persist_persistencemanager_Tests(wtc.WidgetTestCase):

    def setUp(self):
        super(lib_agw_persist_persistencemanager_Tests, self).setUp()
        dirName = os.path.dirname(os.path.abspath(__file__))
        self._configFile1 = os.path.join(dirName, "PersistTest1")


    def test_persistencemanagerCtor(self):

        self._persistMgr = PM.PersistenceManager.Get()
        self._persistMgr.SetManagerStyle(PM.PM_SAVE_RESTORE_AUI_PERSPECTIVES)
        self._persistMgr.SetPersistenceFile(self._configFile1)

        # give the frame a Name for below
        self.frame.SetName('PersistTestFrame')
        cb = wx.CheckBox(self.frame, name='PersistCheck')
        cb.persistValue = True
        cb.SetValue(False)

        self._persistMgr.RegisterAndRestoreAll(self.frame)

        self._persistMgr.SaveAndUnregister()


    def test_persistencemanagerRestore(self):

        self._persistMgr = PM.PersistenceManager.Get()
        self._persistMgr.SetPersistenceFile(self._configFile1)

        # give the frame a Name for below
        self.frame.SetName('PersistTestFrame')

        self._persistMgr.RegisterAndRestoreAll(self.frame)

        self.assertEqual(self._persistMgr.HasRestored(), True, "Persistence should be there, as it was created in CTOR test.")


    def test_persistencemanagerPersistValue(self):

        self._persistMgr = PM.PersistenceManager.Get()
        self._persistMgr.SetManagerStyle(PM.PM_SAVE_RESTORE_AUI_PERSPECTIVES)
        self._persistMgr.SetPersistenceFile(self._configFile1)

        # give the frame a Name for below
        self.frame.SetName('PersistTestFrame')
        cb = wx.CheckBox(self.frame, name='PersistCheck')
        cb.persistValue = True

        self._persistMgr.RegisterAndRestoreAll(self.frame)

        self.assertEqual(self._persistMgr.HasRestored(), True, "Persistence should be there, as it was created in CTOR test.")
        self.assertEqual(cb.GetValue(), False, "Should be False as set in CTOR test")


    def test_persistencemanagerZZZZCleanup(self):
        # Just clean up the test file used by the other tests...
        # TODO: Fix these tests to be self-contained and to clean up after themselves
        if os.path.exists(self._configFile1):
            os.unlink(self._configFile1)


    def test_persistencemanagerConstantsExist(self):
        # PersistenceManager styles
        PM.PM_SAVE_RESTORE_AUI_PERSPECTIVES
        PM.PM_SAVE_RESTORE_TREE_LIST_SELECTIONS
        PM.PM_PERSIST_CONTROL_VALUE
        PM.PM_RESTORE_CAPTION_FROM_CODE
        PM.PM_DEFAULT_STYLE


        # String constants used by BookHandler

        PM.PERSIST_BOOK_KIND
        PM.PERSIST_BOOK_SELECTION

        # To save and restore wx.lib.agw.aui.AuiNotebook perspectives
        PM.PERSIST_BOOK_AGW_AUI_PERSPECTIVE

        # ----------------------------------------------------------------------------------- #
        # String constants used by TreebookHandler

        PM.PERSIST_TREEBOOK_KIND

        # this key contains the indices of all expanded nodes in the tree book
        # separated by PERSIST_SEP
        PM.PERSIST_TREEBOOK_EXPANDED_BRANCHES
        PM.PERSIST_SEP

        # ----------------------------------------------------------------------------------- #
        # String constants used by TLWHandler

        # we use just "Window" to keep configuration files and such short, there
        # should be no confusion with wx.Window itself as we don't have persistent
        # windows, just persistent controls which have their own specific kind strings

        PM.PERSIST_TLW_KIND

        # Names for various persistent options
        PM.PERSIST_TLW_X
        PM.PERSIST_TLW_Y
        PM.PERSIST_TLW_W
        PM.PERSIST_TLW_H

        PM.PERSIST_TLW_MAXIMIZED
        PM.PERSIST_TLW_ICONIZED

        # To save and restore wx.aui and wx.lib.agw.aui perspectives
        PM.PERSIST_AGW_AUI_PERSPECTIVE
        PM.PERSIST_AUI_PERSPECTIVE

        PM.PERSIST_AUIPERSPECTIVE_KIND

        # ----------------------------------------------------------------------------------- #
        # String constants used by CheckBoxHandler

        PM.PERSIST_CHECKBOX_KIND
        PM.PERSIST_CHECKBOX_3STATE
        PM.PERSIST_CHECKBOX

        # ----------------------------------------------------------------------------------- #
        # String constants used by ListBoxHandler

        PM.PERSIST_LISTBOX_KIND
        PM.PERSIST_LISTBOX_SELECTIONS

        # ----------------------------------------------------------------------------------- #
        # String constants used by ListCtrlHandler

        PM.PERSIST_LISTCTRL_KIND
        PM.PERSIST_LISTCTRL_COLWIDTHS

        # ----------------------------------------------------------------------------------- #
        # String constants used by CheckListBoxHandler

        PM.PERSIST_CHECKLISTBOX_KIND
        PM.PERSIST_CHECKLIST_CHECKED
        PM.PERSIST_CHECKLIST_SELECTIONS

        # ----------------------------------------------------------------------------------- #
        # String constants used by ChoiceComboHandler

        PM.PERSIST_CHOICECOMBO_KIND
        PM.PERSIST_CHOICECOMBO_SELECTION

        # ----------------------------------------------------------------------------------- #
        # String constants used by RadioBoxHandler

        PM.PERSIST_RADIOBOX_KIND
        PM.PERSIST_RADIOBOX_SELECTION

        # ----------------------------------------------------------------------------------- #
        # String constants used by RadioButtonHandler

        PM.PERSIST_RADIOBUTTON_KIND
        PM.PERSIST_RADIOBUTTON_VALUE

        # ----------------------------------------------------------------------------------- #
        # String constants used by ScrolledWindowHandler

        PM.PERSIST_SCROLLEDWINDOW_KIND
        PM.PERSIST_SCROLLEDWINDOW_POS_H
        PM.PERSIST_SCROLLEDWINDOW_POS_V

        # ----------------------------------------------------------------------------------- #
        # String constants used by SliderHandler

        PM.PERSIST_SLIDER_KIND
        PM.PERSIST_SLIDER_VALUE

        # ----------------------------------------------------------------------------------- #
        # String constants used by SpinHandler

        PM.PERSIST_SPIN_KIND
        PM.PERSIST_SPIN_VALUE

        # ----------------------------------------------------------------------------------- #
        # String constants used by SplitterHandler

        PM.PERSIST_SPLITTER_KIND
        PM.PERSIST_SPLITTER_POSITION

        # ----------------------------------------------------------------------------------- #
        # String constants used by TextCtrlHandler

        PM.PERSIST_TEXTCTRL_KIND
        PM.PERSIST_TEXTCTRL_VALUE

        # ----------------------------------------------------------------------------------- #
        # String constants used by ToggleButtonHandler

        PM.PERSIST_TOGGLEBUTTON_KIND
        PM.PERSIST_TOGGLEBUTTON_TOGGLED

        # ----------------------------------------------------------------------------------- #
        # String constants used by TreeCtrlHandler

        PM.PERSIST_TREECTRL_KIND
        PM.PERSIST_TREECTRL_CHECKED_ITEMS
        PM.PERSIST_TREECTRL_EXPANSION
        PM.PERSIST_TREECTRL_SELECTIONS

        # ----------------------------------------------------------------------------------- #
        # String constants used by TreeListCtrlHandler

        PM.PERSIST_TREELISTCTRL_KIND
        PM.PERSIST_TREELISTCTRL_COLWIDTHS

        # ----------------------------------------------------------------------------------- #
        # String constants used by CalendarCtrlHandler

        PM.PERSIST_CALENDAR_KIND
        PM.PERSIST_CALENDAR_DATE

        # ----------------------------------------------------------------------------------- #
        # String constants used by CollapsiblePaneHandler

        PM.PERSIST_COLLAPSIBLE_KIND
        PM.PERSIST_COLLAPSIBLE_STATE

        # ----------------------------------------------------------------------------------- #
        # String constants used by DatePickerHandler

        PM.PERSIST_DATEPICKER_KIND
        PM.PERSIST_DATEPICKER_DATE

        # ----------------------------------------------------------------------------------- #
        # String constants used by MediaCtrlHandler

        PM.PERSIST_MEDIA_KIND

        PM.PERSIST_MEDIA_POS
        PM.PERSIST_MEDIA_VOLUME
        PM.PERSIST_MEDIA_RATE

        # ----------------------------------------------------------------------------------- #
        # String constants used by ColourPickerHandler

        PM.PERSIST_COLOURPICKER_KIND
        PM.PERSIST_COLOURPICKER_COLOUR

        # ----------------------------------------------------------------------------------- #
        # String constants used by FileDirPickerHandler

        PM.PERSIST_FILEDIRPICKER_KIND
        PM.PERSIST_FILEDIRPICKER_PATH

        # ----------------------------------------------------------------------------------- #
        # String constants used by FontPickerHandler

        PM.PERSIST_FONTPICKER_KIND
        PM.PERSIST_FONTPICKER_FONT

        # ----------------------------------------------------------------------------------- #
        # String constants used by FileHistoryHandler

        PM.PERSIST_FILEHISTORY_KIND
        PM.PERSIST_FILEHISTORY_PATHS

        # ----------------------------------------------------------------------------------- #
        # String constants used by FindReplaceHandler

        PM.PERSIST_FINDREPLACE_KIND
        PM.PERSIST_FINDREPLACE_FLAGS
        PM.PERSIST_FINDREPLACE_SEARCH
        PM.PERSIST_FINDREPLACE_REPLACE

        # ----------------------------------------------------------------------------------- #
        # String constants used by FontDialogHandler

        PM.PERSIST_FONTDIALOG_KIND
        PM.PERSIST_FONTDIALOG_EFFECTS
        PM.PERSIST_FONTDIALOG_SYMBOLS
        PM.PERSIST_FONTDIALOG_COLOUR
        PM.PERSIST_FONTDIALOG_FONT
        PM.PERSIST_FONTDIALOG_HELP

        # ----------------------------------------------------------------------------------- #
        # String constants used by ColourDialogHandler

        PM.PERSIST_COLOURDIALOG_KIND
        PM.PERSIST_COLOURDIALOG_COLOUR
        PM.PERSIST_COLOURDIALOG_CHOOSEFULL
        PM.PERSIST_COLOURDIALOG_CUSTOMCOLOURS

        # ----------------------------------------------------------------------------------- #
        # String constants used by ChoiceDialogHandler

        PM.PERSIST_CHOICEDIALOG_KIND
        PM.PERSIST_CHOICEDIALOG_SELECTIONS

        # ----------------------------------------------------------------------------------- #
        # String constants used by MenuBarHandler

        PM.PERSIST_MENUBAR_KIND
        PM.PERSIST_MENUBAR_CHECKRADIO_ITEMS

        # ----------------------------------------------------------------------------------- #
        # String constants used by ToolBarHandler

        PM.PERSIST_TOOLBAR_KIND
        PM.PERSIST_TOOLBAR_CHECKRADIO_ITEMS

        # ----------------------------------------------------------------------------------- #
        # String constants used by FoldPanelBarHandler

        PM.PERSIST_FOLDPANELBAR_KIND
        PM.PERSIST_FOLDPANELBAR_EXPANDED

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
