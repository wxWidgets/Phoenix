#!/usr/bin/env python

"""
This module implements a demo application that shows many of the features of
the RibbonBar and related classes found in the wx.ribbon module.  It is very
similar to the pure-python implementation found in the wx.lib.agw.ribbon
package.  In fact, this demo was ported from the AGW version of the demo with
just a few relatively minor edits.
"""

import wx
import wx.ribbon as RB

import images


# --------------------------------------------------- #
# Some constants for ribbon buttons

ID_CIRCLE = wx.ID_HIGHEST + 1
ID_CROSS = ID_CIRCLE + 1
ID_TRIANGLE = ID_CIRCLE + 2
ID_SQUARE = ID_CIRCLE + 3
ID_POLYGON = ID_CIRCLE + 4
ID_SELECTION_EXPAND_H = ID_CIRCLE + 5
ID_SELECTION_EXPAND_V = ID_CIRCLE + 6
ID_SELECTION_CONTRACT = ID_CIRCLE + 7
ID_PRIMARY_COLOUR = ID_CIRCLE + 8
ID_SECONDARY_COLOUR = ID_CIRCLE + 9
ID_DEFAULT_PROVIDER = ID_CIRCLE + 10
ID_AUI_PROVIDER = ID_CIRCLE + 11
ID_MSW_PROVIDER = ID_CIRCLE + 12
ID_MAIN_TOOLBAR = ID_CIRCLE + 13
ID_POSITION_TOP = ID_CIRCLE + 14
ID_POSITION_TOP_ICONS = ID_CIRCLE + 15
ID_POSITION_TOP_BOTH = ID_CIRCLE + 16
ID_POSITION_LEFT = ID_CIRCLE + 17
ID_POSITION_LEFT_LABELS = ID_CIRCLE + 18
ID_POSITION_LEFT_BOTH = ID_CIRCLE + 19
ID_TOGGLE_PANELS = ID_CIRCLE + 20



# --------------------------------------------------- #

def CreateBitmap(imgName):
    bmp = getattr(images, imgName).Bitmap
    return bmp


#---------------------------------------------------------------------------

class ColourClientData(object):
    def __init__(self, name, colour):
        self._name = name
        self._colour = colour

    def GetName(self):
        return self._name

    def GetColour(self):
        return self._colour

    @property
    def name(self):
        return self._name

    @property
    def colour(self):
        return self._colour

#---------------------------------------------------------------------------

