#---------------------------------------------------------------------------
# Name:        etg/rearrangectrl.py
# Author:      Robin Dunn
#
# Created:     25-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "rearrangectrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxRearrangeList",
           "wxRearrangeCtrl",
           "wxRearrangeDialog",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/rearrangectrl.h>')

    c = module.find('wxRearrangeList')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    c.addPrivateCopyCtor()

    c.find('wxRearrangeList.order').default = 'wxArrayInt()'
    c.find('wxRearrangeList.items').default = 'wxArrayString()'
    c.find('Create.order').default = 'wxArrayInt()'
    c.find('Create.items').default = 'wxArrayString()'

    module.addGlobalStr('wxRearrangeListNameStr', c)
    module.addGlobalStr('wxRearrangeDialogNameStr', c)


    c = module.find('wxRearrangeCtrl')
    tools.fixWindowClass(c)
    c.addPrivateCopyCtor()
    c.find('wxRearrangeCtrl.order').default = 'wxArrayInt()'
    c.find('wxRearrangeCtrl.items').default = 'wxArrayString()'
    c.find('Create.order').default = 'wxArrayInt()'
    c.find('Create.items').default = 'wxArrayString()'


    c = module.find('wxRearrangeDialog')
    tools.fixTopLevelWindowClass(c)
    c.addPrivateCopyCtor()
    c.find('wxRearrangeDialog.order').default = 'wxArrayInt()'
    c.find('wxRearrangeDialog.items').default = 'wxArrayString()'
    c.find('Create.order').default = 'wxArrayInt()'
    c.find('Create.items').default = 'wxArrayString()'


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

