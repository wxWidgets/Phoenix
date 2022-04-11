#---------------------------------------------------------------------------
# Name:        etg/ribbon_panel.py
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
NAME      = "ribbon_panel"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'ribbon_2panel_8h.xml',
           'wxRibbonPanel',
           'wxRibbonPanelEvent',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/ribbon/panel.h>')

    c = module.find('wxRibbonPanel')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    tools.ignoreConstOverloads(c)


    c = module.find('wxRibbonPanelEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_RIBBONPANEL_EXTBUTTON_ACTIVATED = wx.PyEventBinder(wxEVT_RIBBONPANEL_EXTBUTTON_ACTIVATED, 1)
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

