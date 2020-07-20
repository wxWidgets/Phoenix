#!/usr/bin/env python

import wx
import math
import random
import os

import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

try:
    from agw import flatmenu as FM
    from agw.artmanager import ArtManager, RendererBase, DCSaver
    from agw.fmresources import ControlFocus, ControlPressed
    from agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.flatmenu as FM
    from wx.lib.agw.artmanager import ArtManager, RendererBase, DCSaver
    from wx.lib.agw.fmresources import ControlFocus, ControlPressed
    from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR

import images

if wx.VERSION >= (2,7,0,0):
    import wx.lib.agw.aui as AUI
    AuiPaneInfo = AUI.AuiPaneInfo
    AuiManager = AUI.AuiManager
    _hasAUI = True
else:
    try:
        import PyAUI as AUI
        _hasAUI = True
        AuiPaneInfo = AUI.PaneInfo
        AuiManager = AUI.FrameManager
    except:
        _hasAUI = False

#----------------------------------------------------------------------

#-------------------------------
# Menu items IDs
#-------------------------------

MENU_STYLE_DEFAULT = wx.NewIdRef()
MENU_STYLE_XP = wx.NewIdRef()
MENU_STYLE_2007 = wx.NewIdRef()
MENU_STYLE_VISTA = wx.NewIdRef()
MENU_STYLE_MY = wx.NewIdRef()
MENU_USE_CUSTOM = wx.NewIdRef()
MENU_LCD_MONITOR = wx.NewIdRef()
MENU_HELP = wx.NewIdRef()

MENU_DISABLE_MENU_ITEM = wx.NewIdRef()
MENU_REMOVE_MENU = wx.NewIdRef()
MENU_TRANSPARENCY = wx.NewIdRef()

MENU_NEW_FILE = 10005
MENU_SAVE = 10006
MENU_OPEN_FILE = 10007
MENU_NEW_FOLDER = 10008
MENU_COPY = 10009
MENU_CUT = 10010
MENU_PASTE = 10011


def switchRGBtoBGR(colour):

    return wx.Colour(colour.Blue(), colour.Green(), colour.Red())


def CreateBackgroundBitmap():

    mem_dc = wx.MemoryDC()
    bmp = wx.Bitmap(200, 300)
    mem_dc.SelectObject(bmp)

    mem_dc.Clear()

    # colour the menu face with background colour
    top = wx.BLUE
    bottom = wx.Colour("light blue")
    filRect = wx.Rect(0, 0, 200, 300)
    mem_dc.GradientFillConcentric(filRect, top, bottom, wx.Point(100, 150))

    mem_dc.SelectObject(wx.NullBitmap)
    return bmp

#------------------------------------------------------------
# A custom renderer class for FlatMenu
#------------------------------------------------------------

class FM_MyRenderer(FM.FMRenderer):
    """ My custom style. """

    def __init__(self):

        FM.FMRenderer.__init__(self)


    def DrawMenuButton(self, dc, rect, state):
        """Draws the highlight on a FlatMenu"""

        self.DrawButton(dc, rect, state)


    def DrawMenuBarButton(self, dc, rect, state):
        """Draws the highlight on a FlatMenuBar"""

        self.DrawButton(dc, rect, state)


    def DrawButton(self, dc, rect, state, colour=None):

        if state == ControlFocus:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())
        elif state == ControlPressed:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().HighlightBackgroundColour())
        else:   # ControlNormal, ControlDisabled, default
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())

        # Draw the button borders
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRoundedRectangle(rect.x, rect.y, rect.width, rect.height,4)


    def DrawMenuBarBackground(self, dc, rect):

        # For office style, we simple draw a rectangle with a gradient colouring
        vertical = ArtManager.Get().GetMBVerticalGradient()

        dcsaver = DCSaver(dc)

        # fill with gradient
        startColour = self.menuBarFaceColour
        endColour   = ArtManager.Get().LightColour(startColour, 90)

        dc.SetPen(wx.Pen(endColour))
        dc.SetBrush(wx.Brush(endColour))
        dc.DrawRectangle(rect)


    def DrawToolBarBg(self, dc, rect):

        if not ArtManager.Get().GetRaiseToolbar():
            return

        # fill with gradient
        startColour = self.menuBarFaceColour()
        dc.SetPen(wx.Pen(startColour))
        dc.SetBrush(wx.Brush(startColour))
        dc.DrawRectangle(0, 0, rect.GetWidth(), rect.GetHeight())


