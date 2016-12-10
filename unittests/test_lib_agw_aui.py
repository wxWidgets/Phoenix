import unittest
from unittests import wtc
import wx
import os

import wx.lib.agw.aui as aui

#---------------------------------------------------------------------------

class lib_agw_aui_Tests(wtc.WidgetTestCase):

    def test_lib_agw_auiCtor(self):
        self._mgr = aui.AuiManager()

        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self.frame)

        pane = wx.Panel()
        self._mgr.AddPane(pane, aui.AuiPaneInfo().Name("pane1").Caption("A pane")
                          .CenterPane())
        pane = wx.Panel()
        self._mgr.AddPane(pane, aui.AuiPaneInfo().Name("pane2").Caption("A pane")
                          .Top())
        pane = wx.Panel()
        self._mgr.AddPane(pane, aui.AuiPaneInfo().Name("pane3").Caption("A pane")
                          .Left())
        pane = wx.Panel()
        self._mgr.AddPane(pane, aui.AuiPaneInfo().Name("pane4").Caption("A pane")
                          .Bottom())
        self._mgr.Update()

    def tearDown(self):
        self._mgr.UnInit()


class lib_agw_aui_additional_Tests(wtc.WidgetTestCase):

    def test_lib_agw_aui_ToolbarCtor(self):
        tb = aui.AuiToolBar(self.frame, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_VERT_TEXT)
        tb_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))
        tb.AddSimpleTool(-1, "Test", tb_bmp1)
        tb.AddSimpleTool(-1, "Check 1", tb_bmp1, "Check 1", aui.ITEM_CHECK)
        tb.AddSimpleTool(-1, "Radio 1", tb_bmp1, "Radio 1", aui.ITEM_RADIO)
        tb.AddSeparator()

        # prepare a few custom overflow elements for the toolbars' overflow buttons

        prepend_items, append_items = [], []
        item = aui.AuiToolBarItem()

        item.SetKind(wx.ITEM_SEPARATOR)
        append_items.append(item)

        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_NORMAL)
        item.SetId(-1)
        item.SetLabel("Customize...")
        append_items.append(item)
        tb.SetCustomOverflowItems(prepend_items, append_items)
        tb.Realize()


    def test_lib_agw_auiEvents(self):
        aui.EVT_AUI_PANE_BUTTON
        """ Fires an event when the user left-clicks on a pane button. """
        aui.EVT_AUI_PANE_CLOSE
        """ A pane in `AuiManager` has been closed. """
        aui.EVT_AUI_PANE_MAXIMIZE
        """ A pane in `AuiManager` has been maximized. """
        aui.EVT_AUI_PANE_RESTORE
        """ A pane in `AuiManager` has been restored from a maximized state. """
        aui.EVT_AUI_RENDER
        """ Fires an event every time the AUI frame is being repainted. """
        aui.EVT_AUI_FIND_MANAGER
        """ Used to find which AUI manager is controlling a certain pane. """
        aui.EVT_AUI_PANE_MINIMIZE
        """ A pane in `AuiManager` has been minimized. """
        aui.EVT_AUI_PANE_MIN_RESTORE
        """ A pane in `AuiManager` has been restored from a minimized state. """
        aui.EVT_AUI_PANE_FLOATING
        """ A pane in `AuiManager` is about to be floated. """
        aui.EVT_AUI_PANE_FLOATED
        """ A pane in `AuiManager` has been floated. """
        aui.EVT_AUI_PANE_DOCKING
        """ A pane in `AuiManager` is about to be docked. """
        aui.EVT_AUI_PANE_DOCKED
        """ A pane in `AuiManager` has been docked. """
        aui.EVT_AUI_PANE_ACTIVATED
        """ A pane in `AuiManager` has been activated. """
        aui.EVT_AUI_PERSPECTIVE_CHANGED
        """ The layout in `AuiManager` has been changed. """

    def test_lib_agw_auiConstantsExist(self):

        # For auibook
        # -----------
        aui.AuiBaseTabCtrlId
        """ Base window identifier for AuiTabCtrl. """

        aui.AUI_NB_TOP
        """ With this style, tabs are drawn along the top of the notebook. """
        aui.AUI_NB_LEFT
        """ With this style, tabs are drawn along the left of the notebook.
        Not implemented yet. """
        aui.AUI_NB_RIGHT
        """ With this style, tabs are drawn along the right of the notebook.
        Not implemented yet. """
        aui.AUI_NB_BOTTOM
        """ With this style, tabs are drawn along the bottom of the notebook. """
        aui.AUI_NB_TAB_SPLIT
        """ Allows the tab control to be split by dragging a tab. """
        aui.AUI_NB_TAB_MOVE
        """ Allows a tab to be moved horizontally by dragging. """
        aui.AUI_NB_TAB_EXTERNAL_MOVE
        """ Allows a tab to be moved to another tab control. """
        aui.AUI_NB_TAB_FIXED_WIDTH
        """ With this style, all tabs have the same width. """
        aui.AUI_NB_SCROLL_BUTTONS
        """ With this style, left and right scroll buttons are displayed. """
        aui.AUI_NB_WINDOWLIST_BUTTON
        """ With this style, a drop-down list of windows is available. """
        aui.AUI_NB_CLOSE_BUTTON
        """ With this style, a close button is available on the tab bar. """
        aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
        """ With this style, a close button is available on the active tab. """
        aui.AUI_NB_CLOSE_ON_ALL_TABS
        """ With this style, a close button is available on all tabs. """
        aui.AUI_NB_MIDDLE_CLICK_CLOSE
        """ Allows to close `AuiNotebook` tabs by mouse middle button click. """
        aui.AUI_NB_SUB_NOTEBOOK
        """ This style is used by `AuiManager` to create automatic `AuiNotebooks`. """
        aui.AUI_NB_HIDE_ON_SINGLE_TAB
        """ Hides the tab window if only one tab is present. """
        aui.AUI_NB_SMART_TABS
        """ Use `Smart Tabbing`, like ``Alt`` + ``Tab`` on Windows. """
        aui.AUI_NB_USE_IMAGES_DROPDOWN
        """ Uses images on dropdown window list menu instead of check items. """
        aui.AUI_NB_CLOSE_ON_TAB_LEFT
        """ Draws the tab close button on the left instead of on the right
        (a la Camino browser). """
        aui.AUI_NB_TAB_FLOAT
        """ Allows the floating of single tabs.
        Known limitation: when the notebook is more or less full screen, tabs
        cannot be dragged far enough outside of the notebook to become
        floating pages. """
        aui.AUI_NB_DRAW_DND_TAB
        """ Draws an image representation of a tab while dragging. """
        aui.AUI_NB_ORDER_BY_ACCESS
        """ Tab navigation order by last access time. """
        aui.AUI_NB_NO_TAB_FOCUS
        """ Don't draw tab focus rectangle. """

        aui.AUI_NB_DEFAULT_STYLE
        """ Default `AuiNotebook` style. """

        # -------------------------- #
        # - FrameManager Constants - #
        # -------------------------- #

        # Docking Styles
        aui.AUI_DOCK_NONE
        """ No docking direction. """
        aui.AUI_DOCK_TOP
        """ Top docking direction. """
        aui.AUI_DOCK_RIGHT
        """ Right docking direction. """
        aui.AUI_DOCK_BOTTOM
        """ Bottom docking direction. """
        aui.AUI_DOCK_LEFT
        """ Left docking direction. """
        aui.AUI_DOCK_CENTER
        """ Center docking direction. """
        aui.AUI_DOCK_CENTRE
        """ Centre docking direction. """
        aui.AUI_DOCK_NOTEBOOK_PAGE
        """ Automatic AuiNotebooks docking style. """

        # Floating/Dragging Styles
        aui.AUI_MGR_ALLOW_FLOATING
        """ Allow floating of panes. """
        aui.AUI_MGR_ALLOW_ACTIVE_PANE
        """ If a pane becomes active, "highlight" it in the interface. """
        aui.AUI_MGR_TRANSPARENT_DRAG
        """ If the platform supports it, set transparency on a floating pane
        while it is dragged by the user. """
        aui.AUI_MGR_TRANSPARENT_HINT
        """ If the platform supports it, show a transparent hint window when
        the user is about to dock a floating pane. """
        aui.AUI_MGR_VENETIAN_BLINDS_HINT
        """ Show a "venetian blind" effect when the user is about to dock a
        floating pane. """
        aui.AUI_MGR_RECTANGLE_HINT
        """ Show a rectangle hint effect when the user is about to dock a
        floating pane. """
        aui.AUI_MGR_HINT_FADE
        """ If the platform supports it, the hint window will fade in and out. """
        aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        """ Disables the "venetian blind" fade in and out. """
        aui.AUI_MGR_LIVE_RESIZE
        """ Live resize when the user drag a sash. """
        aui.AUI_MGR_ANIMATE_FRAMES
        """ Fade-out floating panes when they are closed (all platforms which support
        frames transparency) and show a moving rectangle when they are docked
        (Windows < Vista and GTK only). """
        aui.AUI_MGR_AERO_DOCKING_GUIDES
        """ Use the new Aero-style bitmaps as docking guides. """
        aui.AUI_MGR_PREVIEW_MINIMIZED_PANES
        """ Slide in and out minimized panes to preview them. """
        aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES
        """ Use the new Whidbey-style bitmaps as docking guides. """
        aui.AUI_MGR_SMOOTH_DOCKING
        """ Performs a "smooth" docking of panes (a la PyQT). """
        aui.AUI_MGR_USE_NATIVE_MINIFRAMES
        """ Use miniframes with native caption bar as floating panes instead or custom
        drawn caption bars (forced on wxMac). """
        aui.AUI_MGR_AUTONB_NO_CAPTION
        """ Panes that merge into an automatic notebook will not have the pane
        caption visible. """


        aui.AUI_MGR_DEFAULT
        """ Default `AuiManager` style. """

        # Panes Customization
        aui.AUI_DOCKART_SASH_SIZE
        """ Customizes the sash size. """
        aui.AUI_DOCKART_CAPTION_SIZE
        """ Customizes the caption size. """
        aui.AUI_DOCKART_GRIPPER_SIZE
        """ Customizes the gripper size. """
        aui.AUI_DOCKART_PANE_BORDER_SIZE
        """ Customizes the pane border size. """
        aui.AUI_DOCKART_PANE_BUTTON_SIZE
        """ Customizes the pane button size. """
        aui.AUI_DOCKART_BACKGROUND_COLOUR
        """ Customizes the background colour. """
        aui.AUI_DOCKART_BACKGROUND_GRADIENT_COLOUR
        """ Customizes the background gradient colour. """
        aui.AUI_DOCKART_SASH_COLOUR
        """ Customizes the sash colour. """
        aui.AUI_DOCKART_ACTIVE_CAPTION_COLOUR
        """ Customizes the active caption colour. """
        aui.AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR
        """ Customizes the active caption gradient colour. """
        aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR
        """ Customizes the inactive caption colour. """
        aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR
        """ Customizes the inactive gradient caption colour. """
        aui.AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR
        """ Customizes the active caption text colour. """
        aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR
        """ Customizes the inactive caption text colour. """
        aui.AUI_DOCKART_BORDER_COLOUR
        """ Customizes the border colour. """
        aui.AUI_DOCKART_GRIPPER_COLOUR
        """ Customizes the gripper colour. """
        aui.AUI_DOCKART_CAPTION_FONT
        """ Customizes the caption font. """
        aui.AUI_DOCKART_GRADIENT_TYPE
        """ Customizes the gradient type (no gradient, vertical or horizontal). """
        aui.AUI_DOCKART_DRAW_SASH_GRIP
        """ Draw a sash grip on the sash. """
        aui.AUI_DOCKART_HINT_WINDOW_COLOUR
        """ Customizes the hint window background colour (currently light blue). """

        # Caption Gradient Type
        aui.AUI_GRADIENT_NONE
        """ No gradient on the captions. """
        aui.AUI_GRADIENT_VERTICAL

        """ Vertical gradient on the captions. """
        aui.AUI_GRADIENT_HORIZONTAL
        """ Horizontal gradient on the captions. """

        # Pane Button State
        aui.AUI_BUTTON_STATE_NORMAL
        """ Normal button state. """
        aui.AUI_BUTTON_STATE_HOVER
        """ Hovered button state. """
        aui.AUI_BUTTON_STATE_PRESSED
        """ Pressed button state. """
        aui.AUI_BUTTON_STATE_DISABLED
        """ Disabled button state. """
        aui.AUI_BUTTON_STATE_HIDDEN
        """ Hidden button state. """
        aui.AUI_BUTTON_STATE_CHECKED
        """ Checked button state. """

        # Pane minimize mode
        aui.AUI_MINIMIZE_POS_SMART
        """ Minimizes the pane on the closest tool bar. """
        aui.AUI_MINIMIZE_POS_TOP
        """ Minimizes the pane on the top tool bar. """
        aui.AUI_MINIMIZE_POS_LEFT
        """ Minimizes the pane on its left tool bar. """
        aui.AUI_MINIMIZE_POS_RIGHT
        """ Minimizes the pane on its right tool bar. """
        aui.AUI_MINIMIZE_POS_BOTTOM
        """ Minimizes the pane on its bottom tool bar. """
        aui.AUI_MINIMIZE_POS_TOOLBAR
        """ Minimizes the pane on its bottom tool bar. """
        aui.AUI_MINIMIZE_POS_MASK
        """ Mask to filter the position flags. """
        aui.AUI_MINIMIZE_CAPT_HIDE
        """ Hides the caption of the minimized pane. """
        aui.AUI_MINIMIZE_CAPT_SMART
        """ Displays the caption in the best rotation (horz or clockwise). """
        aui.AUI_MINIMIZE_CAPT_HORZ
        """ Displays the caption horizontally. """
        aui.AUI_MINIMIZE_CAPT_MASK
        """ Mask to filter the caption flags. """

        # Button kind
        aui.AUI_BUTTON_CLOSE
        """ Shows a close button on the pane. """
        aui.AUI_BUTTON_MAXIMIZE_RESTORE
        """ Shows a maximize/restore button on the pane. """
        aui.AUI_BUTTON_MINIMIZE
        """ Shows a minimize button on the pane. """
        aui.AUI_BUTTON_PIN
        """ Shows a pin button on the pane. """
        aui.AUI_BUTTON_OPTIONS
        """ Shows an option button on the pane (not implemented). """
        aui.AUI_BUTTON_WINDOWLIST
        """ Shows a window list button on the pane (for AuiNotebook). """
        aui.AUI_BUTTON_LEFT
        """ Shows a left button on the pane (for AuiNotebook). """
        aui.AUI_BUTTON_RIGHT
        """ Shows a right button on the pane (for AuiNotebook). """
        aui.AUI_BUTTON_UP
        """ Shows an up button on the pane (not implemented). """
        aui.AUI_BUTTON_DOWN
        """ Shows a down button on the pane (not implemented). """
        aui.AUI_BUTTON_CUSTOM1
        """ Shows a custom button on the pane. """
        aui.AUI_BUTTON_CUSTOM2
        """ Shows a custom button on the pane. """
        aui.AUI_BUTTON_CUSTOM3
        """ Shows a custom button on the pane. """
        aui.AUI_BUTTON_CUSTOM4
        """ Shows a custom button on the pane. """
        aui.AUI_BUTTON_CUSTOM5
        """ Shows a custom button on the pane. """
        aui.AUI_BUTTON_CUSTOM6
        """ Shows a custom button on the pane. """
        aui.AUI_BUTTON_CUSTOM7
        """ Shows a custom button on the pane. """
        aui.AUI_BUTTON_CUSTOM8
        """ Shows a custom button on the pane. """
        aui.AUI_BUTTON_CUSTOM9
        """ Shows a custom button on the pane. """

        # Pane Insert Level
        aui.AUI_INSERT_PANE
        """ Level for inserting a pane. """
        aui.AUI_INSERT_ROW
        """ Level for inserting a row. """
        aui.AUI_INSERT_DOCK
        """ Level for inserting a dock. """

        # ------------------------ #
        # - AuiToolBar Constants - #
        # ------------------------ #

        aui.ITEM_CONTROL
        """ The item in the AuiToolBar is a control. """
        aui.ITEM_LABEL
        """ The item in the AuiToolBar is a text label. """
        aui.ITEM_SPACER
        """ The item in the AuiToolBar is a spacer. """
        aui.ITEM_SEPARATOR
        """ The item in the AuiToolBar is a separator. """
        aui.ITEM_CHECK
        """ The item in the AuiToolBar is a toolbar check item. """
        aui.ITEM_NORMAL
        """ The item in the AuiToolBar is a standard toolbar item. """
        aui.ITEM_RADIO
        """ The item in the AuiToolBar is a toolbar radio item. """
        aui.ID_RESTORE_FRAME
        """ Identifier for restoring a minimized pane. """

        aui.BUTTON_DROPDOWN_WIDTH
        """ Width of the drop-down button in AuiToolBar. """

        aui.DISABLED_TEXT_GREY_HUE
        """ Hue text colour for the disabled text in AuiToolBar. """
        aui.DISABLED_TEXT_COLOUR
        """ Text colour for the disabled text in AuiToolBar. """

        aui.AUI_TB_TEXT
        """ Shows the text in the toolbar buttons; by default only icons are shown. """
        aui.AUI_TB_NO_TOOLTIPS
        """ Don't show tooltips on `AuiToolBar` items. """
        aui.AUI_TB_NO_AUTORESIZE
        """ Do not auto-resize the `AuiToolBar`. """
        aui.AUI_TB_GRIPPER
        """ Shows a gripper on the `AuiToolBar`. """
        aui.AUI_TB_OVERFLOW
        """ The `AuiToolBar` can contain overflow items. """
        aui.AUI_TB_VERTICAL
        """ The `AuiToolBar` is vertical. """
        aui.AUI_TB_HORZ_LAYOUT
        """ Shows the text and the icons alongside, not vertically stacked.
        This style must be used with ``AUI_TB_TEXT``. """
        aui.AUI_TB_PLAIN_BACKGROUND
        """ Don't draw a gradient background on the toolbar. """
        aui.AUI_TB_CLOCKWISE
        aui.AUI_TB_COUNTERCLOCKWISE

        aui.AUI_TB_HORZ_TEXT
        """ Combination of ``AUI_TB_HORZ_LAYOUT`` and ``AUI_TB_TEXT``. """
        aui.AUI_TB_VERT_TEXT

        aui.AUI_TB_DEFAULT_STYLE
        """ `AuiToolBar` default style. """

        # AuiToolBar settings
        aui.AUI_TBART_SEPARATOR_SIZE
        """ Separator size in AuiToolBar. """
        aui.AUI_TBART_GRIPPER_SIZE
        """ Gripper size in AuiToolBar. """
        aui.AUI_TBART_OVERFLOW_SIZE
        """ Overflow button size in AuiToolBar. """

        # AuiToolBar text orientation
        aui.AUI_TBTOOL_TEXT_LEFT
        """ Text in AuiToolBar items is aligned left. """
        aui.AUI_TBTOOL_TEXT_RIGHT
        """ Text in AuiToolBar items is aligned right. """
        aui.AUI_TBTOOL_TEXT_TOP
        """ Text in AuiToolBar items is aligned top. """
        aui.AUI_TBTOOL_TEXT_BOTTOM
        """ Text in AuiToolBar items is aligned bottom. """

        # AuiToolBar tool orientation
        aui.AUI_TBTOOL_HORIZONTAL
        aui.AUI_TBTOOL_VERT_CLOCKWISE
        aui.AUI_TBTOOL_VERT_COUNTERCLOCKWISE

        # ------------------------------- #
        # - AuiSwitcherDialog Constants - #
        # ------------------------------- #

        aui.SWITCHER_TEXT_MARGIN_X
        aui.SWITCHER_TEXT_MARGIN_Y


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
