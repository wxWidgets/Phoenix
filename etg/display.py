#---------------------------------------------------------------------------
# Name:        etg/display.py
# Author:      Robin Dunn
#
# Created:     27-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "display"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxDisplay', ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/display.h>")

    c = module.find('wxDisplay')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateAssignOp()
    c.addPrivateCopyCtor()
    c.mustHaveApp()
    c.find('GetCount').mustHaveApp()
    c.find('GetFromPoint').mustHaveApp()
    c.find('GetFromWindow').mustHaveApp()


    c.addProperty('ClientArea GetClientArea')
    c.addProperty('CurrentMode GetCurrentMode')
    c.addProperty('Geometry GetGeometry')
    c.addProperty('Name GetName')



    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

