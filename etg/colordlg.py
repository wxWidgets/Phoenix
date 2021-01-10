#---------------------------------------------------------------------------
# Name:        etg/colordlg.py
# Author:      Robin Dunn
#
# Created:     30-Mar-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "colordlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxColourData",
           "wxColourDialog",
           "wxColourDialogEvent" ,
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/colordlg.h>")

    c = module.find('wxColourDialog')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixTopLevelWindowClass(c)


    c = module.find('wxGetColourFromUser')
    c.mustHaveApp()


    c = module.find('wxColourDialogEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_COLOUR_CHANGED = PyEventBinder(wxEVT_COLOUR_CHANGED, 1)
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