#------------------------------------------------------------
# Declare our main frame
#------------------------------------------------------------

class FlatMenuDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent, size=(700, 500), style=wx.DEFAULT_FRAME_STYLE |
                          wx.NO_FULL_REPAINT_ON_RESIZE)

        self.SetIcon(images.Mondrian.GetIcon())
        wx.SystemOptions.SetOption("msw.remap", "0")
        self.SetTitle("FlatMenu wxPython Demo ;-D")

        if _hasAUI:
            self._mgr = AuiManager()
            self._mgr.SetManagedWindow(self)

        self._popUpMenu = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Create a main panel and place some controls on it
        mainPanel = wx.Panel(self, wx.ID_ANY)

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        mainPanel.SetSizer(panelSizer)

        # Create minibar Preview Panel
        minibarPanel= wx.Panel(self, wx.ID_ANY)
        self.CreateMinibar(minibarPanel)
        miniSizer = wx.BoxSizer(wx.VERTICAL)
        miniSizer.Add(self._mtb, 0, wx.EXPAND)
        minibarPanel.SetSizer(miniSizer)

        # Add log window
        self.log = log

        hs = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(mainPanel, wx.ID_ANY, "Press me for pop up menu!")
        hs.Add(btn, 0, wx.ALL, 5)

        # Connect a button
        btn.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

        btn = wx.Button(mainPanel, wx.ID_ANY, "Press me for a long menu!")
        hs.Add(btn, 0, wx.ALL, 5)

        panelSizer.Add(hs, 0, wx.ALL, 5)

        # Connect a button
        btn.Bind(wx.EVT_BUTTON, self.OnLongButtonClicked)

        statusbar = self.CreateStatusBar(2)
        statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("FlatMenu wxPython Demo, Andrea Gavana @ 01 Nov 2006"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)

        self.CreateMenu()
        self.ConnectEvents()

        mainSizer.Add(self._mb, 0, wx.EXPAND)
        mainSizer.Add(mainPanel, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        mainSizer.Layout()

        if _hasAUI:
            # AUI support
            self._mgr.AddPane(mainPanel, AuiPaneInfo().Name("main_panel").
                              CenterPane())

            self._mgr.AddPane(minibarPanel, AuiPaneInfo().Name("minibar_panel").
                              Caption("Minibar Preview").Right().
                              MinSize(wx.Size(150, 200)))

            self._mb.PositionAUI(self._mgr)
            self._mgr.Update()

        ArtManager.Get().SetMBVerticalGradient(True)
        ArtManager.Get().SetRaiseToolbar(False)

        self._mb.Refresh()
        self._mtb.Refresh()

        self.CenterOnScreen()


    def CreateMinibar(self, parent):
        # create mini toolbar
        self._mtb = FM.FlatMenuBar(parent, wx.ID_ANY, 16, 6, options = FM_OPT_SHOW_TOOLBAR|FM_OPT_MINIBAR)

        checkCancelBmp = wx.Bitmap(os.path.join(bitmapDir, "ok-16.png"), wx.BITMAP_TYPE_PNG)
        viewMagBmp = wx.Bitmap(os.path.join(bitmapDir, "viewmag-16.png"), wx.BITMAP_TYPE_PNG)
        viewMagFitBmp = wx.Bitmap(os.path.join(bitmapDir, "viewmagfit-16.png"), wx.BITMAP_TYPE_PNG)
        viewMagZoomBmp = wx.Bitmap(os.path.join(bitmapDir, "viewmag-p-16.png"), wx.BITMAP_TYPE_PNG)
        viewMagZoomOutBmp = wx.Bitmap(os.path.join(bitmapDir, "viewmag-m-16.png"), wx.BITMAP_TYPE_PNG)

        self._mtb.AddCheckTool(wx.ID_ANY, "Check Settings Item", checkCancelBmp)
        self._mtb.AddCheckTool(wx.ID_ANY, "Check Info Item", checkCancelBmp)
        self._mtb.AddSeparator()
        self._mtb.AddRadioTool(wx.ID_ANY, "Magnifier", viewMagBmp)
        self._mtb.AddRadioTool(wx.ID_ANY, "Fit", viewMagFitBmp)
        self._mtb.AddRadioTool(wx.ID_ANY, "Zoom In", viewMagZoomBmp)
        self._mtb.AddRadioTool(wx.ID_ANY, "Zoom Out", viewMagZoomOutBmp)


    def CreateMenu(self):

        # Create the menubar
        self._mb = FM.FlatMenuBar(self, wx.ID_ANY, 32, 5, options = FM_OPT_SHOW_TOOLBAR | FM_OPT_SHOW_CUSTOMIZE)

        fileMenu  = FM.FlatMenu()
        styleMenu = FM.FlatMenu()
        editMenu  = FM.FlatMenu()
        multipleMenu = FM.FlatMenu()
        historyMenu = FM.FlatMenu()
        subMenu = FM.FlatMenu()
        helpMenu = FM.FlatMenu()
        subMenu1 = FM.FlatMenu()
        subMenuExit = FM.FlatMenu()

        self.newMyTheme = self._mb.GetRendererManager().AddRenderer(FM_MyRenderer())

        # Load toolbar icons (32x32)
        copy_bmp = wx.Bitmap(os.path.join(bitmapDir, "editcopy.png"), wx.BITMAP_TYPE_PNG)
        cut_bmp = wx.Bitmap(os.path.join(bitmapDir, "editcut.png"), wx.BITMAP_TYPE_PNG)
        paste_bmp = wx.Bitmap(os.path.join(bitmapDir, "editpaste.png"), wx.BITMAP_TYPE_PNG)
        open_folder_bmp = wx.Bitmap(os.path.join(bitmapDir, "fileopen.png"), wx.BITMAP_TYPE_PNG)
        new_file_bmp = wx.Bitmap(os.path.join(bitmapDir, "filenew.png"), wx.BITMAP_TYPE_PNG)
        new_folder_bmp = wx.Bitmap(os.path.join(bitmapDir, "folder_new.png"), wx.BITMAP_TYPE_PNG)
        save_bmp = wx.Bitmap(os.path.join(bitmapDir, "filesave.png"), wx.BITMAP_TYPE_PNG)
        context_bmp = wx.Bitmap(os.path.join(bitmapDir, "contexthelp-16.png"), wx.BITMAP_TYPE_PNG)
        colBmp = wx.Bitmap(os.path.join(bitmapDir, "month-16.png"), wx.BITMAP_TYPE_PNG)
        view1Bmp = wx.Bitmap(os.path.join(bitmapDir, "view_choose.png"), wx.BITMAP_TYPE_PNG)
        view2Bmp = wx.Bitmap(os.path.join(bitmapDir, "view_detailed.png"), wx.BITMAP_TYPE_PNG)
        view3Bmp = wx.Bitmap(os.path.join(bitmapDir, "view_icon.png"), wx.BITMAP_TYPE_PNG)
        view4Bmp = wx.Bitmap(os.path.join(bitmapDir, "view_multicolumn.png"), wx.BITMAP_TYPE_PNG)

        # Set an icon to the exit/help/transparency menu item
        exitImg = wx.Bitmap(os.path.join(bitmapDir, "exit-16.png"), wx.BITMAP_TYPE_PNG)
        helpImg = wx.Bitmap(os.path.join(bitmapDir, "help-16.png"), wx.BITMAP_TYPE_PNG)
        ghostBmp = wx.Bitmap(os.path.join(bitmapDir, "field-16.png"), wx.BITMAP_TYPE_PNG)

        # Create a context menu
        context_menu = FM.FlatMenu()

        # Create the menu items
        menuItem = FM.FlatMenuItem(context_menu, wx.ID_ANY, "Test Item", "", wx.ITEM_NORMAL, None, context_bmp)
        context_menu.AppendItem(menuItem)

        item = FM.FlatMenuItem(fileMenu, MENU_NEW_FILE, "&New File\tCtrl+N", "New File", wx.ITEM_NORMAL)
        fileMenu.AppendItem(item)
        item.SetContextMenu(context_menu)

        self._mb.AddTool(MENU_NEW_FILE, "New File", new_file_bmp)

        item = FM.FlatMenuItem(fileMenu, MENU_SAVE, "&Save File\tCtrl+S", "Save File", wx.ITEM_NORMAL)
        fileMenu.AppendItem(item)
        self._mb.AddTool(MENU_SAVE, "Save File", save_bmp)

        item = FM.FlatMenuItem(fileMenu, MENU_OPEN_FILE, "&Open File\tCtrl+O", "Open File", wx.ITEM_NORMAL)
        fileMenu.AppendItem(item)
        self._mb.AddTool(MENU_OPEN_FILE, "Open File", open_folder_bmp)
        self._mb.AddSeparator()   # Toolbar separator

        item = FM.FlatMenuItem(fileMenu, MENU_NEW_FOLDER, "N&ew Folder\tCtrl+E", "New Folder", wx.ITEM_NORMAL)
        fileMenu.AppendItem(item)

        self._mb.AddTool(MENU_NEW_FOLDER, "New Folder",new_folder_bmp)
        self._mb.AddSeparator()   # Toobar separator

        item = FM.FlatMenuItem(fileMenu, MENU_COPY, "&Copy\tCtrl+C", "Copy", wx.ITEM_NORMAL)
        fileMenu.AppendItem(item)
        self._mb.AddTool(MENU_COPY, "Copy", copy_bmp)

        item = FM.FlatMenuItem(fileMenu, MENU_CUT, "Cut\tCtrl+X", "Cut", wx.ITEM_NORMAL)
        fileMenu.AppendItem(item)
        self._mb.AddTool(MENU_CUT, "Cut", cut_bmp)

        item = FM.FlatMenuItem(fileMenu, MENU_PASTE, "Paste\tCtrl+V", "Paste", wx.ITEM_NORMAL, subMenuExit)
        fileMenu.AppendItem(item)
        self._mb.AddTool(MENU_PASTE, "Paste", paste_bmp)

        self._mb.AddSeparator()   # Separator

        # Add a wx.ComboBox to FlatToolbar
        combo = wx.ComboBox(self._mb, -1, choices=["Hello", "World", "wxPython"])
        self._mb.AddControl(combo)

        self._mb.AddSeparator()   # Separator

        stext = wx.StaticText(self._mb, -1, "Hello")
        #stext.SetBackgroundStyle(wx.BG_STYLE_CUSTOM )

        self._mb.AddControl(stext)

        self._mb.AddSeparator()   # Separator

        # Add another couple of bitmaps
        self._mb.AddRadioTool(wx.ID_ANY, "View Column", view1Bmp)
        self._mb.AddRadioTool(wx.ID_ANY, "View Icons", view2Bmp)
        self._mb.AddRadioTool(wx.ID_ANY, "View Details", view3Bmp)
        self._mb.AddRadioTool(wx.ID_ANY, "View Multicolumn", view4Bmp)

        # Add non-toolbar item
        item = FM.FlatMenuItem(subMenuExit, wx.ID_EXIT, "E&xit\tAlt+X", "Exit demo", wx.ITEM_NORMAL, None, exitImg)
        subMenuExit.AppendItem(item)
        fileMenu.AppendSeparator()
        item = FM.FlatMenuItem(subMenuExit, wx.ID_EXIT, "E&xit\tAlt+Q", "Exit demo", wx.ITEM_NORMAL, None, exitImg)
        fileMenu.AppendItem(item)

        # Second menu
        item = FM.FlatMenuItem(styleMenu, MENU_STYLE_DEFAULT, "Menu style Default\tAlt+N", "Menu style Default", wx.ITEM_RADIO)
        styleMenu.AppendItem(item)
        item.Check(True)

        item = FM.FlatMenuItem(styleMenu, MENU_STYLE_MY, "Menu style Custom \tAlt+C", "Menu style Custom", wx.ITEM_RADIO)
        styleMenu.AppendItem(item)

        item = FM.FlatMenuItem(styleMenu, MENU_STYLE_XP, "Menu style XP\tAlt+P", "Menu style XP", wx.ITEM_RADIO)
        styleMenu.AppendItem(item)

        item = FM.FlatMenuItem(styleMenu, MENU_STYLE_2007, "Menu style 2007\tAlt+O", "Menu style 2007", wx.ITEM_RADIO)
        styleMenu.AppendItem(item)

        item = FM.FlatMenuItem(styleMenu, MENU_STYLE_VISTA, "Menu style Vista\tAlt+V", "Menu style Vista", wx.ITEM_RADIO)
        styleMenu.AppendItem(item)

        styleMenu.AppendSeparator()
        item = FM.FlatMenuItem(styleMenu, MENU_USE_CUSTOM, "Show Customize DropDown", "Shows the customize drop down arrow", wx.ITEM_CHECK)

        # Demonstrate how to set custom font and text colour to a FlatMenuItem
        item.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Courier New"))
        item.SetTextColour(wx.RED)

        item.Check(True)
        styleMenu.AppendItem(item)

        styleMenu.AppendSeparator()
        item = FM.FlatMenuItem(styleMenu, MENU_LCD_MONITOR, "Use LCD monitors option", "Instructs FlatMenu to use LCD drawings", wx.ITEM_CHECK)
        styleMenu.AppendItem(item)

        # Add some radio items
        styleMenu.AppendSeparator()
        # Add sub-menu to main menu
        item = FM.FlatMenuItem(styleMenu, wx.ID_ANY, "Sub-&menu radio items", "", wx.ITEM_NORMAL, subMenu1)
        styleMenu.AppendItem(item)
        item.SetContextMenu(context_menu)

        item = FM.FlatMenuItem(subMenu1, wx.ID_ANY, "Radio Item 1", "Radio Item 1", wx.ITEM_RADIO)
        subMenu1.AppendItem(item)

        item = FM.FlatMenuItem(subMenu1, wx.ID_ANY, "Radio Item 2", "Radio Item 2", wx.ITEM_RADIO)
        subMenu1.AppendItem(item)
        item.Check(True)

        item = FM.FlatMenuItem(subMenu1, wx.ID_ANY, "Radio Item 3", "Radio Item 3", wx.ITEM_RADIO)
        subMenu1.AppendItem(item)

        item = FM.FlatMenuItem(editMenu, MENU_REMOVE_MENU, "Remove menu", "Remove menu", wx.ITEM_NORMAL)
        editMenu.AppendItem(item)

        item = FM.FlatMenuItem(editMenu, MENU_DISABLE_MENU_ITEM, "Disable Menu Item ...", "Disable Menu Item", wx.ITEM_NORMAL)
        editMenu.AppendItem(item)

        editMenu.AppendSeparator()

        item = FM.FlatMenuItem(editMenu, MENU_TRANSPARENCY, "Set FlatMenu transparency...", "Sets the FlatMenu transparency",
                               wx.ITEM_NORMAL, None, ghostBmp)

        editMenu.AppendItem(item)

        # Add some dummy entries to the sub menu
        # Add sub-menu to main menu
        item = FM.FlatMenuItem(editMenu, 9001, "Sub-&menu items", "", wx.ITEM_NORMAL, subMenu)
        editMenu.AppendItem(item)

        # Create the submenu items and add them
        item = FM.FlatMenuItem(subMenu, 9002, "&Sub-menu Item 1", "", wx.ITEM_NORMAL)
        subMenu.AppendItem(item)

        item = FM.FlatMenuItem(subMenu, 9003, "Su&b-menu Item 2", "", wx.ITEM_NORMAL)
        subMenu.AppendItem(item)

        item = FM.FlatMenuItem(subMenu, 9004, "Sub-menu Item 3", "", wx.ITEM_NORMAL)
        subMenu.AppendItem(item)

        item = FM.FlatMenuItem(subMenu, 9005, "Sub-menu Item 4", "", wx.ITEM_NORMAL)
        subMenu.AppendItem(item)

        maxItems = 17
        numCols = 2
        switch = int(math.ceil(maxItems/float(numCols)))

        fnt = wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Courier New")
        colours = [wx.RED, wx.GREEN, wx.BLUE]
        for i in range(17):
            row, col = i%switch, i/switch
            result = random.randint(0, 1) == 1
            bmp = (result and [colBmp] or [wx.NullBitmap])[0]
            item = FM.FlatMenuItem(multipleMenu, wx.ID_ANY, "Row %d, Col %d"%((row+1, col+1)), "", wx.ITEM_NORMAL, None, bmp)
            if result == 0:
                # Demonstrate how to set custom font and text colour to a FlatMenuItem
                col = random.randint(0, 2)
                item.SetFont(fnt)
                item.SetTextColour(colours[col])

            multipleMenu.AppendItem(item)

        multipleMenu.SetNumberColumns(2)

        historyMenu.Append(wx.ID_OPEN, "&Open...")
        self.historyMenu = historyMenu
        self.filehistory = FM.FileHistory()
        self.filehistory.UseMenu(self.historyMenu)

        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFileOpenDialog, id=wx.ID_OPEN)

        item = FM.FlatMenuItem(helpMenu, MENU_HELP, "&About\tCtrl+A", "About...", wx.ITEM_NORMAL, None, helpImg)
        helpMenu.AppendItem(item)

        fileMenu.SetBackgroundBitmap(CreateBackgroundBitmap())

        # Add menu to the menu bar
        self._mb.Append(fileMenu, "&File")
        self._mb.Append(styleMenu, "&Style")
        self._mb.Append(editMenu, "&Edit")
        self._mb.Append(multipleMenu, "&Multiple Columns")
        self._mb.Append(historyMenu, "File Histor&y")
        self._mb.Append(helpMenu, "&Help")


    def ConnectEvents(self):

        # Attach menu events to some handlers
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnQuit, id=wx.ID_EXIT)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnEdit, id=MENU_DISABLE_MENU_ITEM, id2=MENU_REMOVE_MENU)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStyle, id=MENU_STYLE_XP, id2=MENU_STYLE_VISTA)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFlatMenuCmd, id=MENU_NEW_FILE, id2=20013)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnAbout, id=MENU_HELP)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStyle, id=MENU_STYLE_MY)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStyle, id=MENU_STYLE_DEFAULT)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnShowCustom, id=MENU_USE_CUSTOM)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnLCDMonitor, id=MENU_LCD_MONITOR)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnTransparency, id=MENU_TRANSPARENCY)

        self.Bind(FM.EVT_FLAT_MENU_ITEM_MOUSE_OVER, self.OnMouseOver, id=MENU_NEW_FILE)
        self.Bind(FM.EVT_FLAT_MENU_ITEM_MOUSE_OUT, self.OnMouseOut, id=MENU_NEW_FILE)

        self.Bind(wx.EVT_UPDATE_UI, self.OnFlatMenuCmdUI, id=20001, id2=20013)
        if "__WXMAC__" in wx.Platform:
            self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(FM.EVT_FLAT_MENU_RANGE, self.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9+1)


    def OnSize(self, event):

        self._mgr.Update()
        self.Layout()


    def OnQuit(self, event):

        if _hasAUI:
            self._mgr.UnInit()

        self.Destroy()


    def OnButtonClicked(self, event):

        # Demonstrate using the wxFlatMenu without a menu bar
        btn = event.GetEventObject()

        # Create the popup menu
        self.CreatePopupMenu()

        # Position the menu:
        # The menu should be positioned at the bottom left corner of the button.
        btnSize = btn.GetSize()
        btnPt = btn.GetPosition()

        # Since the btnPt (button position) is in client coordinates,
        # and the menu coordinates is relative to screen we convert
        # the coords
        btnPt = btn.GetParent().ClientToScreen(btnPt)

        # A nice feature with the Popup menu, is the ability to provide an
        # object that we wish to handle the menu events, in this case we
        # pass 'self'
        # if we wish the menu to appear under the button, we provide its height
        self._popUpMenu.SetOwnerHeight(btnSize.y)
        self._popUpMenu.Popup(wx.Point(btnPt.x, btnPt.y), self)


    def OnLongButtonClicked(self, event):

        # Demonstrate using the wxFlatMenu without a menu bar
        btn = event.GetEventObject()

        # Create the popup menu
        self.CreateLongPopupMenu()

        # Position the menu:
        # The menu should be positioned at the bottom left corner of the button.
        btnSize = btn.GetSize()

        # btnPt is returned relative to its parent
        # so, we need to convert it to screen
        btnPt  = btn.GetPosition()
        btnPt = btn.GetParent().ClientToScreen(btnPt)

        # if we wish the menu to appear under the button, we provide its height
        self._longPopUpMenu.SetOwnerHeight(btnSize.y)
        self._longPopUpMenu.Popup(wx.Point(btnPt.x, btnPt.y), self)


    def CreatePopupMenu(self):

        if not self._popUpMenu:

            self._popUpMenu = FM.FlatMenu()
            #-----------------------------------------------
            # Flat Menu test
            #-----------------------------------------------

            # First we create the sub-menu item
            subMenu = FM.FlatMenu()
            subSubMenu = FM.FlatMenu()

            # Create the menu items
            menuItem = FM.FlatMenuItem(self._popUpMenu, 20001, "First Menu Item", "", wx.ITEM_CHECK)
            self._popUpMenu.AppendItem(menuItem)

            menuItem = FM.FlatMenuItem(self._popUpMenu, 20002, "Sec&ond Menu Item", "", wx.ITEM_CHECK)
            self._popUpMenu.AppendItem(menuItem)

            menuItem = FM.FlatMenuItem(self._popUpMenu, wx.ID_ANY, "Checkable-Disabled Item", "", wx.ITEM_CHECK)
            menuItem.Enable(False)
            self._popUpMenu.AppendItem(menuItem)

            menuItem = FM.FlatMenuItem(self._popUpMenu, 20003, "Third Menu Item", "", wx.ITEM_CHECK)
            self._popUpMenu.AppendItem(menuItem)

            self._popUpMenu.AppendSeparator()

            # Add sub-menu to main menu
            menuItem = FM.FlatMenuItem(self._popUpMenu, 20004, "Sub-&menu item", "", wx.ITEM_NORMAL, subMenu)
            self._popUpMenu.AppendItem(menuItem)

            # Create the submenu items and add them
            menuItem = FM.FlatMenuItem(subMenu, 20005, "&Sub-menu Item 1", "", wx.ITEM_NORMAL)
            subMenu.AppendItem(menuItem)

            menuItem = FM.FlatMenuItem(subMenu, 20006, "Su&b-menu Item 2", "", wx.ITEM_NORMAL)
            subMenu.AppendItem(menuItem)

            menuItem = FM.FlatMenuItem(subMenu, 20007, "Sub-menu Item 3", "", wx.ITEM_NORMAL)
            subMenu.AppendItem(menuItem)

            menuItem = FM.FlatMenuItem(subMenu, 20008, "Sub-menu Item 4", "", wx.ITEM_NORMAL)
            subMenu.AppendItem(menuItem)

            # Create the submenu items and add them
            menuItem = FM.FlatMenuItem(subSubMenu, 20009, "Sub-menu Item 1", "", wx.ITEM_NORMAL)
            subSubMenu.AppendItem(menuItem)

            menuItem = FM.FlatMenuItem(subSubMenu, 20010, "Sub-menu Item 2", "", wx.ITEM_NORMAL)
            subSubMenu.AppendItem(menuItem)

            menuItem = FM.FlatMenuItem(subSubMenu, 20011, "Sub-menu Item 3", "", wx.ITEM_NORMAL)
            subSubMenu.AppendItem(menuItem)

            menuItem = FM.FlatMenuItem(subSubMenu, 20012, "Sub-menu Item 4", "", wx.ITEM_NORMAL)
            subSubMenu.AppendItem(menuItem)

            # Add sub-menu to submenu menu
            menuItem = FM.FlatMenuItem(subMenu, 20013, "Sub-menu item", "", wx.ITEM_NORMAL, subSubMenu)
            subMenu.AppendItem(menuItem)


    def CreateLongPopupMenu(self):

        if hasattr(self, "_longPopUpMenu"):
            return

        self._longPopUpMenu = FM.FlatMenu()
        sub = FM.FlatMenu()

        #-----------------------------------------------
        # Flat Menu test
        #-----------------------------------------------

        for ii in range(30):
            if ii == 0:
                menuItem = FM.FlatMenuItem(self._longPopUpMenu, wx.ID_ANY, "Menu Item #%ld"%(ii+1), "", wx.ITEM_NORMAL, sub)
                self._longPopUpMenu.AppendItem(menuItem)

                for k in range(5):

                    menuItem = FM.FlatMenuItem(sub, wx.ID_ANY, "Sub Menu Item #%ld"%(k+1))
                    sub.AppendItem(menuItem)

            else:

                menuItem = FM.FlatMenuItem(self._longPopUpMenu, wx.ID_ANY, "Menu Item #%ld"%(ii+1))
                self._longPopUpMenu.AppendItem(menuItem)

