#---------------------------------------------------------------------------
# Name:        etg/unichar.py
# Author:      Robin Dunn
#
# Created:     25-Aug-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "unichar"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxUniChar',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/unichar.h>')

    c = module.find('wxUniChar')
    assert isinstance(c, etgtools.ClassDef)

    m = c.find('wxUniChar').findOverload('long int')
    m.find('c').type = 'long'

    m = c.find('wxUniChar').findOverload('unsigned long int')
    m.find('c').type = 'unsigned long'

    for m in c.find('wxUniChar').all():
        p = m.find('c')
        if 'long' not in p.type:
            m.ignore()


    tools.ignoreAllOperators(c)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

