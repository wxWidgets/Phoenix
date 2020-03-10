#---------------------------------------------------------------------------
# Name:        etg/progdlg
# Author:      Robin Dunn
#
# Created:     9-Sept-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
import copy

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

    c = gpd = module.find('wxGenericProgressDialog')
    assert isinstance(c, etgtools.ClassDef)

    tools.fixWindowClass(c)#, False)
    #tools.removeVirtuals(c)

    c.find('Pulse.skip').out = True
    c.find('Update.skip').out = True


    c = module.find('wxProgressDialog')

    # Copy methods from the generic to the native class. This is needed
    # because none of the methods are declared in the interface files, and
    # since on MSW some non-virtual methods are reimplemented in
    # wxProgressDialogs they will not be called if SIP doesn't know about
    # them. We'll copy all of them and let the C++ compiler sort things out.
    for item in gpd:
        if (isinstance(item, etgtools.MethodDef) and
                not item.isCtor and
                not item.isDtor):
            c.addItem(copy.deepcopy(item))

    tools.fixWindowClass(c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

