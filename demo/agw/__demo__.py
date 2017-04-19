#!/usr/bin/env python

"""
This module contains the meta data needed for integrating the samples
in the AGW subdir into the wxPython demo framework. Once imported,
this module returns the following information:

* GetDemoBitmap: returns the bitmap used in the wxPython tree control
  to characterize the AGW package;
* GetRecentAdditions: returns a subset (or the whole set) of demos in
  the AGW package which will appear under the Recent Additions tree
  item in the wxPython demo;
* GetDemos: returns all the demos in the AGW package;
* GetOverview: returns a wx.html-ready representation of the AGW docs.

These meta data are merged into the wxPython demo tree at startup.

Last updated: Andrea Gavana @ 04 Feb 2013, 21.00 GMT.
Version 0.9.7.

"""

__version__ = "0.9.7"
__author__ = "Andrea Gavana <andrea.gavana@gmail.com>"


# Start the imports...
import wx
from wx.lib.embeddedimage import PyEmbeddedImage

# ========================================
# For AGW (Advanced Generic Widgets :-D )
# ========================================

import wx.lib.agw
_agwDocs = wx.lib.agw.__doc__

# ========================================
# End AGW things
# ========================================


def GetDemoBitmap():
    """ Returns the bitmap to be used in the demo tree for the AGW package. """

    # Get the image as PyEmbeddedImage
    image = PyEmbeddedImage(
        b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAvdJ"
        b"REFUOI2NkX1I3HUcx1/f7+/B85yXpXa38o+ltIdzGRUUs4fpClaYi5iFERpkG6yQtkEEBZ0Q"
        b"QkW1GotVFEEQGcFkOIK2Nq1mszqJdeKdDzsU9fS86dx5nre78/vtj3ViBtH73/f7/eLzIFij"
        b"A8fHm6evmU/3+q1sbLT0efrEfM7Tvg9dZJOHVSi8V0Yj21VscViGB942c4Gd+/0lgaWyur4e"
        b"STaGyUSoFJgH0K2tLianT2UvnLzXTA21YSmHjBtNlKrXVwEu75bG7m4KsuMqSKHchr3VDQwB"
        b"MBY/TODMgyI/9III8/n1xkobgAlQu/9sRWRpw67E4MKCXZ7/c8bK26Znlm8DfgLgz9BelsOY"
        b"Y9fL+tlDZ5idg4s9WQlQoS74HCfuqK3fWPnE196HjhTSX4DJxtXjRMObIQPAZ08aV6b8R2s5"
        b"3/EI9sRF+VrdlmOVMV+Tac5aBim+DfrLqyvvq9lZ1PRUrj/uupwgo1m+wQq2zOyuK66v/oW8"
        b"QqY8Wos9XjMbtJpHRiI1x4g1f/TSA489PrjQ3ZlXmjLf32V8PBUke3VCt9RHVVwlpVvaHmUb"
        b"xo/xhsjdfyyoIU4fkHrA57XXvvNsMxWzHTK92G/o/n2G+v4Zu551Gus0TwfeknNyeobMrZ7R"
        b"PWvNh7/k0uQPso0eKLuTFYeRHlgPsG1uTsdJmoNR0eH5XX0x90FBqPjg0oDwceqmiLNoLnWt"
        b"6tdunbIPKsdXl8Vwxz6jutGTdTgkrxZNO1eMRLpqZEgcFQCv7BDfbS4Ruzfkyyvtvcql08ps"
        b"rJI9b+xQgXK/9eimmsztx++RHOnTVwOzwmotEc4bJ3Wg9xZ1l8iN1LIdtzBkwzdl1nMJrzWv"
        b"nca7aP0yAmHFlX1oMpk8Nybud1kkG4p1+4td6lMAsX43fK53AC/oMRBlwCiwFU0UgRulP+HN"
        b"xa5cXP4LsCqxCfT5vwEgcKP1IknnubWp/wAAWdH5T6Y4yXvRpf8L+I32+CUQwwBoVkjkd60P"
        b"/QWR0DSJqhvOegAAAABJRU5ErkJggg==")

    # Return the AGW bitmap to use in
    # the wxPython demo tree control
    return image


def GetRecentAdditions():
    """
    Returns a subset (or the full set) of the AGW demo names which will go
    into the Recent Additions tree item in the wxPython demo.
    """

    # For the moment, we add all the widgets in AGW as
    # Recent Additions
    if wx.VERSION < (2, 9):
        recentAdditions = ['AdvancedSplash', 'AquaButton', 'AUI', 'BalloonTip',
                           'ButtonPanel', 'CubeColourDialog', 'CustomTreeCtrl',
                           'FlatMenu', 'FlatNotebook', 'FloatSpin',
                           'FoldPanelBar', 'FourWaySplitter', 'GenericMessageDialog',
                           'GradientButton', 'HyperLinkCtrl', 'HyperTreeList',
                           'AGWInfoBar', 'KnobCtrl', 'LabelBook', 'MultiDirDialog',
                           'PeakMeter', 'PersistentControls', 'PieCtrl', 'PyBusyInfo',
                           'PyCollapsiblePane', 'PyProgress', 'RibbonBar', 'RulerCtrl',
                           'ShapedButton', 'ShortcutEditor', 'SpeedMeter', 'SuperToolTip',
                           'ThumbnailCtrl', 'ToasterBox', 'UltimateListCtrl',
                           'XLSGrid', 'ZoomBar']
    elif wx.VERSION < (2,9,2):
        recentAdditions = ['AUI', 'AGWInfoBar', 'PersistentControls', 'PyBusyInfo', 'PyGauge',
                           'RibbonBar', 'ShortcutEditor', 'UltimateListCtrl',
                           'XLSGrid', 'ZoomBar']
    else:
        recentAdditions = ['AGWInfoBar', 'PersistentControls', 'ShortcutEditor', 'XLSGrid']

    # Return the Recent Additions for AGW
    return recentAdditions


