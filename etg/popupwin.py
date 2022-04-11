#---------------------------------------------------------------------------
# Name:        etg/popupwin.py
# Author:      Robin Dunn
#
# Created:     15-Dec-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "popupwin"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxPopupWindow",
           "wxPopupTransientWindow",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addCppCode("#include <wx/popupwin.h>")

    c = module.find('wxPopupWindow')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    tools.fixWindowClass(c)
    c.find('Position').isVirtual = True


    c = module.find('wxPopupTransientWindow')
    c.mustHaveApp()
    tools.fixWindowClass(c)
    c.find('Dismiss').isVirtual = True
    c.find('ProcessLeftDown').isVirtual = True
    c.find('OnDismiss').ignore(False)
    c.find('OnDismiss').isVirtual = True



    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

