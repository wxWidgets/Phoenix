#---------------------------------------------------------------------------
# Name:        etg/ribbon_bar.py
# Author:      Robin Dunn
#
# Created:     20-Jun-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_ribbon"
NAME      = "ribbon_bar"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxRibbonBarEvent',
           'wxRibbonPageTabInfo',
           'wxRibbonBar',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/ribbon/bar.h>')

    c = module.find('wxRibbonBar')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    c.find('SetArtProvider.art').transfer = True


    c = module.find('wxRibbonBarEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_RIBBONBAR_PAGE_CHANGED    = wx.PyEventBinder(wxEVT_RIBBONBAR_PAGE_CHANGED, 1)
        EVT_RIBBONBAR_PAGE_CHANGING   = wx.PyEventBinder(wxEVT_RIBBONBAR_PAGE_CHANGING,1)
        EVT_RIBBONBAR_TAB_MIDDLE_DOWN = wx.PyEventBinder(wxEVT_RIBBONBAR_TAB_MIDDLE_DOWN, 1)
        EVT_RIBBONBAR_TAB_MIDDLE_UP   = wx.PyEventBinder(wxEVT_RIBBONBAR_TAB_MIDDLE_UP, 1)
        EVT_RIBBONBAR_TAB_RIGHT_DOWN  = wx.PyEventBinder(wxEVT_RIBBONBAR_TAB_RIGHT_DOWN, 1)
        EVT_RIBBONBAR_TAB_RIGHT_UP    = wx.PyEventBinder(wxEVT_RIBBONBAR_TAB_RIGHT_UP, 1)
        EVT_RIBBONBAR_TAB_LEFT_DCLICK = wx.PyEventBinder(wxEVT_RIBBONBAR_TAB_LEFT_DCLICK, 1)
        EVT_RIBBONBAR_TOGGLED         = wx.PyEventBinder(wxEVT_RIBBONBAR_TOGGLED, 1)
        EVT_RIBBONBAR_HELP_CLICK      = wx.PyEventBinder(wxEVT_RIBBONBAR_HELP_CLICK, 1)
        """)


    module.addItem(
        tools.wxArrayWrapperTemplate('wxRibbonPageTabInfoArray',
                                     'wxRibbonPageTabInfo',
                                     module))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