def GetDemos():
    """
    Returns all the demo names in the AGW package, together with the tree item
    name which will go in the wxPython demo tree control.
    """

    # The tree item text for AGW
    AGWTreeItem = "Advanced Generic Widgets"

    # The AGW demos
    AGWDemos = ['AdvancedSplash', 'AquaButton', 'AUI', 'BalloonTip',
                'ButtonPanel', 'CubeColourDialog', 'CustomTreeCtrl',
                'FlatMenu', 'FlatNotebook', 'FloatSpin',
                'FoldPanelBar', 'FourWaySplitter', 'GenericMessageDialog',
                'GradientButton', 'HyperLinkCtrl', 'HyperTreeList',
                'AGWInfoBar', 'KnobCtrl', 'LabelBook', 'MultiDirDialog',
                'PeakMeter', 'PersistentControls', 'PieCtrl', 'PyBusyInfo',
                'PyCollapsiblePane', 'PyGauge', 'PyProgress', 'RibbonBar',
                'RulerCtrl', 'ShapedButton', 'ShortcutEditor', 'SpeedMeter',
                'SuperToolTip', 'ThumbnailCtrl', 'ToasterBox',
                'UltimateListCtrl', 'XLSGrid', 'ZoomBar']

    return AGWTreeItem, AGWDemos


def GetOverview():
    """
    Creates the HTML code to display the Advanced Generic Widgets documentation
    starting from wx.lib.agw.__doc__.
    """

    # wxPython widgets to highlight using the <code> tag
    wxPythonWidgets = ["wx.SplashScreen", "wx.ColourDialog", "wx.TreeCtrl", "wx.MenuBar",
                       "wx.Menu", "wx.ToolBar", "wx.Notebook", "wx.MessageDialog",
                       "wx.gizmos.TreeListCtrl", "wx.DirDialog", "wx.CollapsiblePane",
                       "wx.ProgressDialog", "wx.TipWindow", "wx.lib", "wx.aui", "wx.ListCtrl",
                       "wx.BusyInfo", "wx.Panel", "wx.Gauge", "wx.grid.Grid"]

    import wx.lib.agw
    _agwDocs = wx.lib.agw.__doc__

    _agwDocs = _agwDocs.replace("`", "").replace("L{", "").replace("}", "")

    # Split the docs in many lines
    splitted = _agwDocs.split("\n")
    # Add the title
    strs = "<html><body>\n<h2><center>Advanced Generic Widgets (AGW)</center></h2>\n\n"

    # Get the number of widgets in the package...
    numWidgets = len(GetDemos()[1])
    widgetsFound, endRemarks = 0, 0
    for line in splitted:
        # Loop over the lines in the AGW documentation
        newLine = line
        if line.startswith("- "):
            # That's a new widget
            indxStart = line.index("-") + 1
            indxEnd = line.index(":")
            sw = line[indxStart:indxEnd]
            # Put a bullet
            newLine = "<li><b> %s</b>:"%sw + line[indxEnd+1:]
            if widgetsFound == 0:
                newLine = "<p><ul>\n" + newLine
            widgetsFound += 1
        elif line.strip().endswith(";"):
            newLine = "%s</li>"%line
        elif line.startswith("Description:"):
            # It's a title
            newLine = "<p><h5>%s</h5>"%line
        if endRemarks:
            if ":" in newLine and not line.startswith("http"):
                indxEnd = newLine.index(":")
                newLine = "<br><i>%s</i>"%newLine[0:indxEnd] + newLine[indxEnd:]
            else:
                newLine = "<br>%s"%newLine
        if line.startswith("http:"):
            # It's a web address
            newLine = "  <a href='%s'>%s</a>"%(newLine, newLine)
        elif line.find("@") > 0:
            # It's an email address
            newLine = "  <a href='mailto:%s'>%s</a>"%(newLine, newLine)

        strs += newLine

        if widgetsFound == numWidgets and line.find(".") >= 0 and line.find("ListCtrl") < 0:
            # Break the loop, all widgets included
            strs += "\n</ul><p>"
            widgetsFound = 0
            endRemarks = 1

    strs += "</body></html>"
    # Make AGW bold and wxPython underlined...
    strs = strs.replace("AGW", "<b>AGW</b>")
    strs = strs.replace("wxPython", "<u>wxPython</u>")
    for widget in wxPythonWidgets:
        # Show wx things with the <code> tag
        strs = strs.replace(widget, "<code>%s</code>"%widget)

    # Return the beautified AGW docs, ready for wx.html
    return strs

