#---------------------------------------------------------------------------
# Name:        etg/bmpbndl.py
# Author:      Scott Talbert
#
# Created:     13-Apr-2022
# Copyright:   (c) 2022 by Scott Talbert
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import MethodDef

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "bmpbndl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxBitmapBundle',
           'wxBitmapBundleImpl',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    #module.addHeaderCode('#include <wx/some_header_file.h>')

    c = module.find('wxBitmapBundle')
    assert isinstance(c, etgtools.ClassDef)

    c.find('FromSVG').findOverload('char *data, const wxSize &sizeDef').ignore()


    c = module.find('wxBitmapBundleImpl')
    assert isinstance(c, etgtools.ClassDef)

    m = MethodDef(name='~wxBitmapBundleImpl', isDtor=True, isVirtual=True, protection='protected')
    c.addItem(m)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

