#---------------------------------------------------------------------------
# Name:        etg/ribbon_toolbar.py
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
NAME      = "ribbon_toolbar"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxRibbonToolBar',
           'wxRibbonToolBarEvent',
           'interface_2wx_2ribbon_2toolbar_8h.xml',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/ribbon/toolbar.h>')
    module.insertItem(0, etgtools.WigCode("""\
        // forward declarations
        class wxRibbonToolBarToolBase;
        """))


    c = module.find('wxRibbonToolBar')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    # Use wxPyUserData for the clientData values instead of a plain wxObject
    for item in c.allItems():
        if isinstance(item, etgtools.ParamDef) and item.name == 'clientData':
            item.type = 'wxPyUserData*'
            item.transfer = True
    meth = c.find('GetToolClientData')
    meth.type = 'wxPyUserData*'
    meth.setCppCode('return dynamic_cast<wxPyUserData*>(self->GetToolClientData(tool_id));')



    c = module.find('wxRibbonToolBarEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_RIBBONTOOLBAR_CLICKED = wx.PyEventBinder( wxEVT_RIBBONTOOLBAR_CLICKED, 1 )
        EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED = wx.PyEventBinder( wxEVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, 1 )
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

