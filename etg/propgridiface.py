#---------------------------------------------------------------------------
# Name:        etg/propgridiface.py
# Author:      Robin Dunn
#
# Created:     23-Feb-2015
# Copyright:   (c) 2015 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "propgridiface"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxPGPropArgCls',
           'wxPropertyGridInterface',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPGPropArgCls')
    assert isinstance(c, etgtools.ClassDef)
    c.find('GetPtr').overloads[0].ignore()


    c = module.find('wxPropertyGridInterface')
    for m in c.findAll('GetIterator'):
        if m.type == 'wxPropertyGridConstIterator':
            m.ignore()

    c.find('SetPropertyValue').findOverload('int value').ignore()
    c.find('SetPropertyValue').findOverload('bool value').ignore()
    c.find('SetPropertyValue').findOverload('wxLongLong_t value').ignore()
    c.find('SetPropertyValue').findOverload('wxULongLong_t value').ignore()
    c.find('SetPropertyValue').findOverload('wxObject *value').ignore()

    module.addItem(
        tools.wxArrayPtrWrapperTemplate('wxArrayPGProperty', 'wxPGProperty', module))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

