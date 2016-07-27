#---------------------------------------------------------------------------
# Name:        etg/pseudodc.py
# Author:      Robin Dunn
#
# Created:     26-Jul-2016
# Copyright:   (c) 2016 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_adv"
NAME      = "pseudodc"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ ]

OTHERDEPS = [ 'src/pseudodc.h',
              'src/pseudodc.cpp',
              ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # The PseudoDC classes are not in wxWidgets, so there is no Doxygen XML
    # for them. That means we'll have to construct each of the extractor
    # objects from scratch.

    module.addHeaderCode('#include "pseudodc.h"')
    module.includeCppCode('src/pseudodc.cpp')



    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