class RibbonFrame(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, log=None):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        panel = wx.Panel(self)

        self._ribbon = RB.RibbonBar(panel, style=RB.RIBBON_BAR_DEFAULT_STYLE
                                                |RB.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS)

        self._bitmap_creation_dc = wx.MemoryDC()
        self._colour_data = wx.ColourData()

        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Examples", CreateBitmap("ribbon"))
        toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "Toolbar",
                                       style=RB.RIBBON_PANEL_NO_AUTO_MINIMISE
                                             |RB.RIBBON_PANEL_EXT_BUTTON)

        toolbar = RB.RibbonToolBar(toolbar_panel, ID_MAIN_TOOLBAR)
        toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_left"))
        toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_center"))
        toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_right"))
        toolbar.AddSeparator()
        toolbar.AddHybridTool(wx.ID_NEW, wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddSeparator()
        toolbar.AddDropdownTool(wx.ID_UNDO, wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddDropdownTool(wx.ID_REDO, wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddSeparator()
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddSeparator()
        toolbar.AddHybridTool(ID_POSITION_LEFT, CreateBitmap("position_left"), "Align ribbonbar vertically\non the left\nfor demonstration purposes")
        toolbar.AddHybridTool(ID_POSITION_TOP, CreateBitmap("position_top"), "Align the ribbonbar horizontally\nat the top\nfor demonstration purposes")
        toolbar.AddSeparator()
        toolbar.AddHybridTool(wx.ID_PRINT, wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(16, 15)),
                              "This is the Print button tooltip\ndemonstrating a tooltip")
        toolbar.SetRows(2, 3)

        selection_panel = RB.RibbonPanel(home, wx.ID_ANY, "Selection", CreateBitmap("selection_panel"))
        selection = RB.RibbonButtonBar(selection_panel)
        selection.AddButton(ID_SELECTION_EXPAND_V, "Expand Vertically", CreateBitmap("expand_selection_v"),
                            "This is a tooltip for Expand Vertically\ndemonstrating a tooltip")
        selection.AddButton(ID_SELECTION_EXPAND_H, "Expand Horizontally", CreateBitmap("expand_selection_h"), "")
        selection.AddButton(ID_SELECTION_CONTRACT, "Contract", CreateBitmap("auto_crop_selection"),
                            CreateBitmap("auto_crop_selection_small"))

        shapes_panel = RB.RibbonPanel(home, wx.ID_ANY, "Shapes", CreateBitmap("circle_small"))
        shapes = RB.RibbonButtonBar(shapes_panel)
        shapes.AddButton(ID_CIRCLE, "Circle", CreateBitmap("circle"), CreateBitmap("circle_small"),
                         help_string="This is a tooltip for the circle button\ndemonstrating another tooltip",
                         kind=RB.RIBBON_BUTTON_TOGGLE)
        shapes.AddButton(ID_CROSS, "Cross", CreateBitmap("cross"), "")
        shapes.AddHybridButton(ID_TRIANGLE, "Triangle", CreateBitmap("triangle"))
        shapes.AddButton(ID_SQUARE, "Square", CreateBitmap("square"), "")
        shapes.AddDropdownButton(ID_POLYGON, "Other Polygon", CreateBitmap("hexagon"), "")

        sizer_panel = RB.RibbonPanel(home, wx.ID_ANY, "Panel with Sizer",
                                     style=RB.RIBBON_PANEL_DEFAULT_STYLE)

        strs = ["Item 1 using a box sizer now", "Item 2 using a box sizer now"]
        sizer_panelcombo = wx.ComboBox(sizer_panel, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
                                       strs, wx.CB_READONLY)

        sizer_panelcombo2 = wx.ComboBox(sizer_panel, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
                                        strs, wx.CB_READONLY)

        sizer_panelcombo.Select(0)
        sizer_panelcombo2.Select(1)
        sizer_panelcombo.SetMinSize(wx.Size(150, -1))
        sizer_panelcombo2.SetMinSize(wx.Size(150, -1))

        # not using wx.WrapSizer(wx.HORIZONTAL) as it reports an incorrect min height
        sizer_panelsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_panelsizer.AddStretchSpacer(1)
        sizer_panelsizer.Add(sizer_panelcombo, 0, wx.ALL|wx.EXPAND, 2)
        sizer_panelsizer.Add(sizer_panelcombo2, 0, wx.ALL|wx.EXPAND, 2)
        sizer_panelsizer.AddStretchSpacer(1)
        sizer_panel.SetSizer(sizer_panelsizer)

        label_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
        self._bitmap_creation_dc.SetFont(label_font)

        scheme = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Appearance", CreateBitmap("eye"))

        (self._default_primary,
         self._default_secondary,
         self._default_tertiary) = self._ribbon.GetArtProvider().GetColourScheme()

        provider_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Art",
                                        style=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        provider_bar = RB.RibbonButtonBar(provider_panel, wx.ID_ANY)
        provider_bar.AddButton(ID_DEFAULT_PROVIDER, "Default Provider",
                                     wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(32, 32)), "")
        provider_bar.AddButton(ID_AUI_PROVIDER, "AUI Provider", CreateBitmap("aui_style"), "")
        provider_bar.AddButton(ID_MSW_PROVIDER, "MSW Provider", CreateBitmap("msw_style"), "")

        primary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Primary Colour", CreateBitmap("colours"))
        self._primary_gallery = self.PopulateColoursPanel(primary_panel, self._default_primary, ID_PRIMARY_COLOUR)

        secondary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Secondary Colour", CreateBitmap("colours"))
        self._secondary_gallery = self.PopulateColoursPanel(secondary_panel, self._default_secondary, ID_SECONDARY_COLOUR)

        dummy_2 = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Empty Page", CreateBitmap("empty"))
        dummy_3 = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Another Page", CreateBitmap("empty"))

        self._ribbon.Realize()

        self._logwindow = wx.TextCtrl(panel, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
                                      wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE)

        self._togglePanels = wx.ToggleButton(panel, ID_TOGGLE_PANELS, "&Toggle panels")
        self._togglePanels.SetValue(True)

        s = wx.BoxSizer(wx.VERTICAL)

        s.Add(self._ribbon, 0, wx.EXPAND)
        s.Add(self._logwindow, 1, wx.EXPAND)
        s.Add(self._togglePanels, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)

        panel.SetSizer(s)
        self.panel = panel

        self.BindEvents(selection, shapes, provider_bar, toolbar_panel)

        self.SetIcon(images.Mondrian.Icon)
        self.CenterOnScreen()



    def BindEvents(self, selection, shapes, provider_bar, toolbar_panel):
        provider_bar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnDefaultProvider, id=ID_DEFAULT_PROVIDER)
        provider_bar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnAUIProvider, id=ID_AUI_PROVIDER)
        provider_bar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnMSWProvider, id=ID_MSW_PROVIDER)
        selection.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSelectionExpandHButton, id=ID_SELECTION_EXPAND_H)
        selection.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSelectionExpandVButton, id=ID_SELECTION_EXPAND_V)
        selection.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSelectionContractButton, id=ID_SELECTION_CONTRACT)
        shapes.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnCircleButton, id=ID_CIRCLE)
        shapes.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnCrossButton, id=ID_CROSS)
        shapes.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnTriangleButton, id=ID_TRIANGLE)
        shapes.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSquareButton, id=ID_SQUARE)
        shapes.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnTriangleDropdown, id=ID_TRIANGLE)
        shapes.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnPolygonDropdown, id=ID_POLYGON)
        toolbar_panel.Bind(RB.EVT_RIBBONPANEL_EXTBUTTON_ACTIVATED, self.OnExtButton)

        self.Bind(RB.EVT_RIBBONGALLERY_HOVER_CHANGED, self.OnHoveredColourChange, id=ID_PRIMARY_COLOUR)
        self.Bind(RB.EVT_RIBBONGALLERY_HOVER_CHANGED, self.OnHoveredColourChange, id=ID_SECONDARY_COLOUR)
        self.Bind(RB.EVT_RIBBONGALLERY_SELECTED, self.OnPrimaryColourSelect, id=ID_PRIMARY_COLOUR)
        self.Bind(RB.EVT_RIBBONGALLERY_SELECTED, self.OnSecondaryColourSelect, id=ID_SECONDARY_COLOUR)
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnNew, id=wx.ID_NEW)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnNewDropdown, id=wx.ID_NEW)
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnPrint, id=wx.ID_PRINT)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnPrintDropdown, id=wx.ID_PRINT)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnRedoDropdown, id=wx.ID_REDO)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnUndoDropdown, id=wx.ID_UNDO)
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnPositionLeft, id=ID_POSITION_LEFT)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnPositionLeftDropdown, id=ID_POSITION_LEFT)
        self.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.OnPositionTop, id=ID_POSITION_TOP)
        self.Bind(RB.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnPositionTopDropdown, id=ID_POSITION_TOP)
        self.Bind(wx.EVT_BUTTON, self.OnColourGalleryButton, id=ID_PRIMARY_COLOUR)
        self.Bind(wx.EVT_BUTTON, self.OnColourGalleryButton, id=ID_SECONDARY_COLOUR)
        self.Bind(wx.EVT_MENU, self.OnPositionLeftIcons, id=ID_POSITION_LEFT)
        self.Bind(wx.EVT_MENU, self.OnPositionLeftLabels, id=ID_POSITION_LEFT_LABELS)
        self.Bind(wx.EVT_MENU, self.OnPositionLeftBoth, id=ID_POSITION_LEFT_BOTH)
        self.Bind(wx.EVT_MENU, self.OnPositionTopLabels, id=ID_POSITION_TOP)
        self.Bind(wx.EVT_MENU, self.OnPositionTopIcons, id=ID_POSITION_TOP_ICONS)
        self.Bind(wx.EVT_MENU, self.OnPositionTopBoth, id=ID_POSITION_TOP_BOTH)

        self._togglePanels.Bind(wx.EVT_TOGGLEBUTTON, self.OnTogglePanels, id=ID_TOGGLE_PANELS)


    def SetBarStyle(self, style):
        self._ribbon.Freeze()
        self._ribbon.SetWindowStyleFlag(style)

        pTopSize = self.panel.GetSizer()
        pToolbar = wx.FindWindowById(ID_MAIN_TOOLBAR)

        if style & RB.RIBBON_BAR_FLOW_VERTICAL:
            self._ribbon.SetTabCtrlMargins(10, 10)
            pTopSize.SetOrientation(wx.HORIZONTAL)
            if pToolbar:
                pToolbar.SetRows(3, 5)

        else:
            self._ribbon.SetTabCtrlMargins(50, 20)
            pTopSize.SetOrientation(wx.VERTICAL)
            if pToolbar:
                pToolbar.SetRows(2, 3)

        self._ribbon.Realize()
        self._ribbon.Thaw()
        self.panel.Layout()


    def PopulateColoursPanel(self, panel, defc, gallery_id):
        gallery = wx.FindWindowById(gallery_id, panel)
        if gallery:
            gallery.Clear()
        else:
            gallery = RB.RibbonGallery(panel, gallery_id)

        dc = self._bitmap_creation_dc
        def_item = self.AddColourToGallery(gallery, "Default", dc, defc)
        gallery.SetSelection(def_item)

        self.AddColourToGallery(gallery, "BLUE", dc)
        self.AddColourToGallery(gallery, "BLUE VIOLET", dc)
        self.AddColourToGallery(gallery, "BROWN", dc)
        self.AddColourToGallery(gallery, "CADET BLUE", dc)
        self.AddColourToGallery(gallery, "CORAL", dc)
        self.AddColourToGallery(gallery, "CYAN", dc)
        self.AddColourToGallery(gallery, "DARK GREEN", dc)
        self.AddColourToGallery(gallery, "DARK ORCHID", dc)
        self.AddColourToGallery(gallery, "FIREBRICK", dc)
        self.AddColourToGallery(gallery, "GOLD", dc)
        self.AddColourToGallery(gallery, "GOLDENROD", dc)
        self.AddColourToGallery(gallery, "GREEN", dc)
        self.AddColourToGallery(gallery, "INDIAN RED", dc)
        self.AddColourToGallery(gallery, "KHAKI", dc)
        self.AddColourToGallery(gallery, "LIGHT BLUE", dc)
        self.AddColourToGallery(gallery, "LIME GREEN", dc)
        self.AddColourToGallery(gallery, "MAGENTA", dc)
        self.AddColourToGallery(gallery, "MAROON", dc)
        self.AddColourToGallery(gallery, "NAVY", dc)
        self.AddColourToGallery(gallery, "ORANGE", dc)
        self.AddColourToGallery(gallery, "ORCHID", dc)
        self.AddColourToGallery(gallery, "PINK", dc)
        self.AddColourToGallery(gallery, "PLUM", dc)
        self.AddColourToGallery(gallery, "PURPLE", dc)
        self.AddColourToGallery(gallery, "RED", dc)
        self.AddColourToGallery(gallery, "SALMON", dc)
        self.AddColourToGallery(gallery, "SEA GREEN", dc)
        self.AddColourToGallery(gallery, "SIENNA", dc)
        self.AddColourToGallery(gallery, "SKY BLUE", dc)
        self.AddColourToGallery(gallery, "TAN", dc)
        self.AddColourToGallery(gallery, "THISTLE", dc)
        self.AddColourToGallery(gallery, "TURQUOISE", dc)
        self.AddColourToGallery(gallery, "VIOLET", dc)
        self.AddColourToGallery(gallery, "VIOLET RED", dc)
        self.AddColourToGallery(gallery, "WHEAT", dc)
        self.AddColourToGallery(gallery, "WHITE", dc)
        self.AddColourToGallery(gallery, "YELLOW", dc)

        return gallery


    def GetGalleryColour(self, gallery, item, name=None):
        data = gallery.GetItemClientData(item)

        if name != None:
            name = data.GetName()

        return data.GetColour(), name


    def OnHoveredColourChange(self, event):
        # Set the background of the gallery to the hovered colour, or back to the
        # default if there is no longer a hovered item.

        gallery = event.GetGallery()
        provider = gallery.GetArtProvider()

        if event.GetGalleryItem() != None:
            if provider == self._ribbon.GetArtProvider():
                gallery.SetArtProvider(provider)

            provider.SetColour(RB.RIBBON_ART_GALLERY_HOVER_BACKGROUND_COLOUR,
                               self.GetGalleryColour(event.GetGallery(), event.GetGalleryItem(), None)[0])

        else:
            if provider != self._ribbon.GetArtProvider():
                gallery.SetArtProvider(self._ribbon.GetArtProvider())
                del provider


    def OnPrimaryColourSelect(self, event):
        colour, name = self.GetGalleryColour(event.GetGallery(), event.GetGalleryItem(), "")
        self.AddText("Colour %s selected as primary."%name)

        dummy, secondary, tertiary = self._ribbon.GetArtProvider().GetColourScheme()
        self._ribbon.GetArtProvider().SetColourScheme(colour, secondary, tertiary)
        self.ResetGalleryArtProviders()
        self._ribbon.Refresh()


    def OnSecondaryColourSelect(self, event):
        colour, name = self.GetGalleryColour(event.GetGallery(), event.GetGalleryItem(), "")
        self.AddText("Colour %s selected as secondary."%name)

        primary, dummy, tertiary = self._ribbon.GetArtProvider().GetColourScheme()
        self._ribbon.GetArtProvider().SetColourScheme(primary, colour, tertiary)
        self.ResetGalleryArtProviders()
        self._ribbon.Refresh()


    def ResetGalleryArtProviders(self):
        if self._primary_gallery.GetArtProvider() != self._ribbon.GetArtProvider():
            self._primary_gallery.SetArtProvider(self._ribbon.GetArtProvider())

        if self._secondary_gallery.GetArtProvider() != self._ribbon.GetArtProvider():
            self._secondary_gallery.SetArtProvider(self._ribbon.GetArtProvider())


    def OnSelectionExpandHButton(self, event):
        self.AddText("Expand selection horizontally button clicked.")


    def OnSelectionExpandVButton(self, event):
        self.AddText("Expand selection vertically button clicked.")


    def OnSelectionContractButton(self, event):
        self.AddText("Contract selection button clicked.")


    def OnCircleButton(self, event):
        self.AddText("Circle button clicked.")


    def OnCrossButton(self, event):
        self.AddText("Cross button clicked.")


    def OnTriangleButton(self, event):
        self.AddText("Triangle button clicked.")


    def OnTriangleDropdown(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Equilateral")
        menu.Append(wx.ID_ANY, "Isosceles")
        menu.Append(wx.ID_ANY, "Scalene")

        event.PopupMenu(menu)


    def OnSquareButton(self, event):
        self.AddText("Square button clicked.")


    def OnPolygonDropdown(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Pentagon (5 sided)")
        menu.Append(wx.ID_ANY, "Hexagon (6 sided)")
        menu.Append(wx.ID_ANY, "Heptagon (7 sided)")
        menu.Append(wx.ID_ANY, "Octogon (8 sided)")
        menu.Append(wx.ID_ANY, "Nonagon (9 sided)")
        menu.Append(wx.ID_ANY, "Decagon (10 sided)")

        event.PopupMenu(menu)


    def OnNew(self, event):
        self.AddText("New button clicked.")


    def OnNewDropdown(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "New Document")
        menu.Append(wx.ID_ANY, "New Template")
        menu.Append(wx.ID_ANY, "New Mail")

        event.PopupMenu(menu)


    def OnPrint(self, event):
        self.AddText("Print button clicked.")


    def OnPrintDropdown(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Print")
        menu.Append(wx.ID_ANY, "Preview")
        menu.Append(wx.ID_ANY, "Options")

        event.PopupMenu(menu)


    def OnRedoDropdown(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Redo E")
        menu.Append(wx.ID_ANY, "Redo F")
        menu.Append(wx.ID_ANY, "Redo G")

        event.PopupMenu(menu)


    def OnUndoDropdown(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Undo C")
        menu.Append(wx.ID_ANY, "Undo B")
        menu.Append(wx.ID_ANY, "Undo A")

        event.PopupMenu(menu)


    def OnPositionTopLabels(self, event):
        self.SetBarStyle(RB.RIBBON_BAR_DEFAULT_STYLE)


    def OnPositionTopIcons(self, event):
        self.SetBarStyle((RB.RIBBON_BAR_DEFAULT_STYLE &~RB.RIBBON_BAR_SHOW_PAGE_LABELS)
                         | RB.RIBBON_BAR_SHOW_PAGE_ICONS)


    def OnPositionTopBoth(self, event):
        self.SetBarStyle(RB.RIBBON_BAR_DEFAULT_STYLE | RB.RIBBON_BAR_SHOW_PAGE_ICONS)


    def OnPositionLeftLabels(self, event):
        self.SetBarStyle(RB.RIBBON_BAR_DEFAULT_STYLE | RB.RIBBON_BAR_FLOW_VERTICAL)


    def OnPositionLeftIcons(self, event):
        self.SetBarStyle((RB.RIBBON_BAR_DEFAULT_STYLE &~RB.RIBBON_BAR_SHOW_PAGE_LABELS) |
                         RB.RIBBON_BAR_SHOW_PAGE_ICONS | RB.RIBBON_BAR_FLOW_VERTICAL)


    def OnPositionLeftBoth(self, event):
        self.SetBarStyle(RB.RIBBON_BAR_DEFAULT_STYLE | RB.RIBBON_BAR_SHOW_PAGE_ICONS |
                         RB.RIBBON_BAR_FLOW_VERTICAL)


    def OnPositionTop(self, event):
        self.OnPositionTopLabels(event)


    def OnPositionTopDropdown(self, event):
        menu = wx.Menu()
        menu.Append(ID_POSITION_TOP, "Top with Labels")
        menu.Append(ID_POSITION_TOP_ICONS, "Top with Icons")
        menu.Append(ID_POSITION_TOP_BOTH, "Top with Both")
        event.PopupMenu(menu)


    def OnPositionLeft(self, event):
        self.OnPositionLeftIcons(event)


    def OnPositionLeftDropdown(self, event):
        menu = wx.Menu()
        menu.Append(ID_POSITION_LEFT, "Left with Icons")
        menu.Append(ID_POSITION_LEFT_LABELS, "Left with Labels")
        menu.Append(ID_POSITION_LEFT_BOTH, "Left with Both")
        event.PopupMenu(menu)


    def OnTogglePanels(self, event):
        self._ribbon.ShowPanels(self._togglePanels.GetValue())


    def OnExtButton(self, event):
        wx.MessageBox("Extended button activated")


    def AddText(self, msg):
        self._logwindow.AppendText(msg)
        self._logwindow.AppendText("\n")
        self._ribbon.DismissExpandedPanel()


    def AddColourToGallery(self, gallery, colour, dc, value=None):
        item = None

        if colour != "Default":
            c = wx.Colour(colour)

        if value is not None:
            c = value

        if c.IsOk():

            iWidth = 64
            iHeight = 40

            bitmap = wx.Bitmap(iWidth, iHeight)
            dc.SelectObject(bitmap)
            b = wx.Brush(c)
            dc.SetPen(wx.BLACK_PEN)
            dc.SetBrush(b)
            dc.DrawRectangle(0, 0, iWidth, iHeight)

            colour = colour[0] + colour[1:].lower()
            size = wx.Size(*dc.GetTextExtent(colour))
            notcred = min(abs(~c.Red()), 255)
            notcgreen = min(abs(~c.Green()), 255)
            notcblue = min(abs(~c.Blue()), 255)

            foreground = wx.Colour(notcred, notcgreen, notcblue)

            if abs(foreground.Red() - c.Red()) + abs(foreground.Blue() - c.Blue()) + abs(foreground.Green() - c.Green()) < 64:
                # Foreground too similar to background - use a different
                # strategy to find a contrasting colour
                foreground = wx.Colour((c.Red() + 64) % 256, 255 - c.Green(),
                                       (c.Blue() + 192) % 256)

            dc.SetTextForeground(foreground)
            dc.DrawText(colour, (iWidth - size.GetWidth() + 1) / 2, (iHeight - size.GetHeight()) / 2)
            dc.SelectObjectAsSource(wx.NullBitmap)

            item = gallery.Append(bitmap, wx.ID_ANY)
            gallery.SetItemClientData(item, ColourClientData(colour, c))

        return item


    def OnColourGalleryButton(self, event):
        gallery = event.GetEventObject()
        if gallery is None:
            return

        self._ribbon.DismissExpandedPanel()
        if gallery.GetSelection():
            self._colour_data.SetColour(self.GetGalleryColour(gallery, gallery.GetSelection(), None)[0])

        dlg = wx.ColourDialog(self, self._colour_data)

        if dlg.ShowModal() == wx.ID_OK:

            self._colour_data = dlg.GetColourData()
            clr = self._colour_data.GetColour()

            # Try to find colour in gallery
            item = None
            for i in range(gallery.GetCount()):
                item = gallery.GetItem(i)
                if self.GetGalleryColour(gallery, item, None)[0] == clr:
                    break
                else:
                    item = None

            # Colour not in gallery - add it
            if item == None:
                item = self.AddColourToGallery(gallery,
                                               clr.GetAsString(wx.C2S_HTML_SYNTAX),
                                               self._bitmap_creation_dc,
                                               clr)
                gallery.Realize()

            # Set selection
            gallery.EnsureVisible(item)
            gallery.SetSelection(item)

            # Send an event to respond to the selection change
            dummy = RB.RibbonGalleryEvent(RB.wxEVT_RIBBONGALLERY_SELECTED,
                                          gallery.GetId())
            dummy.SetEventObject(gallery)
            dummy.SetGallery(gallery)
            dummy.SetGalleryItem(item)
            self.GetEventHandler().ProcessEvent(dummy)


    def OnDefaultProvider(self, event):
        self._ribbon.DismissExpandedPanel()
        self.SetArtProvider(RB.RibbonDefaultArtProvider())


    def OnAUIProvider(self, event):
        self._ribbon.DismissExpandedPanel()
        self.SetArtProvider(RB.RibbonAUIArtProvider())


    def OnMSWProvider(self, event):
        self._ribbon.DismissExpandedPanel()
        self.SetArtProvider(RB.RibbonMSWArtProvider())


    def SetArtProvider(self, prov):
        self._ribbon.Freeze()
        self._ribbon.SetArtProvider(prov)

        (self._default_primary,
         self._default_secondary,
         self._default_tertiary) = prov.GetColourScheme()

        self.PopulateColoursPanel(self._primary_gallery.GetParent(),
                                  self._default_primary,
                                  ID_PRIMARY_COLOUR)
        self.PopulateColoursPanel(self._secondary_gallery.GetParent(),
                                  self._default_secondary,
                                  ID_SECONDARY_COLOUR)

        self._ribbon.Thaw()
        self.panel.GetSizer().Layout()
        self._ribbon.Realize()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    app = wx.App()
    frm = RibbonFrame(None, -1, "wx.ribbon Sample Application", size=(800, 600))
    frm.Show()

    if False:
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()
