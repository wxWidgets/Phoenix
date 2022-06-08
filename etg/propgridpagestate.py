#---------------------------------------------------------------------------
# Name:        etg/propgridpagestate.py
# Author:      Robin Dunn
#
# Created:     23-Feb-2015
# Copyright:   (c) 2015-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "propgridpagestate"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxPropertyGridHitTestResult',
           'wxPropertyGridIteratorBase',
           'wxPropertyGridIterator',
           'wxPGVIterator',
           'wxPropertyGridPageState',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPropertyGridHitTestResult')
    assert isinstance(c, etgtools.ClassDef)

    c = module.find('wxPropertyGridIterator')
    # TODO: Add python iterator methods to this and other iterator classes

    c = module.find('wxPGVIterator')
    c.find('wxPGVIterator').findOverload('wxPGVIteratorBase').ignore()

    c = module.find('wxPropertyGridPageState')
    tools.ignoreConstOverloads(c)
    # Incorrectly documented in 3.1.7
    c.find('GetColumnFullWidth.p').type = 'wxPGProperty *'


    module.find('wxPG_IT_CHILDREN').ignore()


    # Switch all wxVariant types to wxPGVariant, so the propgrid-specific
    # version of the MappedType will be used for converting to/from Python
    # objects.
    for item in module.allItems():
        if hasattr(item, 'type') and 'wxVariant' in item.type:
            item.type = item.type.replace('wxVariant', 'wxPGVariant')

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

