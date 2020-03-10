#---------------------------------------------------------------------------
# Name:        etg/webkit.py
# Author:      Robin Dunn
#
# Created:     22-Aug-2013
# Copyright:   (c) 2013-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_webkit"
NAME      = "webkit"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxWebKitCtrl',
           'wxWebKitBeforeLoadEvent',
           'wxWebKitStateChangedEvent',
           'wxWebKitNewWindowEvent',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/html/webkit.h>')

    tools.generateStubs('wxUSE_WEBKIT', module,
                        extraHdrCode='extern const char* wxWebKitCtrlNameStr;\n',
                        extraCppCode='const char* wxWebKitCtrlNameStr = "";\n')


    c = module.find('wxWebKitCtrl')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    tools.fixWindowClass(c)
    c.find('wxWebKitCtrl.strURL').default = '""'
    c.find('Create.strURL').default = '""'


    module.addGlobalStr('wxWebKitCtrlNameStr', c)

    c = module.find('wxWebKitBeforeLoadEvent')
    tools.fixEventClass(c)

    c = module.find('wxWebKitStateChangedEvent')
    tools.fixEventClass(c)

    c = module.find('wxWebKitNewWindowEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_WEBKIT_BEFORE_LOAD = wx.PyEventBinder( wxEVT_WEBKIT_BEFORE_LOAD, 1 )
        EVT_WEBKIT_STATE_CHANGED = wx.PyEventBinder( wxEVT_WEBKIT_STATE_CHANGED, 1 )
        EVT_WEBKIT_NEW_WINDOW = wx.PyEventBinder( wxEVT_WEBKIT_NEW_WINDOW, 1 )
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

