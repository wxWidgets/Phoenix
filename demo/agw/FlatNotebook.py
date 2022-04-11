#!/usr/bin/env python

import wx

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    import agw.flatnotebook as FNB
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.flatnotebook as FNB

import random
import images


#----------------------------------------------------------------------


MENU_EDIT_DELETE_ALL = wx.NewIdRef()
MENU_EDIT_ADD_PAGE = wx.NewIdRef()
MENU_EDIT_DELETE_PAGE = wx.NewIdRef()
MENU_EDIT_SET_SELECTION = wx.NewIdRef()
MENU_EDIT_ADVANCE_SELECTION_FWD = wx.NewIdRef()
MENU_EDIT_ADVANCE_SELECTION_BACK = wx.NewIdRef()
MENU_SET_ALL_TABS_SHAPE_ANGLE = wx.NewIdRef()
MENU_SHOW_IMAGES = wx.NewIdRef()
MENU_USE_VC71_STYLE = wx.NewIdRef()
MENU_USE_DEFAULT_STYLE = wx.NewIdRef()
MENU_USE_FANCY_STYLE = wx.NewIdRef()
MENU_USE_RIBBON_STYLE = wx.NewIdRef()
MENU_SELECT_GRADIENT_COLOUR_FROM = wx.NewIdRef()
MENU_SELECT_GRADIENT_COLOUR_TO = wx.NewIdRef()
MENU_SELECT_GRADIENT_COLOUR_BORDER = wx.NewIdRef()
MENU_SET_PAGE_IMAGE_INDEX = wx.NewIdRef()
MENU_HIDE_X = wx.NewIdRef()
MENU_HIDE_NAV_BUTTONS = wx.NewIdRef()
MENU_USE_MOUSE_MIDDLE_BTN = wx.NewIdRef()
MENU_DRAW_BORDER = wx.NewIdRef()
MENU_USE_BOTTOM_TABS = wx.NewIdRef()
MENU_ENABLE_TAB = wx.NewIdRef()
MENU_DISABLE_TAB = wx.NewIdRef()
MENU_ENABLE_DRAG_N_DROP = wx.NewIdRef()
MENU_DCLICK_CLOSES_TAB = wx.NewIdRef()
MENU_USE_VC8_STYLE = wx.NewIdRef()
MENU_USE_FF2_STYLE = wx.NewIdRef()
MENU_HIDE_ON_SINGLE_TAB = wx.NewIdRef()
MENU_HIDE_TABS = wx.NewIdRef()
MENU_NO_TABS_FOCUS = wx.NewIdRef()

MENU_SET_ACTIVE_TEXT_COLOUR = wx.NewIdRef()
MENU_DRAW_TAB_X = wx.NewIdRef()
MENU_SET_ACTIVE_TAB_COLOUR = wx.NewIdRef()
MENU_SET_TAB_AREA_COLOUR = wx.NewIdRef()
MENU_SELECT_NONACTIVE_TEXT_COLOUR = wx.NewIdRef()
MENU_GRADIENT_BACKGROUND = wx.NewIdRef()
MENU_COLOURFUL_TABS = wx.NewIdRef()
MENU_SMART_TABS = wx.NewIdRef()
MENU_USE_DROP_ARROW_BUTTON = wx.NewIdRef()
MENU_ALLOW_FOREIGN_DND = wx.NewIdRef()

MENU_TILE_HORIZONTALLY = wx.NewIdRef()
MENU_TILE_VERTICALLY = wx.NewIdRef()
MENU_TILE_NONE = wx.NewIdRef()


class FlatNotebookDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent, title="FlatNotebook Demo", size=(800,600))
        self.log = log

        self._bShowImages = False
        self._bVCStyle = False
        self._newPageCounter = 0

        self._ImageList = wx.ImageList(16, 16)
        self._ImageList.Add(images._book_red.GetBitmap())
        self._ImageList.Add(images._book_green.GetBitmap())
        self._ImageList.Add(images._book_blue.GetBitmap())

        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("FlatNotebook wxPython Demo, Andrea Gavana @ 02 Oct 2006"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)

        self.SetIcon(images.Mondrian.GetIcon())
        self.CreateMenuBar()
        self.CreateRightClickMenu()
        self.LayoutItems()

        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.OnPageClosing)
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_DROPPED_FOREIGN, self.OnForeignDrop)
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_DROPPED, self.OnDrop)

        self.Bind(wx.EVT_UPDATE_UI, self.OnDropDownArrowUI, id=MENU_USE_DROP_ARROW_BUTTON)
        self.Bind(wx.EVT_UPDATE_UI, self.OnHideNavigationButtonsUI, id=MENU_HIDE_NAV_BUTTONS)
        self.Bind(wx.EVT_UPDATE_UI, self.OnAllowForeignDndUI, id=MENU_ALLOW_FOREIGN_DND)


    def CreateMenuBar(self):

        self._menuBar = wx.MenuBar(wx.MB_DOCKABLE)
        self._fileMenu = wx.Menu()
        self._editMenu = wx.Menu()
        self._visualMenu = wx.Menu()

        item = wx.MenuItem(self._fileMenu, wx.ID_ANY, "&Close\tCtrl-Q", "Close demo window")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        self._fileMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_EDIT_ADD_PAGE, "New Page\tCtrl+N", "Add New Page")
        self.Bind(wx.EVT_MENU, self.OnAddPage, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_EDIT_DELETE_PAGE, "Delete Page\tCtrl+F4", "Delete Page")
        self.Bind(wx.EVT_MENU, self.OnDeletePage, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_EDIT_DELETE_ALL, "Delete All Pages", "Delete All Pages")
        self.Bind(wx.EVT_MENU, self.OnDeleteAll, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_EDIT_SET_SELECTION, "Set Selection", "Set Selection")
        self.Bind(wx.EVT_MENU, self.OnSetSelection, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_EDIT_ADVANCE_SELECTION_FWD, "Advance Selection Forward",
                           "Advance Selection Forward")
        self.Bind(wx.EVT_MENU, self.OnAdvanceSelectionFwd, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_EDIT_ADVANCE_SELECTION_BACK, "Advance Selection Backward",
                           "Advance Selection Backward")
        self.Bind(wx.EVT_MENU, self.OnAdvanceSelectionBack, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_SET_ALL_TABS_SHAPE_ANGLE, "Set an inclination of tab header borders",
                           "Set the shape of tab header")
        self.Bind(wx.EVT_MENU, self.OnSetAllPagesShapeAngle, item)
        self._visualMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_SET_PAGE_IMAGE_INDEX, "Set image index of selected page",
                           "Set image index")
        self.Bind(wx.EVT_MENU, self.OnSetPageImage, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_SHOW_IMAGES, "Show Images", "Show Images", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnShowImages, item)
        self._editMenu.Append(item)

        styleMenu = wx.Menu()
        item = wx.MenuItem(styleMenu, MENU_USE_DEFAULT_STYLE, "Use Default Style", "Use VC71 Style", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnDefaultStyle, item)
        styleMenu.Append(item)

        item = wx.MenuItem(styleMenu, MENU_USE_VC71_STYLE, "Use VC71 Style", "Use VC71 Style", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnVC71Style, item)
        styleMenu.Append(item)

        item = wx.MenuItem(styleMenu, MENU_USE_VC8_STYLE, "Use VC8 Style", "Use VC8 Style", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnVC8Style, item)
        styleMenu.Append(item)

        item = wx.MenuItem(styleMenu, MENU_USE_FANCY_STYLE, "Use Fancy Style", "Use Fancy Style", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnFancyStyle, item)
        styleMenu.Append(item)

        item = wx.MenuItem(styleMenu, MENU_USE_FF2_STYLE, "Use Firefox 2 Style", "Use Firefox 2 Style", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnFF2Style, item)
        styleMenu.Append(item)

        item = wx.MenuItem(styleMenu, MENU_USE_RIBBON_STYLE, "Use Ribbon Style", "Use Ribbon Style", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnRibbonStyle, item)
        styleMenu.Append(item)

        self._visualMenu.Append(wx.ID_ANY, "Tabs Style", styleMenu)

        item = wx.MenuItem(self._visualMenu, MENU_SELECT_GRADIENT_COLOUR_FROM, "Select fancy tab style 'from' colour",
                           "Select fancy tab style 'from' colour")
        self._visualMenu.Append(item)

        item = wx.MenuItem(self._visualMenu, MENU_SELECT_GRADIENT_COLOUR_TO, "Select fancy tab style 'to' colour",
                           "Select fancy tab style 'to' colour")
        self._visualMenu.Append(item)

        item = wx.MenuItem(self._visualMenu, MENU_SELECT_GRADIENT_COLOUR_BORDER, "Select fancy tab style 'border' colour",
                           "Select fancy tab style 'border' colour")
        self._visualMenu.Append(item)

        self._editMenu.AppendSeparator()

        self.Bind(wx.EVT_MENU_RANGE, self.OnSelectColour, id=MENU_SELECT_GRADIENT_COLOUR_FROM,
                  id2=MENU_SELECT_GRADIENT_COLOUR_BORDER)

        item = wx.MenuItem(self._editMenu, MENU_HIDE_ON_SINGLE_TAB, "Hide Page Container when only one Tab",
                           "Hide Page Container when only one Tab", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnStyle, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_HIDE_TABS, "Hide Tabs",
                           "Hide Page Container allowing only keyboard navigation", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnStyle, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_NO_TABS_FOCUS, "No focus on notebook tabs",
                           "No focus on notebook tabs, only pages", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnStyle, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_HIDE_NAV_BUTTONS, "Hide Navigation Buttons",
                           "Hide Navigation Buttons", wx.ITEM_CHECK)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_HIDE_X, "Hide X Button", "Hide X Button", wx.ITEM_CHECK)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_SMART_TABS, "Smart tabbing", "Smart tabbing", wx.ITEM_CHECK)
        self._editMenu.Append(item)
        self.Bind(wx.EVT_MENU, self.OnSmartTabs, item)
        item.Check(False)

        item = wx.MenuItem(self._editMenu, MENU_USE_DROP_ARROW_BUTTON, "Use drop down button for tab navigation",
                           "Use drop down arrow for quick tab navigation", wx.ITEM_CHECK)
        self._editMenu.Append(item)
        self.Bind(wx.EVT_MENU, self.OnDropDownArrow, item)
        item.Check(False)
        self._editMenu.AppendSeparator()

        item = wx.MenuItem(self._editMenu, MENU_TILE_HORIZONTALLY, "Tile pages horizontally",
                           "Tile all the panels in an horizontal sizer", wx.ITEM_RADIO)
        self._editMenu.Append(item)
        self.Bind(wx.EVT_MENU, self.OnTile, item)

        item = wx.MenuItem(self._editMenu, MENU_TILE_VERTICALLY, "Tile pages vertically",
                           "Tile all the panels in a vertical sizer", wx.ITEM_RADIO)
        self._editMenu.Append(item)
        self.Bind(wx.EVT_MENU, self.OnTile, item)

        item = wx.MenuItem(self._editMenu, MENU_TILE_NONE, "No tiling",
                           "No tiling, standard FlatNotebook behaviour", wx.ITEM_RADIO)
        self._editMenu.Append(item)
        self.Bind(wx.EVT_MENU, self.OnTile, item)

        item.Check(True)

        self._editMenu.AppendSeparator()

        item = wx.MenuItem(self._editMenu, wx.ID_ANY, "Use custom page",
                           "Shows a custom page when the main notebook has no pages left", wx.ITEM_CHECK)
        self._editMenu.Append(item)
        self.Bind(wx.EVT_MENU, self.OnCustomPanel, item)

        self._editMenu.AppendSeparator()

        item = wx.MenuItem(self._editMenu, MENU_USE_MOUSE_MIDDLE_BTN, "Use Mouse Middle Button as 'X' button",
                           "Use Mouse Middle Button as 'X' button", wx.ITEM_CHECK)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_DCLICK_CLOSES_TAB, "Mouse double click closes tab",
                           "Mouse double click closes tab", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnDClickCloseTab, item)
        self._editMenu.Append(item)
        item.Check(False)

        self._editMenu.AppendSeparator()

        item = wx.MenuItem(self._editMenu, MENU_USE_BOTTOM_TABS, "Use Bottoms Tabs", "Use Bottoms Tabs",
                           wx.ITEM_CHECK)
        self._editMenu.Append(item)

        self.Bind(wx.EVT_MENU_RANGE, self.OnStyle, id=MENU_HIDE_X, id2=MENU_USE_BOTTOM_TABS)

        item = wx.MenuItem(self._editMenu, MENU_ENABLE_TAB, "Enable Tab", "Enable Tab")
        self.Bind(wx.EVT_MENU, self.OnEnableTab, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_DISABLE_TAB, "Disable Tab", "Disable Tab")
        self.Bind(wx.EVT_MENU, self.OnDisableTab, item)
        self._editMenu.Append(item)

        item = wx.MenuItem(self._editMenu, MENU_ENABLE_DRAG_N_DROP, "Enable Drag And Drop of Tabs",
                           "Enable Drag And Drop of Tabs", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableDrag, item)
        self._editMenu.Append(item)
        item.Check(False)

        item = wx.MenuItem(self._editMenu, MENU_ALLOW_FOREIGN_DND, "Enable Drag And Drop of Tabs from foreign notebooks",
                           "Enable Drag And Drop of Tabs from foreign notebooks", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnAllowForeignDnd, item)
        self._editMenu.Append(item)
        item.Check(False);

        item = wx.MenuItem(self._visualMenu, MENU_DRAW_BORDER, "Draw Border around tab area",
                           "Draw Border around tab area", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnStyle, item)
        self._visualMenu.Append(item)
        item.Check(True)

        item = wx.MenuItem(self._visualMenu, MENU_DRAW_TAB_X, "Draw X button On Active Tab",
                           "Draw X button On Active Tab", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnDrawTabX, item)
        self._visualMenu.Append(item)

        item = wx.MenuItem(self._visualMenu, MENU_SET_ACTIVE_TAB_COLOUR, "Select Active Tab Colour",
                           "Select Active Tab Colour")
        self.Bind(wx.EVT_MENU, self.OnSelectColour, item)
        self._visualMenu.Append(item)

        item = wx.MenuItem(self._visualMenu, MENU_SET_TAB_AREA_COLOUR, "Select Tab Area Colour",
                           "Select Tab Area Colour")
        self.Bind(wx.EVT_MENU, self.OnSelectColour, item)
        self._visualMenu.Append(item)

        item = wx.MenuItem(self._visualMenu, MENU_SET_ACTIVE_TEXT_COLOUR, "Select active tab text colour",
                           "Select active tab text colour")
        self.Bind(wx.EVT_MENU, self.OnSelectColour, item)
        self._visualMenu.Append(item)

        item = wx.MenuItem(self._visualMenu, MENU_SELECT_NONACTIVE_TEXT_COLOUR,
                           "Select NON-active tab text colour", "Select NON-active tab text colour")
        self.Bind(wx.EVT_MENU, self.OnSelectColour, item)
        self._visualMenu.Append(item)

        item = wx.MenuItem(self._visualMenu, MENU_GRADIENT_BACKGROUND, "Use Gradient Colouring for tab area",
                           "Use Gradient Colouring for tab area", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnGradientBack, item)
        self._visualMenu.Append(item)
        item.Check(False)

        item = wx.MenuItem(self._visualMenu, MENU_COLOURFUL_TABS, "Colourful tabs", "Colourful tabs", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnColourfulTabs, item)
        self._visualMenu.Append(item)
        item.Check(False)

        help_menu = wx.Menu()
        item = wx.MenuItem(help_menu, wx.ID_ANY, "About...", "Shows The About Dialog")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        help_menu.Append(item)

        self._menuBar.Append(self._fileMenu, "&File")
        self._menuBar.Append(self._editMenu, "&Edit")
        self._menuBar.Append(self._visualMenu, "&Tab Appearance")

        self._menuBar.Append(help_menu, "&Help")

        self.SetMenuBar(self._menuBar)


    def CreateRightClickMenu(self):

        self._rmenu = wx.Menu()
        item = wx.MenuItem(self._rmenu, MENU_EDIT_DELETE_PAGE, "Close Tab\tCtrl+F4", "Close Tab")
        self._rmenu.Append(item)


    def LayoutItems(self):

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        bookStyle = FNB.FNB_NODRAG

        self.book = FNB.FlatNotebook(self, wx.ID_ANY, agwStyle=bookStyle)

        bookStyle &= ~(FNB.FNB_NODRAG)
        bookStyle |= FNB.FNB_ALLOW_FOREIGN_DND
        self.secondBook = FNB.FlatNotebook(self, wx.ID_ANY, agwStyle=bookStyle)

        # Set right click menu to the notebook
        self.book.SetRightClickMenu(self._rmenu)

        # Set the image list
        self.book.SetImageList(self._ImageList)
        mainSizer.Add(self.book, 6, wx.EXPAND)

        # Add spacer between the books
        spacer = wx.Panel(self, -1)
        spacer.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        mainSizer.Add(spacer, 0, wx.ALL | wx.EXPAND)

        mainSizer.Add(self.secondBook, 2, wx.EXPAND)

        # Add some pages to the second notebook
        self.Freeze()

        text = wx.TextCtrl(self.secondBook, -1, "Second Book Page 1\n", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.secondBook.AddPage(text, "Second Book Page 1")

        text = wx.TextCtrl(self.secondBook, -1, "Second Book Page 2\n", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.secondBook.AddPage(text,  "Second Book Page 2")

        self.Thaw()

        mainSizer.Layout()
        self.SendSizeEvent()


    def OnStyle(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        eventid = event.GetId()

        if eventid == MENU_HIDE_NAV_BUTTONS:
            if event.IsChecked():
                # Hide the navigation buttons
                style |= FNB.FNB_NO_NAV_BUTTONS
            else:
                style &= ~FNB.FNB_NO_NAV_BUTTONS
                style &= ~FNB.FNB_DROPDOWN_TABS_LIST

            self.book.SetAGWWindowStyleFlag(style)

        elif eventid == MENU_HIDE_ON_SINGLE_TAB:
            if event.IsChecked():
                # Hide the navigation buttons
                style |= FNB.FNB_HIDE_ON_SINGLE_TAB
            else:
                style &= ~(FNB.FNB_HIDE_ON_SINGLE_TAB)

            self.book.SetAGWWindowStyleFlag(style)

        elif eventid == MENU_HIDE_TABS:
            if event.IsChecked():
                # Hide the tabs
                style |= FNB.FNB_HIDE_TABS
            else:
                style &= ~(FNB.FNB_HIDE_TABS)

            self.book.SetAGWWindowStyleFlag(style)

        elif eventid == MENU_HIDE_X:
            if event.IsChecked():
                # Hide the X button
                style |= FNB.FNB_NO_X_BUTTON
            else:
                if style & FNB.FNB_NO_X_BUTTON:
                    style ^= FNB.FNB_NO_X_BUTTON

            self.book.SetAGWWindowStyleFlag(style)

        elif eventid == MENU_DRAW_BORDER:
            if event.IsChecked():
                style |= FNB.FNB_TABS_BORDER_SIMPLE
            else:
                if style & FNB.FNB_TABS_BORDER_SIMPLE:
                    style ^= FNB.FNB_TABS_BORDER_SIMPLE

            self.book.SetAGWWindowStyleFlag(style)

        elif eventid == MENU_USE_MOUSE_MIDDLE_BTN:
            if event.IsChecked():
                style |= FNB.FNB_MOUSE_MIDDLE_CLOSES_TABS
            else:
                if style & FNB.FNB_MOUSE_MIDDLE_CLOSES_TABS:
                    style ^= FNB.FNB_MOUSE_MIDDLE_CLOSES_TABS

            self.book.SetAGWWindowStyleFlag(style)

        elif eventid == MENU_USE_BOTTOM_TABS:
            if event.IsChecked():
                style |= FNB.FNB_BOTTOM
            else:
                if style & FNB.FNB_BOTTOM:
                    style ^= FNB.FNB_BOTTOM

            self.book.SetAGWWindowStyleFlag(style)
            self.book.Refresh()

        elif eventid == MENU_NO_TABS_FOCUS:
            if event.IsChecked():
                # Hide the navigation buttons
                style |= FNB.FNB_NO_TAB_FOCUS
            else:
                style &= ~(FNB.FNB_NO_TAB_FOCUS)

            self.book.SetAGWWindowStyleFlag(style)


    def OnQuit(self, event):

        self.Destroy()


    def OnDeleteAll(self, event):

        self.book.DeleteAllPages()


    def OnShowImages(self, event):

        self._bShowImages = event.IsChecked()


    def OnForeignDrop(self, event):

        self.log.write('Foreign drop received\n')
        self.log.write('new NB: %s  ||  old NB: %s\n' % (event.GetNotebook(), event.GetOldNotebook()))
        self.log.write('new tab: %s  ||  old tab: %s\n' % (event.GetSelection(), event.GetOldSelection()))


    def OnDrop(self, event):

        self.log.write('Drop received - same notebook\n')
        self.log.write('new: %s old: %s\n' % (event.GetSelection(), event.GetOldSelection()))


    def OnFF2Style(self, event):

        style = self.book.GetAGWWindowStyleFlag()

        # remove old tabs style
        mirror = ~(FNB.FNB_VC71 | FNB.FNB_VC8 | FNB.FNB_FANCY_TABS | FNB.FNB_FF2 | FNB.FNB_RIBBON_TABS)
        style &= mirror

        style |= FNB.FNB_FF2

        self.book.SetAGWWindowStyleFlag(style)


    def OnVC71Style(self, event):

        style = self.book.GetAGWWindowStyleFlag()

        # remove old tabs style
        mirror = ~(FNB.FNB_VC71 | FNB.FNB_VC8 | FNB.FNB_FANCY_TABS | FNB.FNB_FF2 | FNB.FNB_RIBBON_TABS)
        style &= mirror

        style |= FNB.FNB_VC71

        self.book.SetAGWWindowStyleFlag(style)


    def OnVC8Style(self, event):

        style = self.book.GetAGWWindowStyleFlag()

        # remove old tabs style
        mirror = ~(FNB.FNB_VC71 | FNB.FNB_VC8 | FNB.FNB_FANCY_TABS | FNB.FNB_FF2 | FNB.FNB_RIBBON_TABS)
        style &= mirror

        # set new style
        style |= FNB.FNB_VC8

        self.book.SetAGWWindowStyleFlag(style)

    def OnRibbonStyle(self, event):

        style = self.book.GetAGWWindowStyleFlag()

        # remove old tabs style
        mirror = ~(FNB.FNB_VC71 | FNB.FNB_VC8 | FNB.FNB_FANCY_TABS | FNB.FNB_FF2 | FNB.FNB_RIBBON_TABS)
        style &= mirror

        # set new style
        style |= FNB.FNB_RIBBON_TABS

        self.book.SetAGWWindowStyleFlag(style)


    def OnDefaultStyle(self, event):

        style = self.book.GetAGWWindowStyleFlag()

        # remove old tabs style
        mirror = ~(FNB.FNB_VC71 | FNB.FNB_VC8 | FNB.FNB_FANCY_TABS | FNB.FNB_FF2 | FNB.FNB_RIBBON_TABS)
        style &= mirror

        self.book.SetAGWWindowStyleFlag(style)


    def OnFancyStyle(self, event):

        style = self.book.GetAGWWindowStyleFlag()

        # remove old tabs style
        mirror = ~(FNB.FNB_VC71 | FNB.FNB_VC8 | FNB.FNB_FANCY_TABS | FNB.FNB_FF2 | FNB.FNB_RIBBON_TABS)
        style &= mirror

        style |= FNB.FNB_FANCY_TABS
        self.book.SetAGWWindowStyleFlag(style)


    def OnSelectColour(self, event):

        eventid = event.GetId()

        # Open a colour dialog
        data = wx.ColourData()

        dlg = wx.ColourDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:

            if eventid == MENU_SELECT_GRADIENT_COLOUR_BORDER:
                self.book.SetGradientColourBorder(dlg.GetColourData().GetColour())
            elif eventid == MENU_SELECT_GRADIENT_COLOUR_FROM:
                self.book.SetGradientColourFrom(dlg.GetColourData().GetColour())
            elif eventid == MENU_SELECT_GRADIENT_COLOUR_TO:
                self.book.SetGradientColourTo(dlg.GetColourData().GetColour())
            elif eventid == MENU_SET_ACTIVE_TEXT_COLOUR:
                self.book.SetActiveTabTextColour(dlg.GetColourData().GetColour())
            elif eventid == MENU_SELECT_NONACTIVE_TEXT_COLOUR:
                self.book.SetNonActiveTabTextColour(dlg.GetColourData().GetColour())
            elif eventid == MENU_SET_ACTIVE_TAB_COLOUR:
                self.book.SetActiveTabColour(dlg.GetColourData().GetColour())
            elif eventid == MENU_SET_TAB_AREA_COLOUR:
                self.book.SetTabAreaColour(dlg.GetColourData().GetColour())

            self.book.Refresh()


    def OnAddPage(self, event):

        caption = "New Page Added #" + str(self._newPageCounter)

        self.Freeze()

        image = -1
        if self._bShowImages:
            image = random.randint(0, self._ImageList.GetImageCount()-1)

        self.book.AddPage(self.CreatePage(caption), caption, True, image)
        self.Thaw()
        self._newPageCounter = self._newPageCounter + 1


    def CreatePage(self, caption):

        p = wx.Panel(self.book, style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)
        wx.StaticText(p, -1, caption, (20,20))
        wx.TextCtrl(p, -1, "", (20,40), (150,-1))
        return p


    def OnDeletePage(self, event):

        self.book.DeletePage(self.book.GetSelection())


    def OnSetSelection(self, event):

        dlg = wx.TextEntryDialog(self, "Enter Tab Number to select:", "Set Selection")

        if dlg.ShowModal() == wx.ID_OK:

            val = dlg.GetValue()
            self.book.SetSelection(int(val))


    def OnEnableTab(self, event):

        dlg = wx.TextEntryDialog(self, "Enter Tab Number to enable:", "Enable Tab")

        if dlg.ShowModal() == wx.ID_OK:

            val = dlg.GetValue()
            self.book.EnableTab(int(val))


    def OnDisableTab(self, event):

        dlg = wx.TextEntryDialog(self, "Enter Tab Number to disable:", "Disable Tab")

        if dlg.ShowModal() == wx.ID_OK:

            val = dlg.GetValue()
            self.book.EnableTab(int(val), False)


    def OnEnableDrag(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        style2 = self.secondBook.GetAGWWindowStyleFlag()

        if event.IsChecked():
            if style & FNB.FNB_NODRAG:
                style ^= FNB.FNB_NODRAG
            if style2 & FNB.FNB_NODRAG:
                style2 ^= FNB.FNB_NODRAG
        else:
            style |= FNB.FNB_NODRAG
            style2 |= FNB.FNB_NODRAG

        self.book.SetAGWWindowStyleFlag(style)
        self.secondBook.SetAGWWindowStyleFlag(style2)


    def OnAllowForeignDnd(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        if event.IsChecked():
            style |= FNB.FNB_ALLOW_FOREIGN_DND
        else:
            style &= ~(FNB.FNB_ALLOW_FOREIGN_DND)

        self.book.SetAGWWindowStyleFlag(style)
        self.book.Refresh()


    def OnSetAllPagesShapeAngle(self, event):


        dlg = wx.TextEntryDialog(self, "Enter an inclination of header borders (0-15):", "Set Angle")
        if dlg.ShowModal() == wx.ID_OK:

            val = dlg.GetValue()
            self.book.SetAllPagesShapeAngle(int(val))


    def OnSetPageImage(self, event):

        dlg = wx.TextEntryDialog(self, "Enter an image index (0-%i):"%(self.book.GetImageList().GetImageCount()-1), "Set Image Index")
        if dlg.ShowModal() == wx.ID_OK:
            val = dlg.GetValue()
            self.book.SetPageImage(self.book.GetSelection(), int(val))


    def OnAdvanceSelectionFwd(self, event):

        self.book.AdvanceSelection(True)


    def OnAdvanceSelectionBack(self, event):

        self.book.AdvanceSelection(False)


    def OnPageChanging(self, event):

        self.log.write("Page Changing From %d To %d" % (event.GetOldSelection(), event.GetSelection()))
        event.Skip()


    def OnPageChanged(self, event):

        self.log.write("Page Changed To %d" % event.GetSelection())
        event.Skip()


    def OnPageClosing(self, event):

        self.log.write("Page Closing, Selection: %d" % event.GetSelection())
        event.Skip()


    def OnDrawTabX(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        if event.IsChecked():
            style |= FNB.FNB_X_ON_TAB
        else:
            if style & FNB.FNB_X_ON_TAB:
                style ^= FNB.FNB_X_ON_TAB

        self.book.SetAGWWindowStyleFlag(style)


    def OnDClickCloseTab(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        if event.IsChecked():
            style |= FNB.FNB_DCLICK_CLOSES_TABS
        else:
            style &= ~(FNB.FNB_DCLICK_CLOSES_TABS)

        self.book.SetAGWWindowStyleFlag(style)


    def OnGradientBack(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        if event.IsChecked():
            style |= FNB.FNB_BACKGROUND_GRADIENT
        else:
            style &= ~(FNB.FNB_BACKGROUND_GRADIENT)

        self.book.SetAGWWindowStyleFlag(style)
        self.book.Refresh()


    def OnColourfulTabs(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        if event.IsChecked():
            style |= FNB.FNB_COLOURFUL_TABS
        else:
            style &= ~(FNB.FNB_COLOURFUL_TABS)

        self.book.SetAGWWindowStyleFlag(style)
        self.book.Refresh()


    def OnSmartTabs(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        if event.IsChecked():
            style |= FNB.FNB_SMART_TABS
        else:
            style &= ~FNB.FNB_SMART_TABS

        self.book.SetAGWWindowStyleFlag(style)
        self.book.Refresh()


    def OnDropDownArrow(self, event):

        style = self.book.GetAGWWindowStyleFlag()

        if event.IsChecked():

            style |= FNB.FNB_DROPDOWN_TABS_LIST
            style |= FNB.FNB_NO_NAV_BUTTONS

        else:

            style &= ~FNB.FNB_DROPDOWN_TABS_LIST
            style &= ~FNB.FNB_NO_NAV_BUTTONS

        self.book.SetAGWWindowStyleFlag(style)
        self.book.Refresh()


    def OnTile(self, event):

        evId = event.GetId()
        if evId == MENU_TILE_HORIZONTALLY:
            self.book.Tile(wx.HORIZONTAL)
        elif evId == MENU_TILE_VERTICALLY:
            self.book.Tile(wx.VERTICAL)
        else:
            self.book.Tile(None)


    def OnCustomPanel(self, event):

        if event.IsChecked():
            custom = LogoPanel(self.book, -1)
            self.book.SetCustomPage(custom)
        else:
            self.book.SetCustomPage(None)


    def OnHideNavigationButtonsUI(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        event.Check((style & FNB.FNB_NO_NAV_BUTTONS and [True] or [False])[0])


    def OnDropDownArrowUI(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        event.Check((style & FNB.FNB_DROPDOWN_TABS_LIST and [True] or [False])[0])


    def OnAllowForeignDndUI(self, event):

        style = self.book.GetAGWWindowStyleFlag()
        event.Enable((style & FNB.FNB_NODRAG and [False] or [True])[0])


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The FlatNotebook Demo.\n\n" + \
            "Author: Andrea Gavana @ 02 Oct 2006\n\n" + \
            "Please Report Any Bug/Requests Of Improvements\n" + \
            "To Me At The Following Addresses:\n\n" + \
            "andrea.gavana@gmail.com\n" + "andrea.gavana@maerskoil.com\n\n" + \
            "Based On Eran C++ Implementation (wxWidgets Forum).\n\n" + \
            "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "FlatNotebook wxPython Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class LogoPanel(wx.Panel):

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.CLIP_CHILDREN):

        wx.Panel.__init__(self, parent, id, pos, size, style)

        self.SetBackgroundColour(wx.WHITE)
        self.bmp = images.Vippi.GetBitmap()

        self.bigfont = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
        self.normalfont = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSize(self, event):

        event.Skip()
        self.Refresh()


    def OnPaint(self, event):

        dc = wx.AutoBufferedPaintDC(self)
        self.DoDrawing(dc)


    def DoDrawing(self, dc):

        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()

        w, h = self.GetClientSize()
        bmpW, bmpH = self.bmp.GetWidth(), self.bmp.GetHeight()

        xpos, ypos = int((w - bmpW)/2), int((h - bmpH)/2)

        dc.DrawBitmap(self.bmp, xpos, ypos, True)

        dc.SetFont(self.bigfont)
        dc.SetTextForeground(wx.BLUE)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(wx.BLUE, 2))

        tw, th = dc.GetTextExtent("FlatNotebook")
        xpos = int((w - tw)/2)
        ypos = int(h/3)

        dc.DrawRoundedRectangle(xpos-5, ypos-3, tw+10, th+6, 3)
        dc.DrawText("FlatNotebook", xpos, ypos)

        dc.SetFont(self.normalfont)
        dc.SetTextForeground(wx.RED)
        tw, th = dc.GetTextExtent("Andrea Gavana")
        xpos = int((w - tw)/2)
        ypos = int(2*h/3)
        dc.DrawText("Andrea Gavana", xpos, ypos)
        tw, th = dc.GetTextExtent("02 Oct 2006")

        xpos = int((w - tw)/2)
        ypos = int(2*h/3 + 3*th/2)

        dc.DrawText("02 Oct 2006", xpos, ypos)


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test FlatNotebook ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = FlatNotebookDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = FNB.__doc__



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

