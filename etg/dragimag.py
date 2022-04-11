#---------------------------------------------------------------------------
# Name:        etg/dragimag.py
# Author:      Robin Dunn
#
# Created:     09-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "dragimag"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxDragImage",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    di = module.find('wxDragImage')
    assert isinstance(di, etgtools.ClassDef)
    di.mustHaveApp()

    # make a copy and rename it to 'wxGenericDragImage'
    gdi = tools.copyClassDef(di, 'wxGenericDragImage')
    module.insertItemAfter(di, gdi)

    # now add some tweaks for wxDragImage
    di.find('DoDrawImage').ignore()
    di.find('GetImageRect').ignore()
    di.find('UpdateBackingFromWindow').ignore()
    di.addPrivateCopyCtor()

    # and for wxGenericDragImage
    gdi.addPrivateCopyCtor()
    gdi.addHeaderCode("#include <wx/generic/dragimgg.h>")


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

