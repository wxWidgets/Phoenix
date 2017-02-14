#---------------------------------------------------------------------------
# Name:        etg/progdlg
# Author:      Robin Dunn
#
# Created:     9-Sept-2011
# Copyright:   (c) 2011-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "progdlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxGenericProgressDialog',
           'wxProgressDialog'
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/progdlg.h>")

    c = module.find('wxGenericProgressDialog')
    assert isinstance(c, etgtools.ClassDef)

    tools.fixWindowClass(c)#, False)
    #tools.removeVirtuals(c)

    c.find('Pulse.skip').out = True
    c.find('Update.skip').out = True


    c = module.find('wxProgressDialog')
    tools.fixWindowClass(c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

