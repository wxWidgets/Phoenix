#---------------------------------------------------------------------------
# Name:        etg/statbmp.py
# Author:      Kevin Ollivier
#
# Created:     26-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import copy

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "statbmp"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxStaticBitmap' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxStaticBitmap')
    c.find('wxStaticBitmap.label').default = 'wxNullBitmap'
    c.find('wxStaticBitmap.label').name = 'bitmap'
    c.find('Create.label').default = 'wxNullBitmap'
    c.find('Create.label').name = 'bitmap'
    tools.fixWindowClass(c)

    # Make a copy of wxStaticBitmap so we can generate wrapper code for
    # wxGenericStaticBitmap too.
    module.addHeaderCode('#include <wx/generic/statbmpg.h>')
    gsb = copy.deepcopy(c)
    assert isinstance(gsb, etgtools.ClassDef)
    gsb.name = 'wxGenericStaticBitmap'
    for ctor in gsb.findAll('wxStaticBitmap'):
        ctor.name = 'wxGenericStaticBitmap'
    module.addItem(gsb)

    module.addGlobalStr('wxStaticBitmapNameStr', c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