# ------------------------------------------
# Event handlers
# ------------------------------------------

    def OnStyle(self, event):

        eventId = event.GetId()

        if eventId == MENU_STYLE_DEFAULT:
            self._mb.GetRendererManager().SetTheme(FM.StyleDefault)
        elif eventId == MENU_STYLE_2007:
            self._mb.GetRendererManager().SetTheme(FM.Style2007)
        elif eventId == MENU_STYLE_XP:
            self._mb.GetRendererManager().SetTheme(FM.StyleXP)
        elif eventId == MENU_STYLE_VISTA:
            self._mb.GetRendererManager().SetTheme(FM.StyleVista)
        elif eventId == MENU_STYLE_MY:
            self._mb.GetRendererManager().SetTheme(self.newMyTheme)

        self._mb.ClearBitmaps()

        self._mb.Refresh()
        self._mtb.Refresh()
        self.Update()


    def OnShowCustom(self, event):

        self._mb.ShowCustomize(event.IsChecked())


    def OnLCDMonitor(self, event):

        self._mb.SetLCDMonitor(event.IsChecked())


    def OnTransparency(self, event):

        transparency = ArtManager.Get().GetTransparency()
        dlg = wx.TextEntryDialog(self, 'Please enter a value for menu transparency',
                                 'FlatMenu Transparency', str(transparency))

        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return

        value = dlg.GetValue()
        dlg.Destroy()

        try:
            value = int(value)
        except:
            dlg = wx.MessageDialog(self, "Invalid transparency value!", "Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

        if value < 0 or value > 255:
            dlg = wx.MessageDialog(self, "Invalid transparency value!", "Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

        ArtManager.Get().SetTransparency(value)


    def OnMouseOver(self, event):

        self.log.write("Received Flat menu mouse enter ID: %d\n"%(event.GetId()))


    def OnMouseOut(self, event):

        self.log.write("Received Flat menu mouse leave ID: %d\n"%(event.GetId()))


    def OnFlatMenuCmd(self, event):

        self.log.write("Received Flat menu command event ID: %d\n"%(event.GetId()))


    def OnFlatMenuCmdUI(self, event):

        self.log.write("Received Flat menu update UI event ID: %d\n"%(event.GetId()))


    def GetStringFromUser(self, msg):

        dlg = wx.TextEntryDialog(self, msg, "Enter Text")

        userString = ""
        if dlg.ShowModal() == wx.ID_OK:
            userString = dlg.GetValue()

        dlg.Destroy()

        return userString


    def OnFileOpenDialog(self, evt):
        dlg = wx.FileDialog(self, defaultDir = os.getcwd(),
                            wildcard = "All Files|*", style = wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.log.write("You selected %s\n" % path)

            # add it to the history
            self.filehistory.AddFileToHistory(path)

        dlg.Destroy()


    def OnFileHistory(self, evt):
        # get the file based on the menu ID
        fileNum = evt.GetId() - wx.ID_FILE1
        path = self.filehistory.GetHistoryFile(fileNum)
        self.log.write("You selected %s\n" % path)

        # add it back to the history so it will be moved up the list
        self.filehistory.AddFileToHistory(path)


    def OnEdit(self, event):

        if event.GetId() == MENU_REMOVE_MENU:

            idxStr = self.GetStringFromUser("Insert menu index to remove:")
            if idxStr.strip() != "":

                idx = int(idxStr)
                self._mb.Remove(idx)

        elif event.GetId() == MENU_DISABLE_MENU_ITEM:

            idxStr = self.GetStringFromUser("Insert menu item ID to be disabled (10005 - 10011):")
            if idxStr.strip() != "":

                idx = int(idxStr)
                mi = self._mb.FindMenuItem(idx)
                if mi:
                    mi.Enable(False)


    def OnAbout(self, event):

        msg = "This is the About Dialog of the FlatMenu demo.\n\n" + \
              "Author: Andrea Gavana @ 03 Nov 2006\n\n" + \
              "Please report any bug/requests or improvements\n" + \
              "to Andrea Gavana at the following email addresses:\n\n" + \
              "andrea.gavana@gmail.com\nandrea.gavana@maerskoil.com\n\n" + \
              "Welcome to wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "FlatMenu wxPython Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test FlatMenu ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = FlatMenuDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    if wx.Platform != '__WXMAC__':
        win = TestPanel(nb, log)
        return win
    else:
        from Main import MessagePanel
        win = MessagePanel(nb, 'This demo only works on MSW and GTK.',
                           'Sorry', wx.ICON_WARNING)
        return win

#----------------------------------------------------------------------


overview = FM.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

