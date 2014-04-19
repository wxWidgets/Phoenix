# --------------------------------------------------------------------------------- #
# ribbon wxPython IMPLEMENTATION
#
# Andrea Gavana, @ 03 Nov 2006
#
#
# TODO List
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@maerskoil.com
# andrea.gavana@gmail.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
# Tags:        phoenix-port, unittest, documented, py3-port
#
# End Of Comments
# --------------------------------------------------------------------------------- #
"""
The `RibbonBar` library is a set of classes for writing a ribbon user interface.

Description
===========

At the most generic level, this is a combination of a tab control with a toolbar.
At a more functional level, it is similar to the user interface present in recent
versions of Microsoft Office.

A ribbon user interface typically has a :class:`bar.RibbonBar`, which contains one or more
:class:`page.RibbonPage`, which in turn each contains one or more :class:`panel.RibbonPanel`, which in turn
contain controls.


Usage
=====

Usage example::

    import wx
    import wx.lib.agw.ribbon as RB

    class MyFrame(wx.Frame):

        def __init__(self, parent, id=-1, title="Ribbon Demo", pos=wx.DefaultPosition,
                     size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):

            wx.Frame.__init__(self, parent, id, title, pos, size, style)

            self._ribbon = RB.RibbonBar(self, wx.ID_ANY)
            
            home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Examples", CreateBitmap("ribbon"))
            toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "Toolbar", wx.NullBitmap, wx.DefaultPosition,
                                           wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
            
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
            toolbar.AddHybridTool(ID_POSITION_LEFT, CreateBitmap("position_left"),
                                  "Align ribbonbar vertically on the left for demonstration purposes")
            toolbar.AddHybridTool(ID_POSITION_TOP, CreateBitmap("position_top"),
                                  "Align the ribbonbar horizontally at the top for demonstration purposes")
            toolbar.AddSeparator()
            toolbar.AddHybridTool(wx.ID_PRINT, wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(16, 15)),
                                  "This is the Print button tooltip demonstrating a tooltip")
            toolbar.SetRows(2, 3)

            selection_panel = RB.RibbonPanel(home, wx.ID_ANY, "Selection", CreateBitmap("selection_panel"))
            selection = RB.RibbonButtonBar(selection_panel)
            selection.AddSimpleButton(ID_SELECTION_EXPAND_V, "Expand Vertically", CreateBitmap("expand_selection_v"),
                                      "This is a tooltip for Expand Vertically demonstrating a tooltip")
            selection.AddSimpleButton(ID_SELECTION_EXPAND_H, "Expand Horizontally", CreateBitmap("expand_selection_h"), "")
            selection.AddSimpleButton(ID_SELECTION_CONTRACT, "Contract", CreateBitmap("auto_crop_selection"),
                                      CreateBitmap("auto_crop_selection_small"))

            shapes_panel = RB.RibbonPanel(home, wx.ID_ANY, "Shapes", CreateBitmap("circle_small"))
            shapes = RB.RibbonButtonBar(shapes_panel)

            # Show toggle buttons behaviour
            shapes.AddButton(ID_CIRCLE, "Circle", CreateBitmap("circle"), CreateBitmap("circle_small"),
                             help_string="This is a tooltip for the circle button demonstrating another tooltip",
                             kind=RB.RIBBON_BUTTON_TOGGLE)
                             
            shapes.AddSimpleButton(ID_CROSS, "Cross", CreateBitmap("cross"), "")
            shapes.AddHybridButton(ID_TRIANGLE, "Triangle", CreateBitmap("triangle"))
            shapes.AddSimpleButton(ID_SQUARE, "Square", CreateBitmap("square"), "")
            shapes.AddDropdownButton(ID_POLYGON, "Other Polygon", CreateBitmap("hexagon"), "")

            sizer_panel = RB.RibbonPanel(home, wx.ID_ANY, "Panel with Sizer",
                                         wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                         agwStyle=RB.RIBBON_PANEL_DEFAULT_STYLE)

            scheme = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Appearance", CreateBitmap("eye"))
            self._default_primary, self._default_secondary, self._default_tertiary = self._ribbon.GetArtProvider().GetColourScheme(1, 1, 1)

            provider_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Art", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                            agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
            provider_bar = RB.RibbonButtonBar(provider_panel, wx.ID_ANY)
            provider_bar.AddSimpleButton(ID_DEFAULT_PROVIDER, "Default Provider",
                                         wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(32, 32)), "")
            provider_bar.AddSimpleButton(ID_AUI_PROVIDER, "AUI Provider", CreateBitmap("aui_style"), "")
            provider_bar.AddSimpleButton(ID_MSW_PROVIDER, "MSW Provider", CreateBitmap("msw_style"), "")
            
            primary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Primary Colour", CreateBitmap("colours"))
            self._primary_gallery = self.PopulateColoursPanel(primary_panel, self._default_primary, ID_PRIMARY_COLOUR)

            secondary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Secondary Colour", CreateBitmap("colours"))
            self._secondary_gallery = self.PopulateColoursPanel(secondary_panel, self._default_secondary, ID_SECONDARY_COLOUR)
        
            dummy_2 = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Empty Page", CreateBitmap("empty"))
            dummy_3 = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Another Page", CreateBitmap("empty"))

            self._ribbon.Realize()

            self._logwindow = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
                                          wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE)
        
            s = wx.BoxSizer(wx.VERTICAL)

            s.Add(self._ribbon, 0, wx.EXPAND)
            s.Add(self._logwindow, 1, wx.EXPAND)

            self.SetSizer(s)


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()
    


What's New
==========

Current wxRibbon version tracked: wxWidgets 2.9.5 (SVN HEAD)

New features recently implemented:

- Possibility to hide panels in the :class:`bar.RibbonBar`;
- Added the ``EVT_RIBBONBAR_TAB_LEFT_DCLICK`` event, which generates a special event
  when a ribbon bar tab is double-clicked;
- Added support for toggle buttons in the :class:`bar.RibbonBar`;
- Improved support for ribbon panel sizers: panels with sizers should now automatically
  minimise at small sizes, and behave properly when popping up from a minimised state;
- Added tooltips via `SetToolTip` for those buttons which have the `help_string` attribute set.


License And Version
===================

RIBBON library is distributed under the wxPython license. 

Latest revision: Andrea Gavana @ 27 Dec 2012, 21.00 GMT

Version 0.3. 

"""

__author__ = "Andrea Gavana <andrea.gavana@gmail.com>"
__date__ = "16 October 2009"


from .art import *
from .art_aui import *
from .art_internal import *
from .art_msw import *
from .art_default import *

from .bar import *
from .buttonbar import *
from .control import *
from .gallery import *

from .page import *
from .panel import *
from .toolbar import *

