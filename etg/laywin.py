#---------------------------------------------------------------------------
# Name:        etg/laywin.py
# Author:      Robin Dunn
#
# Created:     26-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "laywin"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxLayoutAlgorithm",
           "wxSashLayoutWindow",
           "wxQueryLayoutInfoEvent",
           "wxCalculateLayoutEvent",
           "laywin_8h.xml",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/laywin.h>')

    c = module.find('wxSashLayoutWindow')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)


    c = module.find('wxQueryLayoutInfoEvent')
    tools.fixEventClass(c)


    c = module.find('wxCalculateLayoutEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_QUERY_LAYOUT_INFO = wx.PyEventBinder( wxEVT_QUERY_LAYOUT_INFO )
        EVT_CALCULATE_LAYOUT = wx.PyEventBinder( wxEVT_CALCULATE_LAYOUT )
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

