#---------------------------------------------------------------------------
# Name:        etg/sashwin.py
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
NAME      = "sashwin"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxSashWindow",
           "wxSashEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/sashwin.h>')

    c = module.find('wxSashWindow')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    c = module.find('wxSashEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_SASH_DRAGGED = wx.PyEventBinder( wxEVT_SASH_DRAGGED, 1 )
        EVT_SASH_DRAGGED_RANGE = wx.PyEventBinder( wxEVT_SASH_DRAGGED, 2 )
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

